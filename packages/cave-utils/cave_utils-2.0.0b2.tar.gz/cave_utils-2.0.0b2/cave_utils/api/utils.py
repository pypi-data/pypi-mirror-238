"""
Special utility functions to help in validating your data against the CAVE API. This is not a key that should be passed as part of your `session_data`.
"""
from pamda import pamda
import type_enforced
import re
from cave_utils.log import LogHelper, LogObject


class ApiValidator:
    def __init__(self, **fields):
        self.__validate__(**fields)

    def spec(self, **kwargs):
        """
        The default spec method.

        This provides a baseline spec for some utility validators.

        This should be overridden by any non utility child class.
        """
        return {
            "kwargs": {},
            "accepted_values": {},
        }

    def __validate__(self, data, log: LogObject, prepend_path: list = list(), **kwargs):
        """
        Run the api validation process for the passed data.
        """
        self.data = data
        self.ignore_keys = kwargs.get("ignore_keys", set())
        self.log = LogHelper(log=log, prepend_path=prepend_path)
        try:
            spec_output = self.spec(**self.data)
            extra_kwargs = spec_output.get("kwargs", {})
            # TODO: Find way to custom check timeValues and order
            extra_kwargs.pop("order", None)
            extra_kwargs.pop("timeValues", None)
            if extra_kwargs != {}:
                self.__warn__(
                    msg=f"Unknown Fields: {str(list(extra_kwargs.keys()))}",
                )
        except Exception as e:
            self.__error__(
                msg=f"Error validating spec: {e}",
            )
            # Must return since an invalid spec will bug out other validation checks
            return
        for field, accepted_values in spec_output.get("accepted_values", {}).items():
            if field not in self.data:
                continue
            check_value = self.data.get(field)
            if isinstance(check_value, dict):
                check_value = list(check_value.keys())
            if isinstance(check_value, str):
                check_value = [check_value]
            if isinstance(check_value, list):
                if self.__check_subset_valid__(
                    subset=check_value, valid_values=accepted_values, prepend_path=[field]
                ):
                    continue

        # Run additional Validations
        # self.__extend_spec__(**kwargs)
        try:
            self.__extend_spec__(**kwargs)
        except Exception as e:
            self.__error__(
                path=[],
                msg=f"Extended spec validations failed (likely due to another error with your api data). Error: {e}",
            )

    # Placeholder method for additional validations
    def __extend_spec__(self, **kwargs):
        pass

    # Error and Warning Helpers
    def __error__(self, msg: str, path: list = list()):
        """
        Raise an error for the log the log
        """
        self.log.add(path=path, msg=msg)

    def __warn__(self, msg: str, path: list = list()):
        """
        Raise a warning for the log the log
        """
        self.log.add(path=path, msg=msg, level="warning")

    # Useful Validator Checks
    def __check_rgba_string_valid__(self, rgba_string: str, prepend_path: list = list()):
        """
        Validate an rgba string and if an issue is present, log an error
        """
        try:
            if "rgba(" != rgba_string[:5]:
                self.__error__(path=prepend_path, msg="Invalid RGBA string")
                return
            if ")" != rgba_string[-1]:
                self.__error__(path=prepend_path, msg="Invalid RGBA string")
                return
            rgba_list = rgba_string[5:-1].replace(" ", "").split(",")
            for rgba in rgba_list:
                if not rgba.isdigit():
                    self.__error__(path=prepend_path, msg="Invalid RGBA string")
                    return
                if int(rgba) < 0 or int(rgba) > 255:
                    self.__error__(path=prepend_path, msg="Invalid RGBA string")
                    return
        except:
            self.__error__(path=prepend_path, msg="Invalid RGBA string")

    def __check_pixel_string_valid__(self, pixel_string: str, prepend_path: list = list()):
        """
        Validate a pixel string and if an issue is present, log an error
        """
        try:
            if "px" != pixel_string[-2:]:
                self.__error__(path=prepend_path, msg="Invalid pixel string")
                return
            if int(pixel_string[:-2]) <= 0:
                self.__error__(path=prepend_path, msg="Invalid pixel string")
        except:
            self.__error__(path=prepend_path, msg="Invalid pixel string")

    def __check_url_valid__(self, url: str, prepend_path: list = list()):
        """
        Validate a url and if an issue is present, log an error
        """
        # Use Django regex for URL validation
        # See https://stackoverflow.com/a/7160778/12014156
        regex = re.compile(
            r"^(?:http|ftp)s?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
            r"localhost|"  # localhost...
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )
        if re.match(regex, url) is None:
            self.__error__(path=prepend_path, msg="Invalid url")

    def __check_subset_valid__(
        self,
        subset: list,
        valid_values: list,
        prepend_path: list = list(),
        valid_values_count: int = 6,
    ):
        """
        Validate a subset of values is in a set of valid values and if an issue is present, log an error

        Returns True if the subset check passed and False otherwise
        """
        invalid_values = pamda.difference(subset, valid_values)
        if len(invalid_values) > 0:
            valid_values = (
                valid_values[:valid_values_count] + ["..."]
                if len(valid_values) > valid_values_count
                else valid_values
            )
            self.__error__(
                path=prepend_path,
                msg=f"Invalid value(s) selected: {str(invalid_values)}. Accepted values are {valid_values}",
            )
            return False
        return True

    def __check_coord_path_valid__(self, coord_path: list, prepend_path: list = list()):
        """
        Validate a coordinate path and if an issue is present, log an error
        """
        try:
            if len(coord_path) < 2:
                self.__error__(path=prepend_path, msg="Invalid coordinate path")
                return
            for coord in coord_path:
                # Ensure coord is less than 3 items (longitude, latitude, altitude)
                if len(coord) > 3:
                    self.__error__(path=prepend_path, msg="Invalid coordinate path")
                    return
                # Check Longitude
                if coord[0] < -180 or coord[0] > 180:
                    self.__error__(path=prepend_path, msg="Invalid coordinate path")
                    return
                # Check Latitude
                if coord[1] < -90 or coord[1] > 90:
                    self.__error__(path=prepend_path, msg="Invalid coordinate path")
                    return
                # Check Altitude (if present)
                if len(coord) == 3:
                    if coord[2] < 0:
                        self.__error__(path=prepend_path, msg="Invalid coordinate path")
                        return
        except:
            self.__error__(path=prepend_path, msg="Invalid coordinate path")

    def __check_type_list__(self, data: list, types: tuple, prepend_path: list = list()):
        """
        Validate a list only contains certain object types and if an issue is present, log an error

        Returns True if the type check passed and False otherwise
        """
        if not isinstance(types, tuple):
            types = (types,)
        for idx, item in enumerate(data):
            if not isinstance(item, types):
                self.__error__(
                    path=prepend_path,
                    msg=f"Invalid list item type at index: {idx} with type: {type(item)}. Expected one of {types}",
                )
                return False
        return True
    
    def __check_type_dict__(self, data: dict, types: tuple, prepend_path: list = list()):
        """
        Validate a dict only contains certain object types for values and if an issue is present, log an error

        Returns True if the type check passed and False otherwise
        """
        if not isinstance(types, tuple):
            types = (types,)
        for key, value in data.items():
            if not isinstance(value, types):
                self.__error__(
                    path=prepend_path,
                    msg=f"Invalid dict item type at key: {key} with type: {type(value)}. Expected one of {types}",
                )
                return False
        return True

    def __check_type__(self, value, check_type, prepend_path: list = list()):
        """
        Validate a value is a certain type and if an issue is present, log an error

        Returns True if the type check passed and False otherwise

        Required Arguments:

        - `value`:
            - Type: any
            - What: The value to check.
        - `check_type`:
            - Type: type | tuple of types
            - What: The type(s) to check against.

        Optional Arguments:

        - `prepend_path`:
            - Type: list
            - What: The path to prepend to the error message.
            - Default: `[]`
        """
        if not isinstance(value, check_type):
            self.__error__(
                msg=f"({value}) Invalid Type: Expected one of {check_type} but got type {type(value)} instead.",
                path=prepend_path,
            )
            return False
        return True


@type_enforced.Enforcer
class CustomKeyValidator(ApiValidator):
    @staticmethod
    def spec(**kwargs):
        for k, v in kwargs.items():
            if not isinstance(v, dict):
                raise Exception(
                    f"Error for field ({k}): Type {type(dict())} is required but instead received {type(v)}"
                )
        return {
            "kwargs": {},
            "accepted_values": {},
        }

    def __extend_spec__(self, **kwargs):
        validator = kwargs.get("validator")
        assert validator is not None, "Must pass validator to CustomKeyValidator"
        kwargs = {k: v for k, v in kwargs.items() if k not in ["validator", "CustomKeyValidatorFieldId"]}
        for field, value in self.data.items():
            validator(data=value, log=self.log, prepend_path=[field], CustomKeyValidatorFieldId=field, **kwargs)