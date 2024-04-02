#  Copyright (C) 2021  Igor Garmaev, garmaev@gmx.net
#
#  This program is made available under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#  without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#  A copy of the GNU General Public License is available at http://www.gnu.org/licenses/
#
#  This program is made available under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#  without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#  A copy of the GNU General Public License is available at http://www.gnu.org/licenses/

import inspect
import re
from abc import ABCMeta
from enum import Enum
from typing import List, Dict, Type, Set

NOT_GIVEN = "NotGivenValueAASEditor"


def nameIsSpecial(method_name):
    """Returns true if the method name starts with underscore"""
    return method_name.startswith('_')


def getAttrs(obj, exclSpecial=True, exclCallable=True) -> List[str]:
    attrs: List[str] = dir(obj)
    if exclSpecial:
        attrs[:] = [attr for attr in attrs if not nameIsSpecial(attr)]
    if exclCallable:
        attrs[:] = [attr for attr in attrs
                    if type(getattr(obj, attr)) in (type, ABCMeta)
                    or not callable(getattr(obj, attr))]
    return attrs


def getDefaultVal(objType: Type, param: str, default=NOT_GIVEN):
    """
    :param objType: type
    :param param: name of argument in __init__ or __new__
    :param default: value to return if nothing found
    :raise AttributeError if no default value found and default is not given
    :return: default value for the given attribute for type init
    """
    params, defaults = getParams4init(objType)
    if params and defaults:
        params = list(params.keys())
        revParams = reversed(params)
        revDefaults = list(reversed(defaults))
        for n, par in enumerate(revParams):
            try:
                if par == param:
                    defValue = revDefaults[n]
                    return defValue
                elif par.rstrip('_') == param:  # TODO change if aas changes
                    defValue = revDefaults[n]
                    return defValue
            except IndexError:
                pass

    if default == NOT_GIVEN:
        raise AttributeError("No such default parameter found:", param)
    else:
        return default


def getParams4init(objType: Type, withDefaults=True):
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


def getDoc(typ: type) -> str:
    return typ.__doc__


def getAttrDoc(attr: str, parentObj: type = None, doc: str = None) -> str:
    """
    Returns doc of specified parameter
    :param attr: parameter of obj init
    :param parentObj: if no doc is given, doc will be extracted from typ
    :param doc: doc of obj init
    :return: doc of specified parameter
    """
    if not doc and parentObj:
        doc = getDoc(parentObj)

    if doc:
        doc = " ".join(doc.split())
        pattern = fr":ivar [~]?[.]?{attr}_?:(.*?)(:ivar|:raises|TODO|$)"
        res = re.search(pattern, doc)
        if res:
            reg = res.regs[1]
            doc = doc[reg[0]: reg[1]]
            doc = re.sub("([(]inherited from.*[)])?", "", doc)
            doc = re.sub("[~]([a-zA-Z]+\.)+", "", doc)
            doc = re.sub("(:class:)?", "", doc)
            doc = re.sub("(<.*>)?", "", doc)
            doc = re.sub("`", "", doc)
            doc = re.sub("[~]\.", "", doc)
            doc = f"{attr}: {doc}"
            return doc
    return ""


def richText(text: str):
    if text:
        return f"<html><head/><body><p>{text}</p></body></html>"
    else:
        return ""


def inheritors(klass) -> set:
    """Return all inheritors of the class"""
    subclasses = set()
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses


