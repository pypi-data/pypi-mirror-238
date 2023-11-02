"""
Build out an app bar with buttons to launch pages, launch maps and trigger api commands.
"""
from cave_utils.api.utils import ApiValidator, CustomKeyValidator
import type_enforced

@type_enforced.Enforcer
class viewport(ApiValidator):
    """
    ## Api Path: maps.data.*.defaultViewport
    ## Api Path: maps.data.*.optionalViewports.*
    """
    @staticmethod
    def spec(latitude: [int, float], longitude: [int, float], zoom: [int, float], bearing: [int, float, None] = None, pitch: [int, float, None] = None, maxZoom: [int, float, None] = None, minZoom: [int, float, None] = None, icon: [str, None] = None, name: [str, None] = None, **kwargs):
        """
        Required Arguments:

        - `latitude`:
            - Type: float | int
            - What: The latitude of the viewport.
            - Note: Between -90 and 90.
        - `longitude`:
            - Type: float | int
            - What: The longitude of the viewport.
            - Note: Between -180 and 180.
        - `zoom`:
            - Type: float | int
            - What: The zoom of the viewport.
            - Note: Between 0 and 22.
        - `bearing`:
            - Type: float | int | None
            - What: The bearing of the viewport.
            - Default: `None`
            - Note: Between 0 and 360.
        - `pitch`:
            - Type: float | int | None
            - What: The pitch of the viewport.
            - Default: `None`
            - Note: Between 0 and 60.
        - `maxZoom`:
            - Type: float | int | None
            - What: The maximum zoom of the viewport.
            - Default: `None`
            - Note: Between 0 and 22.
        - `minZoom`:
            - Type: float | int | None
            - What: The minimum zoom of the viewport.
            - Default: `None`
            - Note: Between 0 and 22.
        - `icon`:
            - Type: str | None
            - What: The icon to use for the viewport.
            - Default: `None`
            - Note: If `None`, the default icon will be used.
            - TODO: Check this
        - `name`:
            - Type: str | None
            - What: The name of the viewport.
            - Note: Only used for optional viewports.

        """
        return {
            "kwargs": kwargs,
            "accepted_values": {},
        }

    def __extend_spec__(self, **kwargs):
        field_validation = {
            "latitude": (-90, 90),
            "longitude": (-180, 180),
            "zoom": (0, 22),
            "bearing": (0, 360),
            "pitch": (0, 60),
            "maxZoom": (0, 22),
            "minZoom": (0, 22),
        }
        if kwargs.get('is_optional_viewport'):
            if self.data.get("name") is None:
                self.__error__(
                    msg="`name` must be specified for optional viewports"
                )
            if self.data.get("icon") is None:
                self.__error__(
                    msg="`icon` must be specified for optional viewports"
                )
        for field in ["latitude", "longitude", "zoom", "bearing", "pitch", "maxZoom", "minZoom"]:
            value = self.data.get(field)
            if value is not None:
                if not isinstance(value, (int, float)):
                    continue
                if value < field_validation[field][0] or value > field_validation[field][1]:
                    self.__error__(
                        msg=f"`{field} = {value}` but it should be between {field_validation[field][0]} and {field_validation[field][1]}"
                    )
                    continue
        # TODO: Validate Icons
        # if self.data.get("icon") is not None:
        #     self.__check_url_valid__(url=self.data.get("icon"), prepend_path=["icon"])

