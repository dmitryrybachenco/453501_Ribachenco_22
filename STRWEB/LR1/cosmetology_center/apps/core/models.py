from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.users.models import User
from apps.services.models import Service


class News(models.Model):
    """Модель новостей - список статей с заголовком, кратким содержанием, картинкой"""
    title = models.CharField('Заголовок', max_length=200)
    short_description = models.CharField('Краткое описание (одно предложение)', max_length=300)
    content = models.TextField('Полное содержание')
    image = models.ImageField('Картинка', upload_to='news/', blank=True, null=True)
    published_at = models.DateTimeField('Дата публикации', default=timezone.now)
    is_published = models.BooleanField('Опубликовано', default=True)
    created_at = models.DateTimeField('Создана', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлена', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-published_at']


class Glossary(models.Model):
    """Модель словаря терминов и понятий - список часто задаваемых вопросов и ответов"""
    term = models.CharField('Термин/Вопрос', max_length=200)
    definition = models.TextField('Определение/Ответ')
    added_at = models.DateTimeField('Дата добавления на сайт', auto_now_add=True)

    def __str__(self):
        return self.term

    class Meta:
        verbose_name = 'Термин'
        verbose_name_plural = 'Словарь терминов'
        ordering = ['term']


class Contact(models.Model):
    """Модель контактов - фото сотрудников с описанием работ, телефонами, почтой"""
    full_name = models.CharField('ФИО', max_length=150)
    position = models.CharField('Должность', max_length=100)
    description = models.TextField('Описание выполняемых работ')
    phone = models.CharField(
        'Телефон',
        max_length=20,
        help_text='Формат: +375 (29) XXX-XX-XX'
    )
    email = models.EmailField('Email')
    photo = models.ImageField('Фото', upload_to='contacts/', blank=True, null=True)
    order = models.IntegerField('Порядок сортировки', default=0)
    is_active = models.BooleanField('Активен', default=True)

    def __str__(self):
        return f"{self.full_name} - {self.position}"

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['order', 'full_name']


class Vacancy(models.Model):
    """Модель вакансий - список вакансий с описанием"""
    title = models.CharField('Название вакансии', max_length=150)
    description = models.TextField('Описание вакансии')
    requirements = models.TextField('Требования к кандидату')
    salary = models.CharField('Зарплата', max_length=100, blank=True)
    location = models.CharField('Местоположение', max_length=200, default='Минск')
    is_active = models.BooleanField('Активна', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-created_at']


class CompanyInfo(models.Model):
    """Модель информации о компании для страницы 'О компании'"""
    company_name = models.CharField('Название компании', max_length=200, default='Косметологический центр')
    short_description = models.TextField('Краткое описание')
    full_description = models.TextField('Полное описание')
    logo = models.ImageField('Логотип', upload_to='company/', blank=True, null=True)
    video_url = models.URLField('Ссылка на видео', blank=True)

    inn = models.CharField('ИНН', max_length=20, blank=True)
    ogrn = models.CharField('ОГРН', max_length=20, blank=True)
    legal_address = models.CharField('Юридический адрес', max_length=300, blank=True)
    actual_address = models.CharField('Фактический адрес', max_length=300, blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    email = models.EmailField('Email', blank=True)
    bank_details = models.TextField('Банковские реквизиты', blank=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = 'Информация о компании'
        verbose_name_plural = 'Информация о компании'


class CompanyHistory(models.Model):
    """Модель истории компании по годам"""
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, related_name='history')
    year = models.IntegerField('Год')
    event = models.CharField('Событие', max_length=300)
    description = models.TextField('Описание', blank=True)

    def __str__(self):
        return f"{self.year} - {self.event}"

    class Meta:
        verbose_name = 'История компании'
        verbose_name_plural = 'История компании'
        ordering = ['year']


class CompanyRequirement(models.Model):
    """Модель реквизитов компании (отдельная таблица для детализации)"""
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, related_name='requirements')
    name = models.CharField('Название реквизита', max_length=100)
    value = models.CharField('Значение', max_length=200)

    def __str__(self):
        return f"{self.name}: {self.value}"

    class Meta:
        verbose_name = 'Реквизит'
        verbose_name_plural = 'Реквизиты'


class Banner(models.Model):
    """Баннер для главной страницы"""
    title = models.CharField('Заголовок', max_length=200)
    subtitle = models.CharField('Подзаголовок', max_length=300, blank=True)
    image = models.ImageField('Изображение баннера', upload_to='banners/')
    url = models.URLField('Ссылка', blank=True, help_text='Куда ведет баннер (опционально)')
    order = models.IntegerField('Порядок отображения', default=0)
    is_active = models.BooleanField('Активен', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'
        ordering = ['order', '-id']


class Partner(models.Model):
    """Компания-партнер"""
    name = models.CharField('Название компании', max_length=200)
    logo = models.ImageField('Логотип', upload_to='partners/')
    website = models.URLField('Сайт компании')
    description = models.TextField('Описание', blank=True)
    order = models.IntegerField('Порядок отображения', default=0)
    is_active = models.BooleanField('Активен', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'
        ordering = ['order', 'name']


class Cart(models.Model):
    """Корзина пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField('Создана', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлена', auto_now=True)

    def get_total(self):
        """Общая сумма корзины"""
        total = sum(item.get_total() for item in self.items.all())
        return total

    def get_items_count(self):
        """Количество товаров в корзине"""
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return f"Корзина {self.user.username}"

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    """Товар в корзине"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField('Количество', default=1, validators=[MinValueValidator(1)])

    def get_total(self):
        """Стоимость позиции в корзине"""
        return self.service.price * self.quantity

    def __str__(self):
        return f"{self.service.name} x{self.quantity}"

    class Meta:
        verbose_name = 'Позиция в корзине'
        verbose_name_plural = 'Позиции в корзине'
        unique_together = ['cart', 'service']


class Order(models.Model):
    """Заказ"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('cancelled', 'Отменен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(CartItem, related_name='orders')
    total = models.DecimalField('Итоговая сумма', max_digits=10, decimal_places=2)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлен', auto_now=True)

    # Поля для оплаты
    payment_method = models.CharField('Способ оплаты', max_length=50, blank=True)
    payment_date = models.DateTimeField('Дата оплаты', null=True, blank=True)

    def __str__(self):
        return f"Заказ #{self.id} - {self.user.username} - {self.total} руб."

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']