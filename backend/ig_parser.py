#pylint: disable=R0201,W0613,C0103,C0301
"""Содержит методы для извлечения данных из Instagram"""
import logging
import json
import csv
import requests
import os.path

from pathlib import Path
from collections import Counter
from instagrapi import Client, exceptions
from progress.bar import IncrementalBar


log = logging.getLogger(__name__)


def write_file(data: str, filename: str):
    """Create credential file"""
    fin = open(filename, "w")
    try:
        fin.write(json.dumps(data))
    finally:
        fin.close()


def read_file(filename: str) -> json:
    """Read from credential file"""
    fin = open(filename, "r")
    return json.load(fin)


class IGUser:
    """Класс для работы с пользователями из Instagram с помощью Instagrpai"""

    def __init__(self):
        """Инициализация имени пользователя и прокси"""
        self.username = []
        # self.proxy_address = self.read_proxy_from_file()
        self.bot_username = ""
        self.bot_password = ""
        self.client = ""
        self.limits = {}

    def set_usernames(self, username):
        """Инициализация имени пользователей"""
        self.username = username

    def set_limits(self, limits):
        self.limits = limits
    
    def get_client(self):
        return self.client

    def initialize_bot(self, bot_username: str, bot_password: str):
        """Инициализация бота"""
        self.bot_username = bot_username
        self.bot_password = bot_password

    def read_proxy_from_file(self):
        """Читает из файла данные для прокси"""
        try:
            proxy_file_name = "proxy_file"
            proxy_file = open(proxy_file_name, "r")
        except Exception as ex:
            log.warning(ex)
        return proxy_file.read()

    def download_user_profile_photo(self, users_info: list):
        """Загружает фото профиля"""
        path = './frontend/src/assets/profile_photos'
        for info in users_info:
            if 'profile_pic_url' in info:
                self.client.photo_download_by_url(info['profile_pic_url'],info['username'], path)

    def create_session(self):
        """Создает файл сессии для дальнейшего подключения с помощью него"""
        try:
            self.client = Client()
            proxy = self.read_proxy_from_file()
            if len(proxy) != 0:
                self.client.set_proxy(proxy)
            if os.path.isfile(f'./{self.bot_username}'):
                self.client = Client(read_file(self.bot_username))
            else:
                self.client.login(self.bot_username, self.bot_password)
                write_file(self.client.get_settings(), self.bot_username)
            
        except Exception as err:
            self.client = {'error_message': 'Не удалось установить соединение с Instagram, \
            попробуйте обновить страницу, либо задайте новый акканут для подключения'}
            log.warning(err)     

    def get_user_info(self) -> list:
        """
        Получает базовые данные о пользователе
        На выход: user_info: list
        user_info = [{'pk': 1231, 'username': user1, ...},
                    {'pk': 32, 'username': user2, ...}, ...]
        """
        user_info = []           
        for name in self.username:
            try:
                info = self.client.user_info_by_username(name)
                user_info.append(info.dict())
            except Exception as err:
                user_info.append({'pk': 0, 'username': name, 'full_name': 'Не найден', 'is_private': '',
                'media_count': 0, 'follower_count': 0, 'following_count': 0})
                log.warning(err)

        return user_info

    def get_started_usernames_info(self, started_usernames: list):
        user_info = []
        if len(started_usernames) != 0:           
            for name in started_usernames:
                try:
                    info = self.client.user_info_by_username(name)
                    user_info.append(info.dict())
                except Exception as err:
                    user_info.append({'pk': 0, 'username': name, 'full_name': 'Не найден', 'is_private': '',
                    'media_count': 0, 'follower_count': 0, 'following_count': 0})
                    log.warning(err)

        return user_info

    def get_followings(self) -> list:
        """
        Создаются данные для таблицы подписчиков
        По этапам:
        1. Извлекается информация о пользователе, у которого извлекаются подписчики;
        2. Извлекается иноформация о подписчиках;
        3. Добавляются дополнительные поля в ифнормацию о подписчиках
        На выход: followings_info: list
        followings_info = [{'pk': 12, 'username': user1, 'full_name': fullname1, 'media_count': 4,
        'following_count': 6, 'followings_count': 7},..]
        """
        try:
            user_info = self.get_user_info()
            all_user_following = self.get_all_user_following(user_info)
            followings_info = self.fill_extra_users_info(all_user_following)
        except Exception as err:
            followings_info = {'error_message': 'Не удалось загрузить данные о пользователях Instagram, \
            попробуйте закрыть окно и снова начать поиск'}
            log.warning(err) 

        return followings_info

    def get_post_likers(self) -> list:
        """
        Получает всех пользователей, которые лайкали посты с количеством лайков.
        По этапам:
        1. Извлекается user_info;
        2. Извлекается user_id;
        3. Извлекается количество подписичков пользователя;
        4. Извлекаются все посты интересующего пользователя;
        5. Извлекаются все пользователи, которые лайкнули посты;
        6. Создается список словарей с id пользовтелей лайкнувших запись и их username;
        7. К списку из пункта 6, к каждому пользователю добавляется количество их лайков;
        8. Извлекается список всех подписчиков;
        9. Извелкаются только имена;
        10. Проверка на то, являются пользователи, которые лайкнули записи, подписчиками.
        На выход: post_likers: list
        post_likers = [{'id':1, 'username': user1, 'like_count': 4, 'is_following': True, 'is_private: True}, ...]
        """
        try:
            user_info = self.get_user_info()
            user_id = user_info[0]['pk']
            post_amount = user_info[0]['media_count']
            amount = self.get_correct_limit(post_amount, self.limits)
            user_media = self.client.user_medias(user_id, amount)
            all_user_likers = self.set_all_user_likers(user_media)
            user_and_id = self.create_username_with_id_list(all_user_likers)
            each_user_like = self.count_each_user_like(user_and_id)
            all_user_following = self.get_all_user_following(user_info)
            all_user_following_usernames = self.extract_username(all_user_following)
            post_likers = self.is_following(all_user_following_usernames, each_user_like)
        except Exception as err:
            post_likers = {'error_message': 'Не удалось загрузить данные о пользователях Instagram, \
            попробуйте закрыть окно и снова начать поиск'}
            log.warning(err) 


        return post_likers

    def get_reverse_activity(self, post_likers: list) -> list:
        """
        Формирует данные для таблицы обратной активности.
        По этапам:
        1. Проверка аккаунта пользователя на приватность;
        2.1. Извлекаются все посты пользователя;
        2.2 Проверка наличие инзачльно заданного пользователя в списке лайкающих.
        На вход: post_likers: list
        На выход: user_reverse_actitvity: list
        user_reverse_actitvity = [{'pk':11, 'username': user1, 'like_count': 1}, ...]
        """
        started_user = self.username
        user_reverse_activity = self.get_users_activity(post_likers, started_user)

        return user_reverse_activity

    def get_graph_data_common_followings(self) -> list:
        """
        Формирует данные для графа общих подписчиков пользоватлей.
        По этапам:
        1. Извлекаются только пользователи с открытым аккаунтом;
        2. Извлекаются подписчики у интересующих пользователей;
        3. Извлекаются только общие подписчики;
        4. Строятся узлы для графа;
        5. Строятся ребра для графа;
        6. Задаются цвета графу;
        На выход: graph_data_common_followings: list
        graph_data_common_followings = [nodes,links]
        """
        try:
            common_followings_code = 2
            user_infos = self.get_user_info()
            users_followings = self.get_all_user_following(user_infos)
            common_followings = self.get_common_followings(users_followings)
            nodes = self.get_nodes(user_infos, common_followings, common_followings_code)
            links = self.get_links(nodes, user_infos)
            graph_data_common_followings = [nodes, links]
        except Exception as err:
            graph_data_common_followings = {'error_message': 'Не удалось загрузить данные о пользователях Instagram, \
            попробуйте закрыть окно и снова начать поиск'}
            log.warning(err) 

        return graph_data_common_followings

    def get_graph_likers_data(self, post_likers: list) -> list:
        """
        Формирует данные для графа лайкнувших пользователей
        По этапам:
        1. Задается главный узел, от которого сторятся остальные ребра;
        2. Строятся узлы для графа;
        3. Строятся ребра для графа.
        4. Задаются цвета графу;
        На выход: graph_likers_data: list
        graph_likers_data = [nodes, links]
        """
        try:
            likers_code = 1
            main_node = self.get_user_info()
            nodes = self.get_nodes(main_node, post_likers, likers_code)
            links = self.get_links(nodes, main_node)
            # color = '#517d99'
            # painted_links = self.paint_links(links, color)
            graph_likers_data = [nodes, links]
        except Exception as err:
            graph_likers_data = {'error_message': 'Не удалось загрузить данные о пользователях Instagram, \
            попробуйте закрыть окно и снова начать поиск'}
            log.warning(err) 

        return graph_likers_data

    def get_common_followings(self, users_followings: list) -> list:
        """
        Формирует список общих подписчиков
        На вход: users_followings: dict
        На выход: common_followings: list
        common_followings = [{'id':1, 'name':'common_user1', ...}, ...]
        """
        common_followings_names = []
        common_followings = []
        for user in users_followings:
            common_followings_names.append(user['username'])

        common_followings_names = self.set_duplicated_elements(common_followings_names)
        for name in common_followings_names:
            common_followings.append((self.client.user_info_by_username(name)))
        common_followings = self.convert_from_UserShortType_to_dict(common_followings)

        return common_followings

    def set_duplicated_elements(self, data: list) -> list:
        """
        Извлекает только повторяющиеся элементы
        На вход: data: list ([1,1,3,3,4,4,5,6,7])
        На выход: duplicate: list
        duplicates = [1,3,4]
        """
        duplicates = []
        for elem in data:
            if data.count(elem) > 1 and elem not in duplicates:
                duplicates.append(elem)

        return duplicates

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

    def get_users_activity(self, users: list, started_user: list) -> list:
        """
        Формирует структуру того, сколько раз интересующий пользователь лайкнул записи.
        На вход: users: list, started_user: list
        На выход: user_reverse_actitvity: list
        user_reverse_actitvity = [{'pk':11, 'username': user1, 'like_count': 1}, ...]
        """
        try:
            user_reverse_activity = [] 
            # count = 1 # костыль, т.к очень много и долго считать
            for user in users:
                reverse_activity = {}
                user_id = user['pk']
                user_media = self.client.user_medias(user_id)
                if len(user_media) != 0:  # значит пользователь не приватный
                    all_media_likers = self.set_all_user_likers(user_media)
                    only_usernames = self.extract_username(all_media_likers)
                    like_count = only_usernames.count(started_user[0])
                    reverse_activity['pk'] = user_id
                    reverse_activity['username'] = user['username']
                    reverse_activity['like_count'] = like_count
                    user_reverse_activity.append(reverse_activity)
                    # count = count + 1
                    # if count == 5:
                    #     break
        except Exception as err:
            user_reverse_activity = {'error_message': 'Не удалось загрузить данные о пользователях Instagram, \
            попробуйте закрыть окно и снова начать поиск'}
            log.warning(err) 
        return user_reverse_activity

    def set_all_user_likers(self, user_media: list) -> list:
        """
        Формирует список всех пользователей лайкнувших записи
        На вход: user_media: list
        На выход: all_user_likers: list
        all_user_likers = [{'id': 123, 'username': user1, ...}, ...]
        """
        all_user_likers = []
        for media in user_media:
            post_likers = self.client.media_likers(media.dict()['id'])
            all_user_likers.extend(post_likers)
        all_user_likers = self.convert_from_UserShortType_to_dict(all_user_likers)
        return all_user_likers

    def convert_from_UserShortType_to_dict(self, users: list):
        """
        Библиотека Instagrapi использует свой тип данных UserShort
        И надо это преобразвать его в dict формат
        """
        normal_type = []
        for user in users:
            normal_type.append(user.dict())
        return normal_type

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
            user['is_private'] = True # костыль, т.к в предыдущей библиотеке это поле указывалось, а здесь нет
            # self.client.user_info_by_username_v1(user['username']).dict()['is_private']
            user['full_name'] = all_user_likers[index]['full_name']
            all_user_liker.append(user)
        return all_user_liker

    def count_each_user_like(self, user_and_id: list) -> list:
        """
        Считает количество лайков от каждого пользователя
        На вход: user_and_id: list
        На выход: user_like_list list
        user_like_list = [{'pk':1, 'username': user1, 'is_private': True, 'like_count': 2}, ...]
        """
        each_user_like = Counter((user_and_id_elem['pk'], user_and_id_elem['username'], 
        user_and_id_elem['is_private'], user_and_id_elem['full_name'])
                                 for user_and_id_elem in user_and_id)

        user_like_list = [{'pk': user[0], 'username': user[1], 
                            'is_private': user[2], 'full_name': user[3],
                           'like_count': each_user_like[user]} for user in each_user_like]  # user принимает tuple (id, username), each_user_like(user) возвращает количество повторений
        return user_like_list

    def get_all_user_following(self, user_info: list) -> list:
        """
        Формирует список всех подписчиков для пользователя
        На вход: user_id: str
        На выход: all_user_following: list
        all_user_following = [{'id':1, 'username': user1, ...}, ...]
        """
        all_user_following = []

        for info in user_info:
            if info['is_private'] == False:
                user_id = info['pk']
                followings = self.client.user_followers(user_id)
                followings = self.convert_from_UserShortType_to_dict(
                    followings.values())
                all_user_following.extend(followings)
        return all_user_following
    
    def fill_extra_users_info(self, user_info: list) -> list:
        """
        Функция добавляет дополнительные поля для пользователей
        На вход: user_info: list
        На выход: user_info: list
        user_info = [{'id': 123, 'media_count': 4, 'follower_count': 6, 'following_count': 5, 'is_private': True},]
        """
        for info in user_info:
            full_info = self.client.user_info_by_username(info['username']).dict()
            info['media_count'] = full_info['media_count']
            info['follower_count'] = full_info['follower_count']
            info['following_count'] = full_info['following_count']
            info['is_private'] = full_info['is_private']
        return user_info

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

    def get_post_location(self) -> list:
        """
        Извлекает координаты публикаций
        На вход: 
        На выход:  
        """
        try:
            user_info = self.get_user_info()
            user_id = user_info[0]['pk']
            post_amount = user_info[0]['media_count']
            medias = self.client.user_medias(user_id, post_amount)
            post_location = self.create_location_data(medias, user_info)
            print(post_location)
        except Exception as err:
            post_location = {'error_message': 'Не удалось загрузить данные местоположении публикаций пользователях Instagram, \
            попробуйте закрыть окно и снова начать поиск'}
            log.warning(err) 
        
        return post_location

    def create_location_data(self, medias: list, user_info: list) -> list:
        print('START////////////')
        post_location = []
        bar = IncrementalBar('Получение геопозиции публикаций', max = len(medias))
        folder = path = f"./frontend/src/assets/{user_info[0]['username']}"
        Path(folder).mkdir(parents=True, exist_ok=True)
        for ids, media in enumerate(medias):
            location = {}
            media_pk = media.dict()['pk']
            location['username'] = user_info[0]['username']
            
            media_info = self.client.media_info(media_pk).dict()
            location['taken_at'] = media_info['taken_at'].strftime("%d/%m/%Y, %H:%M:%S")
            location['caption_text'] = media_info['caption_text']
            if media_info.get('location') != None:
                if media_info.get('media_type') == 1: #photo type
                    location['media_pk'] = str(media_pk)
                    self.client.photo_download(media_pk, folder)
                location['position'] = {'lat': media_info['location']['lat'], 'lng': media_info['location']['lng']}
                location['name'] = media_info['location']['name']
                location['address'] = media_info['location']['address']
                
            post_location.append(location)
            bar.next()
        bar.finish()
        return post_location

    def get_correct_limit(self, post_amount: int, limit: dict) -> int:
        if len(limit) != 0:
            if post_amount >= limit['publicationLimit'] and limit['publicationLimit'] != 0:
                return limit
        return post_amount


    def get_nodes(self, username: list, nodes_users: list, group_code: int) -> list:
        """
        Формирует nodes
        На вход: username: list (нужен для формирования главных node, 
        от которых строится граф), nodes_users: list
        На выход: nodes: list
        nodes = [{'id':12312, 'name': user1, ...}, ...]
        """
        try:
            nodes = []
            group = username[0]['pk']
            for user in username:
                main_node = {'id': user['username'],
                            'group': group}
                nodes.append(main_node)

            for usual_node in nodes_users:  # формирует nodes специально для работы с графом
                node = {}
                node['id'] = f"{usual_node['username']}\n ({usual_node['full_name']})"  # не везде pk
                node['group'] = group
                # node['_color'] = _color
                if 'like_count' in usual_node:
                    node['like_count'] = usual_node['like_count']
                nodes.append(node)
        except Exception as err:
            print(nodes_users)

        return nodes

    def get_links(self, nodes: list, main_node: list) -> list:
        """
        Формирует links для отображения 
        На вход: nodes: list, main_node: links
        На выход: links: list
        links = [{'sid':12312, 'tid': 11, ...}, ...]
        """
        links = []
        main_node_username = self.extract_username(main_node)
        for node in main_node:
            for usual_node in nodes:
                if usual_node['id'] not in main_node_username:
                    link = {}
                    link['source'] = usual_node['id']
                    link['target'] = node['username']
                    if 'like_count' in usual_node:
                        link['like_count'] = usual_node['like_count']
                    links.append(link)

        return links
