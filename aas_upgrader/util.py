import inspect
from typing import Type

NOT_GIVEN = "NotGivenValueAASEditor"


def get_initialization_parameters(objType: Type, withDefaults=True):
    """Return params for init with their type and default values"""
    if hasattr(objType, "__origin__") and objType.__origin__:
        objType = objType.__origin__

    if hasattr(objType, "_field_types"):
        # for NamedTuple
        params = objType._field_types.copy()
        defaults = objType._field_defaults if hasattr(objType, "_field_defaults") else {}
    elif hasattr(objType, "__init__") or hasattr(objType, "__new__"):
        if hasattr(objType, "__init__"):
            g = inspect.getfullargspec(objType.__init__)
            params = g.annotations.copy()
            defaults = g.defaults
        if not params and hasattr(objType, "__new__"):
            g = inspect.getfullargspec(objType.__new__)
            params = g.annotations.copy()
            defaults = g.defaults
        if g.kwonlydefaults:
            defaults = defaults + tuple(g.kwonlydefaults.values())
    else:
        raise TypeError(f"no init or new func in objectType: {objType}")

    try:
        params.pop('return')
    except KeyError:
        pass

    if withDefaults:
        return params, defaults
    else:
        return params
