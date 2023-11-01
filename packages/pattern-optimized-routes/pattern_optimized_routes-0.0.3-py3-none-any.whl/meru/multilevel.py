from routing_lib import *
from shapely.geometry import Point, Polygon
from sklearn.preprocessing import MinMaxScaler
from skmob.tessellation.tilers import tiler

import sys
import os
import geopandas as gpd
import numpy as np
from tqdm import tqdm

import warnings

def make_gdf_from_geom(geom):
    """
    Creates a GeoDataFrame from a provided geometry array.

    Parameters:
        geom (geometry): The input geometry.

    Returns:
        result_gdf (GeoDataFrame): The resulting GeoDataFrame.
    """

    # Create a GeoDataFrame with the provided geometry and set CRS to EPSG:4326 (WGS84)
    result_gdf = gpd.GeoDataFrame(geometry = geom).set_crs('EPSG:4326')
    # Reproject the GeoDataFrame to its own CRS (since the geometries may be raw)
    result_gdf.to_crs(result_gdf.crs)

    return result_gdf

def get_edges_to_tile(G, tile_shape = 'squared', tile_side_meters = 1000):

    """
    Assign a tile to each edge.

    Parameters:
        G (graph): The input iGraph road network
        tile_shape (str): The shape of the tiles (available in skmob.tessellation.tilers, default is 'squared')
        tile_side_meters (int): The side length in meters for a single tile (default is 1000)

    Returns:
        edge_tile_dict (dict): A dictionary mapping edge IDs to their corresponding tile IDs.
    """

    from_array = np.array([x['from'] for x in G.es['coordinates']]) # Extract 'from' coordinates from edges
    to_array = np.array([x['to'] for x in G.es['coordinates']]) # Extract 'to' coordinates from edges

    # Retrieve the boundaries of the road network
    maxmin_coord = ((max(from_array[:,0].max(), to_array[:,0].max()),
                    max(from_array[:,1].max(), to_array[:,1].max())),
                    (min(from_array[:,0].min(), to_array[:,0].min()),
                    min(from_array[:,1].min(), to_array[:,1].min())))

    # Create a bounding box around the coordinates
    map____coords = (maxmin_coord[0],
                    (maxmin_coord[1][0], maxmin_coord[0][1]),
                    maxmin_coord[1],
                    (maxmin_coord[0][0], maxmin_coord[1][1]))

    # Create a GeoDataFrame representing the city shape using the bounding box
    city_shape = make_gdf_from_geom([Polygon(map____coords)])

    # Generate a tiling of the city shape based on the specified parameters
    kroad_tess = tiler.get(tile_shape, base_shape = city_shape, meters = tile_side_meters)
    # Create a GeoDataFrame of points from the 'from' coordinates
    coord_pts = make_gdf_from_geom([Point(*p) for p in from_array])

    # Spatially join the points with the tiles and sort by index (which is the original edge index)
    sorted_tiles = coord_pts.sjoin(kroad_tess).sort_index()['tile_ID'].astype(int).tolist()

    # Create a dictionary mapping edge IDs to their corresponding tile IDs
    edge_tile_dict = {eid : tile_id for tile_id, eid in zip(sorted_tiles, G.es['original_id'])}

    return edge_tile_dict

def normalize_eru(id_eru_dict):
    """
    Normalizes the Expected Road Usage (ERU) values in a dictionary.

    Parameters:
        id_eru_dict (dict): A dictionary mapping IDs to their ERU values.

    Returns:
        id_eru_dict (dict): The updated dictionary with normalized ERU values.
    """

    to_scale = np.array(list(id_eru_dict.items()), dtype=np.float64)  # Convert dictionary items to array

    data = to_scale[:, 1]  # Extract ERU values
    data_reshaped = np.array(list(data)).reshape(-1, 1)  # Reshape data for scaling

    scaler = MinMaxScaler()  # Initialize MinMaxScaler
    normalized_data = scaler.fit_transform(data_reshaped).ravel().tolist()  # Normalize data and convert to list

    to_scale[:, 1] = normalized_data  # Update the ERU values with normalized values

    for key, val in to_scale:  # Iterate through the scaled data
        id_eru_dict[int(key)] = val  # Update the original dictionary with normalized values

    return id_eru_dict

