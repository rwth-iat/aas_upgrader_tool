import abc
from basyx.aas import model as model3
from basyx2.aas import model as model2
from aas_upgrader.util import get_initialization_parameters

NEWCLASS = "newclass"  # new class to use
NEWPARAM_TO_OLDATTR = "newparam_to_oldattr"  # mapping betw. init-params of new object and attrs of old object
IGNORE_PARAMS = "ignore_params"  # params to ignore
# NEWPARAM_VAL = "newparam_val"  # init-params values of new object
NEWPARAM_EVAL = "newparam_eval"  # init-params values of new object as str to be executed in python
VAL_EVAL = "val_eval"  # value of ne object as str to be executed in python


#   - fromV2toV3 - function to modify object from V2 to V3
#   - old_obj - old object of version 2


class AAS_Classes_Upgrader:
    COMMON_OBJECTS = [bool, int, float, str, type(None), model2.datatypes.Int]
    UPGRADER_RULES = {
        model2.base.AdministrativeInformation: {
            NEWCLASS: model3.base.AdministrativeInformation,
            IGNORE_PARAMS: ["creator", "template_id"],
        },
        model2.base.Qualifier: {
            NEWCLASS: model3.base.Qualifier,
            NEWPARAM_TO_OLDATTR: {"type_": "type"},
            IGNORE_PARAMS: ["kind"],
        },
        model2.base.KeyElements: {
            VAL_EVAL: "model3.base.KeyTypes(old_obj.value)"
        },
        model2.base.Key: {
            NEWCLASS: model3.base.Key,
            NEWPARAM_TO_OLDATTR: {"type_": "type"}
        },
        model2.base.Identifier: {
            VAL_EVAL: "old_obj.id"
        },
        model2.base.Reference: {
            VAL_EVAL: "cls._upgrade_reference(old_obj)"
        },
        model2.base.AASReference: {
            VAL_EVAL: "cls._upgrade_reference(old_obj)"
        },
        # model2.base.Reference: {
        #     NEWCLASS: model3.base.ExternalReference,
        #     IGNORE_PARAMS: ["referred_semantic_id"],
        #     NEWPARAM_EVAL: {
        #         "key": "AAS_Classes_Upgrader.upgrade(old_obj.key))",
        #     },
        # },
        # model2.base.AASReference: {
        #     NEWCLASS: model3.base.ModelReference,
        #     IGNORE_PARAMS: ["referred_semantic_id"],
        #     NEWPARAM_TO_OLDATTR: {"type_": "type"}
        # },

        model2.base.NamespaceSet: {
            VAL_EVAL: "cls._upgrade_iterable([i for i in old_obj])",
        },
        model2.base.OrderedNamespaceSet: {
            VAL_EVAL: "cls._upgrade_iterable([i for i in old_obj])",
        },

        # aas
        model2.aas.AssetAdministrationShell: {
            NEWCLASS: model3.aas.AssetAdministrationShell,
            NEWPARAM_EVAL: {
                "asset_information": "AAS_Classes_Upgrader.upgrade(old_obj.asset.resolve(cls.provider))",
                "id_": "old_obj.identification.id",
            },
        },
        model2.aas.Asset: {
            NEWCLASS: model3.aas.AssetInformation,
            NEWPARAM_TO_OLDATTR: {"asset_kind": "kind"},
            NEWPARAM_EVAL: {
                "global_asset_id": "model2.base.AASReference.from_referable(old_obj).get_identifier().id",
                "default_thumbnail": "None",
            },
            IGNORE_PARAMS: ["specific_asset_id", "asset_type"],
        },
        # submodel
        model2.submodel.Entity: {
            NEWCLASS: model3.submodel.Entity,
            NEWPARAM_TO_OLDATTR: {"asset_kind": "kind", },
            NEWPARAM_EVAL: {"global_asset_id": "model2.base.AASReference.from_referable(old_obj).get_identifier().id"},
            IGNORE_PARAMS: ["specific_asset_id"],
        },
        model2.submodel.Submodel: {
            NEWCLASS: model3.submodel.Submodel,
            NEWPARAM_TO_OLDATTR: {"id_": "identification", },
        },
        model2.submodel.AnnotatedRelationshipElement: {NEWCLASS: model3.submodel.AnnotatedRelationshipElement},
        # model2.submodel.BasicEvent: {NEWCLASS: model3.submodel.BasicEventElement},
        model2.submodel.Capability: {NEWCLASS: model3.submodel.Capability},
        model2.submodel.Blob: {
            NEWCLASS: model3.submodel.Blob,
            NEWPARAM_TO_OLDATTR: {"content_type": "mime_type"},
        },
        model2.submodel.File: {
            NEWCLASS: model3.submodel.File,
            NEWPARAM_TO_OLDATTR: {"content_type": "mime_type"},
        },
        model2.submodel.MultiLanguageProperty: {NEWCLASS: model3.submodel.MultiLanguageProperty},
        model2.submodel.OperationVariable: {
            VAL_EVAL: "AAS_Classes_Upgrader.upgrade(old_obj.value)" # Upgrade SubmodelElement saved in OperationVariable
        },
        model2.submodel.Operation: {NEWCLASS: model3.submodel.Operation},
        model2.submodel.Property: {NEWCLASS: model3.submodel.Property},
        model2.submodel.Range: {NEWCLASS: model3.submodel.Range},
        model2.submodel.ReferenceElement: {NEWCLASS: model3.submodel.ReferenceElement},
        model2.submodel.RelationshipElement: {NEWCLASS: model3.submodel.RelationshipElement},
        model2.submodel.SubmodelElementCollectionOrdered: {NEWCLASS: model3.submodel.SubmodelElementCollection},
        model2.submodel.SubmodelElementCollectionUnordered: {NEWCLASS: model3.submodel.SubmodelElementCollection},
        # concept
        model2.concept.ConceptDescription: {
            NEWCLASS: model3.concept.ConceptDescription,
            NEWPARAM_TO_OLDATTR: {"id_": "identification"},
        }
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
                    model2.base.Constraint,
                    model2.base.ValueReferencePair,
                    # enums
                    model2.base.IdentifierType,
                    model2.base.KeyType,
                    model2.base.EntityType,
                    model2.base.ModelingKind,
                    model2.base.AssetKind,
                    ]
    NOT_SUPPORTED_TYPES = [model2.aas.View, model2.base.Formula, model2.submodel.BasicEvent]

    DICT_TYPES = [dict]
    ITERABLE_TYPES = [list, tuple, set]

    PARAMS_TO_IGNORE = ["embedded_data_specifications", "supplemental_semantic_id", "extension", "parent"]
    COMMON_NEWPARAMS_TO_OLDATTRS = {"display_name": "id_short"}

    @classmethod
    def _upgrade_reference(cls, old_obj):
        if type(old_obj) is model2.base.AASReference:
            new_key = cls.upgrade(old_obj.key)
            return model3.base.ModelReference(key=new_key, type_=old_obj.type)
        if type(old_obj) is model2.base.Reference:
            new_key = list(cls.upgrade(old_obj.key))
            new_key[0] = model3.base.Key(model3.base.KeyTypes.GLOBAL_REFERENCE, new_key[0].value)
            return model3.base.ExternalReference(key=tuple(new_key))

    @classmethod
    def _upgrade_iterable(cls, old_iterable):
        upgraded_items = []
        for i in old_iterable:
            try:
                upgraded_items.append(cls.upgrade(i))
            except NotImplementedError:
                continue
        return type(old_iterable)(upgraded_items)

    @classmethod
    def _upgrade_dict(cls, old_dict: dict):
        upgraded_dict = {}
        for key, value in old_dict.items():
            try:
                key = cls.upgrade(key)
                value = cls.upgrade(value)
                upgraded_dict[key] = value
            except NotImplementedError:
                continue
        return upgraded_dict

    @classmethod
    def _upgrade_from_defined_rules(cls, old_obj):
        rule = cls.UPGRADER_RULES[type(old_obj)]

        new_class = rule[NEWCLASS]

        init_params = list(get_initialization_parameters(new_class, withDefaults=False).keys())
        init_params = [param for param in init_params if param not in cls.PARAMS_TO_IGNORE]
        init_params = [param for param in init_params if param not in rule.get(IGNORE_PARAMS, [])]

        rule_param_to_oldattr = cls.COMMON_NEWPARAMS_TO_OLDATTRS.copy()
        rule_param_to_oldattr.update(rule.get(NEWPARAM_TO_OLDATTR, {}))
        param_eval = rule.get(NEWPARAM_EVAL, {})

        kwargs = {}
        for param in init_params:
            if param in rule.get(NEWPARAM_EVAL, {}):
                newobj_param = eval(param_eval[param])
            else:
                old_obj_attr_name = rule_param_to_oldattr.get(param, param)
                old_obj_attr = getattr(old_obj, old_obj_attr_name)
                newobj_param = cls.upgrade(old_obj_attr)
            kwargs[param] = newobj_param
        newobj = new_class(**kwargs)
        return newobj

    @classmethod
    def obj_is_aas_type(cls, obj):
        if (type(obj) is type or type(obj) is abc.ABCMeta) and obj in cls.UPGRADER_RULES:
            return True
        return False

    @classmethod
    def upgrade(cls, old_obj):
        old_obj_typ = type(old_obj)
        if old_obj_typ in cls.NOT_SUPPORTED_TYPES:
            raise NotImplementedError(f"Not supported type for upgrade: {old_obj_typ}")

        if old_obj in cls.COMMON_OBJECTS:
            upgraded_obj = old_obj
        elif old_obj_typ in cls.COMMON_TYPES:
            upgraded_obj = old_obj
        elif old_obj_typ in cls.DICT_TYPES:
            upgraded_obj = cls._upgrade_dict(old_obj)
        elif old_obj_typ in cls.ITERABLE_TYPES:
            upgraded_obj = cls._upgrade_iterable(old_obj)
        elif cls.obj_is_aas_type(old_obj):
            upgraded_obj = cls.UPGRADER_RULES.get(old_obj).get(NEWCLASS)
        elif old_obj_typ in cls.UPGRADER_RULES and VAL_EVAL in cls.UPGRADER_RULES[old_obj_typ]:
            upgraded_obj = eval(cls.UPGRADER_RULES[old_obj_typ][VAL_EVAL])
        elif old_obj_typ in cls.UPGRADER_RULES:
            upgraded_obj = cls._upgrade_from_defined_rules(old_obj)
        else:
            raise NotImplementedError(f"Upgrade of object {old_obj} failed, as it is not supported.")
            upgraded_obj = old_obj
        return upgraded_obj

    @classmethod
    def upgrade_obj_store(cls, obj_store):
        cls.provider = obj_store
        new_obj_store = model3.DictObjectStore()
        for old_obj in obj_store:
            if isinstance(old_obj, model2.aas.Asset):
                continue
            new_obj = cls.upgrade(old_obj)
            new_obj_store.add(new_obj)
        return new_obj_store