@type_enforced.Enforcer
class colorByOptions(ApiValidator):
    """
    ## Api Path: maps.data.*.legendGroups.*.data.*.colorByOptions
    """
    @staticmethod
    def spec(
        startGradientColor: [str, None] = None,
        endGradientColor: [str, None] = None,
        min: [float, int, None] = None,
        max: [float, int, None] = None,
        nullColor: [str, None] = None,
        **kwargs,
    ):
        """
        Required Arguments:

        - `startGradientColor`:
            - Type: str
            - What: The starting color for the gradient.
            - Accepted Values:
                - Any valid rgba string.
            - Eg: `"rgba(255, 255, 255, 1)"`
            - Note: This is only required for numeric props.
        - `endGradientColor`:
            - Type: str
            - What: The ending color for the gradient.
            - Accepted Values:
                - Any valid rgba string.
            - Eg: `"rgba(255, 255, 255, 1)"`
            - Note: This is only required for numeric props.
        - `customKey`:
            - Type: str
            - What: A color (RGBA String) assigned to a categorical value.
                - Note: You should provide one `customKey` per option key in the associated prop.
            - Note: This is only required for non numeric props.
            - TODO: Flesh this out better

        Optional Arguments:

        - `min`:
            - Type: float | int | None
            - What: The minimum value for calculating the gradient.
            - Default: `None`
            - Note: If None, the min of the relevant data will be used.
        - `max`:
            - Type: float | int | None
            - What: The maximum value for calculating the gradient.
            - Default: `None`
            - Note: If None, the max of the relevant data will be used.
        - `nullColor`:
            - Type: str | None
            - What: The color to use for null values.
            - Default: `None`
            - Note: If None, null values will not be shown
        """

        if startGradientColor is not None or endGradientColor is not None:
            if startGradientColor is None:
                raise Exception("Must provide a `startGradientColor` if `endGradientColor` is provided")
            if endGradientColor is None:
                raise Exception("Must provide a `endGradientColor` if `startGradientColor` is provided")
            return {
                "kwargs": kwargs,
                "accepted_values": {},
            }
        else:
            return {
                "kwargs": {},
                "accepted_values": {},
            }

    def __extend_spec__(self, **kwargs):
        prop_data = kwargs.get('colorBy_availableProps').get(kwargs.get('CustomKeyValidatorFieldId'))
        if prop_data is None:
            return
        prop_type = prop_data.get("type")
        if prop_type == "num":
            for obj_key in ['startGradientColor', 'endGradientColor', 'nullColor']:
                obj_val = self.data.get(obj_key)
                if obj_val is not None:
                    self.__check_rgba_string_valid__(rgba_string=obj_val, prepend_path=[obj_key])
                if obj_key in ['startGradientColor', 'endGradientColor'] and obj_val==None:
                    self.__error__(
                        msg=f"Missing key `{obj_key}`"
                    )
            for obj_key in ['min', 'max']:
                obj_val = self.data.get(obj_key)
                if obj_val is not None:
                    if not isinstance(obj_val, (int, float)):
                        self.__error__(
                            msg=f"Invalid `{obj_key}` ({obj_val}) must be a number"
                        )
                        continue
        elif prop_type == "toggle":
            for key, value in self.data.items():
                if not self.__check_subset_valid__(
                    subset=[key],
                    valid_values=['true', 'false', 'nullColor'],
                    prepend_path=[],
                ):
                    return
                self.__check_rgba_string_valid__(rgba_string=value, prepend_path=[key])
        elif prop_type == "selector":
            for key, value in self.data.items():
                if not self.__check_subset_valid__(
                    subset=[key],
                    valid_values=list(prop_data.get("options").keys()) + ['nullColor'],
                    prepend_path=[],
                ):
                    return
                self.__check_rgba_string_valid__(rgba_string=value, prepend_path=[key])
        else:
            self.__error__(
                msg=f"Invalid prop type ({prop_type}) for colorByOptions"
            )


@type_enforced.Enforcer
class sizeByOptions(ApiValidator):
    @staticmethod
    def spec(
        startSize: [str, None] = None,
        endSize: [str, None] = None,
        min: [float, int, None] = None,
        max: [float, int, None] = None,
        nullSize: [str, None] = None,
        **kwargs,
    ):
        """
        Required Arguments:

        - `startSize`:
            - Type: str
            - What: The starting size for the gradient.
            - Accepted Values:
                - Any valid pixel string.
            - Eg: `"10px"`
            - Note: This is only required for numeric props.
        - `endSize`:
            - Type: str
            - What: The ending size for the gradient.
            - Accepted Values:
                - Any valid pixel string.
            - Eg: `"10px"`
            - Note: This is only required for numeric props.
        - `customKey`:
            - Type: str
            - What: A pixel size (pixel String) assigned to a categorical value.
                - Note: You should provide one `customKey` per option key in the associated prop.
            - Note: This is only required for non numeric props.
            - TODO: Flesh this out better

        Optional Arguments:

        - `min`:
            - Type: float | int | None
            - What: The minimum value for calculating the size.
            - Default: `None`
            - Note: If None, the min of the relevant data will be used.
        - `max`:
            - Type: float | int | None
            - What: The maximum value for calculating the size.
            - Default: `None`
            - Note: If None, the max of the relevant data will be used.
        - `nullSize`:
            - Type: str | None
            - What: The size to use for null values.
            - Default: `None`
            - Note: If None, null values will not be shown

        """
        if startSize is not None or endSize is not None:
            if startSize is None:
                raise Exception("Must provide a `startSize` if `endSize` is provided")
            if endSize is None:
                raise Exception("Must provide a `endSize` if `startSize` is provided")
            return {
                "kwargs": kwargs,
                "accepted_values": {},
            }
        else:
            return {
                "kwargs": {},
                "accepted_values": {},
            }

    def __extend_spec__(self, **kwargs):
        prop_data = kwargs.get('sizeBy_availableProps').get(kwargs.get('CustomKeyValidatorFieldId'))
        if prop_data is None:
            return
        prop_type = prop_data.get("type")
        if prop_type == "num":
            for obj_key in ['startSize', 'endSize', 'nullSize']:
                obj_val = self.data.get(obj_key)
                if obj_val is not None:
                    self.__check_pixel_string_valid__(pixel_string=obj_val, prepend_path=[obj_key])
                if obj_key in ['startSize', 'endSize'] and obj_val==None:
                    self.__error__(
                        msg=f"Missing key `{obj_key}`"
                    )
            for obj_key in ['min', 'max']:
                obj_val = self.data.get(obj_key)
                if obj_val is not None:
                    if not isinstance(obj_val, (int, float)):
                        self.__error__(
                            msg=f"Invalid `{obj_key}` ({obj_val}) must be a number"
                        )
                        continue
        else:
            self.__error__(
                msg=f"Invalid prop type ({prop_type}) for sizeByOptions"
            )


