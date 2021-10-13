"""Supply data for tests"""
import pytest
import json
import instagrapi
from ..ig_parser import IGUser
from ..graph_queue import GraphQueue


@pytest.fixture
def supply_grpah_data():
    graph_queue = GraphQueue()
    username = ['testname']
    graph_name = 'TestGraph'
    graph_data = ['nodes_data', 'links_data']
    graph_queue.set_graph_queue(graph_data, username, graph_name)
    username2 = ['testname2']
    graph_name2 = 'TestGraph2'
    graph_data2 = ['nodes_data2', 'links_data2']
    graph_queue.set_graph_queue(graph_data2, username2, graph_name2)
    response = graph_queue.get_grpah_queue()
    return response

@pytest.fixture
def supply_grpah_data_dublicate_username():
    graph_queue = GraphQueue()
    username = ['testname']
    graph_name = 'TestGraph'
    graph_data = ['nodes_data', 'links_data']
    graph_queue.set_graph_queue(graph_data, username, graph_name)
    username2 = ['testname']
    graph_name2 = 'TestGraph2'
    graph_data2 = ['nodes_data2', 'links_data2']
    graph_queue.set_graph_queue(graph_data2, username2, graph_name2)
    response = graph_queue.get_grpah_queue()
    return response

@pytest.fixture
def supply_grpah_data_from_Vue():
    graph_queue = GraphQueue()
    data_Vue = ['testGraph1 user1', 'testGraph2 user2']
    graph_queue.graph_queue_Vue = data_Vue
    graph_queue.parse_data_from_Vue()
    response = graph_queue.get_parsed_data_Vue()
    return response

@pytest.fixture
def supply_dublicate_grpah_data_from_Vue():
    graph_queue = GraphQueue()
    data_Vue = ['testGraph1 user1', 'testGraph2 user1', 'testGraph3 user3']
    graph_queue.graph_queue_Vue = data_Vue
    graph_queue.parse_data_from_Vue()
    response = graph_queue.get_parsed_data_Vue()
    return response


@pytest.fixture
def supply_dublicate_data_from_Vue():
    graph_queue = GraphQueue()
    checking_list = [{'user1': ['testGraph1']}, {'user2': ['testGraph2']}]
    checking_name = 'user1'
    response = graph_queue.isDublicated(checking_name, checking_list)
    return response

    
@pytest.fixture
def supply_bad_dublicate_data_from_Vue():
    graph_queue = GraphQueue()
    checking_list = [{'user1': ['testGraph1']}, {'user2': ['testGraph2']}]
    checking_name = 'user4'
    response = graph_queue.isDublicated(checking_name, checking_list)
    return response

@pytest.fixture
def supply_common_graphs():
    graph_queue = GraphQueue()
    graph_queue.parsed_data_Vue = {'user1': ['TestGraph1','TestGraph2'], 'user3': ['TestGraph2']}
    graph_queue.graph_queue = {'user1': {'TestGraph1': ['nodes_data', 'links_data']},
                        'user3': {'TestGraph2': ['nodes_data2', 'links_data2'],
                        'TestGraph2': ['nodes_data2', 'links_data2']}}
    
    graph_queue.find_common_graphs()
    response = graph_queue.get_common_graphs()
    return response

@pytest.fixture
def supply_common_graphs_single_person():
    graph_queue = GraphQueue()
    graph_queue.parsed_data_Vue = {'user1': ['TestGraph1','TestGraph2']}
    graph_queue.graph_queue = {'user1': {'TestGraph1': ['nodes_data', 'links_data'], 
    'TestGraph2':['nodes_data', 'links_data']}}  
    graph_queue.find_common_graphs()
    response = graph_queue.get_common_graphs()
    return response

@pytest.fixture
def supply_union_graph():
    graph_queue = GraphQueue()
    graph_queue.common_graphs = [{'TestGraph1': [['nodes_data'], ['links_data']]}, 
    {'TestGraph2': [['nodes_data2'], ['links_data2']]}]
    graph_queue.union_graph()
    response = graph_queue.get_union_graph_data()
    return response

client = IGUser()
started_usernames = ['aikmartirosan']
client.set_usernames(started_usernames)
bot_name = 'zeleniychai123'
bot_password = 'zeleniychai1234'
client.initialize_bot(bot_name,bot_password)
client.create_session()


@pytest.fixture
def supply_get_user_info():
    response = client.get_user_info()

    return response

@pytest.fixture
def supply_get_post_likers():
    response = client.get_post_likers()

    return response

@pytest.fixture
def supply_get_reverse_activity():
    post_likers = client.get_post_likers()
    response = client.get_reverse_activity(post_likers)
    return response

@pytest.fixture
def supply_get_graph_likers_data():
    post_likers = client.get_post_likers()
    response = client.get_graph_likers_data(post_likers)
    return response

