"""
Create grouped outputs for creating generalized charts and tables.
"""
from cave_utils.api.utils import ApiValidator, CustomKeyValidator
from cave_utils.api.general import props, values, layout
import type_enforced


@type_enforced.Enforcer
class groupedOutputs_groupings_star_data_star(ApiValidator):
    """
    ## Api Path: groupedOutputs.groupings.*.data.*
    """
    @staticmethod
    def spec(
        **kwargs
    ):
        """
        Accepts any key value pairs as a dictionary structure for the data.
        Each key must be in `groupedOutputs.groupings.*.levels.*`
        """
        return {"kwargs": {}, "accepted_values": {}}
    
    def __extend_spec__(self, **kwargs):
        self.__check_subset_valid__(
            subset=list(self.data.keys()), valid_values=kwargs.get("acceptable_data_keys", []), prepend_path=[]
        )
        self.__check_type_dict__(data=self.data, types=(str,), prepend_path=[])


@type_enforced.Enforcer
class groupedOutputs_groupings_star_levels_star(ApiValidator):
    """
    ## Api Path: groupedOutputs.groupings.*.levels.*
    """
    @staticmethod
    def spec(
        name:str, parent:[str, None]=None, ordering:[list, None]=None, **kwargs
    ):
        """
        Required Arguments:

        - `name`:
            - Type: str
            - What: The name of the level.

        Optional Arguments:

        - `parent`:
            - Type: str
            - What: The key of the parent level. This is used to create a hierarchy of levels.
            - Note: The parent level key must be defined in `groupedOutputs.groupings.*.levels.*`
            - Note: If none, this will be considered to be the root of the hierarchy.
        """
        # TODO: Figure out new way for ordering
        # - `ordering`:
        #     - Type: list
        #     - What: The ordering of individual values for this level in charts and tables.
        #     - Note: If none, the ordering will be alphabetical.
        #     - Note: If a partial ordering is provided, the provided values will be placed first in order.
        #     - Note: If a partial ordering is provided, the remaining values will be placed in alphabetical order.
        #     - Note: All items in this list must be defined in `groupedOutputs.groupings.*.levels.*.values.*`
        # """
        return {"kwargs": kwargs, "accepted_values": {}}
    
    def __extend_spec__(self, **kwargs):
        parent = self.data.get("parent")
        if parent is not None:
            self.__check_subset_valid__(
                subset=[parent], valid_values=kwargs.get("acceptable_parents", []), prepend_path=["parent"]
            )
        # ordering = self.data.get("ordering")
        # if ordering is not None:
        #     print(ordering, kwargs.get("acceptable_data_keys", []))
        #     self.__check_subset_valid__(
        #         subset=ordering, valid_values=kwargs.get("acceptable_data_keys", []), prepend_path=["ordering"]
        #     )
        

@type_enforced.Enforcer
class groupedOutputs_groupings_star(ApiValidator):
    """
    ## Api Path: groupedOutputs.groupings.*
    """

    @staticmethod
    def spec(
        levels:dict, data:dict, name:str, layoutDirection:str='vertical', grouping:[str,None] = None, **kwargs
    ):
        """
        Required Arguments:

        - `levels`:
            - Type: dict
            - What: A dictionary of levels that are available for the grouping.
            - See: `cave_utils.api.groupedOutputs.groupedOutputs_groupings_star_levels_star`
        - `data`:
            - Type: dict
            - What: The data to be grouped.
            - See: `cave_utils.api.groupedOutputs.groupedOutputs_groupings_star_data_star`
        - `name`:
            - Type: str
            - What: The name of the grouping.
        
        Optional Arguments:
        
        - `layoutDirection`:
            - Type: str
            - What: The direction of the grouping levels in the layout.
            - Default: `None`
            - Accepted Values: ['horizontal', 'vertical']
        - `grouping`:
            - Type: str
            - What: A group that is created to put similar groupings together in the UI dropdowns when selecting groupings.
            - Default: `None`
            - Note: If `grouping` is not provided, the grouping will be placed in the root of the UI dropdowns.

        """
        return {"kwargs": kwargs, "accepted_values": {
            "layoutDirection": ['horizontal', 'vertical']
        }}

    def __extend_spec__(self, **kwargs):
        levels_data = self.data.get("levels", {})
        levels_data_keys = list(levels_data.keys())
        data_data = self.data.get("data", {})
        # data_data_keys = list(data_data.keys())

        CustomKeyValidator(
            data=levels_data,
            log=self.log,
            prepend_path=["levels"],
            validator=groupedOutputs_groupings_star_levels_star,
            acceptable_parents=levels_data_keys,
            # acceptable_data_keys = data_data_keys,
            **kwargs,
        )

        CustomKeyValidator(
            data=data_data,
            log=self.log,
            prepend_path=["data"],
            validator=groupedOutputs_groupings_star_data_star,
            acceptable_data_keys=levels_data_keys,
            **kwargs,
        )