def get_source_kroad_dist(G, list_routes, edge_tile_dict, mds_threshold = 0.8, normalize = True):
    """
    Computes a k-road distribution, or the expected road usage in this context,
    with the provided paths and mapping of edges to tiles.

    Parameters:
        G (Graph): The input graph.
        list_routes (list): List of routes.
        edge_tile_dict (dict): A dictionary mapping edge IDs to their corresponding tile IDs.
        mds_threshold (float, optional): Major Driver Sources threshold (default is 0.8).
        normalize (bool, optional): Flag to normalize the results (default is True).

    Returns:
        expected_road_usage_dict (dict): A dictionary mapping edge IDs to expected road usage values.
    """

    # Compute driver sources, major driver sources, and k-road values
    ds_dict = compute_driver_sources(list_routes, edge_tile_dict, origin = True)
    mds_dict = compute_MDS(ds_dict, mds_threshold)
    k_road_vals = compute_k_road(mds_dict)

    # Initialize expected road usage dictionary with default value 0
    expected_road_usage_dict = {eid: k_road_vals.get(eid, 0) for eid in range(len(G.es))}

    if normalize:
        expected_road_usage_dict = normalize_eru(expected_road_usage_dict)

    return expected_road_usage_dict

def get_kroad_levels(G, k, attribute, edge_tile_dict, expected_vehicles,
                     normalize = True, verbose = True, random_state = None):

    """
    Generates k-road levels for a graph based on specified parameters.

    Parameters:
        G (Graph): The input graph.
        k (int): The number of k-road levels to generate (= desired alternative paths).
        attribute (str): The attribute to use for calculations.
        edge_tile_dict (dict): A dictionary mapping edge IDs to their corresponding tile IDs.
        expected_vehicles (int): The number of expected vehicles (graph scans to perform).
        normalize (bool): To normalize the values or not (default is True).
        verbose (bool): To choose if a progress bar should be shown or not (default is True).
        random_state (int, optional): Seed for random number generation (default is None).

    Returns:
        kroad_levels (dict): A dictionary containing k-road levels and their associated popularity values.
    """

    warnings.filterwarnings("ignore")

    if type(random_state) == int:
        np.random.seed(random_state)

    # Setting an upper limit to avoid RAM overload
    size_to_square = 15000 if expected_vehicles >= 15000 else expected_vehicles

    # I squared to include the rare cases two random points are not connected
    seed_iter = iter(np.random.randint(0, 999999, size = k*size_to_square**2))

    kroad_levels = {}
    tmp_attribute = f'tmp_{attribute}'

    G.es[tmp_attribute] = G.es[attribute]

    # Filter out edges with ID 'connection'
    edge_list = list(filter(lambda x: x['id'] != 'connection', G.es))

    for n in range(1, k+1):

        list_routes = list()

        # Initialize progress bar with total number of expected_vehicles
        with tqdm(total=expected_vehicles, leave=True, file=sys.stdout if verbose else open(os.devnull, 'w')) as pbar:

            while len(list_routes) < expected_vehicles:

                np.random.seed(next(seed_iter))  # Retrieve a seed from the iterator

                od_indexes = np.random.randint(0, len(edge_list), size=2)  # Generate random edge indexes
                from_edge = edge_list[od_indexes[0]]['id']  # Get 'from' edge ID
                to_edge = edge_list[od_indexes[1]]['id']  # Get 'to' edge ID

                # scan if possible otherwise move to other two random edges
                try:
                    sp = get_shortest_path(G, from_edge, to_edge, tmp_attribute)
                except:
                    continue

                # skip if the resulting path is comprised of only origin and destination
                if len(sp['ig']) <= 2:
                    continue
                else:
                    list_routes.append(sp['ig'])

                pbar.update(1)

        kroad_levels[n] = get_source_kroad_dist(G, list_routes, edge_tile_dict, mds_threshold = 0.8, normalize = normalize)

        # Reassign the weights according to the current expected road usage level
        for e in G.es:
            if e["id"] != "connection":
                idx = G["edge_sumo_ig"][e['id']]
                k_road = kroad_levels[n][idx]
                e[tmp_attribute] *= (1+k_road)

    return kroad_levels

def kroad_weight_update(G, edges, attribute, kroad_levels, lvl):
    """
    Update edge weights based on k-road level.

    Parameters:
        G (Graph): The input graph.
        edges (list): List of edges to penalize (either of the Graph or of the Path).
        attribute (str): The attribute to update.
        kroad_levels (dict): A dictionary containing k-road levels and their associated road usage values.
        lvl (int): The specific k-road level to use for weight update.

    """
    # Get the popularity values for the specified k-road level (otherwise avoid update)
    k_dist = kroad_levels.get(lvl, None)

    if k_dist is not None:
        for e in edges:  # Iterate through the list of edges
            if e["id"] != "connection":  # Skip edges with ID 'connection'
                idx = G["edge_sumo_ig"][e["id"]]  # Get the corresponding index
                k_road = k_dist[idx]  # Get the k-road value for the edge
                e[attribute] *= (1+k_road)  # Update the edge weight using the k-road value

