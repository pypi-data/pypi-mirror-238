# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import os
import typing
import dataclasses
import json
import yaml

from configparser import RawConfigParser

from .base import Utils


class HostType(str):

    @classmethod
    def decode(cls, val):

        if not val:
            return None

        host, port = val.split(r':', 2)
        return host.strip(), int(port.strip())


class JsonType(str):

    @classmethod
    def decode(cls, val):

        if not val:
            return None

        return Utils.json_decode(val)


class StrListType(str):

    @classmethod
    def decode(cls, val):
        return Utils.split_str(val)


class IntListType(str):

    @classmethod
    def decode(cls, val):
        return Utils.split_int(val)


class FloatListType(str):

    @classmethod
    def decode(cls, val):
        return Utils.split_float(val)


class Field:

    __slots__ = [r'section', r'default']

    def __init__(self, section, default=None):

        self.section = section
        self.default = default


class ConfigureMetaclass(type):
    """配置类元类，增加dataclass修饰
    """

    def __new__(mcs, name, bases, attrs):
        return dataclasses.dataclass(init=False)(
            type.__new__(mcs, name, bases, attrs)
        )


class KeySection(typing.NamedTuple):

    key: str
    type: typing.Any
    section: str
    default: typing.Any


class ConfigureBase(metaclass=ConfigureMetaclass):
    """配置类
    """

    __slots__ = [r'_data', r'_parser', r'_key_section']

    def __init__(self):

        super().__init__()

        self._parser = RawConfigParser()

        self._key_section: typing.Dict[str, KeySection] = {
            f'{_field.default.section}_{_key}': KeySection(
                _key,
                _field.type,
                _field.default.section,
                _field.default.default,
            )
            for _key, _field in self.__dataclass_fields__.items()
        }

    @property
    def data(self) -> typing.Dict:

        return dataclasses.asdict(self)

    def _load_options(self):

        for _key_section in self._key_section.values():

            # 优先处理环境变量
            _env_key = f'{_key_section.section}_{_key_section.key}'.upper()
            _env_val = os.getenv(_env_key, None)

            if _env_val is not None:
                self._parser.set(_key_section.section, _key_section.key, _env_val)
                Utils.log.info(f'load environment variable {_env_key}: {_env_val}')

            if _key_section.type is str:
                _val = self._parser.get(_key_section.section, _key_section.key)
            elif _key_section.type is int:
                _val = self._parser.getint(_key_section.section, _key_section.key)
            elif _key_section.type is float:
                _val = self._parser.getfloat(_key_section.section, _key_section.key)
            elif _key_section.type is bool:
                _val = self._parser.getboolean(_key_section.section, _key_section.key)
            else:
                _val = _key_section.type.decode(self._parser.get(_key_section.section, _key_section.key))

            self.__setattr__(_key_section.key, _val)

    def _clear_options(self):

        self._parser.clear()

        _config = {}

        for _key_section in self._key_section.values():
            if _key_section.default is not None:
                _config.setdefault(_key_section.section, {})[_key_section.key] = _key_section.default

        if _config:
            self._parser.read_dict(_config)


class Configure(ConfigureBase):
    """配置类
    """

    def get_option(self, section, option) -> typing.Any:

        return self._parser.get(section, option)

    def get_options(self, section) -> typing.Dict:

        parser = self._parser

        options = {}

        for option in parser.options(section):
            options[option] = parser.get(section, option)

        return options

    def set_options(self, section, **options):

        if not self._parser.has_section(section):
            self._parser.add_section(section)

        for option, value in options.items():
            self._parser.set(section, option, value)

        self._load_options()

    def read(self, path, encoding=r'utf-8'):

        self._clear_options()

        self._parser.read(path, encoding=encoding)

        self._load_options()

    def read_env(self):

        self._clear_options()

        self._load_options()

    def read_str(self, val):

        self._clear_options()

        self._parser.read_string(val)

        self._load_options()

    def read_dict(self, val):

        self._clear_options()

        self._parser.read_dict(val)

        self._load_options()

    def read_json(self, path, encoding=r'utf-8'):

        self._clear_options()

        with open(path, encoding=encoding) as fp:
            self._parser.read_dict(json.loads(fp.read()))

        self._load_options()

    def read_yaml(self, path, encoding=r'utf-8'):

        self._clear_options()

        with open(path, encoding=encoding) as fp:
            self._parser.read_dict(yaml.load(fp.read(), yaml.Loader))

        self._load_options()
