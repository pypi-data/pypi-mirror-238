from enum import Enum


class ApplicationProfilesEnum(Enum):
    """Enum class representing various properties for Python application properties."""

    APPLICATION_PROFILE_ENVIRONEMNT_VALUE = "APP_PROFILES"
    """str: The property key for accessing the application environment value.
    This string could a single value or a list separated by `,` (comma), where the profile(s) to be loaded are indicated.
    """

    PROFILE_FILE_PREFIX = "application"
    """str: The property key for accessing the properties file prefix.
    By default, the most basic file to be provide is `application.yaml`, in the case of having more than one file, the `APP_PROFILE`
    value will indicate by predence criteria all the profile listed, the first file loaded is always the default file, then it 
    will loop through the contennt of `APP_PROFILE`.
    """

    PROFILE_FILE_FORMATS = ["yaml", "yml"]
    """list[str]: The property key for accessing the supported properties file formats."""

    PROFILES_MODULE = "profiles"
    """str: The property key for accessing the properties Python module identifier. It location stores the application-XXX.yaml files"""

    PROFILES_SEPARATOR = ","

    DEFAULT_PROFILE = "default"
