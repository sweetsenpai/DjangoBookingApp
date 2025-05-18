[![Coverage Status](https://coveralls.io/repos/github/sweetsenpai/DjangoBookingApp/badge.svg?t=12345)](https://coveralls.io/github/sweetsenpai/DjangoBookingApp)
[![Run Pytest with Docker](https://github.com/sweetsenpai/DjangoBookingApp/actions/workflows/tests.yml/badge.svg)](https://github.com/sweetsenpai/DjangoBookingApp/actions/workflows/tests.yml)
[![Django](https://img.shields.io/badge/Django-5.2-green?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16-blue?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![Python 3.10](https://img.shields.io/badge/python-3.10%2B-orange?logo=python)](https://www.python.org/downloads/release/python-3100/)

# DjangoBookingApp
## 📝Краткая информация
RestAPI приложение реализующее функционал:
* **Регистрации новых пользователей**
* **Поиска и сортировки комнат**
* **Работы с бронями**

---
### ⚙️Стэк
- Django
- DRF
- PostgreSQL
- docker-compose
- django-pytest
---
### 🔌Запуск приложения
Для запуска достаточно скачать репозиторий любым удобным способом, после чего выполнить следующие действия:
1. Перейти в директорию приложения
   ```commandline
   cd booking_app
   ```
2. Запустить приложение с помощью `docker-compose`
    ```commandline
   docker-compose -f docker-compose.prod.yml up --build
   ```
3. Для полноценной работы с приложением потребуется создать суперпользователся.
   Сделать это можно следующим образом:
   1. Необходимо перейти в контейнер django:
      ```commandline
      docker exec -it django bash
      ```
   2. Далее необходимо ввести команду ниже в консоль и следовать указаниям Django:
      ```commandline
         python manage.py createsuperuser
      ```
---
### 📕Документация
Все доступные API методы и их работа должны быть доступны тут -> [`документация`](http://127.0.0.1:8000/api/docs/), после старта приложения.
![API документация](images/api_docs.png)
---

### 🌳Структура проекта
- **[`🗂booking_app/`](booking_app/booking_app)** — Модуль с настройками:
    - ⚙️ [`settings_prod`](booking_app/booking_app/settings_prod.py) — Оснавные настройки Django.
    - ⚙️ [`settings_dev`](booking_app/booking_app/settings_dev.py) — Настройки Django для разработки.
    - ⚙️ [`settings_dev`](booking_app/booking_app/settings_test.py) — Настройки Django для тестирования.
- **[`🗂core/`](booking_app/booking_app_admin)** — Основное приложение:
- - **[`🗂booking_api/`](booking_app/core/booking_api)** — Модуль с api:
- - - 🔪 [`serializers`](booking_app/core/booking_api/serializers) — Сериализаторы.
- - - 💻[`views`](booking_app/core/booking_api/views) — Views API.
  - 💃🏻 [`models`](booking_app/core/models.py) — Модели.
  - 🧙‍♂️ [`admin`](booking_app/core/admin.py) — Настройки панели администратора.
  - 🤖 [`tests`](booking_app/core/tests) — Тесты.
  - ⚒️ [`utils`](booking_app/core/utils) — Вспомогательные утилиты для работы API.
  - 🧼 [`filters`](booking_app/core/filters) - Фильтры.
  - 📚 [`urls`](booking_app/core/urls.py) - urls
- **[`⚓️docker-compose.prod.yml`](booking_app/docker-compose.prod.yml)** — `docker-compose` для продакшн среды.
- **[`⚓️docker-compose.dev.yml`](booking_app/docker-compose.dev.yml)** — `docker-compose` для разработки.
- **[`⚓️docker-compose.test.yml`](booking_app/docker-compose.test.yml)** — `docker-compose` для тестирования.
- **[`🐳Docker.prod`](booking_app/Dockerfile.prod)** — `Dockerfile` для продакшн среды.
- **[`🐳Docker.dev`](booking_app/Dockerfile.dev)** — `Dockerfile` для разработки и тестов.
- **[`📀init.sql`](booking_app/init.sql)** — init-файл для postresql, для загруски необходимых для работы расширений.
- **[`📚logs/`](booking_app/logs)** — Папка для хранения логов, реализована ротация файлов логирования.
- - **[`🟥critical.log`]** — логирование критических ошибок.
- - **[`🟨error.log`]** — логирование ошибок.
- - **[`🟩info.log`]** — логирование.



---
## 📚Не краткая информация
Далее пройдусь по всем пунктам задания и опишу их реализацию

### 💃🏻Модели
Для реализации функционала необходимо три модели.
1. Пользователи - в ТЗ не было каких-то особых требований к этой модели, поэтому использовалась стандартная модель `User`

2. Комнаты - описана модель достаточная для работы приложения. Содержит поля:
   * name - номер/название комнаты
   * price_per_day - стоимость комнаты в сутки. Для этого поля был выбран формат данных Decimal так как он считается наиболее безопасным и рекомендуемым для работы с деньгами.
   * capacity - максимальное количество проживающих в комнате
   ```python
   class Room(models.Model):
    name = models.CharField(
        max_length=100, help_text="Название/номер комнаты", unique=True, blank=False
    )
    price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text="Стоимость комнаты за сутки",
    )
    capacity = models.IntegerField(
        help_text="Количество человек на которое рассчитана комната",
        blank=False,
        null=False,
        validators=[MinValueValidator(1)],
    )
   ```
3. Брони - описана модель достаточная для работы приложение, тут есть интересный момент связанный с пересечениями дат, но его опишу в работе эндпоинта бронирования. 
Содержит поля:
      * date_start - дата и время заезда
      * date_end - дата и время выезда
      * room - связанное поле модели `Room`
      * user - связанное поле модели `User`
      * обе связи many-to-one

   ```python
   class Booking(models.Model):
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            ExclusionConstraint(
                name="exclude_overlapping_booking",
                expressions=[
                    (
                        TsTzRange("date_start", "date_end", RangeBoundary()),
                        RangeOperators.OVERLAPS,
                    ),
                    ("room", RangeOperators.EQUAL),
                ],
            )
        ]

    def __str__(self):
        return f"{self.user.username} – {self.room.name} – {self.date_start:%Y-%m-%d}"
   ```
---
## 🏠Комнаты
**Задача**
```
* Пользователи должны уметь фильтровать и сортировать комнаты по цене, по количеству мест.
* Пользователи должны уметь искать свободные комнаты в заданном временном интервале.
Просматривать комнаты можно без логина.
```
**Реализация**
```python
class RoomsApi(ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RoomFilter
    ordering_fields = ["price_per_day", "capacity"]
    ordering = ["price_per_day"]

    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        return Response(
            {"detail": "Method 'retrieve' not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
```
Эндпоинт реализованный с помощью `ReadOnlyModelViewSet`, так как нам требуются данные только на чтение. 
Фильтрация реализованна с помощью `django-filters`.
```python
class RoomFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price_per_day", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price_per_day", lookup_expr="lte")
    capacity = filters.NumberFilter(field_name="capacity", lookup_expr="gte")

    date_start = filters.DateFilter(method="filter_by_availability")
    date_end = filters.DateFilter(method="filter_by_availability")

    class Meta:
        model = Room
        fields = ["min_price", "max_price", "capacity", "date_start", "date_end"]

    def get_free_rooms(self, date_start: datetime, date_end: datetime) -> QuerySet:
        """
        Поиск свободных комнат в заданный временной промежуток.

        :param date_start: дата заезда
        :param date_end: дата выезда
        :return: возвращает QuerySet с доступными комнатами по заданым параметрам
        """

        busy_rooms = Booking.objects.filter(
            Q(date_start__lt=date_end) & Q(date_end__gt=date_start)
        ).values_list("room_id", flat=True)
        free_rooms = Room.objects.exclude(id__in=busy_rooms)
        return free_rooms

    def filter_by_availability(self, queryset, name, value):
        date_start = self.form.cleaned_data.get("date_start")
        date_end = self.form.cleaned_data.get("date_end")

        if not date_start or not date_end:
            return queryset

        date_start_dt = timezone.make_aware(datetime.combine(date_start, time.min))
        date_end_dt = timezone.make_aware(datetime.combine(date_end, time.min))

        validate_dates(date_start_dt, date_end_dt)

        free_rooms = self.get_free_rooms(date_start_dt, date_end_dt)
        return queryset.filter(id__in=free_rooms.values_list("id", flat=True))
```



---
## 🔒Бронирование комнат
**Задача**
```
* Пользователи должны уметь забронировать свободную комнату.
* Брони могут быть отменены как самим юзером, так и суперюзером.
* Чтобы забронировать комнату пользователи должны быть авторизованными.
* Авторизованные пользователи должны видеть свои брони.
```
**Решение**
```python
class BookingAPI(ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsOwnerOrSuperUser, IsAuthenticated]
    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).prefetch_related("room")

    def get_serializer_class(self):
        if self.action == "create":
            return BookingCreateSerializer
        return BookingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {
                    "detail": "Комната уже забронирована. Попробуйте изменить даты бронирования или выберите другую комнату."
                },
                status=status.HTTP_409_CONFLICT,
            )

```

---


---
## 🧙‍♂️Суперпользователь
**Задача**
```
Суперюзер должен уметь добавлять/удалять/редактировать комнаты и редактировать записи о бронях через админ панель Django.
```
**Решение**
Просто импортируем модель в администраторскую панель Django, весь функционал уже реализован в самом фреймворке.
О пересичении бронирования в процессе редактирования можно не переживать из-за решения на уровне БД описанного выше.

Код:
```python
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price_per_day", "capacity")
    list_filter = ("price_per_day", "capacity")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "user", "date_start", "date_end")
    list_filter = ("room", "user", "date_start")
    search_fields = ("room__name", "user__username")
```
![документация просмотр броней](images/admin.png)
---

---
## 🛂Регистрация и авторизация
**Задача**
```
Пользователи должны уметь регистрироваться и авторизовываться (логиниться).
```
**Решение**
Для авторизации использовал jwt-токены с помощью simplejwt.
Для удобства тестирования и проверки поставил срок жизни для `ACCESS_TOKEN` - 2 часа.

Решение полностью реализованно с помощью библиотеки.
Два эндпоинта, один - для получения токена, второй - для его обновления.
```python
path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh")
```
![документация авторизация](images/api_token.png)
![документация авторизация](images/api_refresh_token.png)
Логика выхода по заданию не нужна, а на практике решается на стороне фронтенда, через бэкенд решается костылями с черным списком.

Для регистрации реализован следующий эндпоинт. Тут я всю логику создания нового пользователя обернул в транзакцию - сделано это для того, чтобы при ошибке не связанной с работой бд пользователь не получал 
ошибку регистрации при том что его данные уже в БД.

Добавил тротлинг для защиты проекта.
При успешной регистрации отдается токен чтобы фронтенд мог продолжить работу с пользователем ужен как с зарегистрированным.

Код:
```python
class UserApi(ModelViewSet):
    """
    API эндпоинт для регистрации нового пользователя.

    Данный эндпоинт создает нового пользователя с предоставленными данными (username, password, password2, email),
    валидирует их и возвращает access_token при успешной регистрации.


    Примечание:
    - Этот эндпоинт доступен без авторизации.
    - Данные в поле password должны удовлетворять требованиям безопасности (минимальная длина, сложность).
    """

    queryset = get_user_model().objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer
    throttle_classes = [UserRegistrationThrottle]
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            with transaction.atomic():
                serializer.is_valid(raise_exception=True)
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                response_data = {
                    "access_token": str(refresh.access_token),
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
        except ValidationError:
            raise

        except Exception as e:  # pragma: no cover
            logger.error(
                "Вовремя регистрации нового пользователя проищошла непредвиденая ошибка.\n"
                f"data: {request.data}\n"
                f"error: {str(e)}"
            )
            return Response(
                {"detail": "Произошла непредвиденная ошибка. Попробуйте позднее."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
```
![документация авторизация](images/api_registration.png)
---

## 👋Приветствуется

---
### Автотесты
Тесты прогоняются в контейнере так как для работы приложения необходим postgresql.
Контейнер можно запустить самостоятельно с помощью команды:
```commandline
docker-compose -f docker-compose.test.yml up --build
```

Так же тесты запускаются автоматически при изменениях в ветке `main` с помощью `github workflows`. 
После прохождения тестов формируется отчет и загружается на [coveralls.io](https://coveralls.io/github/sweetsenpai/DjangoBookingApp)

Покрытие тестами составляет 100%.

Тесты написаны с помощью `pytest-django`.
С конфигурацией pytest можно ознакомиться тут:
* [conftest.py📝](booking_app/conftest.py)
* [pytest.ini📝](booking_app/pytest.ini)
* [settings_test.py📝](booking_app/booking_app/settings_test.py)

### Линтер
При запуске тестов так же запускается pylint. На данный моментоценка кода `9.6/10`.
С конфигурацией pytest можно ознакомиться тут:
* [pylintrc📝](booking_app/.pylintrc)
* 
### Автоформатирование кода

На проекте использовались isort и black.
Их конфигурация находится тут: 
* [pyproject.toml📝](booking_app/pyproject.toml)

---
## Дополнительно
Дополнительно на проекте можно было бы настроить:
* `celery` - для асинхронных задач
* `reddis` - для хранения кэша и в качестве брокера сообщений.
* `senrty` - для мониторинга ошибок.
* `grafana + prometheus` - для мониторинга.
* `flower` - для мониторинга `celery`.
