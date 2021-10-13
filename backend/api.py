# pylint: disable=E0402,W0613
"""API реализация"""
import logging
import requests
import time

from rest_framework.views import APIView
from rest_framework.response import Response

from .ig_parser import IGUser
from .graph_queue import GraphQueue
from .insta_user import UserData


log = logging.getLogger(__name__)
user_data = UserData()
graph_queue = GraphQueue()
client = IGUser()

graph_likers_name = 'UserGraph' # имя для графа лайкнувших пользователей, как во Vue
grpah_common_followings_name = 'UserCommonFollowingsGraph'


#Если запрос на поиск инфы о пользователях пришел со стартовой страницы, то вызывается метод get_user_info(),
#Если нет, то проверяется переменная starterd_users, если в ней есть новый пользователь, то для отображения
#информации применяется метод get_started_user_info()
class InstUser(APIView):
    """
    API класс, в котором реализованы POST, GET методы для endpoint username/
    """
    @classmethod
    def post(cls, request) -> Response:
        """
        Принимает POST запрос от Vue
        На вход: request (username: list, proxy: str)
        На выход: Response
        """
        user_data.usernames = ""
        user_data.bot_name = ""
        user_data.bot_password = ""
        user_data.started_usernames = []
        try:
            user_data.usernames = request.data['username']
            user_data.bot_name = request.data['botUsername']
            user_data.bot_password = request.data['botPassword']
        except requests.exceptions.RequestException as err:
            log.warning(err)

        return Response(data="Succsess POST from Vue", status=200)

    @classmethod
    def get(cls, request) -> Response:
        """
        Отправляет GET запрос к Vue, данные для таблицы информации о пользователях
        На вход: request
        На выход: Response(user_info: dict)
        """
        try:
            client.set_usernames(user_data.usernames)
            client.initialize_bot(user_data.get_bot_name(),
                                  user_data.get_bot_password())
            client.create_session()
            if isinstance(client.get_client(), dict): #  если словарь - значит ошибка, если не словарь - данные получены успешно
                users_info = client.get_client()
            else:
                if len(user_data.started_usernames) == 0:
                    users_info = client.get_user_info()
                    user_data.add_started_usernames(user_data.usernames)
                    client.download_user_profile_photo(users_info)
                else:
                    users_info = client.get_started_usernames_info(user_data.started_usernames)
        except requests.exceptions.RequestException as err:
            log.warning(err)
        # print(users_info)
        return Response(users_info)


class UserInfo(APIView):
    """
    API класс, в котором реализованы POST, GET методы для endpoint username/
    """
    @classmethod
    def post(cls, request) -> Response:
        """
        Принимает POST запрос от Vue
        На вход: request (username: list, proxy: str)
        На выход: Response
        """
        user_data.usernames = ""
        try:
            user_data.usernames = request.data['username']
            print(user_data.usernames)
            user_data.add_started_usernames(user_data.usernames)
        except requests.exceptions.RequestException as err:
            log.warning(err)

        return Response(data="Succsess POST from Vue", status=200)

    @classmethod
    def get(cls, request) -> Response:
        """
        Отправляет GET запрос к Vue, данные для таблицы информации о пользователях
        На вход: request
        На выход: Response(user_info: dict)
        """
        try:
            client.set_usernames(user_data.usernames)
            users_info = client.get_user_info()
            client.download_user_profile_photo(users_info)
        except requests.exceptions.RequestException as err:
            log.warning(err)
        print(users_info)
        return Response(users_info)

class UserDelete(APIView):
    """
    API класс, в котором реализованы POST, GET методы для endpoint username/
    """
    @classmethod
    def post(cls, request) -> Response:
        """
        Принимает POST запрос от Vue
        На вход: request (username: list, proxy: str)
        На выход: Response
        """
        user_data.usernames = ""
        try:
            user_data.usernames = request.data['username']
            print(user_data.usernames)
            user_data.delete_started_usernames(user_data.usernames)
        except requests.exceptions.RequestException as err:
            log.warning(err)

        return Response(data="Succsess POST from Vue", status=200)

    @classmethod
    def get(cls, request) -> Response:
        """
        Отправляет GET запрос к Vue, данные для таблицы информации о пользователях
        На вход: request
        На выход: Response(user_info: dict)
        """
        try:
            users_info = client.get_started_usernames_info(user_data.started_usernames)
        except requests.exceptions.RequestException as err:
            log.warning(err)
        print(users_info)
        return Response(users_info)

