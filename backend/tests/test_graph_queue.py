def test_grpah_queue(supply_grpah_data):
    response = supply_grpah_data
    correct_response = {'testname': {'TestGraph': ['nodes_data', 'links_data']},
                        'testname2': {'TestGraph2': ['nodes_data2', 'links_data2']}}
    assert response == correct_response

def test_grpah_data_dublicate_username(supply_grpah_data_dublicate_username):
    response = supply_grpah_data_dublicate_username
    correct_response = {'testname': {'TestGraph': ['nodes_data', 'links_data'], 
    'TestGraph2': ['nodes_data2', 'links_data2']}}
    assert response == correct_response

def test_grpah_data_from_Vue(supply_grpah_data_from_Vue):
    response = supply_grpah_data_from_Vue
    correct_response = {'user1': ['testGraph1'],'user2': ['testGraph2']}
    assert response == correct_response
    
def test_dublicate_grpah_data_from_Vue(supply_dublicate_grpah_data_from_Vue):
    response = supply_dublicate_grpah_data_from_Vue
    correct_response = {'user1': ['testGraph1','testGraph2'],'user3': ['testGraph3']}
    assert response == correct_response

def test_dublicate_data_from_Vue(supply_dublicate_data_from_Vue):
    response = supply_dublicate_data_from_Vue
    correct_response = {'isDublicated': True, 'index': 0}
    assert response == correct_response

def test_dublicate_data_from_Vue(supply_bad_dublicate_data_from_Vue):
    response = supply_bad_dublicate_data_from_Vue
    correct_response = {'isDublicated': False, 'index': ''}
    assert response == correct_response

def test_common_graphs(supply_common_graphs):
    response = supply_common_graphs
    correct_response = [{'TestGraph1': ['nodes_data', 'links_data']}, 
    {'TestGraph2': ['nodes_data2', 'links_data2']}]
    assert response == correct_response

def test_common_graphs_single_person(supply_common_graphs_single_person):
    response = supply_common_graphs_single_person
    correct_response = [{'TestGraph1': ['nodes_data', 'links_data']}, 
    {'TestGraph2': ['nodes_data', 'links_data']}]
    assert response == correct_response

def test_union_graph(supply_union_graph):
    response = supply_union_graph
    correct_response = [['nodes_data', 'nodes_data2'], ['links_data', 'links_data2']]
    assert response == correct_response