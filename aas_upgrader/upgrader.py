import abc
from basyx3.basyx.aas import model as model3
from basyx2.basyx.aas import model as model2
from util import getParams4init


NEWCLASS = "newclass"  # new class to use
NEWPARAM_TO_OLDATTR = "newparam_to_oldattr"  # mapping betw. init-params of new object and attrs of old object
#NEWPARAM_VAL = "newparam_val"  # init-params values of new object
NEWPARAM_EVAL = "newparam_eval"  # init-params values of new object as str to be executed in python
VAL_EVAL = "val_eval"  # value of ne object as str to be executed in python
#   - fromV2toV3 - function to modify object from V2 to V3
#   - oldobj - old object of version 2


class AAS_Classes_Upgrader():
    UPGRADERS = {
        model2.base.AdministrativeInformation: {NEWCLASS: model3.base.AdministrativeInformation, },
        model2.base.Reference: {NEWCLASS: model3.base.Reference, },
        model2.base.Qualifier: {
            NEWCLASS: model3.base.Qualifier,
            NEWPARAM_TO_OLDATTR: {"type_": "type"}
        },
        model2.base.Key: {
            NEWCLASS: model3.base.Key,
            NEWPARAM_TO_OLDATTR: {"type_": "type"}
        },
        model2.base.Identifier: {
            NEWCLASS: model3.base.Identifier,
            NEWPARAM_TO_OLDATTR: {"id_": "id"}
        },
        model2.base.AASReference: {
            NEWCLASS: model3.base.AASReference,
            NEWPARAM_TO_OLDATTR: {"target_type": "type"}
        },

        # aas
        model2.aas.AssetAdministrationShell: {
            NEWCLASS: model3.aas.AssetAdministrationShell,
            NEWPARAM_EVAL: {"asset_information": "fromV2toV3(oldobj.asset.resolve(p), p)"},  # TODO: check
        },
        model2.aas.Asset: {
            NEWCLASS: model3.aas.AssetInformation,
            NEWPARAM_TO_OLDATTR: {"asset_kind": "kind"},
            NEWPARAM_EVAL: {
                "global_asset_id": "fromV2toV3(model2.base.AASReference.from_referable(oldobj), p)",
                "default_thumbnail": "None",
            },
            # TODO: check
        },
        # submodel
        model2.submodel.Entity: {
            NEWCLASS: model3.submodel.Entity,
            NEWPARAM_TO_OLDATTR: {"asset_kind": "kind", },
            NEWPARAM_EVAL: {"global_asset_id": "fromV2toV3(model2.base.AASReference.from_referable(oldobj), p)"},
            # TODO: check
        },
        model2.submodel.Submodel: {NEWCLASS: model3.submodel.Submodel, },
        model2.submodel.AnnotatedRelationshipElement: {NEWCLASS: model3.submodel.AnnotatedRelationshipElement},
        model2.submodel.BasicEvent: {NEWCLASS: model3.submodel.BasicEvent},
        model2.submodel.Capability: {NEWCLASS: model3.submodel.Capability},
        model2.submodel.Blob: {NEWCLASS: model3.submodel.Blob},
        model2.submodel.File: {NEWCLASS: model3.submodel.File},
        model2.submodel.MultiLanguageProperty: {NEWCLASS: model3.submodel.MultiLanguageProperty},
        model2.submodel.OperationVariable: {NEWCLASS: model3.submodel.OperationVariable},
        model2.submodel.Operation: {NEWCLASS: model3.submodel.Operation},
        model2.submodel.Property: {NEWCLASS: model3.submodel.Property},
        model2.submodel.Range: {NEWCLASS: model3.submodel.Range},
        model2.submodel.ReferenceElement: {NEWCLASS: model3.submodel.ReferenceElement},
        model2.submodel.RelationshipElement: {NEWCLASS: model3.submodel.RelationshipElement},
        model2.submodel.SubmodelElementCollectionOrdered: {NEWCLASS: model3.submodel.SubmodelElementCollectionOrdered},
        model2.submodel.SubmodelElementCollectionUnordered: {
            NEWCLASS: model3.submodel.SubmodelElementCollectionUnordered},
        # concept
        model2.concept.ConceptDescription: {NEWCLASS: model3.concept.ConceptDescription, }
    }
    COMMON_TYPES = [bool, int, float, str, type(None), bytearray,
                    # datatypes
                    model2.datatypes.Date,
                    model2.datatypes.GYear,
                    model2.datatypes.GMonthDay,
                    model2.datatypes.GDay,
                    model2.datatypes.GMonth,
                    model2.datatypes.Base64Binary,
                    model2.datatypes.HexBinary,
                    model2.datatypes.Float,
                    model2.datatypes.Long,
                    model2.datatypes.Int,
                    model2.datatypes.Short,
                    model2.datatypes.NonPositiveInteger,
                    model2.datatypes.NegativeInteger,
                    model2.datatypes.NonNegativeInteger,
                    model2.datatypes.PositiveInteger,
                    model2.datatypes.UnsignedLong,
                    model2.datatypes.UnsignedInt,
                    model2.datatypes.UnsignedShort,
                    model2.datatypes.Duration,
                    model2.datatypes.DateTime,
                    model2.datatypes.Time,
                    model2.datatypes.UnsignedByte,
                    model2.datatypes.Byte,
                    model2.datatypes.AnyURI,
                    model2.datatypes.NormalizedString,
                    # base
                    model2.base.IdentifierType,
                    model2.base.KeyElements,  # TODO: small check
                    model2.base.KeyType,
                    model2.base.EntityType,
                    model2.base.ModelingKind,
                    model2.base.AssetKind,
                    model2.base.ValueReferencePair,
                    model2.base.Constraint,
                    ]
    COMMON_OBJECTS = [bool, int, float, str, type(None), model2.datatypes.Int]
    NOT_SUPPORTED_TYPES = [model2.aas.View, model2.base.Formula]

    DICT_TYPES = [dict]
    ITERABLE_TYPES = [model2.base.NamespaceSet, model2.base.OrderedNamespaceSet, list, tuple, set]

    PARAMS_TO_IGNORE = ["extension", "specific_asset_id", "parent"]
    COMMON_NEWPARAMS_TO_OLDATTRS = {"display_name": "id_short"}

    @classmethod
    def _upgrade_iterable(cls, oldobj):
        newobj = []
        for i in oldobj:
            try:
                newobj.append(cls.upgrade(i))
            except NotImplementedError:
                continue
        return type(oldobj)(newobj)

    @classmethod
    def _upgrade_dict(cls, oldobj: dict):
        newobj = {}
        for key in oldobj:
            newobj[cls.upgrade(key)] = cls.upgrade(oldobj[key])
        return newobj

    @classmethod
    def _upgrade_from_defined_upgraders(cls, old_obj):
        map_info = cls.UPGRADERS[type(old_obj)]
        newtyp = map_info[NEWCLASS]

        new_param_to_oldattr = cls.COMMON_NEWPARAMS_TO_OLDATTRS.copy()
        new_param_to_oldattr.update(map_info.get(NEWPARAM_TO_OLDATTR, {}))
        new_param_eval = map_info.get(NEWPARAM_EVAL, {})

        kwargs = {}
        newtyp_init_params = list(getParams4init(newtyp, withDefaults=False).keys())
        for param in newtyp_init_params:
            if param in cls.PARAMS_TO_IGNORE:
                continue
            elif param in new_param_eval:
                newobj_param = eval(new_param_eval[param])
            elif param in new_param_to_oldattr:
                oldobj_attr_name = new_param_to_oldattr.get(param)
                oldobj_attr = getattr(old_obj, oldobj_attr_name)
                newobj_param = cls.upgrade(oldobj_attr)
            else:
                oldobj_attr_name = param
                oldobj_attr = getattr(old_obj, oldobj_attr_name)
                if type(oldobj_attr) in [model2.NamespaceSet, model2.OrderedNamespaceSet]:
                    oldobj_attr = [i for i in oldobj_attr]
                newobj_param = cls.upgrade(oldobj_attr)
            kwargs[param] = newobj_param
        newobj = newtyp(**kwargs)
        return newobj

    @classmethod
    def upgrade(cls, old_obj):
        old_obj_typ = type(old_obj)
        if old_obj_typ in cls.NOT_SUPPORTED_TYPES:
            raise NotImplementedError(f"Not supported type for upgrade: {old_obj_typ}")

        if old_obj_typ in cls.COMMON_OBJECTS + cls.COMMON_TYPES:
            obj = old_obj
        elif old_obj_typ in cls.DICT_TYPES:
            obj = cls._upgrade_dict(old_obj)
        elif old_obj_typ in cls.ITERABLE_TYPES:
            obj = cls._upgrade_iterable(old_obj)
        elif (old_obj_typ is type or old_obj_typ is abc.ABCMeta) and old_obj in cls.UPGRADERS:
            obj = cls.UPGRADERS[old_obj][NEWCLASS]
        elif old_obj_typ in cls.UPGRADERS and VAL_EVAL in cls.UPGRADERS[old_obj_typ]:
            obj = eval(cls.UPGRADERS[old_obj_typ][VAL_EVAL])
        elif old_obj_typ in cls.UPGRADERS:
            obj = cls._upgrade_from_defined_upgraders(old_obj)
        else:
            obj = old_obj
        return obj

    @classmethod
    def upgrade_obj_store(cls, obj_store):
        new_obj_store = model3.DictObjectStore()
        for old_obj in obj_store:
            try:
                new_obj = cls.upgrade(old_obj)
                new_obj_store.add(new_obj)
            except NotImplementedError:
                print(f"Upgrade of object {old_obj} failed, as it is not supported. Skipping...")
                continue
        return new_obj_store
