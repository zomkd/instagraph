# instagraph

Веб-приложение для агрегации данных о пользователе из Instagram. 

Написано на Django REST Framework + Vue.

### Возможности

- Построение таблицы с общей информацией об интересующих пользователях;

- Построение таблицы с информацией о пользователях, лайкнувших ваши записи;
- Построение таблицы с информацией о пользователях, которых вы лайкнули запись;
- Построение таблицы с информацией о подписчиках;
- Запись информации о пользователях лайкнувших запись в CSV;
- Построение графа пользователей лайкнувших ваши записи;
- Построение графа общих подписчиков;
- Построение объединенного графа.

### Как запустить

##### 	С использованием Docker

```
git clone https://github.com/zomkd/instagraph.git
cd instagraph
docker-compose up -d
```

##### 	Без использования Docker

###### 		Запуск Django	

```
cd instagraph
pip install -r requirements.txt
python manage.py runserver
```

###### 		Запуск Vue

```
cd instagraph/frontend
npm run serve
```

По умолчанию веб-приложение доступно по адресу: http://localhost:8080

Для использования прокси, нужно файл *proxy_file.txt* заполнить согласно следующей схеме: *“scheme://username:password@host:port”*

### Как запустить тесты

###### Запуск Python тестов

```
cd instagraph
pytest backend/tests
```

###### Запуск Vue тестов

```
cd instagraph/frontend
npm run unit
```

