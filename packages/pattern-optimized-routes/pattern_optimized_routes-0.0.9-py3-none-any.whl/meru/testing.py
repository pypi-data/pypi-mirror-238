from .extract_measures import get_resulting_paths_and_measures
from .multilevel import MultiLevelModel
from .baselines import BaselineModel

from .simulate import save_sumo_routes
from .simulate import simulate_sumo_paths
from .simulate import save_results

from routing_lib import from_sumo_to_igraph_network

import numpy as np
from tqdm import tqdm
from datetime import datetime
from itertools import combinations

import sumolib
import json
import os

def pipeline_test_reproducible_kdistributions(road_network_path, output_folder, 
                                              mobility_demand_path, distributions_to_test,
                                              k = 3, attribute = 'traveltime', 
                                              experiment_per_rs = 10, 
                                              random_state = 42, increase_rs_by = 3,
                                              sample = None):
  
    os.makedirs(output_folder, exist_ok=True)
    
    road_network = sumolib.net.readNet(road_network_path, withInternal=False)
    G = from_sumo_to_igraph_network(road_network)

    with open(mobility_demand_path, 'r') as f:
        mobility_demand = json.loads(f.read())
        # Get unique paths to predict (same OD pair)
        od_set = {tuple(mobility_demand[v]['edges']) for v in mobility_demand}

    def sample_md(md, od_pairs):
        "Sample mobility demand according to a OD Matrix. (Lazy testing)"
        sampled_vehicles = list(filter(lambda x: tuple(md[x]['edges']) in od_pairs, list(md)))
        return {key : md[key] for key in sampled_vehicles}

    if type(sample) is int:
        # Redefine OD matrix according to the selected sample value
        np.random.seed(random_state)
        random_indexes = np.random.choice(np.arange(len(od_set)), size = sample)
        sampled_od = {(from_edge, to_edge) for from_edge, to_edge in np.array(list(od_set))[random_indexes]}

        # Redefine mobility demand according to OD Matrix
        mobility_demand = sample_md(mobility_demand, sampled_od)
        od_set = {tuple(mobility_demand[v]['edges']) for v in mobility_demand}

    path_results = {param : [] for param in distributions_to_test}
    ew_results = {param : [] for param in distributions_to_test}

    starting_random_state = random_state

    for param in distributions_to_test:
        model = MultiLevelModel(G, k, attribute)
        model.parameter_selection(n_vehicles = param, verbose = False, random_state = random_state)

        for exp in range(experiment_per_rs):

              if random_state is not None:
                  random_state = starting_random_state if exp == 0 else random_state * increase_rs_by
              
              print('Test n°:', exp, 
                    'Parameter selected:', model.fitted_vehicles, 
                    'Random state selected:', random_state)
              
              model.fit(random_state = random_state)
              
              result_paths = dict()
              for from_edge, to_edge in tqdm(od_set, desc="Paths Computed"):
                  result_paths[(from_edge, to_edge)] = model.predict(from_edge, to_edge)

              edge_weights = model.weights[1]

              paths_and_measures = get_resulting_paths_and_measures(road_network, mobility_demand, result_paths, edge_weights, attribute, model.algorithm_name,
                                                                    selection_criterion = np.random.choice, random_state = random_state, G = G)
              
              ew_results[param].append((random_state, edge_weights))
              path_results[param].append((random_state, paths_and_measures['paths']))

              current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
              file_name = f'{model.algorithm_name}_{current_time}'
              save_sumo_routes(paths_and_measures['paths'], mobility_demand, save_path = output_folder, name = file_name)

              # simulation parameters
              route_filename = f'{output_folder}/sumo_routes_{file_name}.rou.xml'
              simulation_result = simulate_sumo_paths(paths_and_measures, road_network_path, route_filename)
              print('******************')
              for key, value in simulation_result.items():
                  print(f'{key}: {value}')
              print('******************\n')

              df_measure_results = save_results(paths_and_measures['measures'], save_path = output_folder)

    return {'measures' : df_measure_results, 'weights' : ew_results, 'paths' : path_results}

def generate_parameter_combinations(algorithm_parameters):
    for algorithm_name, parameters in algorithm_parameters.items():
        parameter_sets = []

        # Generate a list of dictionaries representing parameter combinations
        for parameter_name, values in parameters.items():
            parameter_sets.extend([{parameter_name: value} for value in values])

        # Generate combinations of parameter sets
        for combination in combinations(parameter_sets, len(parameters)):
            combined_parameters = {}
            for sub_parameter_set in combination:
                combined_parameters.update(sub_parameter_set)

            # Check if the combined dictionary has the expected number of parameters
            if len(combined_parameters) == len(parameters):
                yield algorithm_name, combined_parameters


