"""
Build out an app bar with buttons to launch pages, launch panes and trigger api commands.
"""
from cave_utils.api.utils import ApiValidator, CustomKeyValidator
from cave_utils.api.general import props, values, layout
import type_enforced


@type_enforced.Enforcer
class panes_data_star(ApiValidator):
    """
    ## Api Path: panes.data.*
    """

    @staticmethod
    def spec(
        name: str, props: dict, values: [dict, None] = None, layout: [dict, None] = None, **kwargs
    ):
        """
        Required Arguments:

        - `name`:
            - Type: str
            - What: The name of the pane.
        - `props`:
            - Type: dict
            - What: The props that will be rendered in the pane.
            - See: `cave_utils.api.general.props`
        - `values`:
            - Type: dict
            - What: The values that will be passed to the props.
            - Required: False
            - See: `cave_utils.api.general.values`

        Optional Arguments:

        - `layout`:
            - Type: dict
            - What: The layout of the pane.
            - Required: False
            - See: `cave_utils.api.general.layout`
        """
        return {"kwargs": kwargs, "accepted_values": {}}

    def __extend_spec__(self, **kwargs):
        # Validate Props
        props_data = self.data.get("props", {})
        CustomKeyValidator(
            data=props_data,
            log=self.log,
            prepend_path=["props"],
            validator=props,
            **kwargs,
        )
        values(
            data=self.data.get("values", {}),
            log=self.log,
            prepend_path=["values"],
            props_data=props_data,
            **kwargs,
        )
        layout_data = self.data.get("layout")
        if layout_data is not None:
            layout(
                data=layout_data,
                log=self.log,
                prepend_path=["layout"],
                prop_id_list=list(props_data.keys()),
                **kwargs,
            )


@type_enforced.Enforcer
class panes_paneState_star(ApiValidator):
    """
    ## Api Path: panes.paneState.*
    """

    @staticmethod
    def spec(
        type: str = 'pane', open: [str, None] = None, pin: bool = False, **kwargs
    ):
        """
        Required Arguments:

        - `type`:
            - Type: str
            - What: The type of item to render.
            - Default: `pane`
            # TODO: There are other valid values such that we can display map modals
            - Valid Values: `pane`
        - `open`:
            - Type: str
            - What: The id of the open pane.
            - Note: This id has to match the id of a pane in `panes.data` if type is `pane`.
        - `pin`:
            - Type: bool
            - What: Whether or not the pane is pinned.
            - Required: False
            - Default: `False`
        """
        return {"kwargs": kwargs, "accepted_values": {
            # TODO: Add type for map modal
            "type":['pane'],
        }}

    def __extend_spec__(self, **kwargs):
        if self.data.get("type", "pane") == "pane":
            self.__check_subset_valid__(
                subset=[self.data.get("open")],
                valid_values=kwargs.get("pane_keys"),
                prepend_path=["open"],
            )
        # TODO: Validate map modal/panes



@type_enforced.Enforcer
class panes(ApiValidator):
    """
    ## Api Path: panes
    """

    @staticmethod
    def spec(data: dict = dict(), paneState: dict = dict(), **kwargs):
        """
        Optional Arguments:

        - `data`:
            - Type: dict
            - What: The data to pass to `panes.data.*`.
            - Default: `{}`
        - `paneState`:
            - Type: dict
            - What: The state of the pane.
            - Default: `{}`
        """
        return {"kwargs": kwargs, "accepted_values": {
            "paneState":['left','center','right']
        }}

    def __extend_spec__(self, **kwargs):
        data = self.data.get("data", {})
        CustomKeyValidator(
            data=data, log=self.log, prepend_path=["data"], validator=panes_data_star, **kwargs
        )
        pane_keys = list(data.keys())
        paneState = self.data.get("paneState", {})
        CustomKeyValidator(
            data=paneState,
            log=self.log,
            prepend_path=["paneState"],
            validator=panes_paneState_star,
            pane_keys=pane_keys,
            **kwargs,
        )