@type_enforced.Enforcer
class maps_data_star_legendGroups_star_data_star(ApiValidator):
    """
    ## Api Path: maps.data.*.legendGroups.*.data.*
    """
    @staticmethod
    def spec(
        value: bool,
        sizeBy: [str, None] = None,
        colorBy: [str, None] = None,
        lineBy: [str, None] = None,
        allowGrouping: bool = False,
        group: [bool, None] = None,
        groupCalcBySize: [str, None] = None,
        groupCalcByColor: [str, None] = None,
        groupScaleWithZoom: bool = False,
        groupScale: [int, float, None] = None,
        colorByOptions: [dict, None] = None,
        sizeByOptions: [dict, None] = None,
        icon: [str, None] = None,
        **kwargs
    ):
        """
        Required Arguments:

        - `value`:
            - Type: bool
            - What: Whether or not to show this data layer on the map.
        
        Optional Arguments:

        - `sizeBy`:
            - Type: str | None
            - What: The prop to use for sizing the data layer.
            - Default: `None`
            - Note: If `None`, the data layer will not be sized.
            - Note: Does not apply to shape layers.
        - `colorBy`:
            - Type: str | None
            - What: The prop to use for coloring the data layer.
            - Default: `None`
            - Note: If `None`, the data layer will not be colored.
        - `lineBy`:
            - Type: str | None
            - What: The type of line to use for the data layer.
            - Accepted Values: `solid`, `dashed`, `dotted`
            - Default: `solid`
            - Note: Only applies to arc layers
        - `allowGrouping`:
            - Type: bool
            - What: Whether or not to allow grouping of the data layer.
            - Default: `False`
            - Note: Only applies to node layers.
        - `group`:
            - Type: bool | None
            - What: Whether or not to group the data layer.
            - TODO: Validate default value
            - Default: `False`
            - Note: If `None`, the data layer will not be grouped.
            - Note: Only applies to node layers.
        - `groupCalcBySize`:
            - Type: str | None
            - What: The prop to use for calculating the size of the group.
            - Default: `sum`
            - Accepted Values: [`sum`, `mean`, `median`, `mode`, `min`, `max`, `count`, `and`, `or`]
            - Note: If `None`, the data layer will not be grouped.
            - Note: Only applies to node layers.
        - `groupCalcByColor`:
            - Type: str | None
            - What: The prop to use for calculating the color of the group.
            - TODO: Validate default value
            - Default: `sum`
            - Accepted Values: [`sum`, `mean`, `median`, `mode`, `min`, `max`, `count`, `and`, `or`]
            - Note: If `None`, the data layer will not be grouped.
            - Note: Only applies to node layers.
        - `groupScaleWithZoom`:
            - Type: bool
            - What: Whether or not to scale the group size with zoom.
            - Default: `False`
            - Note: Only applies to node layers.
            - Note: If `False`, the group size will be constant as set by `groupScale`.
        - `groupScale`:
            - Type: float | int | None
            - What: The zoom level at which to conduct grouping of the nodes.
            - Default: `None`
            - Note: Only applies to node layers.
            - Note: If `None`, the group scale willl be determined by the map zoom.
        - `colorByOptions`:
            - Type: dict | None
            - What: The options for coloring the data layer.
            - Default: `None`
            - Note: If `None`, the data layer will not be colored.
            - Note: Does not apply to shape layers.
            - TODO: Add numeric and categorical example here.
            - See: `cave_utils.api.maps.colorByOptions`
        - `sizeByOptions`:
            - Type: dict | None
            - What: The options for sizing the data layer.
            - Default: `None`
            - Note: If `None`, the data layer will not be sized.
            - Note: Does not apply to shape layers.
            - TODO: Add numeric and categorical example here.
            - See: `cave_utils.api.maps.sizeByOptions`
        - `icon`:
            - Type: str | None
            - What: The icon to use for the data layer.
            - Note: Only applies to node layers.
            - Note: Arc layer icons are determined by `lineBy`.
            - Note: Shape layer icons are always the default icon.
        """
        return {"kwargs": kwargs, "accepted_values": {
            # TODO: Validate these are correct accepted values
            'lineBy': ["solid", "dashed", "dotted"],
            'groupCalcBySize': ["sum", "mean", "median", "mode", "min", "max", 'count', 'and', 'or'],
            'groupCalcByColor': ["sum", "mean", "median", "mode", "min", "max", 'count', 'and', 'or'],
        }}
    
    def __extend_spec__(self, **kwargs):
        mapFeatures_feature_props = kwargs.get("mapFeatures_feature_props", {})
        field_id=kwargs.get("CustomKeyValidatorFieldId")
        if not self.__check_subset_valid__(
            subset=[field_id],
            valid_values=list(mapFeatures_feature_props.keys()),
            prepend_path=[],
        ):
            return
        available_props = mapFeatures_feature_props.get(field_id)
        colorBy_availableProps = {k:v for k,v in available_props.items() if v.get("type") in ["num", 'toggle', 'selector']}
        sizeBy_availableProps = {k:v for k,v in available_props.items() if v.get("type") in ["num"]}

        passed_colorByOptions = self.data.get("colorByOptions", {})
        passed_sizeByOptions = self.data.get("sizeByOptions", {})
        if not self.__check_subset_valid__(
            subset=list(passed_colorByOptions.keys()),
            valid_values=list(colorBy_availableProps.keys()),
            prepend_path=["colorByOptions"],
        ) or not self.__check_subset_valid__(
            subset=list(passed_sizeByOptions.keys()),
            valid_values=list(sizeBy_availableProps.keys()),
            prepend_path=["sizeByOptions"],
        ):
            return
        # to validate that option values are valid
        if passed_colorByOptions is not None:
            CustomKeyValidator(
                data = passed_colorByOptions,
                log = self.log,
                prepend_path = ["colorByOptions"],
                validator = colorByOptions,
                # Custom Key for available props
                colorBy_availableProps = colorBy_availableProps,
                **kwargs
            )
        if passed_sizeByOptions is not None:
            CustomKeyValidator(
                data = passed_sizeByOptions,
                log = self.log,
                prepend_path = ["sizeByOptions"],
                validator = sizeByOptions,
                # Custom Key for available props
                sizeBy_availableProps = sizeBy_availableProps,
                **kwargs
            )
        for by in ["colorBy", "sizeBy"]:
            by_value = self.data.get(by)
            if by_value is not None:
                available_options = list(self.data.get(f"{by}Options", {}).keys())
                if by_value not in available_options:
                    self.__error__(
                        msg=f"Invalid `{by}` ({by_value}) must be one of {available_options}"
                    )
        colorByOptions_keys = list(passed_colorByOptions.keys())
        sizeByOptions_keys = list(passed_sizeByOptions.keys())
        # TODO: Validate Icons