class UserLikers(APIView):
    """
    API класс, в котором реализованы POST, GET методы для endpoint user_likers/
    """
    @classmethod
    def post(cls, request) -> Response:
        """
        Принимает POST запрос от Vue
        На вход: request (username: str)
        На выход: Response
        """
        try:
            user_data.usernames = ""
            user_data.usernames = request.data['username']
            client.set_usernames(user_data.usernames)
            client.set_limits(request.data['limits'])
        except requests.exceptions.RequestException as err:
            log.warning(err)
        return Response(data="Succsess POST from Vue", status=200)

    @classmethod
    def get(cls, request) -> Response:
        """
        Отправляет GET запрос к Vue, данные для таблицы о лайкнувших запись пользователях
        На вход: request
        На выход: Response(user_likers: dict)
        user_likers = {'id','username','like_count','is_following'}
        """
        try:
            user_likers = client.get_post_likers()
            graph_queue.set_post_likers(user_data.usernames, user_likers)
        except requests.exceptions.RequestException as err:
            log.warning(err)
        return Response(user_likers)


class UserLikersGraph(APIView):
    """
    API класс, в котором реализованы POST, GET методы для endpoint user_likers_graph/
    """
    @classmethod
    def post(cls, request) -> Response:
        """
        Принимает POST запрос от Vue
        На вход: request (username: str)
        На выход: Response
        """
        try:
            user_data.usernames = ""
            user_data.usernames = request.data['username']
            client.set_usernames(user_data.usernames)
        except requests.exceptions.RequestException as err:
            log.warning(err)
        return Response(data="Succsess POST from Vue", status=200)

    @classmethod
    def get(cls, request) -> Response:
        """
        Отправляет GET запрос к Vue, данные для графа лайкнувших запись
        На вход: request
        На выход: Response(graph_likers: list)
        graph_likers = [nodes: list, links:list ]
        """
        try:
            user_likers = client.get_post_likers()
            graph_likers = client.get_graph_likers_data(user_likers)
            graph_queue.set_graph_queue(graph_likers, user_data.usernames, 
            graph_likers_name)
        except requests.exceptions.RequestException as err:
            log.warning(err)
        return Response(graph_likers)


class UserCommonFollowingsGraph(APIView):
    """
    API класс, в котором реализованы GET методы для endpoint user_common_followings_graph/
    """

    def post(self, request) -> Response:
        """
        Post request from Vue (username, proxy)
        """
        try:
            user_data.usernames = ""
            user_data.usernames = request.data['username']
            client.set_usernames(user_data.started_usernames)
        except requests.exceptions.RequestException as err:
            log.warning(err)
        return Response(data="Succsess POST from Vue", status=200)

    @classmethod
    def get(cls, request) -> Response:
        """
        Отправляет GET запрос к Vue, данные для графа общих подписичков
        На вход: request
        На выход: Response(user_common_followers: list)

        user_common_followers = [nodes: list, links:list ]
        """
        try:
            user_common_followers = client.get_graph_data_common_followings()
            graph_queue.set_graph_queue(user_common_followers, user_data.usernames, grpah_common_followings_name)
        except requests.exceptions.RequestException as err:
            log.warning(err)
        return Response(user_common_followers)


class UserUnionGraph(APIView):
    """
    API класс, в котором реализован GET методы для endpoint user_union_graph/
    """
    @classmethod
    def post(cls, request) -> Response:
        try:
            graph_queue.graph_queue_Vue = request.data['graphsQueue']
        except requests.exceptions.RequestException as err:
            log.warning(err)
        return Response(data="Succsess POST from Vue", status = 200)
        

    @classmethod
    def get(cls, request) -> Response:
        """
        Отправляет GET запрос к Vue, данные для общего графа
        На вход: request
        На выход: Response(user_union_grpah: list)

        user_common_followers = [nodes: list, links:list ]
        """
        try:
            graph_queue.union_graph()
            data = graph_queue.get_union_graph_data()
        except requests.exceptions.RequestException as err:
            log.warning(err)
        return Response(data) 
 