def multilevel_edge_penalization(G, from_edge, to_edge, k, attribute, kroad_levels, all_distinct=True, remove_tmp_attribute=True, max_iter=1e3):
    """
    Apply edge penalization with the multilevel based expected road usage

    Parameters:
        G (Graph): The input graph.
        from_edge (Edge or str): The starting edge (or its ID).
        to_edge (Edge or str): The target edge (or its ID).
        k (int): The k desired number of paths to return.
        attribute (str): The attribute to be updated.
        kroad_levels (dict): A dictionary containing k-road levels and their associated road usage values.
        all_distinct (bool, optional): Flag for finding all distinct shortest paths (default is True).
        remove_tmp_attribute (bool, optional): Flag to remove temporary attribute after processing (default is True).
        max_iter (int, optional): Maximum number of iterations for finding alternative paths (default is 1000).

    Returns:
        result_list (list): List of k alternative routes.
    """

    from_edge = from_edge.getID() if type(from_edge) != str else from_edge  # Get ID if edge object is provided
    to_edge = to_edge.getID() if type(to_edge) != str else to_edge  # Get ID if edge object is provided

    tmp_attribute = f'tmp_{attribute}'  # Create temporary attribute name
    G.es[tmp_attribute] = G.es[attribute]  # Copy the specified attribute to the temporary attribute

    k_level = [1]  # Assigned to a list to allow modification by reference

    kroad_weight_update(G, G.es, tmp_attribute, kroad_levels, k_level[0])  # Update Graph weights with 1st k-road level

    # Function called after a path is found
    def update_edges_weights(edge_list, attribute, p=0):
        """
        Function called after a path is found,
        """
        k_level[0] += 1
        kroad_weight_update(G, edge_list, attribute, kroad_levels, 1)  # Update path weights with 1st k-road level
        kroad_weight_update(G, G.es, attribute, kroad_levels, k_level[0])  # Update Graph weights with next k-road level

    dict_args = {}  # Additional arguments (mandatory)

    apply_to = "sp_edges"  # Apply the function to shortest path edges

    result_list = apply_penalization(G, from_edge, to_edge, k, tmp_attribute, update_edges_weights, dict_args,
                                    apply_to=apply_to, all_distinct=all_distinct,
                                    remove_tmp_attribute=remove_tmp_attribute, max_iter=max_iter)

    if remove_tmp_attribute:
        del G.es[tmp_attribute]  # Delete temporary attribute after processing

    return result_list  # Return the list of paths with penalized weights

def balance_test(kroad_levels, lvl = 1, threshold = 0.0):
    """
    Perform a balance test on a specific k-road level.

    Parameters:
        kroad_levels (dict): A dictionary containing k-road levels and their associated ERU values.
        lvl (int): The level of the k-road levels to analyze (default is 1)
        threshold (float): Threshold value for the balance test.

    Returns:
        bool: True if the data is considered balanced, False otherwise.
    """

    import matplotlib.pyplot as plt

    # Extract ERU values from the k-road level and take the logarithm (ignoring zeros)
    data = np.log2(list(filter(lambda x: x!=0, kroad_levels[lvl].values())))

    # Generate box plot data from the log-transformed ERU values
    box_plot_data = plt.boxplot(data)
    plt.close()  # Close the plot to avoid displaying it

    # Calculate the first quartile (q1) and minimum value from the box plot data
    q1 = box_plot_data['boxes'][0].get_ydata()[0]  # Get the first quartile value
    min_val = min(box_plot_data['whiskers'][0].get_ydata())  # Get the minimum value

    # Calculate the relative difference between q1 and min_val
    relative_difference = abs((q1 - min_val) / q1)

    if relative_difference > threshold:  # Check if the relative difference exceeds the threshold
        return True  # Return True if the data is considered balanced
    else:
        return False  # Return False if the data is considered not balanced

