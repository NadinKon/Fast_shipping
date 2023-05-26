## Fast Shipping - (Django REST framework)
### API: Сервис поиска ближайших машин для перевозки грузов.

### Установка:

Клонируйте репозиторий:
git clone https://github.com/NadinKon/Fast_shipping

Перейдите в директорию проекта:
cd fast_shipping

Скачайте образы и запустите контейнеры:
docker-compose up -d --build

Выполните миграции БД в контейнере Docker:

Определите имя или ID контейнера Django с помощью команды docker ps. Это покажет вам список всех запущенных контейнеров. <br>
Используйте docker exec -it <container_name_or_id> python manage.py makemigrations для создания миграций. <br>
Затем используйте docker exec -it <container_name_or_id> python manage.py migrate для применения миграций к базе данных. <br>

### Использование:

Приложение доступно на http://localhost:8000/delivery_app/ 

### Примеры использовани через интерфейс Django Rest Framework:

Для создания нового груза нужно перейти на http://localhost:8000/delivery_app/cargos/ <br>

* Добавляем новый груз командой PUT:
{
    "pick_up_zip": "00653", 
    "delivery_zip": "00683", 
    "weight": 568,
    "description": "новый груз"
}

* Редактирование машины (изменение локации)
Перейдите на страницу конкретного объекта Truck, который вы хотите обновить. Это обычно делается добавлением id объекта в конец URL. Например, если вы хотите обновить Truck с id=1, URL будет выглядеть так: http://localhost:8000/trucks/1/. <br>
Переключите интерфейс Django Rest Framework в режим PUT (или PATCH, если вы хотите выполнить частичное обновление). Обычно для этого достаточно выбрать соответствующий пункт из выпадающего списка вверху страницы. <br>
Введите новый zip-код в соответствующее поле формы. Помните, что в вашей базе данных должна быть локация с этим zip-кодом. <br>
Нажмите кнопку PUT (или PATCH), чтобы отправить форму и выполнить обновление. <br>
Добавляем новую локацию машине:

{
    "zip": "00601"
}

* Получение списка грузов <br>
Выполнив GET запрос на http://localhost:8000/delivery_app/cargos/ можно просмотреть все грузы

* Получение информации о конкретном грузе по ID <br>
Выполнив GET запрос к URL вида http://localhost:8000/delivery_app/cargos/{id}/, где {id} - это идентификатор груза. 

* Редактирование груза: <br>
Чтобы проверить этот код через интерфейс Django Rest Framework, вы должны отправить запрос PUT на /delivery_app/cargos/<id>, где <id> - это ID груза, который вы хотите обновить. 

{
    "weight": 10,
    "description": "Новое описание"
}

* Удаление груза по ID <br>
Вы сможете отправить DELETE запрос на URL вида /delivery_app/cargos/<id>/, где <id> - это ID груза, который вы хотите удалить.