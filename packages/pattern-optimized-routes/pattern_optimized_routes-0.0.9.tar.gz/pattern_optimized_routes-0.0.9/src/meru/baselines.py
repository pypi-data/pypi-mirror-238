from routing_lib.routing_algorithms import path_penalization
from routing_lib.routing_algorithms import graph_randomization
from routing_lib.routing_algorithms import path_randomization
from routing_lib.routing_algorithms import duarouter
from routing_lib.routing_algorithms import k_disjointed
from routing_lib.routing_algorithms import no_randomization
from routing_lib.routing_algorithms import k_mdnsp
from routing_lib.routing_algorithms import kspml
from routing_lib.routing_algorithms import kspmo
from routing_lib.routing_algorithms import plateau_algorithm
from routing_lib.routing_algorithms import k_shortest_paths
import inspect
import igraph


class BaselineModel(object):
    """
    Initialize one of the baselines

    Attributes:
        G (Graph): The input graph.
        k (int): The number of k-road levels.
        attribute (str): The attribute to be updated.

    Methods:
        __init__: Initializes the BaselineModel.
        predict: Predicts the path between two edges.

    """

    def __init__(self, algorithm_name, G, k, attribute, **kwargs):
        """
        Initializes one of these algorithms: PP, GR, PR, DR, KD, NR, KMMD, KML, KMO, PLAT and KSP

        Parameters:
            algorithm_name (str) : The name of the algorithm to apply
            G (Graph): The input graph.
            k (int): The number of k-road levels.
            attribute (str): The attribute to be updated.

        """
        
        algo_dict =  {'PP' : path_penalization,
                      'GR' : graph_randomization,
                      'PR' : path_randomization,
                      'DR' : duarouter,
                      'KD' : k_disjointed,
                      'NR' : no_randomization,
                      'KMD' : k_mdnsp,
                      'KML' : kspml,
                      'KMO' : kspmo,
                      'PLAT' : plateau_algorithm,
                      'KSP' : k_shortest_paths}

        self.algorithm_name = algorithm_name
        assert self.algorithm_name in algo_dict, f'{self.algorithm_name} is not valid, choose from: {", ".join(list(algo_dict))}'
        self.G = G
        assert type(G) is igraph.Graph, 'G must be an igraph.Graph'
        self.k = k
        assert type(self.k) is int, "k must be an integer"
        self.attribute = attribute
        assert self.attribute in list(G.es[0].attributes()), f'{self.attribute} is not valid, choose from: {", ".join(list(G.es[0].attributes()))}'
        
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        self.algorithm = algo_dict[self.algorithm_name]

        mandatory = ['G', 'k', 'attribute', 'from_edge', 'to_edge']
        params = inspect.signature(self.algorithm).parameters
        param_types = (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        empty = inspect.Parameter.empty
        pos_params = [k for k, p in params.items() if p.default == empty and p.kind in param_types and k not in mandatory]

        assert all([hasattr(self, param_name) for param_name in pos_params]), f'One or more of the required parameters is missing: {", ".join(list(pos_params))}'

    def predict(self, from_edge, to_edge):
        """
        Predicts the paths between two edges.

        Parameters:
            from_edge (Edge or str): The starting edge (or its ID).
            to_edge (Edge or str): The target edge (or its ID).

        Returns:
            dict: Dictionary containing the paths information.

        """
        
        params = inspect.signature(self.algorithm).parameters
        param_types = (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        empty = inspect.Parameter.empty
        pos_params = [k for k, p in params.items() if p.default == empty and p.kind in param_types]

        required_parameters = {}

        for param in pos_params:
            if param not in ('from_edge', 'to_edge'):
                required_parameters[param] = getattr(self, param)

        required_parameters['from_edge'] = from_edge
        required_parameters['to_edge'] = to_edge

        return self.algorithm(**required_parameters)
