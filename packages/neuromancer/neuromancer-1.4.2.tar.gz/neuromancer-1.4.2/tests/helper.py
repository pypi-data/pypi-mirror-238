import pytest
import torch
import torch.nn as nn
import pydot
import itertools
from neuromancer.system import Node, System, MovingHorizon
from collections import defaultdict


torch.manual_seed(0)


""" BEGIN TESTING METHODS FOR SYSTEM """
# PAIR OF BASIC NODE LIST AND ITS ADJACENCY LIST
def sample_basic_nodes():
    """ Create list of nodes that form a "basic" DAG """
    node_1 = Node(callable=lambda x: x, input_keys=['x1'], output_keys=['y1'], name='node_1')
    net_2 = torch.nn.Sequential(torch.nn.Linear(2, 5),
                                torch.nn.ReLU(),
                                torch.nn.Linear(5, 3),
                                torch.nn.ReLU(),
                                torch.nn.Linear(3, 1))
    node_2 = Node(callable=net_2, input_keys=['x2'], output_keys=['y2'], name='node_2')
    node_3 = Node(callable=lambda x1, x2: 2.*x1 - x2**2, input_keys=['y1', 'y2'], output_keys=['y3'], name='quadratic')
    return [node_1, node_2, node_3]


def sample_basic_nodes_edges():
    # The edges associated with sample basic nodes
    edges = defaultdict(list,
                       {'node_2': ['quadratic', 'out'],
                        'node_1': ['quadratic', 'out'],
                        'in': ['node_1', 'node_2'],
                        'quadratic': ['out']})
    return dict(edges)


# PAIR OF BASIC NODE LIST W/0 NAMES AND ITS ADJACENCY LIST
def sample_basic_nodes_without_names():
    """ Create list of nodes that form a "basic" DAG, nodes are without name """
    node_1 = Node(callable=lambda x: x, input_keys=['x1'], output_keys=['y1'])
    net_2 = torch.nn.Sequential(torch.nn.Linear(2, 5),
                                torch.nn.ReLU(),
                                torch.nn.Linear(5, 3),
                                torch.nn.ReLU(),
                                torch.nn.Linear(3, 1))
    node_2 = Node(callable=net_2, input_keys=['x2'], output_keys=['y2'])
    node_3 = Node(callable=lambda x1, x2: 2.*x1 - x2**2, input_keys=['y1', 'y2'], output_keys=['y3'])
    return [node_1, node_2, node_3]


def sample_basic_nodes_without_names_edges():
    """ The edges associated with sample_basic_nodes_without_names """

    edges = defaultdict(list,
            {'node_2': ['node_3', 'out'],
             'node_1': ['node_3', 'out'],
             'in': ['node_1', 'node_2'],
             'node_3': ['out']})
    return dict(edges)


# PAIR OF ISOLATED (isolated from dataset) NODE LIST AND ITS ADJACENCY LIST
def sample_isolated_graph_nodes():
    """ Create list of nodes that form an isolated graph (isolated from dataset) """
    node_1 = Node(callable=lambda x: x, input_keys=['x1'], output_keys=['y1'], name='node_1')
    node_2 = Node(callable=lambda x: x, input_keys=['y1'], output_keys=['x1'], name='node_2')
    return [node_1, node_2]


def sample_isolated_graph_nodes_edges():
    """ edges associated with isolated graph """
    edges = defaultdict(list, {'node_1': ['node_2', 'out'], 'node_2': ['out']})
    return dict(edges)


# PAIR OF SINGLE ELEMENT NODE LIST AND ITS ADJACENCY LIST
def sample_single_node_basic():
    """ create a node list containing single node """
    node_1 = Node(callable=lambda x: x, input_keys=['x1'], output_keys=['y1'], name='node_1')
    return [node_1]


def sample_single_node_basic_edges():
    """ edges for the single node graph """
    edges = defaultdict(list, {'in': ['node_1'], 'node_1': ['out']})
    return dict(edges)


# PAIR OF SINGLE ELEMENT NODE (with self-loop) LIST AND ITS ADJACENCY LIST
def sample_single_node_recurrent():
    """ create a node list containing a single node with self-loop """
    node_1 = Node(callable=lambda x: x, input_keys=['x1'], output_keys=['x1'], name='node_1')
    return [node_1]


def sample_single_node_recurrent_edges():
    """ edges for the self-loop single-node graph """
    edges = defaultdict(list, {'node_1': ['node_1', 'out'], 'in': ['node_1']})
    return dict(edges)


# Define fixtures for different (node list, adjacency list) pairs
@pytest.fixture(params=[(sample_basic_nodes(), sample_basic_nodes_edges()), \
                        (sample_basic_nodes_without_names(), sample_basic_nodes_without_names_edges()), \
                        #(sample_isolated_graph_nodes(), sample_isolated_graph_nodes_edges()), \
                        (sample_single_node_basic(), sample_single_node_basic_edges()), \
                        (sample_single_node_recurrent(), sample_single_node_recurrent_edges() )
                        ])
def get_nodes_and_edges(request):
    return request.param


# Define a fixture for testing pairs of varying (n_step, batch_sizes)
@pytest.fixture(params=[(0, 0), (1, 1), (1, 2), (2, 2), (2, 50)])
def get_nstep_batch(request):
    return request.param


#sample callable to operate on data dictionaries
def h(data_dict):
    for key in data_dict:
        data_dict[key] = data_dict[key] ** 2
    return data_dict


