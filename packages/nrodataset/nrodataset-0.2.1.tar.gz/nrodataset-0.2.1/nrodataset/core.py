# Insert your code here.
import networkx as nx
import pkg_resources
import scipy.io as sio


def load_networks(network_type, network_size, isd=0, k=4):
    if network_type[:5] != 'real-':
        file_path = pkg_resources.resource_filename(__name__,
                                                    f'networks/{network_type}_isd{isd}_k{k}_{network_size}.mat')
    else:
        file_path = pkg_resources.resource_filename(__name__, f'networks/real-{network_type}.mat')
    mat = sio.loadmat(file_path)
    num_instance = mat['num_instances'][0, 0]
    assert isd == mat['isd'][0, 0]
    assert network_type == mat['network_type'][0]
    assert network_size == mat['size'][0, 0]
    isd = mat['isd'][0, 0]
    isw = mat['isw'][0, 0]
    original_networks = []
    optimized_networks = []
    for i in range(num_instance):
        ori_adj = mat['original'][0, i]['adj'][0, 0]
        if not isd:
            ori_graph = nx.from_scipy_sparse_matrix(ori_adj, create_using=nx.Graph)
        else:
            ori_graph = nx.from_scipy_sparse_matrix(ori_adj, create_using=nx.DiGraph)

        opt_adj = mat['optimized'][0, i]['adj'][0, 0]
        if not isd:
            opt_graph = nx.from_scipy_sparse_matrix(opt_adj, create_using=nx.Graph)
        else:
            opt_graph = nx.from_scipy_sparse_matrix(opt_adj, create_using=nx.DiGraph)
        original_networks.append(ori_graph)
        optimized_networks.append(opt_graph)
    res_dic = {
        'isd': isd,
        'isw': isw,
        'number_of_networks': num_instance,
        'original_networks': original_networks,
        'optimized_networks': optimized_networks,
        'network_type': network_type,
    }
    return res_dic
