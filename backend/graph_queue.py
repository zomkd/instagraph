"""Очередь для графов"""


class GraphQueue:
    """
    Класс для заполнения очереди, состоящая из данных о построенных графах
    """

    def __init__(self):
        """Инициализация пустой очереди"""
        self.graph_queue = {}
        self.post_likers = []
        self.graph_queue_Vue = []
        self.parsed_data_Vue = {}
        self.common_graphs = []
        self.union_graph_data = []

    def get_grpah_queue(self) -> dict:
        return self.graph_queue

    def get_post_likers(self) -> list:
        return self.post_likers

    def set_post_likers(self, username: list, likers_info: list):
        likers_data = {username[0]: likers_info}
        self.post_likers.append(likers_data)

    def get_parsed_data_Vue(self) -> list:
        return self.parsed_data_Vue
    
    def get_common_graphs(self) -> list:
        return self.common_graphs
    
    def get_union_graph_data(self) -> list:
        return self.union_graph_data

    def set_graph_queue(self, graph_data: list, username: list, graph_name: str) -> list:
        """
        Заполняет очередь данными из графа
        На вход: graph_data: list
        На выход: graph_queue: list
        graph_queue = {'username': {
            'graph1': grpah1_data: list,
            'graph2': grpah2_data: list,
            ...
        },
        'username2': {...},
        }
        """
        username = username[0]
        if username in self.graph_queue:
            self.graph_queue[username].update({graph_name: graph_data})
        else:
            self.graph_queue[username] = {graph_name: graph_data}

    def union_graph(self) -> list:
        """
        Объединяет даннные нескольких графов в один
        На вход: graph_data: list
        На выход: graph_queue: list
        graph_queue = [nodes,links]
        """
        self.union_graph_data = []
        self.parse_data_from_Vue()
        self.find_common_graphs()
        for graph_data in self.common_graphs:
            for data in graph_data:
                nodes = graph_data[data][0]
                links = graph_data[data][1]
                if len(self.union_graph_data) != 0:
                    queue_nodes = self.union_graph_data[0]
                    queue_links = self.union_graph_data[1]
                    queue_nodes.extend(nodes)
                    queue_links.extend(links)
                    queue_nodes = self.remove_dublicates(queue_nodes)
                    queue_links = self.remove_dublicates(queue_links)
                    self.union_graph_data[0] = queue_nodes
                    self.union_graph_data[1] = queue_links
                else:
                    self.union_graph_data.append(nodes)
                    self.union_graph_data.append(links)
        self.common_graphs = []
        self.parsed_data_Vue = {}

    def remove_dublicates(self, data: list) -> list:
        without_dublicates = [i for n, i in enumerate(data) if i not in data[n + 1:]]
        return without_dublicates

    def parse_data_from_Vue(self):
        """{'user1': ['testGraph1','testGraph2'], 'user3': ['testGraph3']}"""
        for user_graphs in self.graph_queue_Vue:
            graph_names = []
            splitted_grpah_and_username = user_graphs.split()
            graph_names.append(splitted_grpah_and_username[0])
            isDublicate = self.isDublicated(splitted_grpah_and_username[1],self.parsed_data_Vue)
            if len(self.parsed_data_Vue) != 0 and isDublicate['isDublicated'] == True:
                self.parsed_data_Vue[splitted_grpah_and_username[1]].append(splitted_grpah_and_username[0])
            else:      
                self.parsed_data_Vue[splitted_grpah_and_username[1]] = graph_names

    def isDublicated(self, checking_name: str, checking_list: list):
        dublicated_info = {'isDublicated': False, 'index': ''}
        index = 0
        if len(checking_list) != 0:
            for name in checking_list:
                if checking_name in name:
                    dublicated_info = {'isDublicated': True, 'index': index}
                index +=1
        return dublicated_info
    
    def find_common_graphs(self):
        """Ищет в очереди те графы, которые запросил пользователь из Vue"""
        for vue_graph in self.parsed_data_Vue:
            for graph in self.graph_queue:
                if vue_graph == graph:
                    for selected_graph in self.parsed_data_Vue[vue_graph]:
                        if selected_graph in self.graph_queue[graph]:
                            common = {}
                            common = {selected_graph: self.graph_queue[graph][selected_graph]}
                            self.common_graphs.append(common)
