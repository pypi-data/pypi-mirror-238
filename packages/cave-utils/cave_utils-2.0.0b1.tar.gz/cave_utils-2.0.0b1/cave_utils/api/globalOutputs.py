"""
Create global outputs for that allow for simple charts and tables. 
These outputs should be general to the entire application and can be compared across sessions.
"""
from cave_utils.api.utils import ApiValidator, CustomKeyValidator
from cave_utils.api.general import props, values, layout
import type_enforced


@type_enforced.Enforcer
class globalOutputs(ApiValidator):
    """
    ## Api Path: globalOutputs
    """

    @staticmethod
    def spec(
        props: dict, values: [dict, None] = None, layout: [dict, None] = None, **kwargs
    ):
        """
        Required Arguments:

        - `props`:
            - Type: dict
            - What: The props that will be rendered as global outputs.
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