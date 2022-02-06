# Foodgram
***Project address [3.142.83.202](http://3.142.83.202)***</br>

![Foodgram workflow](https://github.com/nick-rebrik/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

### Description
On this service, users can publish recipes, subscribe to other users' posts, add their favorite recipes to the "Favorites" list, and before going to the store download a summary list of products needed to prepare one or more selected dishes.


### Technologies

- Python 3.9
- Django 3.2
- Django REST Framework 3.12
- Djoser 2.1.0
- Docker

### Quick start

1. Go to the directory 'infra' and run in command line:</br>
```docker-compose up -d```
2. Run in command line:</br>
```docker-compose exec app python manage.py migrate```</br>
```docker-compose exec app python manage.py collectstatic```
3. To load data:</br>
```docker-compose exec app python manage.py loaddata data/data.json```

### Authors

- [Nick Rebrik](https://github.com/nick-rebrik) - Backend part
- [Yandex Praktikum](https://github.com/yandex-praktikum) - Frontend part</br>
