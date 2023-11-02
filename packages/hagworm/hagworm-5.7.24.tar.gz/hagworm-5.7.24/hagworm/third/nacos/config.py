# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import json
import yaml

from ...extend.config import ConfigureBase

from .client import NacosConfig


class Configure(ConfigureBase):
    """配置类
    """

    __slots__ = [r'_format', r'_client']

    def __init__(
            self, servers, data_id, *,
            protocol=None, endpoint=None, group=None, namespace=None, data_format=r'yaml'
    ):

        super().__init__()

        self._format = data_format

        self._client = NacosConfig(
            self._reload_config, servers, data_id,
            protocol=protocol, endpoint=endpoint, group=group, namespace=namespace
        )

    def _reload_config(self, content):

        self._clear_options()

        if self._format == r'text':
            self._parser.read_string(content)
        elif self._format == r'json':
            self._parser.read_dict(json.loads(content))
        elif self._format == r'yaml':
            self._parser.read_dict(yaml.load(content, yaml.Loader))

        self._load_options()

    def open(self):

        self._client.start()

    def close(self):

        self._client.stop()
        self._clear_options()