@type_enforced.Enforcer
class maps_data_star_legendGroups_star(ApiValidator):
    """
    ## Api Path: maps.data.*.legendGroups.*
    """
    @staticmethod
    def spec(
        name: str,
        data: dict,
        **kwargs,
    ):
        """
        Required Arguments:

        - `name`:   
            - Type: str
            - What: The name of the legend group. This is displayed in the legend menu.
        - `data`:
            - Type: dict
            - What: The relevant data dict for this legend group.
            - See: `cave_utils.api.maps.maps_data_star_legendGroups_star_data_star`    
        """
        return {"kwargs": kwargs, "accepted_values": {}}

    def __extend_spec__(self, **kwargs):
        CustomKeyValidator(
            data=self.data.get("data", {}),
            log=self.log,
            prepend_path=["data"],
            validator=maps_data_star_legendGroups_star_data_star,
            **kwargs,
        )

@type_enforced.Enforcer
class maps_data_star(ApiValidator):
    """
    ## Api Path: maps.data.*
    """

    @staticmethod
    def spec(
        name: str,
        currentStyle: [str, None] = None,
        currentProjection: [str, None] = None,
        defaultViewport: [dict, None] = None,
        optionalViewports: [dict, None] = None,
        legendGroups: [dict, None] = None,
        **kwargs,
    ):
        """
        Required Arguments:

        - `name`:
            - Type: str
            - What: The name of the map.
        - `currentStyle`:
            - Type: str
            - What: The id of the style to use when the map is first loaded.
            - Default: `None`
        - `currentProjection`:
            - Type: str
            - What: The id of the projection to use when the map is first loaded.
            - Default: `None`
            - Valid Values: `mercator`, `globe`
        - `defaultViewport`:
            - Type: dict
            - What: The default viewport to use.
            - Default: `None`
            - Note: The value of this field should be a `viewport` object.
            - See: `cave_utils.api.maps.viewport`
        - `optionalViewports`:
            - Type: dict
            - What: The optional viewports that can be selected by the end user.
            - Note: The value of this field should be a dict of `viewport` objects.
            - See: `cave_utils.api.maps.viewport`
        - `legendGroups`:
            - Type: dict
            - What: The legend groups to show in the map selection menu.
        """
        return {"kwargs": kwargs, "accepted_values": {
            "currentProjection": ["mercator", "globe"]
        }}

    def __extend_spec__(self, **kwargs):
        # Validate current style
        current_style = self.data.get("currentStyle")
        available_styles = kwargs.get("available_styles", [])
        if current_style is not None and current_style not in available_styles:
            self.__error__(
                msg=f"Invalid `currentStyle` ({current_style}) must be one of {available_styles}"
            )
        # Validate the default viewport
        viewport(
            data=self.data.get("defaultViewport", {}),
            log=self.log,
            prepend_path=["defaultViewport"],
            is_optional_viewport=False,
        )
        # Validate the optional viewports
        CustomKeyValidator(
            data=self.data.get("optionalViewports", {}),
            log=self.log,
            prepend_path=["optionalViewports"],
            validator=viewport,
            is_optional_viewport=True,
        )
        # Validate legend groups
        CustomKeyValidator(
            data=self.data.get("legendGroups", {}),
            log=self.log,
            prepend_path=["legendGroups"],
            validator=maps_data_star_legendGroups_star,
            **kwargs,
        )


