
from routing_lib.routing_measures import div
from routing_lib.routing_measures import redundancy
from routing_lib.routing_measures import compute_temp_redundancy_sliding
from routing_lib.routing_measures import get_load_balance_entropy

from routing_lib import from_sumo_to_igraph_network

from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

def get_edge_popularity_map(edge_weights):
    # Defining the 3 categories
    categories = ('L', 'M', 'H')

    # Getting the K-road values
    original_indexes = list(edge_weights.keys())
    kroad_list = list(edge_weights.values())

    # Log2 of the data to extract the supposedly balanced distribution
    logged_data = np.log2(kroad_list)

    # Extracting bin values (filtering out not appearing edges as log2(0) = -np.inf)
    _, bin_edges = np.histogram(logged_data[logged_data > -np.inf], bins = len(categories))

    # Extracting the indexes of the bins
    bin_low = logged_data <= bin_edges[1]
    bin_medium = (logged_data > bin_edges[1]) & (logged_data <= bin_edges[2])
    bin_high = logged_data > bin_edges[2]

    # Mapping the original eid to the categorie
    mapper = np.empty(shape=(len(original_indexes), 2), dtype = object)
    mapper[:,0] = original_indexes
    mapper[:,1][bin_low], mapper[:,1][bin_medium], mapper[:,1][bin_high] = categories

    result = {'categories' : categories,
              'log_data' : logged_data,
              'mapper' : dict(mapper)}

    return result

def count_popularity(edge_weights):

    info_dict = get_edge_popularity_map(edge_weights)

    categories = info_dict['categories']
    pop_sorter = {pop : n for n, pop in enumerate(categories)}

    dict_mapper = info_dict['mapper']
    count_popularity = Counter(sorted(dict_mapper.values(), key=lambda x: pop_sorter[x]))

    return count_popularity

def crossing_mapper(road_network):

    node_crossing_map = {}
    for node in road_network.getNodes():
        in_edges = [edge for edge in list(node.getIncoming())]
        out_edges = [edge for edge in list(node.getOutgoing())]
        if (len(in_edges) >= 1 and len(out_edges) >= 1) and (len(in_edges) >= 2 or len(out_edges) >= 2):
            mapped_to = True
        else:
            mapped_to = False
        node_crossing_map[node.getID()] = mapped_to

    edges_to_nodes_type = lambda e: node_crossing_map[e.getFromNode().getID()] or node_crossing_map[e.getToNode().getID()]
    eid_crossing_dict = {e.getID() : edges_to_nodes_type(e) for e in road_network.getEdges()}

    return eid_crossing_dict

def get_crossing_type_mapper(road_network):

    is_crossing = crossing_mapper(road_network)

    crossing_map = {}

    for e in road_network.getEdges():
        eid = e.getID()

        if is_crossing[eid]:
            is_traffic_light = 'traffic_light' in (e.getFromNode().getType(), e.getToNode().getType())
            is_right_before_left = 'right_before_left' in (e.getFromNode().getType(), e.getToNode().getType())

            if is_traffic_light or is_right_before_left:
                crossing_map[eid] = 'slow_crossing'
            else:
                crossing_map[eid] = 'normal_crossing'

        else:
            crossing_map[eid] = 'not_crossing'

    return crossing_map

def count_crossings(road_network):

    dict_mapper = get_crossing_type_mapper(road_network)

    categories = {'not_crossing' : 0, 'slow_crossing' : 1, 'normal_crossing' : 2}
    cross_sorter = {cross_type : n for n, cross_type in enumerate(categories)}

    count_cross = Counter(sorted(dict_mapper.values(), key=lambda x: cross_sorter[x]))

    return count_cross

def measure_diversity(G, result_paths, attribute):
    no_connections = lambda x: G.es[x]['id'] != 'connection'
    fix_ls = lambda x: list(filter(no_connections, x))

    diversity_results = []

    for od in result_paths:

        paths = [fix_ls(x['ig']) for x in result_paths[od]]

        if len(paths) > 1:
            div_val = div(G, paths, 'traveltime')
            diversity_results.append(div_val)

    return diversity_results

