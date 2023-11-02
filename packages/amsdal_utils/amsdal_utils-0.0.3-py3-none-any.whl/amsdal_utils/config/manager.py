from pathlib import Path
from typing import Any

import yaml

from amsdal_utils.config.data_models.amsdal_config import AmsdalConfig
from amsdal_utils.config.data_models.connection_config import ConnectionConfig
from amsdal_utils.config.data_models.repository_config import RepositoryConfig
from amsdal_utils.utils.singleton import Singleton


class AmsdalConfigManager(metaclass=Singleton):
    _config: AmsdalConfig

    def set_config(self, config: AmsdalConfig) -> None:
        self._config = config

    def get_config(self) -> AmsdalConfig:
        return self._config

    def get_connection_name_by_model_name(self, model_name: str) -> str:
        repository_config: RepositoryConfig = self._config.resources_config.repository

        if model_name in repository_config.models:
            return repository_config.models[model_name]
        return repository_config.default

    def load_config(self, config_path: Path) -> None:
        with config_path.open() as config_file:
            self.set_config(self.read_yaml_config(config_file))

    @staticmethod
    def read_yaml_config(config: Any) -> AmsdalConfig:
        config = yaml.safe_load(config)

        if 'connections' not in config:
            config['connections'] = []

        if isinstance(config['connections'], list):
            config['connections'] = [ConnectionConfig(**connection) for connection in config['connections']]

        return AmsdalConfig.model_validate(config)
