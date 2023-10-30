import os
from pathlib import Path
from typing import AnyStr, Optional, Any


class AllureEnvironmentsBuilder:
    """Строитель файла с переменными окружения, которые будут отображаться в allure-report"""

    def __init__(self):
        self._filename = 'environment.properties'
        self._properties = dict()

    def reset(self):
        self._properties = dict()

    def add(self, key: str, value: Any):
        """Добавить переменную

        :param key: имя переменной
        :param value: значение переменной
        :return: экземпляр строителя
        """
        self._properties[key] = value
        return self

    def with_environments(self):
        """Добавить все переменные окружения"""
        self._properties |= os.environ
        return self

    def build(self, results_dir: Optional[AnyStr | Path] = None):
        """Построить файл с переменными окружения для allure

        :param results_dir: путь до директории с результатами теста
        :return: содержимое файла с переменными окружения
        """
        properties = [f'{key}={value}' for key, value in self._properties.items()]
        output = '\n'.join(properties)

        if results_dir:
            path = self._create_path(results_dir)
            with open(path / self._filename, 'w') as file:
                file.write(output)

        return output

    @staticmethod
    def _create_path(value: AnyStr | Path):
        if isinstance(value, Path):
            path = value
        elif isinstance(value, bytes):
            path = Path(value.decode())
        else:
            path = Path(value)

        if not path.exists():
            os.makedirs(path)

        return path
