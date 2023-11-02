"""
Configure general settings for your applicaton like the icons to use, how to sync data with the server, and more.
"""
from cave_utils.api.utils import *
import type_enforced

@type_enforced.Enforcer
class settings_time(ApiValidator):
    """
    ## Api Path: settings.time
    """

    @staticmethod
    def spec(timeLength: int, timeUnits: str, **kwargs):
        """
        Required Arguments:

        - `timeLength`:
            - Type: int
            - What: The amount of time to display.
        - `timeUnits`:
            - Type: str
            - What: The units of time to display.
        """
        return {
            "kwargs": kwargs,
            "accepted_values": {},
        }


@type_enforced.Enforcer
class settings_sync(ApiValidator):
    """
    ## Api Path: settings.sync
    """

    @staticmethod
    def spec(name: str, showToggle: bool, value: bool, data: dict, **kwargs):
        """
        Required Arguments:

        - `name`:
            - Type: str
            - What: The name of the sync setting.
        - `showToggle`:
            - Type: bool
            - What: If `True`, the toggle will be displayed.
        - `value`:
            - Type: bool
            - What: The initial value of the toggle.
        - `data`:
            - Type: dict
            - What: The data to sync with the server.

        """
        return {
            "kwargs": kwargs,
            "accepted_values": {},
        }

    # def __extend_spec__(self, **kwargs):
    #     root_data = kwargs.get("root_data", {})
    #     for key, path in self.data.get("data", {}).items():
    #         if not pamda.hasPath(path, root_data):
    #             self.__warn__(f"Path {path} does not exist.", prepend_path=["data", key])


@type_enforced.Enforcer
class settings_demo(ApiValidator):
    """
    ## Api Path: settings.demo
    """

    @staticmethod
    def spec(scrollSpeed: [int, float] = 1, displayTime: int = 5, **kwargs):
        """
        Optional Arguments:

        - `scrollSpeed`:
            - Type: int
            - What: The speed at which the demo text will scroll.
            - Default: `1`
        - `displayTime`:
            - Type: int
            - What: The amount of time to display the demo text.
            - Default: `5`
        """
        return {
            "kwargs": kwargs,
            "accepted_values": {},
        }


@type_enforced.Enforcer
class settings_defaults(ApiValidator):
    """
    ## Api Path: settings.defaults
    """

    @staticmethod
    def spec(
        precision: int = 2,
        trailingZeros: bool = False,
        unitPlacement: str = "right",
        showToolbar: bool = True,
        **kwargs,
    ):
        """
        Required Arguments:

        - `precision`:
            - Type: int
            - What: The number of decimal places to display.
            - Default: `2`
        - `trailingZeros`:
            - Type: bool
            - What: If `True`, trailing zeros will be displayed.
            - Default: `False`
        - `unitPlacement`:
            - Type: str
            - What: Where to place the unit.
            - Default: `"right"`
            - Accepted Values:
                - `"right"`
                - `"left"`
        - `showToolbar`:
            - Type: bool
            - What: If `True`, the toolbar will be displayed.
            - Default: `True`
        """
        return {
            "kwargs": kwargs,
            "accepted_values": {
                # TODO: "unitPlacement": [],
            },
        }


@type_enforced.Enforcer
class settings(ApiValidator):
    """
    ## Api Path: settings
    """

    @staticmethod
    def spec(
        iconUrl: str,
        demo: dict = dict(),
        sync: dict = dict(),
        time: dict = dict(),
        defaults: dict = dict(),
        debug: bool = False,
        **kwargs,
    ):
        """
        Required Arguments:

        - `iconUrl`:
            - Type: str
            - What: The url to the icon to use for your application.
            - Note: This is the only required field in `settings`.

        Optional Arguments:

        - `demo`:
            - Type: dict
            - What: Settings for the demo mode of your application.
            - See: `settings_demo`
            - Default: `{}`
        - `sync`:
            - Type: dict
            - What: Settings for syncing data with the server.
            - See: `settings_sync`
            - Default: `{}`
        - `time`:
            - Type: dict
            - What: Settings for the time display.
            - See: `settings_time`
            - Default: `{}`
        - `defaults`:
            - Type: dict
            - What: Default settings for your application.
            - See: `settings_defaults`
            - Default: `{}`
        - `debug`:
            - Type: bool
            - What: If `True`, the server will return debug information.
            - Default: `False`
        """
        return {
            "kwargs": kwargs,
            "accepted_values": {},
        }

    def __extend_spec__(self, **kwargs):
        self.__check_url_valid__(
            url=self.data.get("iconUrl"),
        )
        CustomKeyValidator(
            data=self.data.get("sync", {}),
            log=self.log,
            prepend_path=["sync"],
            validator=settings_sync,
            **kwargs,
        )
        CustomKeyValidator(
            data=self.data.get("demo", {}),
            log=self.log,
            prepend_path=["demo"],
            validator=settings_demo,
            **kwargs,
        )
        if self.data.get("time"):
            settings_time(
                data=self.data.get("time", {}),
                log=self.log,
                prepend_path=["time"],
                **kwargs,
            )
        settings_defaults(
            data=self.data.get("defaults", {}),
            log=self.log,
            prepend_path=["defaults"],
            **kwargs,
        )