def get_resulting_paths_and_measures(road_network, mobility_demand, result_paths,
                                     edge_weights,
                                     attribute = 'traveltime',
                                     algorithm_name = None,
                                     selection_criterion = None,
                                     random_state = None, G = None):


    # INSTANTIATE GRAPH IF NOT PROVIDED (OPTIONAL BUT FASTER)
    if G is None:
        G = from_sumo_to_igraph_network(road_network)

    # INSTANTIATE SELECTION CRITERION
    if selection_criterion is None:
        selection_criterion = np.random.choice

    # SET THE SEEDS FOR REPRODUCIBILITY
    if type(random_state) is int:
        np.random.seed(random_state)
    seed_iter = iter(np.random.randint(0, 999999, size = len(mobility_demand)))

    # GET RESULTING PATHS ACCORDING TO CRITERION
    routes_results = {}

    for v in mobility_demand:
        edges = tuple(mobility_demand[v]['edges'])

        np.random.seed(next(seed_iter))
        routes_results[v] = [selection_criterion(result_paths[edges])]

    # DIFFERENT REPRESENTATION OF THE RESULT PATHS (TO HELP W/ FUNCTIONS)
    vehicles = []
    routes_sumo = []
    routes_ig = []
    flat_routes_sumo = []
    flat_routes_ig = []

    for vehicle_key, path in routes_results.items():
        vehicles.append(int(vehicle_key.split('_')[1]))
        sumo_edges = path[0]['edges']
        ig_edges = list(map(lambda x: G['edge_sumo_ig'][x], sumo_edges))

        routes_sumo.append(sumo_edges)
        routes_ig.append(ig_edges)
        flat_routes_sumo += sumo_edges
        flat_routes_ig += ig_edges

    # DIVERSITY
    diversity_values = measure_diversity(G, result_paths, attribute)
    avg_diversity = np.mean(diversity_values)
    std_diversity = np.std(diversity_values)

    # POPULARITY
    popularity_ratio = count_popularity(edge_weights)
    pop_mapper = get_edge_popularity_map(edge_weights)['mapper']
    edge_traversed_by_popularity = Counter(map(lambda x: pop_mapper[x], flat_routes_ig))

    # CROSSINGS
    crossing_edge_ratio = count_crossings(road_network)
    crossing_dict = get_crossing_type_mapper(road_network)
    type_of_travelled_edges = Counter(map(lambda x: crossing_dict[x], flat_routes_sumo))

    # TEMP REDUNDANCY
    window, slide = 300, 60 # (s) or 5 minutes window and 1 minute slide
    temp_redundancy = compute_temp_redundancy_sliding(mobility_demand, dict(zip(vehicles, routes_ig)), window, slide)
    avg_temp_redundancy = np.mean(temp_redundancy)
    std_temp_redundancy = np.std(temp_redundancy)

    resulting_measures = {'algorithm_name' : algorithm_name,
                          
                          'random_state' : random_state, 

                          'CO2 Tons' : 0,

                          'Vehicles Traveltime' : 0,

                          'N Teleports' : 0,

                          'Avg Diversity of Suggestions' : avg_diversity,

                          'Std Diversity of Suggestions' : std_diversity,

                          'N Vehicles (Traveled Paths)' : len(routes_ig),

                          'Available Path Choices' : Counter(sorted([len(x) for x in result_paths.values()])),

                          'Road Coverage' : sum(G.es[set(flat_routes_ig)]['length']) / sum(G.es['length']),

                          'N Traveled Edges' : len(flat_routes_ig),

                          'Edge Coverage' : len(set(flat_routes_sumo)) / (len(set(G.es['id'])) - 1),

                          'Popularity Ratio': popularity_ratio,

                          'Crossing Ratio' : crossing_edge_ratio,

                          'Traveled Popularity' : edge_traversed_by_popularity,

                          'Traveled Crossings' : type_of_travelled_edges,

                          'Avg Traveled Edge Traveltime' : np.mean(G.es[flat_routes_ig][attribute]),
                          
                          'Std Traveled Edge Traveltime' : np.std(G.es[flat_routes_ig][attribute]),

                          'Avg Traveled Path Traveltime' : np.mean([sum(G.es[x][attribute]) for x in routes_ig]),

                          'Std Traveled Path Traveltime' : np.std([sum(G.es[x][attribute]) for x in routes_ig]),

                          'Total Redundancy' : redundancy(routes_ig),

                          'Interval Temp Redundancy (s)' : window,

                          'Avg Temp Redundancy' : avg_temp_redundancy,

                          'Std Temp Redundancy' : std_temp_redundancy,

                          'Entropy' : get_load_balance_entropy(G, routes_ig)}

    if algorithm_name is None:
        del resulting_measures['algorithm_name']

    return {'paths' : routes_results, 'measures' : resulting_measures}