@type_enforced.Enforcer
class groupedOutputs_data_star_stats(ApiValidator):
    """
    ## Api Path: groupedOutputs.data.*.stats
    """
    @staticmethod
    def spec(
        name:str,
        calculation: str,
        unit: [str, None] = None,
        unitPlacement: str = 'after',
        precision: [int, None] = None,
        trailingZeros: bool = False,
        **kwargs
    ):
        """
        Required Arguments:

        - `name`:
            - Type: str
            - What: The name of the stat.
        - `calculation`:
            - Type: str
            - What: The calculation to generate the stat for each group.
            - Note: This can use operators [`+`, `-`, `*`, `/`, and `groupSum`].
            - Note: This can call in keys from `groupedOutputs.data.*.valueLists.*` as variables.
            - EG: Create a variable that can be used to aggregate on your stat demand on arbitrary groupings
                - `'demand'`
            - EG: Create a variable that can be used to aggregate your percent of demand met on arbitrary groupings
                - `'sales / groupSum("demand")'`
                - Note: This only shows the percent of demand met for each group if they are summed in the chart.
        - `unit`:
            - Type: str
            - What: The unit of the stat.
            - Default: `None`
        - `unitPlacement`:
            - Type: str
            - What: Where the unit should be placed.
            - Default: `'after'`
            - Accepted Values: ['before', 'after']
        - `precision`:
            - Type: int
            - What: The number of decimal places to show.
            - Default: `None` (the amount calculated by the calculation)
        - `trailingZeros`:
            - Type: bool
            - What: Whether or not to show trailing zeros.
            - Default: `False`
        """
        return {"kwargs": kwargs, "accepted_values": {
            # TODO: Validate unitPlacement options
            "unitPlacement": ['before', 'after']
        }}


@type_enforced.Enforcer
class groupedOutputs_data_star_valueLists(ApiValidator):
    """
    ## Api Path: groupedOutputs.data.*.valueLists
    """
    @staticmethod
    def spec(
        **kwargs
    ):
        """
        Accepts any key value pairs as a dictionary structure for the data.
        Each value must be a list of integers or floats.
        """
        return {"kwargs": {}, "accepted_values": {}}
    
    def __extend_spec__(self, **kwargs):
        for key, value in self.data.items():
            self.__check_type_list__(data=value, types=(int, float), prepend_path=[key])


@type_enforced.Enforcer
class groupedOutputs_data_star(ApiValidator):
    """
    ## Api Path: groupedOutputs.data.*
    """

    @staticmethod
    def spec(
        stats:dict, valueLists:dict, groupLists:dict, **kwargs
    ):
        """
        Required Arguments:

        - `stats`:
            - Type: dict
            - What: A dictionary of stats that are available for the data.
            - See: `cave_utils.api.groupedOutputs.groupedOutputs_data_star_stats`
        - `valueLists`:
            - Type: dict
            - What: A dictionary of lists that make up the stats for the data.
            - TODO: Flesh out this description
        - `groupLists`:
            - Type: dict
            - What: A dictionary of lists that make up the groupings for the data.
            - TODO: Flesh out this description
        """
        return {"kwargs": kwargs, "accepted_values": {}}

    def __extend_spec__(self, **kwargs):
        stats_data = self.data.get("stats", {})
        CustomKeyValidator(
            data=stats_data,
            log=self.log,
            prepend_path=["stats"],
            validator=groupedOutputs_data_star_stats,
            **kwargs,
        )
        list_lengths = []
        pass_list_lengths = True
        # Ensure Valid Value Lists
        valueLists_data = self.data.get("valueLists", {})
        for key, value in valueLists_data.items():
            if not self.__check_type__(value=value, check_type=(list,), prepend_path=["valueLists", key]):
                pass_list_lengths = False
                continue
            list_lengths.append(len(value))
            self.__check_type_list__(data=value, types=(int, float), prepend_path=["valueLists", key])
        # Ensure Valid Group Lists
        available_groups = kwargs.get("available_groups", {}) 
        groupLists_data = self.data.get("groupLists", {})
        self.__check_subset_valid__(
            subset=list(groupLists_data.keys()), valid_values=list(available_groups.keys()) , prepend_path=["groupLists"]
        )
        for key, value in groupLists_data.items():
            if not self.__check_type__(value=value, check_type=(list,), prepend_path=["groupLists", key]):
                pass_list_lengths = False
                continue
            list_lengths.append(len(value))
            valid_values = available_groups.get(key, [])
            if not self.__check_type_list__(data=valid_values, types=(str,), prepend_path=["groupLists", key]):
                continue
            self.__check_subset_valid__(
                subset=value, valid_values=valid_values, prepend_path=["groupLists", key]
            )
        # Ensure all lists are the same length
        if not pass_list_lengths or len(set(list_lengths)) != 1:

            self.__error__(
                msg="All values in groupedOutputs.data.*.groupLists and groupedOutputs.data.*.valueLists must be lists of the same length.",
            )
        

@type_enforced.Enforcer
class groupedOutputs(ApiValidator):
    """
    ## Api Path: groupedOutputs
    """

    @staticmethod
    def spec(
        groupings:dict, data:dict, **kwargs
    ):
        """
        Required Arguments:

        - `groupings`:
            - Type: dict
            - What: A dictionary of groupings that are available for the data.
            - See: `groupedOutputs.groupings`
        - `data`:
            - Type: dict
            - What: The data to be grouped.
            - See: `groupedOutputs.data`

        """
        return {"kwargs": kwargs, "accepted_values": {}}

    def __extend_spec__(self, **kwargs):
        groupedOutputs_groupings = self.data.get("groupings", {})
        CustomKeyValidator(
            data=groupedOutputs_groupings,
            log=self.log,
            prepend_path=["groupings"],
            validator=groupedOutputs_groupings_star,
            **kwargs,
        )
        groupedOutputs_data = self.data.get("data", {})
        CustomKeyValidator(
            data=groupedOutputs_data,
            log=self.log,
            prepend_path=["data"],
            validator=groupedOutputs_data_star,
            available_groups={k:list(v.get('data',{}).keys()) for k,v in groupedOutputs_groupings.items()},
            **kwargs,
        )