@type_enforced.Enforcer
class maps_additionalMapStyles_star(ApiValidator):
    """
    ## Api Path: maps.additionalMapStyles.*
    """

    @staticmethod
    def spec(name: str, icon: str, spec: [dict, str], fog: [dict, None] = None, **kwargs):
        """
        Required Arguments:

        - `name`:
            - Type: str
            - What: The name of the style.
        - `icon`:
            - Type: str
            - What: The icon to show in the map selection menu.
        - `spec`:
            - Type: dict | str
            - What: The spec to generate the map
            - See: Mapbox: https://docs.mapbox.com/api/maps/styles/
            - See: Carto: https://github.com/CartoDB/basemap-styles/blob/master/docs/basemap_styles.json
            - See: Raster: https://docs.mapbox.com/mapbox-gl-js/example/map-tiles/
            - Note: `spec` can be a dict or a string. If it is a string, it will be treated as a url to a json file.
            - Note: `spec` is not validated except that it should be a dict or a string.

        Optional Arguments:

        - `fog`:
            - Type: dict
            - What: The fog to show in the map selection menu.
            - Note: Fog is not validated except that it should be a dict.
            - See: https://docs.mapbox.com/mapbox-gl-js/api/map/#map#setfog
        """
        return {"kwargs": kwargs, "accepted_values": {}}

    def __extend_spec__(self, **kwargs):
        pass
        # TODO: Validate icon
        # TODO: Possibly validate spec and fog


@type_enforced.Enforcer
class maps(ApiValidator):
    """
    ## Api Path: maps
    """

    @staticmethod
    def spec(additionalMapStyles: dict = dict(), data: dict = dict(), **kwargs):
        """
        Optional Arguments:

        - `data`:
            - Type: dict
            - What: The data to pass to `maps.data.*`.
            - Default: `{}`
        """
        return {"kwargs": kwargs, "accepted_values": {}}

    def __extend_spec__(self, **kwargs):
        data = self.data.get("data", {})
        CustomKeyValidator(
            data=self.data.get("additionalMapStyles", {}),
            log=self.log,
            prepend_path=["additionalMapStyles"],
            validator=maps_additionalMapStyles_star,
            **kwargs,
        )
        available_styles = list(self.data.get("additionalMapStyles", {}).keys()) + ["default", "dark", "light"]
        CustomKeyValidator(
            data=data, 
            log=self.log, 
            prepend_path=["data"], 
            validator=maps_data_star,
            available_styles=available_styles,
            **kwargs
        )