class MultiLevelModel(object):
    """
    A class representing a multi-level model for edge penalization.

    Attributes:
        G (Graph): The input graph.
        k (int): The number of k-road levels.
        attribute (str): The attribute to be updated.
        params (dict): Additional parameters for model configuration.
        edge_tile_dict (dict): A dictionary mapping edge IDs to their corresponding tile IDs.
        fitted_vehicles (int): The number of fitted vehicles (selected during parameter selection).
        weights (dict): Model weights for edge penalization.
        tested_parameters (list): A list containing the balance-tested distributions during tuning.
        algorithm_name (str): A tag containing 'MERU' as a string

    Methods:
        __init__: Initializes the MultiLevelModel.
        parameter_selection: Selects the optimal number of vehicles based on balance testing.
        fit: Fits the model weights using the selected number of vehicles.
        predict: Predicts the least popular path between two edges.

    Note:
        params accepted are {'default_vehicles' : int, 'perform_tuning' : bool, 'tuning_parameters' : List[int]},
        where 'default_vehicles' is mandatory.

    """

    def __init__(self, G, k, attribute, params = {'default_vehicles' : 3500}):
        """
        Initializes the MultiLevelModel.

        Parameters:
            G (Graph): The input graph.
            k (int): The number of k-road levels.
            attribute (str): The attribute to be updated.
            params (dict): Additional parameters for model configuration.

        Raises:
            Exception: If 'params' is None or 'default_vehicles' is not provided.

        """

        self.G = G
        self.k = k
        self.attribute = attribute
        self.algorithm_name = 'MERU'

        self.edge_tile_dict = get_edges_to_tile(G, 'squared', 1000)

        if params is None:
            raise Exception('Must provide a dictionary with at least the "default_vehicles" value')
        else:
            assert type(params) is dict, "The parameters must be provided as a Dictionary"
            assert 'default_vehicles' in params, 'At least default_vehicles (int) must be provided as a parameter'
            self.params = params

    def parameter_selection(self, balance_threshold = 0, n_vehicles = None, verbose = True, random_state = None):
        """
        Selects the optimal number of vehicles based on balance testing.

        Parameters:
            balance_threshold(int, optional): The distribution relative difference of |(Q1 - min_x) / Q1| that must be exceeded (default is 0)
            n_vehicles (int, optional): Number of vehicles (manual input).
            verbose (bool, optional): Flag for printing progress messages (default is True).
            random_state (int, optional): Seed for random number generation (default is None).

        Raises:
            AssertionError: If 'n_vehicles' is provided and is not an integer.

        """

        assert n_vehicles is None or type(n_vehicles) is int, "n_vehicles is expected as None or as an Integer"
        self.tested_parameters = []

        if n_vehicles:
            self.fitted_vehicles = n_vehicles # In case it is launched manually

        else:
            perform_tuning = self.params.get('perform_tuning', True)
            tuning_parameters = self.params.get('tuning_parameters', [200, 500, 1000, 2000, 3500, 5000, 7000, 12000, 15000, 17000, 20000, 30000, 50000, 75000, 100000, 200000])
            self.fitted_vehicles = self.params['default_vehicles'] # In case the tuning fails

            if perform_tuning:
                assert all(type(x) is int for x in tuning_parameters), 'tuning_parameters is expected as a List of Integers!'

                test_distributions = []

                for v in tuning_parameters:
                    kv_distribution = get_kroad_levels(self.G, 1, self.attribute, self.edge_tile_dict,
                                                      expected_vehicles = v, verbose = verbose, random_state = random_state)

                    self.tested_parameters.append((v, kv_distribution))
                    test = balance_test(kv_distribution, threshold = balance_threshold)
                    test_distributions.append(test)

                    if test:
                        if verbose:
                            print('Parameter Selected:', v)
                        self.fitted_vehicles = v
                        break

                if not any(test_distributions):
                    print('Parameter Selection Failed, using default_vehicles parameter: ', self.fitted_vehicles)

    def fit(self, verbose = True, random_state = None):
        """
        Fits the model weights using the selected number of vehicles.

        Parameters:
            verbose (bool, optional): Flag for printing progress messages (default is True).
            random_state (int, optional): Seed for random number generation (default is None).

        Raises:
            AttributeError: If 'fitted_vehicles' attribute is not present.

        """

        self.algorithm_name = f'MERU{self.fitted_vehicles}'
        assert hasattr(self, 'fitted_vehicles'), "You must run parameter selection before fitting the weights!"
        self.weights = get_kroad_levels(self.G, self.k, self.attribute, self.edge_tile_dict, self.fitted_vehicles,
                                        verbose = verbose, random_state = random_state)

    def predict(self, from_edge, to_edge, k = None):
        """
        Predicts the "least popular" paths between two edges.

        Parameters:
            from_edge (Edge or str): The starting edge (or its ID).
            to_edge (Edge or str): The target edge (or its ID).
            k (int, optional): The k-road level to use for penalization.

        Returns:
            dict: Dictionary containing the "least popular" paths information.

        """

        if k is not None:
            what_message = 'Warning: You are using a different k from the one used in the model'
            why_message = "It's not the expected use of the multilevel algorithm"
            ignore_if_message = "Ignore if you are using the simple solution with only one graph weight update"
            warnings.warn(f"{what_message}. {why_message}. {ignore_if_message}.")
        else:
            k = self.k

        return multilevel_edge_penalization(self.G, from_edge, to_edge, k, self.attribute, self.weights, max_iter=5)