class UserReverseActivity(APIView): # не рекомендуется к использованию, пока считает, можно покушать и поспать
    """
    API класс, в котором реализован GET методы для endpoint user_reverse_activity/
    """
    @classmethod
    def post(cls, request) -> Response:
        """
        Принимает POST запрос от Vue
        На вход: request (username: str)
        На выход: Response
        """
        try:
            user_data.usernames = ""
            user_data.usernames = request.data['username']
            client.set_usernames(user_data.usernames)
        except requests.exceptions.RequestException as err:
            log.warning(err)
        return Response(data="Succsess POST from Vue", status = 200)

    @classmethod
    def get(cls, request) -> Response:
        try:
            if len(graph_queue.get_post_likers()) == 0: # поменять извлечение из очереди
                user_likers = client.get_post_likers()
                graph_queue.post_likers = user_likers
            user_post_likers = graph_queue.get_post_likers()                    
            user_reverse_activity = client.get_reverse_activity(user_post_likers)
        except requests.exceptions.RequestException as err:
            log.warning(err)
        return Response(user_reverse_activity)

class UserFollowings(APIView):
    """
    API класс, в котором реализованы POST, GET методы для endpoint user_likers/
    """
    @classmethod
    def post(cls, request) -> Response:
        """
        Принимает POST запрос от Vue
        На вход: request (username: str)
        На выход: Response
        """
        try:
            user_data.usernames = ""
            user_data.usernames = request.data['username']
            client.set_usernames(user_data.usernames)
        except requests.exceptions.RequestException as err:
            log.warning(err)
        return Response(data="Succsess POST from Vue", status=200)

    @classmethod
    def get(cls, request) -> Response:
        """
        Отправляет GET запрос к Vue, данные для таблицы о лайкнувших запись пользователях
        На вход: request
        На выход: Response(user_likers: dict)
        user_likers = {'id','username','like_count','is_following'}
        """
        try:
            user_followers = client.get_followings()
        except requests.exceptions.RequestException as err:
            log.warning(err)
        return Response(user_followers)

class UserCSVWriter(APIView):
    @classmethod
    def post(cls, request) -> Response:
        """
        Принимает POST запрос от Vue
        На вход: request (username: str)
        На выход: Response
        """
        try:
            user_data.usernames = ""
            user_data.usernames = request.data['username']
            client.set_usernames(user_data.usernames)
        except requests.exceptions.RequestException as err:
            log.warning(err)
        return Response(data="Succsess POST from Vue", status=200)

    @classmethod
    def get(cls, request) -> Response:
        """
        Отправляет GET запрос к Vue, данные для таблицы о лайкнувших запись пользователях
        На вход: request
        На выход: Response(user_likers: dict)
        user_likers = {'id','username','like_count','is_following'}
        """
        try:
            if user_data.usernames[0] in graph_queue.get_post_likers():
                user_data.create_csv(graph_queue.get_post_likers()[user_data.usernames[0]])
            else:
                user_likers = client.get_post_likers()
                graph_queue.set_post_likers(user_data.usernames, user_likers)
                user_data.create_csv(user_likers)
            status="Запись прошла успешно!"
        except requests.exceptions.RequestException as err:
            status="Запись не прошла!"
            log.warning(err)
        return Response(status)

class PostLocation(APIView):
    """
    API класс, в котором реализованы POST, GET методы для endpoint post_location/
    """
    @classmethod
    def post(cls, request) -> Response:
        """
        Принимает POST запрос от Vue
        На вход: request (username: str)
        На выход: Response
        """
        try:
            user_data.usernames = ""
            user_data.usernames = request.data['username']
            client.set_usernames(user_data.usernames)
        except requests.exceptions.RequestException as err:
            log.warning(err)
        return Response(data="Succsess POST from Vue", status=200)

    @classmethod
    def get(cls, request) -> Response:
        """
        Отправляет GET запрос к Vue, данные для отображение 
        коордиант публикаций пользователя
        На вход: request
        На выход: Response(post_location: list[dict])
        post_location = [{position: {lat: 24, lng: 12}, address: "test", name: "Moscow"},....]
        """
        try:
            post_location = client.get_post_location()
        except requests.exceptions.RequestException as err:
            log.warning(err)
        return Response(post_location)
