"""
Build out an app bar with buttons to launch pages, launch panes and trigger api commands.
"""
from cave_utils.api.utils import ApiValidator, CustomKeyValidator
import type_enforced


@type_enforced.Enforcer
class appBar_data_star(ApiValidator):
    """
    ## Api Path: appBar.data.*
    """

    @staticmethod
    def spec(
        icon: str,
        type: str,
        bar: str,
        variant: [str, None] = None,
        color: [str, None] = None,
        apiCommand: [str, None] = None,
        apiCommandKeys: [list, None] = None,
        **kwargs,
    ):
        """
        Required Arguments:

        - `icon`:
            - Type: str
            - What: The icon to display.
        - `type`:
            - Type: str
            - What: The type of button.
            - Accepted Values:
                - `"session"`
                - `"settings"`
                - `"button"`
                - `"pane"`
                - `"page"`
        - `bar`:
            - Type: str
            - What: The location of the button.
            - Accepted Values:
                - `"upperLeft"`
                - `"lowerLeft"`
                - `"upperRight"`
                - `"lowerRight"`

        Optional Arguments:

        - `variant`:
            - Type: str | None
            - What: The variant of the button.
            - Accepted Values:
                - Type: `"pane"`
                    - `"modal"`
                    - `"wall"`
                - Type: Any Other Type
                    - None
            - Default: `None`
        - `color`:
            - Type: str | None
            - What: The color of the button.
            - Accepted Values:
                - Any valid rgba string.
            - Default: `None` (the system default)
            - Eg: `"rgba(255, 255, 255, 1)"`
        - `apiCommand`:
            - Type: str | None
            - What: The name of the api command to trigger.
            - Default: `None`
            - Note: if `None`, no `apiCommand` is triggered
        - `apiCommandKeys`:
            - Type: list | None
            - What: The top level api keys to pass to your `execute_command` if an apiCommand is provded.
            - Default: `None`
            - Note: If `None` all api keys are passed to your `execute_command`.

        """
        return {
            "kwargs": kwargs,
            "accepted_values": {
                "type": ["session", "settings", "button", "pane", "page"],
                "variant": ["modal", "wall"] if type == "pane" else [],
                "bar": ["upperLeft", "lowerLeft", "upperRight", "lowerRight"],
            },
        }

    def __extend_spec__(self, **kwargs):
        color = self.data.get("color")
        if color:
            self.__check_rgba_string_valid__(rgba_string=color, prepend_path=["color"])
        # Validate pageIds
        bar_type = self.data.get("type")
        if bar_type == 'page':
            self.__check_subset_valid__(
                subset=[kwargs.get('CustomKeyValidatorFieldId')],
                valid_values=kwargs.get("page_validPageIds", []),
                prepend_path=[],
            )
        if bar_type == 'pane':
            self.__check_subset_valid__(
                subset=[kwargs.get('CustomKeyValidatorFieldId')],
                valid_values=kwargs.get("pane_validPaneIds", []),
                prepend_path=[],
            )



@type_enforced.Enforcer
class appBar(ApiValidator):
    """
    ## Api Path: appBar
    """

    @staticmethod
    def spec(data: dict = dict(), **kwargs):
        """
        Optional Arguments:

        - `data`:
            - Type: dict
            - What: The data to pass to `appBar.data.*`.
            - Default: `{}`
        """
        return {"kwargs": kwargs, "accepted_values": {}}

    def __extend_spec__(self, **kwargs):
        data = self.data.get("data", {})
        CustomKeyValidator(
            data=data, log=self.log, prepend_path=["data"], validator=appBar_data_star, **kwargs
        )
