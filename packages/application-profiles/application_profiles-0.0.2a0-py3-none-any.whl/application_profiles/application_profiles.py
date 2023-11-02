import os
import yaml
from typing import List
from importlib.util import find_spec
from application_profiles.application_profiles_enum import ApplicationProfilesEnum
from application_profiles.application_profiles_exception import (
    ApplicationProfileException,
)
from yaml.loader import SafeLoader
from importlib import resources
import logging


class ApplicationProfiles:
    def __init__(self, profiles: str = "default"):
        self.__profiles: str = profiles
        self.properties: dict = None
        self.logger = logging.getLogger(__name__)
        self.__initialize()

    def __initialize(self) -> None:
        self.__validate_profiles_module()
        profiles_list = self.__get_profiles_to_load()
        self.logger.info(f"Detected Profiles: '{profiles_list}'")

        all_profile_files_list: list = self.__build_filenames_by_profile(
            profiles_list=profiles_list
        )
        self.properties = self.__load_profiles(files_to_load=all_profile_files_list)

    def __get_profiles_to_load(self) -> None:
        profiles_from_env_var: str = os.environ.get(
            ApplicationProfilesEnum.APPLICATION_PROFILE_ENVIRONEMNT_VALUE.value
        )
        if profiles_from_env_var != None:
            self.__profiles = profiles_from_env_var
        profile_list = self.__profiles.split(
            ApplicationProfilesEnum.PROFILES_SEPARATOR.value
        )
        if ApplicationProfilesEnum.DEFAULT_PROFILE.value not in profile_list:
            profile_list.insert(0, ApplicationProfilesEnum.DEFAULT_PROFILE.value)
        return profile_list

    def __validate_profiles_module(self) -> None:
        profiles_module_name = ApplicationProfilesEnum.PROFILES_MODULE.value
        profiles_module_found = find_spec(profiles_module_name)
        if profiles_module_found == None:
            raise ApplicationProfileException(
                f"Module '{profiles_module_name}' does not exist or not found. Properties can not be loaded."
            )

    def __build_filenames_by_profile(self, profiles_list: list):
        all_profile_files: list = []
        for profile in profiles_list:
            all_profile_files.extend(self.__build_filename_list(profile=profile))
        return all_profile_files

    def __build_filename_list(self, profile: str = None) -> list:
        files: list = []
        for format in ApplicationProfilesEnum.PROFILE_FILE_FORMATS.value:
            if profile != ApplicationProfilesEnum.DEFAULT_PROFILE.value:
                files.append(
                    f"{ApplicationProfilesEnum.PROFILE_FILE_PREFIX.value}-{profile}.{format}"
                )
            else:
                files.append(
                    f"{ApplicationProfilesEnum.PROFILE_FILE_PREFIX.value}.{format}"
                )
        return files

    def __load_profiles(self, files_to_load: list) -> dict:
        full_profile: dict = {}
        for file in files_to_load:
            profile = self.__load_profile_file(filename=file)
            full_profile = self.__merge_dicts(full_profile, profile)
        return full_profile

    def __load_profile_file(self, filename: str) -> dict:
        try:
            file_content: str = (
                resources.files(ApplicationProfilesEnum.PROFILES_MODULE.value)
                .joinpath(filename)
                .read_text()
            )
            profile_content: dict = yaml.load(file_content, Loader=SafeLoader)
            self.logger.info(f"Loading profile from: '{filename}'")
            if profile_content == None:
                return {}
            else:
                return profile_content
        except Exception as e:
            self.logger.debug(f"Profile file {filename} not found.")
            return {}

    def __merge_dicts(self, dict1, dict2):
        merged_dict = dict1.copy()

        for key, value in dict2.items():
            if (
                key in merged_dict
                and isinstance(merged_dict[key], dict)
                and isinstance(value, dict)
            ):
                merged_dict[key] = self.__merge_dicts(merged_dict[key], value)
            else:
                merged_dict[key] = value

        return merged_dict