def generate_output_string(algorithm_name, parameter_set):
    output = algorithm_name
    for parameter_name, value in parameter_set.items():
        output += f'_{parameter_name}{str(value).replace(".", "")}'
    return output


def pipeline_test_reproducible_baselines(road_network_path, output_folder, 
                                         mobility_demand_path, algorithm_parameters,
                                         meru_model = None,
                                         k = 3, attribute = 'traveltime', 
                                         experiment_per_rs = 10, 
                                         random_state = 42, increase_rs_by = 3, 
                                         sample = None):
  
    os.makedirs(output_folder, exist_ok=True)
    
    road_network = sumolib.net.readNet(road_network_path, withInternal=False)
    G = from_sumo_to_igraph_network(road_network)

    with open(mobility_demand_path, 'r') as f:
        mobility_demand = json.loads(f.read())
        # Get unique paths to predict (same OD pair)
        od_set = {tuple(mobility_demand[v]['edges']) for v in mobility_demand}

    def sample_md(md, od_pairs):
        "Sample mobility demand according to a OD Matrix. (Lazy testing)"
        sampled_vehicles = list(filter(lambda x: tuple(md[x]['edges']) in od_pairs, list(md)))
        return {key : md[key] for key in sampled_vehicles}

    if type(sample) is int:
        # Redefine OD matrix according to the selected sample value
        np.random.seed(random_state)
        random_indexes = np.random.choice(np.arange(len(od_set)), size = sample)
        sampled_od = {(from_edge, to_edge) for from_edge, to_edge in np.array(list(od_set))[random_indexes]}

        # Redefine mobility demand according to OD Matrix
        mobility_demand = sample_md(mobility_demand, sampled_od)
        od_set = {tuple(mobility_demand[v]['edges']) for v in mobility_demand}

    path_results = {generate_output_string(*x) : [] for x in generate_parameter_combinations(algorithm_parameters)}

    if meru_model is None:
        meru_model = MultiLevelModel(G, k, attribute)
        print('Performing parameter selection!')
        meru_model.parameter_selection(verbose = True, random_state = random_state)

    edge_weights = meru_model.tested_parameters[-1][1][1]

    starting_random_state = random_state

    # Generate and print the output for each algorithm and parameter set
    for algorithm_name, parameter_set in generate_parameter_combinations(algorithm_parameters):

        for exp in range(experiment_per_rs):

              if random_state is not None:
                  random_state = starting_random_state if exp == 0 else random_state * increase_rs_by

              algo_name_out = generate_output_string(algorithm_name, parameter_set)

              model = BaselineModel(algorithm_name, G, k, attribute, 
                                    algo_name_out = algo_name_out, 
                                    compute_in_subgraph = False, **parameter_set)
              
              print('Algo_Param', algo_name_out, 'Test n°:', exp,
                    'Parameters selected:', meru_model.fitted_vehicles,
                    'Random state selected:', random_state)
              
              result_paths = dict()
              for from_edge, to_edge in tqdm(od_set, desc="Paths Computed"):
                  result_paths[(from_edge, to_edge)] = model.predict(from_edge, to_edge)

              paths_and_measures = get_resulting_paths_and_measures(road_network, mobility_demand, result_paths, edge_weights, attribute, model.algo_name_out,
                                                                    selection_criterion = np.random.choice, random_state = random_state, G = G)
              
              path_results[algo_name_out].append((random_state, paths_and_measures['paths']))

              current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
              file_name = f'{algo_name_out}_{current_time}'
              save_sumo_routes(paths_and_measures['paths'], mobility_demand, save_path = output_folder, name = file_name)

              # simulation parameters
              route_filename = f'{output_folder}/sumo_routes_{file_name}.rou.xml'
              simulation_result = simulate_sumo_paths(paths_and_measures, road_network_path, route_filename)
              print('******************')
              for key, value in simulation_result.items():
                  print(f'{key}: {value}')
              print('******************\n')

              df_measure_results = save_results(paths_and_measures['measures'], save_path = output_folder)

    return {'measures' : df_measure_results, 'weights' : {meru_model.fitted_vehicles : edge_weights}, 'paths' : path_results}