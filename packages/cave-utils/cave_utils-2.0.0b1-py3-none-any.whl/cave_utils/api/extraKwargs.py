"""
(Optional) Pass special arguments to the server that are not part of the API spec.
"""
from cave_utils.api.utils import ApiValidator
import type_enforced


@type_enforced.Enforcer
class extraKwargs(ApiValidator):
    """
    ## Api Path: extraKwargs
    """

    @staticmethod
    def spec(wipeExisting: bool = False, **kwargs):
        """
        Optional arguments:

        - `wipeExisting`:
            - Type: bool
            - What: If `True`, the server will delete all existing data before importing the new data. If `False`, the server will merge the new data with the existing data.
                - Note: All data is merged at the top level.
                    - EG: If you update an item in `settings` you should pass the entire `settings` object when you return `session_data`.
            - Default: `False`
        """
        return {
            "kwargs": kwargs,
            "accepted_values": {},
        }
