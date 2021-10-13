import logging
import time
from collections import Counter
from instagram_private_api import Client
# from .graph_queue import GraphQueue


log = logging.getLogger(__name__)

class IGUser:
    """Класс для работы с пользователями из Instagram"""
    def __init__(self, username, proxy_address=""):
        """Инициализация имени пользователя и прокси"""
        self.username = username
        self.proxy_address = proxy_address

    def connection(self):
        """Создается соединение с Instagram
        На выход: client - объект пользователя
        """
        # user_name = 'cherniychai123'
        # password = 'cherniychai1234'
        user_name = 'zeleniychai123'
        password = 'zeleniychai1234'
        # user_name = 'lostignor'
        # password = 'lostignor123'
        try:
            if self.proxy_address != "":
                client = Client(user_name, password, proxy=self.proxy_address)
            else:
                client = Client(user_name, password)
        except Exception as err:
            log.warning(err)

        return client


    def get_user_info(self) -> list:
        """
        Получает базовые данные о пользователе
        На выход: user_info: list
        user_info = [{'pk': 1231, 'username': user1, ...},
                    {'pk': 32, 'username': user2, ...}, ...]
        """
        try:
            client = self.connection()
            time.sleep(5)
            user_info = self.get_info(client)
        except Exception as err:
            log.warning(err)

        return user_info

    def get_info(self, client:Client) -> list:
        """
        Получает базовые данные о пользователе
        На выход: client: client
        На выход: user_info: list
        user_info = [{'pk': 1231, 'username': user1, ...},
                    {'pk': 32, 'username': user2, ...}, ...]
        """
        user_info = []
        for name in self.username:
            info = client.username_info(name.strip())['user']
            user_info.append(info)

        return user_info

    def get_post_likers(self) -> list:
        """
        Получает всех пользователей, которые лайкали посты с количеством лайков.
        По этапам:
        1. Создаетеся соединение с Instagram;
        2. Извлекается user_info;
        3. Извлекается user_id;
        4. Извлекаются все посты интересующего пользователя;
        5. Извлекаются все пользователи, которые лайкнули посты;
        6. Создается список словарей с id пользовтелей лайкнувших запись и их username;
        7. К списку из пункта 5, к каждому пользователю добавляется количество их лайков;
        8. Извлекается список всех подписчиков;
        9. Извелкаются только имена;
        10. Проверка на то, являются пользователи, которые лайкнули записи, подписчиками.
        На выход: post_likers: list
        post_likers = [{'id':1, 'username': user1, 'like_count': 4, 'is_following': True, 'is_private: True}, ...]
        """
        client = self.connection()
        time.sleep(2)
        user_info = self.get_user_info()
        user_id = user_info[0]['pk']
        user_media = client.user_feed(user_id)['items']
        all_user_likers = self.set_all_user_likers(client, user_media)
        user_and_id = self.create_username_with_id_list(all_user_likers)
        each_user_like = self.count_each_user_like(user_and_id)
        all_user_following = self.get_all_user_following(client, user_info)
        all_user_following_usernames = self.extract_username(all_user_following)
        post_likers = self.is_following(all_user_following_usernames, each_user_like)

        return post_likers

    def get_graph_data_common_followings(self) -> list:
        """
        Формирует данные для графа общих подписчиков пользоватлей.
        По этапам:
        1. Создаетеся соединение с Instagram;
        2. Извлекаются только пользователи с открытым аккаунтом;
        3. Извлекаются подписчики у интересующих пользователей;
        4. Извлекаются только общие подписчики;
        5. Строятся узлы для графа;
        6. Строятся ребра для графа.
        На выход: graph_data_common_followings: list
        graph_data_common_followings = [nodes,links]
        """
        time.sleep(5)
        client = self.connection()
        time.sleep(5)
        user_info =  self.get_info(client)
        unprivate_users = self.check_is_private(user_info)
        users_followings = self.get_all_user_following(client, unprivate_users)
        common_followings = self.get_common_followings(client, users_followings)
        nodes = self.get_nodes(client, unprivate_users, common_followings)
        links = self.get_links(client, nodes, unprivate_users)
        graph_data_common_followings = [nodes, links]

        return graph_data_common_followings

    def get_reverse_activity(self, post_likers: list) -> list:
        """
        Формирует данные для таблицы обратной активности.
        По этапам:
        1. Создаетеся соединение с Instagram;
        2. Проверка аккаунта пользователя на приватность;
        3.1. Извлекаются все посты пользователя;
        3.2 Проверка наличие инзачльно заданного пользователя в списке лайкающих.
        На вход: post_likers: list
        На выход: user_reverse_actitvity: list
        user_reverse_actitvity = [{'pk':11, 'username': user1, 'like_count': 1}, ...]
        """
        client = self.connection()
        started_user = self.username
        unprivate_users = self.check_is_private(post_likers)
        user_reverse_activity = self.get_users_activity(client, unprivate_users, started_user)
        
        return user_reverse_activity

    def get_users_activity(self, client: Client, users: list, started_user: list) -> list:
        """
        Формирует структуру того, сколько раз интересующий пользователь лайкнул записи.
        На вход: client: client, started_user: list
        На выход: user_reverse_actitvity: list
        user_reverse_actitvity = [{'pk':11, 'username': user1, 'like_count': 1}, ...]
        """
        user_reverse_activity = []
        count = 1
        for user in users:
            reverse_activity = {}
            user_id = user['pk']
            user_media = client.user_feed(user_id)['items']
            all_media_likers = self.set_all_user_likers(client, user_media)
            only_usernames = self.extract_username(all_media_likers)
            like_count = only_usernames.count(started_user[0])
            reverse_activity['pk'] = user_id
            reverse_activity['username'] = user['username']
            reverse_activity['like_count'] = like_count
            user_reverse_activity.append(reverse_activity)
            count = count + 1
            if count == 10:
                break
        return user_reverse_activity

    def get_common_followings(self, client: Client, users_followings: list) -> list:
        """
        Формирует список общих подписчиков
        На вход: client: Client, users_followings: dict
        На выход: common_followings: list
        common_followings = [{'id':1, 'name':'common_user1', ...}, ...]
        """
        common_followings_names = []
        common_followings = []
        for user in users_followings:
            common_followings_names.append(user['username'])

        common_followings_names = self.set_duplicated_elements(common_followings_names)
        for followings in common_followings_names:
            common_followings.append((client.username_info(followings))['user'])

        return common_followings

    def check_is_private(self, users: list) -> list:
        """
        Фильтрует закрытые аккаунты и открытые, так как из закрытых нельзя извлечь список подписчиков
        На вход: users: list
        На выход: unprivate_users: list
        unprivate_users = [{'id':1, 'username':ivan, ...}, ...]"""
        unprivate_users = []
        for user in users:
            if user['is_private'] == False:
                unprivate_users.append(user)
        return unprivate_users


    def get_nodes(self, client: Client, username: list, nodes_users: list) -> list:
        """
        Формирует nodes
        На вход: client, username, nodes_users: list
        На выход: nodes: list
        nodes = [{'id':12312, 'name': user1, ...}, ...]
        """
        nodes = []
        for user in username:
            user_id = user['pk']
            main_node = {'id': user_id, 'name': user['username'], '_color': 'blue'}
            nodes.append(main_node)

        for usual_node in nodes_users: #формирует nodes специально для работы с графом
            node = {}
            node['id'] = int(usual_node['pk']) # не везде pk
            node['name'] = usual_node['username']
            # node['_color'] = _color
            if 'like_count' in usual_node:
                node['like_count'] = usual_node['like_count']
            nodes.append(node)
        return nodes

    def get_links(self, client: Client, nodes: list, main_node: list) -> list:
        """
        Формирует links
        На вход: client, username, nodes: list, main_node
        На выход: links: list
        links = [{'sid':12312, 'tid': 11, ...}, ...]
        """
        _svgAttrs = {'stroke-width':2, 'opacity':1} # задает парамерты для отображения самих ребер
        _color = 'red'
        links = []
        main_node_id = self.extract_user_id(main_node)
        for node in main_node:
            for usual_node in nodes:
                if usual_node['id'] not in main_node_id:
                    link = {}
                    link['sid'] = int(usual_node['id'])
                    link['tid'] = int(node['pk'])
                    link['_svgAttrs'] = _svgAttrs
                    if 'like_count' in usual_node:
                        link['like_count'] = usual_node['like_count']
                    links.append(link)
        return links

    def get_graph_likers_data(self) -> list:
        """
        Формирует данные для графа лайкнувших пользователей
        По этапам:
        1. Создаетеся соединение с Instagram;
        2. Извлекаются пользователи лайкнувшие посты;
        3. Задается главный узел, от которого сторятся отсальные ребра;
        4. Строятся узлы для графа;
        5. Строятся ребра для графа.
        На выход: graph_likers_data: list
        graph_likers_data = [nodes, links]
        """
        time.sleep(2)
        client = self.connection()
        post_likers = self.get_post_likers()
        main_node = self.get_info(client)
        nodes = self.get_nodes(client, main_node, post_likers)
        links = self.get_links(client, nodes, main_node)
        graph_likers_data = [nodes, links]
        return graph_likers_data

    def set_all_user_likers(self, client: Client, user_media: list) -> list:
        """
        Формирует список всех пользователей лайкнувших записи
        На вход: client: client, user_media: list
        На выход: all_user_likers: list
        all_user_likers = [{'id': 123, 'username': user1, ...}, ...]
        """
        all_user_likers = []
        for media in user_media:
            all_user_likers.extend(client.media_likers(media['id'])['users'])
        return all_user_likers

    def create_username_with_id_list(self, all_user_likers: list) -> list:
        """
        Формирует список из словарей с username, id
        На вход: all_user_likers: list
        На выход: all_user_liker: list
        all_user_liker = [{'pk':1, 'username': user1, 'is_private': True}, ...]
        """
        all_user_liker = []
        for index in range(len(all_user_likers)):
            user = {}
            user['pk'] = all_user_likers[index]['pk']
            user['username'] = all_user_likers[index]['username']
            user['is_private'] = all_user_likers[index]['is_private']
            all_user_liker.append(user)
        return all_user_liker

    def count_each_user_like(self, user_and_id: list) -> list:
        """
        Считает количество лайков от каждого пользователя
        На вход: user_and_id: list
        На выход: user_like_list list
        user_like_list = [{'pk':1, 'username': user1, 'is_private': True, 'like_count': 2}, ...]
        """
        each_user_like = Counter((user_and_id_elem['pk'], user_and_id_elem['username'], user_and_id_elem['is_private']) 
                                for user_and_id_elem in user_and_id)

        user_like_list = [{'pk': user[0], 'username': user[1], 'is_private': user[2], 
                            'like_count': each_user_like[user]} for user in each_user_like] #user принимает tuple (id, username), each_user_like(user) возвращает количество повторений
        return user_like_list

    def get_all_user_following(self, client: Client, user_info: list) -> list:
        """
        Формирует список всех подписчиков для одного пользователя
        На вход: user_id: str, client: client
        На выход: all_user_following: list
        all_user_following = [{'id':1, 'username': user1, ...}, ...]
        """
        all_user_following = []
        sum_followings = 0
        for info in user_info:
            num_of_user_folloiwing = info['following_count']
            sum_followings = int(num_of_user_folloiwing) + sum_followings
            uuid = client.generate_uuid()
            user_following = client.user_following(info['pk'], uuid)
            all_user_following.extend(user_following['users'])
            all_find = True
            while all_find: #за раз можно получить только 100 подписчиков, поэтому поставлен флаг, который True до того пока не извлекутся все подписички
                if len(all_user_following) < sum_followings:
                    max_id = user_following['next_max_id'] #получает оставшиеся число подписичков
                    user_following = client.user_following(info['pk'], uuid, max_id = max_id)
                    all_user_following.extend(user_following['users'])
                else:
                    all_find = False
        return all_user_following


    def extract_username(self, users: list) -> list:
        """
        Из всей информации о подисчиках извлекаются только их имена
        На вход: users: list
        На выход: usernames: list
        usernames = ['user1','user2', ...]
        """
        usernames = []
        for user in users:
            usernames.append(user['username'])
        return usernames

    def extract_user_id(self, users: list) -> list:
        """
        Из всей информации о подисчиках извлекаются только их id
        На вход: users: list
        На выход: user_id: list
        usernames = ['123','22', ...]
        """
        user_id = []
        for user in users:
            user_id.append(user['pk'])
        return user_id

    def is_following(self, each_user_like: list, user_followings: list) -> list:
        """
        Проверка на то, является ли пользователь подписчиком
        На вход: each_user_like: list, user_followings: list
        На выход: user_followings: list
        user_followings = [{'id': 123, 'username': user1, 'is_following': True}, ...]
        """
        for user in user_followings:
            if user['username'] in each_user_like:
                user['is_following'] = True
            else:
                user['is_following'] = False
        return user_followings

    def set_duplicated_elements(self, data: list) -> list:
        """
        Извлекает только повторяющиеся элементы
        На вход: data: list ([1,1,3,3,4,4,5,6,7])
        На выход: duplicate: list
        duplicates = [1,3,4]"""
        duplicates = []
        for elem in data:
            if data.count(elem) > 1 and elem not in duplicates:
                duplicates.append(elem)
        return duplicates