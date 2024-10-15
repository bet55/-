import logging
from sqlite3 import OperationalError
from typing import Any
from diskcache import Cache


class Caching:
    def __init__(self, dirname=None, ttl=None):
        """
        :param dirname: (str) - название папки хранения файла кеша.
        :param ttl: (int) время актуальности кеша в секундах.
        """
        # Признак успешности инициализации
        self.__initialized = True

        # Сообщение об ошибке
        self.__error_message = ""

        # Проверка параметров
        if dirname and type(dirname) is not str:
            self.__error_message = "Переданный dirname не является строкой."
            logging.error(self.__error_message)
            self.__initialized = False
            return None
        if ttl and type(ttl) is not int:
            self.__error_message = "Переданный ttl не является целым числом."
            logging.error(self.__error_message)
            self.__initialized = False
            return None
        if ttl and ttl < 0:
            self.__error_message = "Переданн отрицательный ttl."
            logging.error(self.__error_message)
            self.__initialized = False
            return None

        self.__dirname = dirname if dirname else None
        self.__ttl = ttl if ttl else None

        # Инициализация кешировальщика
        self.__cache = None
        try:
            self.__cache = Cache(self.__dirname)
        except OperationalError as e:
            self.__error_message = f"При инициализации кешировальщика возникла ошибка. [{str(e)}]"
            logging.error(self.__error_message)
            self.__initialized = False
            return None
        except Exception as e:
            self.__error_message = f"При инициализации кешировальщика возникла непредвиденная ошибка. [{str(e)}]"
            logging.error(self.__error_message)
            self.__initialized = False
            return None

    def check_cache(self, key=None) -> bool:
        """
        Проверка наличия параметра в кеше.
        :param key: (int|str) параметр в кеше.
        :return: (bool) результат проверки.
        """
        # Проверка параметров
        if key is None:
            return False
        if type(key) not in [int, str]:
            self.__error_message = "Переданный key не является целым числом или строкой."
            logging.error(self.__error_message)
            return False

        return key in self.__cache

    def get_cache(self, key=None) -> Any:
        """
        Получение данных из кеша.
        :param key: (int|str) ключ размещения данных в кеше.
        :return: (any) python-объект данных из кеша.
        """
        # Проверка параметров
        if key is None:
            self.__error_message = "Параметр key не задан."
            logging.error(self.__error_message)
            return None
        if key and type(key) not in [int, str]:
            self.__error_message = "Переданный key не является целым числом или строкой."
            logging.error(self.__error_message)
            return None

        # Получение данных из кеша
        try:
            return self.__cache.get(key)
        except TypeError as e:
            self.__error_message = "Не удалось получить данные из кеша."
            logging.error(self.__error_message)
            return False
        except Exception as e:
            self.__error_message = "При получении данных из кеша возникла непредвиденная ошибка."
            logging.error(self.__error_message)
            return False

    def get_error_message(self) -> str:
        return self.__error_message

    def get_status(self) -> bool:
        return self.__initialized

    def set_cache(self, key=None, value=None) -> bool:
        """
        Размещение данных в кеш.
        :param key: (int|str) ключ размещения данных в кеше.
        :param value: (any) python-объект.
        :return: (bool) результат кеширования.
        """
        # Проверка параметров
        if key is None:
            self.__error_message = "Параметр key не задан."
            logging.error(self.__error_message)
            return False
        if key and type(key) not in [int, str]:
            self.__error_message = "Переданный key не является целым числом или строкой."
            logging.error(self.__error_message)
            return False

        # Кеширование данных
        try:
            return self.__cache.set(key, value, expire=self.__ttl)
        except TypeError as e:
            self.__error_message = "Не удалось закешировать данные."
            logging.error(self.__error_message)
            return False
        except Exception as e:
            self.__error_message = "При кешировании данных возникла непредвиденная ошибка."
            logging.error(self.__error_message)
            return False
