import csv

class UserData:
    """Класс для работы пользователя"""

    def __init__(self,usernames: list =[], bot_name: str = "",
    bot_password: str = "", started_usernames: str = []):
        """Инициализирует данные пользоваеля"""
        self.usernames = usernames
        self.bot_name = bot_name
        self.bot_password = bot_password
        self.started_usernames = started_usernames

    def get_bot_name(self):
        return self.bot_name
    
    def get_started_usernames(self):
        return self.started_usernames
        
    def get_bot_password(self):
        return self.bot_password

    def add_started_usernames(self, usernames: list):
        self.started_usernames.extend(usernames)
        self.started_usernames = list(set(self.started_usernames))

    def delete_started_usernames(self, usernames: str):
        self.started_usernames.remove(usernames)

    def create_csv(self, users_info: list):
        """Создает csv файл с лайкнувшими пользоваетлями"""
        csv_name = f"{self.usernames[0]}_likers_users.csv"
        dirname = f"./user_likers_csv/"
        with open(dirname + csv_name, mode="w") as csv_file:
            fieldnames = ['ID', 'Имя пользователя', 'Количество лайков', 'Подписчик']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for info in users_info:
                id = info['pk']
                username = info['username']
                like_count = info['like_count']
                is_following = info['is_following']
                writer.writerow({'ID': id, 
                'Имя пользователя': username, 'Количество лайков': like_count,
                'Подписчик': is_following})
