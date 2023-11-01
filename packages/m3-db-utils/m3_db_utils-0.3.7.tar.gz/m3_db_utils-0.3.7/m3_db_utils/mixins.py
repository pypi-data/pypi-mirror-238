from abc import (
    abstractmethod,
)
from typing import (
    Dict,
)

from django.db.models import (
    CharField,
    PositiveIntegerField,
    TextField,
)
from django.db.models.base import (
    Model,
)
from django.utils.decorators import (
    classproperty,
)

from m3_db_utils.consts import (
    DEFAULT_ORDER_NUMBER,
)
from m3_db_utils.models import (
    TitledModelEnum,
)


class TitleFieldMixin(Model):
    """
    Добавляет поле текстовое поле title обязательное для заполнения
    """

    title = TextField(verbose_name='расшифровка значения')

    class Meta:
        abstract = True


class IntegerValueMixin(Model):
    """
    Добавляет положительное целочисленное поле value обязательное для заполнения
    """

    value = PositiveIntegerField(verbose_name='значение ')

    class Meta:
        abstract = True


class CharValueMixin(Model):
    """
    Добавляет символьное поле value обязательное для заполнения
    """

    value = CharField(verbose_name='значение ', max_length=256)

    class Meta:
        abstract = True


class BaseEnumRegisterMixin:
    """
    Базовый миксин, для регистрации класса в модель-перечисление.
    """

    enum: TitledModelEnum
    """Модель-перечисление в которую регистрируется класс."""
    order_number: int = DEFAULT_ORDER_NUMBER
    """Порядковый номер следования значения модели-перечисления."""

    @classmethod
    def get_register_params(cls) -> Dict[str, ...]:
        return {
            'order_number': cls.order_number,
            'title': cls.title,
            'key': cls.key
        }

    @classproperty
    @abstractmethod
    def key(cls) -> str:
        """Ключ класса, регистрируемого в модели-перечисления."""

    @classproperty
    @abstractmethod
    def title(cls) -> str:
        """Расшифровка класса, регистрируемого в модели-перечисления."""

    @classmethod
    def register(cls) -> None:
        """Метод, регистрирующий класс в модель-перечисление."""
        params = cls.get_register_params()
        cls.enum.extend(**params)