# Fixture to create (init_func, expected_error) pairs
@pytest.fixture(params=[(lambda x: x, None),(lambda x: x+1, TypeError), (h, None)])
def get_init_func_error_pairs(request):
    return request.param


def get_input_value_count(nodes):
    """
    Helper function to compute the cardinality of the node's input for each node in a node list

    :param nodes: (list) List of nodes, e.g. from sample_basic_nodes()
    :return: (dict: {str: int}) dictionary of node_name to number of input dimensions
        needed for its callable
    """
    input_value_count = {}
    for node in nodes:
        node_name = node.name
        if isinstance(node.callable, torch.nn.Module):
            first_layer = node.callable[0]
            if hasattr(first_layer, 'in_features'):
                # If the callable has an 'in_features' attribute, it's a nn layer
                input_value_count[node_name] = first_layer.in_features
        else:
            # For other callables, check the number of input keys
            input_value_count[node_name] = len(node.input_keys)
    return input_value_count


def generate_data_dict(sample_nodes, expected_edges, nstep, batch):
    """
    Helper function to generate random data dictionary based on node list, expected adjacency list,
    as well as nstep and batch size dimensions

    :param sample_nodes: (list) List of nodes, e.g. from sample_basic_nodes()
    :param expected_edges: (dict: {str, list}) Dictionary representation of the correct adjacency list for
        the input sample_nodes
    :param nstep (int): Number of steps
    :param batch (int): Batch size
    :return (dict {str: Tensor}): A data dictionary
    """
    data_dict = {}
    input_value_counts = get_input_value_count(sample_nodes)
    if 'in' in list(expected_edges.keys()):
        input_node_names = expected_edges['in']
    else:
        input_node_names = list(expected_edges.keys())
    input_nodes = [n for n in sample_nodes if n.name in input_node_names]
    input_node_names = [n.name for n in input_nodes]
    input_keys = [n.input_keys for n in input_nodes]
    input_keys = list(itertools.chain(*input_keys))

    idx = 0
    for input_key in input_keys:
        node_name = input_node_names[idx]
        # Generate a random tensor of shape [batch x nstep x 1]
        tensor = torch.rand(batch, nstep, input_value_counts[node_name])
        data_dict[input_key] = tensor
        idx += 1

    return data_dict


def generate_expected_output(node_list, nsteps, init_data):
    """
    Helper function to generate expected output based on the input node list, step size and
    initial data

    :param node_list: (list) List of nodes, e.g. from sample_basic_nodes()
    :param nstep (int): Number of steps
    :param init_data (dict {str: Tensor): Data dictionary to send through the node list
    :return (dict {str: Tensor}): The output of sending input data through node list
    """
    expected_data = init_data.copy()
    for i in range(nsteps):
        for node in node_list:
            indata = {k: expected_data[k][:, i] for k in node.input_keys}
            outdata = node(indata)
            expected_data = cat(expected_data, outdata)  # feed the data nodes
    return expected_data


def dict_equals(dict1, dict2):
    """
    Helper function to test equality of two data dictionaries

    :param dict_1 (dict {str: Tensor): one data dictionary
    :param dict_2 (dict {str: Tensor): second data dictionary
    :return (bool): True if data dictionaries have same key, and the (value) tensors
        are equal for each key
    """

    if len(dict1) != len(dict2):
        return False

    for key in dict1:
        if key not in dict2:
            return False
        tensor1 = dict1[key]
        tensor2 = dict2[key]

        if not torch.equal(tensor1, tensor2):
            return False
    return True

def list_equals_modulelist(lst, mod_list):
    """
    Helper function to test if a standard list "equals" a generic iterable (in this case
        a nn.ModuleList)

    :param dict_1 (dict {str: Tensor): one data dictionary
    :param dict_2 (dict {str: Tensor): second data dictionary
    :return (bool): True if data dictionaries have same key, and the (value) tensors
        are equal for each key
    """
    lst2 = []
    for elem in mod_list:
        lst2.append(elem)
    return lst == lst2

def cat(data3d, data2d):
    """
    Concatenates data2d contents to corresponding entries in data3d
    :param data3d: (dict {str: Tensor}) Input to a node
    :param data2d: (dict {str: Tensor}) Output of a node
    :return: (dict: {str: Tensor})
    """
    for k in data2d:
        if k not in data3d:
            data3d[k] = data2d[k][:, None, :]
        else:
            data3d[k] = torch.cat([data3d[k], data2d[k][:, None, :]], dim=1)
    return data3d


def is_valid_node_list(nodes):
    """
    Helper function that checks if within a list of nodes that all child nodes
    are to the right of parent nodes

    :param nodes: (list) A node list e.g. from sample_basic_nodes()
    :return: (bool) True if valid node list
    """
    dependency_dict = dict()
    for node in nodes:
        output_keys, in_keys = node.output_keys, node.input_keys
        for o in output_keys:
            if o not in dependency_dict:
                dependency_dict[o] = in_keys
            else:
                dependency_dict[o].append(in_keys)

    visited = set()
    for node in nodes:
        if not any(i in list(dependency_dict.keys()) for j in range(len(node.output_keys)) for i in
                   dependency_dict[node.output_keys[j]]):
            for n in node.output_keys:
                visited.add(n)
        else:
            for n in node.input_keys:
                if not n in visited:
                    return False
    return True
