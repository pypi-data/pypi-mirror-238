import os
from typing import Optional

import yaml


class ConfigStore:
    __global_cfg_current_file = None
    __global_config = None

    __global_attributes_map_file = None
    __global_attributes_map = None

    __PROXYGUI_CFG_PATH = "perun.proxygui.yaml"

    @staticmethod
    def __load_cfg(cfg_filepath, property_name):
        if not os.path.exists(cfg_filepath):
            raise Exception("Config: missing config file: ", cfg_filepath)
        with open(cfg_filepath, "r", encoding="utf8") as f:
            setattr(ConfigStore, property_name, yaml.safe_load(f))

    @staticmethod
    def get_global_cfg(filepath):
        if (
            ConfigStore.__global_config is None
            or ConfigStore.__global_cfg_current_file != filepath
        ):
            ConfigStore.__load_cfg(filepath, "_ConfigStore__global_config")
            ConfigStore.__global_cfg_current_file = filepath
        return ConfigStore.__global_config

    @staticmethod
    def get_attributes_map(filepath):
        if (
            ConfigStore.__global_attributes_map is None
            or ConfigStore.__global_attributes_map_file != filepath
        ):
            ConfigStore.__load_cfg(filepath, "_ConfigStore__global_attributes_map")
            ConfigStore.__global_attributes_map_file = filepath
        return ConfigStore.__global_attributes_map

    @staticmethod
    def get_config_path(filename: str, required=True) -> Optional[str]:
        etc_filepath = f"/etc/{filename}"
        if os.path.exists(etc_filepath):
            return etc_filepath

        template_filepath = f"./config_templates/{filename}"
        if os.path.exists(template_filepath):
            return template_filepath

        if required:
            raise FileNotFoundError("No viable config file was found.")
        return None

    @staticmethod
    def get_config(filename=__PROXYGUI_CFG_PATH, required=True) -> dict:
        cfg_path = ConfigStore.get_config_path(filename, required)
        if not cfg_path:
            return {}
        with open(
            cfg_path,
            "r",
            encoding="utf8",
        ) as ymlfile:
            loaded_cfg = yaml.safe_load(ymlfile)

        return loaded_cfg
