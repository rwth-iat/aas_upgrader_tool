import abc
from basyx.aas import model as model3
from basyx2.aas import model as model2
from aas_upgrader.util import get_initialization_parameters

NEWCLASS = "newclass"  # new class to use
NEWPARAM_TO_OLDATTR = "newparam_to_oldattr"  # Mapping between new parameters and old attributes
IGNORE_PARAMS = "ignore_params"  # Parameters to exclude from initialization
# NEWPARAM_VAL = "newparam_val"  # init-params values of new object
NEWPARAM_EVAL = "newparam_eval"  # Expressions for evaluating new parameters (str to be executed in python)
VAL_EVAL = "val_eval"  # Expression for evaluating the value of a new object (str to be executed in python)


class AAS_Classes_Upgrader:
    not_supported_types_for_upgrade = [model2.aas.View, model2.base.Formula, model2.submodel.BasicEvent]
    type_mappings = {
        bool: bool,
        int: int,
        float: float,
        str: str,
        type(None): type(None),
        bytearray:bytearray,
        model2.datatypes.GYear: model3.datatypes.GYear,
        model2.datatypes.GMonthDay: model3.datatypes.GMonthDay,
        model2.datatypes.GDay: model3.datatypes.GDay,
        model2.datatypes.GMonth: model3.datatypes.GMonth,
        model2.datatypes.Long: model3.datatypes.Long,
        model2.datatypes.Int: model3.datatypes.Int,
        model2.datatypes.Short: model3.datatypes.Short,
        model2.datatypes.NonPositiveInteger: model3.datatypes.NonPositiveInteger,
        model2.datatypes.NegativeInteger: model3.datatypes.NegativeInteger,
        model2.datatypes.NonNegativeInteger: model3.datatypes.NonNegativeInteger,
        model2.datatypes.PositiveInteger: model3.datatypes.PositiveInteger,
        model2.datatypes.UnsignedLong: model3.datatypes.UnsignedLong,
        model2.datatypes.UnsignedInt: model3.datatypes.UnsignedInt,
        model2.datatypes.UnsignedShort: model3.datatypes.UnsignedShort,
        model2.datatypes.UnsignedByte: model3.datatypes.UnsignedByte,
        model2.datatypes.Byte: model3.datatypes.Byte,
        model2.datatypes.AnyURI: model3.datatypes.AnyURI,
        model2.datatypes.NormalizedString: model3.datatypes.NormalizedString,
    }
    types_requiring_no_upgrade = [bool, int, float, str, type(None), bytearray, bytes,
                                  # datatypes
                                  model2.datatypes.Base64Binary,
                                  model2.datatypes.HexBinary,
                                  model2.datatypes.Float,
                                  model2.datatypes.Duration,
                                  model2.datatypes.DateTime,
                                  model2.datatypes.Time,
                                  # base
                                  model2.base.ValueReferencePair,
                                  # enums
                                  ]
    common_ignored_params = ["display_name", "embedded_data_specifications", "supplemental_semantic_id", "extension",
                               "parent"]
    common_new_params_to_old_attributes = {}
    common_evals_for_new_params = {"description": "model3.base.MultiLanguageTextType(old_obj.description)"}
    upgrade_rules = {
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
            VAL_EVAL: "self._upgrade_reference(old_obj)"
        },
        model2.base.AASReference: {
            VAL_EVAL: "self._upgrade_reference(old_obj)"
        },
        model2.base.NamespaceSet: {
            VAL_EVAL: "self._upgrade_iterable([i for i in old_obj])",
        },
        model2.base.OrderedNamespaceSet: {
            VAL_EVAL: "self._upgrade_iterable([i for i in old_obj])",
        },

        # aas
        model2.aas.AssetAdministrationShell: {
            NEWCLASS: model3.aas.AssetAdministrationShell,
            NEWPARAM_EVAL: {
                "asset_information": "self.upgrade(old_obj.asset.resolve(self.provider))",
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
            NEWPARAM_EVAL: {
                "global_asset_id": "model2.base.AASReference.from_referable(old_obj).get_identifier().id if old_obj.entity_type.value == 1 else None"},
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
        model2.submodel.MultiLanguageProperty: {
            NEWCLASS: model3.submodel.MultiLanguageProperty,
            NEWPARAM_EVAL: {"value": "model3.base.MultiLanguageTextType(old_obj.value)"}
        },
        model2.submodel.OperationVariable: {
            VAL_EVAL: "self.upgrade(old_obj.value)"
            # Upgrade SubmodelElement saved in OperationVariable
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
        },
        model2.base.EntityType: {VAL_EVAL: "model3.base.EntityType(old_obj.value)"},
        model2.base.ModelingKind: {VAL_EVAL: "model3.base.ModellingKind(old_obj.value)"},
        model2.base.AssetKind: {VAL_EVAL: "model3.base.AssetKind(old_obj.value)"},
        model2.datatypes.GYear: {NEWCLASS: model3.datatypes.GYear},
        model2.datatypes.GMonthDay: {NEWCLASS: model3.datatypes.GMonthDay},
        model2.datatypes.GDay: {NEWCLASS: model3.datatypes.GDay},
        model2.datatypes.GMonth: {NEWCLASS: model3.datatypes.GMonth},
        model2.datatypes.Long: {VAL_EVAL: "model3.datatypes.Long(old_obj)"},
        model2.datatypes.Int: {VAL_EVAL: "model3.datatypes.Int(old_obj)"},
        model2.datatypes.Short: {VAL_EVAL: "model3.datatypes.Short(old_obj)"},
        model2.datatypes.NonPositiveInteger: {VAL_EVAL: "model3.datatypes.NonPositiveInteger(old_obj)"},
        model2.datatypes.NegativeInteger: {VAL_EVAL: "model3.datatypes.NegativeInteger(old_obj)"},
        model2.datatypes.NonNegativeInteger: {VAL_EVAL: "model3.datatypes.NonNegativeInteger(old_obj)"},
        model2.datatypes.PositiveInteger: {VAL_EVAL: "model3.datatypes.PositiveInteger(old_obj)"},
        model2.datatypes.UnsignedLong: {VAL_EVAL: "model3.datatypes.UnsignedLong(old_obj)"},
        model2.datatypes.UnsignedInt: {VAL_EVAL: "model3.datatypes.UnsignedInt(old_obj)"},
        model2.datatypes.UnsignedShort: {VAL_EVAL: "model3.datatypes.UnsignedShort(old_obj)"},
        model2.datatypes.UnsignedByte: {VAL_EVAL: "model3.datatypes.UnsignedByte(old_obj)"},
        model2.datatypes.Byte: {VAL_EVAL: "model3.datatypes.Byte(old_obj)"},
        model2.datatypes.AnyURI: {VAL_EVAL: "model3.datatypes.AnyURI(old_obj)"},
        model2.datatypes.NormalizedString: {VAL_EVAL: "model3.datatypes.NormalizedString(old_obj)"},
    }

    dict_types = [dict]
    iterable_types = [list, tuple, set]

    def __init__(self, provider=None):
        self.provider = provider

    def _upgrade_reference(self, old_obj):
        if type(old_obj) is model2.base.AASReference:
            new_key = self.upgrade(old_obj.key)
            return model3.base.ModelReference(key=new_key, type_=old_obj.type)
        if type(old_obj) is model2.base.Reference:
            new_key = list(self.upgrade(old_obj.key))
            new_key[0] = model3.base.Key(model3.base.KeyTypes.GLOBAL_REFERENCE, new_key[0].value)
            return model3.base.ExternalReference(key=tuple(new_key))

    def _upgrade_iterable(self, old_iterable):
        upgraded_items = []
        for i in old_iterable:
            try:
                upgraded_items.append(self.upgrade(i))
            except NotImplementedError as e:
                print(e, f"Upgrade of object {i} failed, as it is not supported.")
                continue
        return type(old_iterable)(upgraded_items)

    def _upgrade_dict(self, old_dict: dict):
        upgraded_dict = {}
        for key, value in old_dict.items():
            try:
                upgraded_key = self.upgrade(key)
            except NotImplementedError as e:
                print(e, f"Upgrade of object {key} of type {type(key)} failed, as it is not supported.")
                continue
            try:
                upgraded_value = self.upgrade(value)
            except NotImplementedError as e:
                print(e, f"Upgrade of object {value} of type {type(value)} failed, as it is not supported.")
                continue
            upgraded_dict[upgraded_key] = upgraded_value
        return upgraded_dict

    def _upgrade_from_defined_rules(self, old_obj):
        old_obj_type = type(old_obj)
        rule = self.upgrade_rules[old_obj_type]

        if VAL_EVAL in rule:
            upgraded_obj = eval(rule[VAL_EVAL])
            return upgraded_obj

        new_class = rule[NEWCLASS]

        init_params = list(get_initialization_parameters(new_class, withDefaults=False).keys())
        init_params = [param for param in init_params if param not in self.common_ignored_params]
        init_params = [param for param in init_params if param not in rule.get(IGNORE_PARAMS, [])]

        rule_param_to_oldattr = self.common_new_params_to_old_attributes.copy()
        rule_param_to_oldattr.update(rule.get(NEWPARAM_TO_OLDATTR, {}))

        rule_param_eval = self.common_evals_for_new_params.copy()
        rule_param_eval.update(rule.get(NEWPARAM_EVAL, {}))

        kwargs = {}
        for param in init_params:
            if param in rule_param_eval:
                upgraded_param = eval(rule_param_eval[param])
            else:
                old_obj_attr_name = rule_param_to_oldattr.get(param, param)
                old_obj_attr = getattr(old_obj, old_obj_attr_name)
                upgraded_param = self.upgrade(old_obj_attr)
            kwargs[param] = upgraded_param
        upgraded_obj = new_class(**kwargs)
        return upgraded_obj

    def is_type(self, obj):
        return type(obj) is type or type(obj) is abc.ABCMeta

    def upgrade_type(self, old_obj):
        if old_obj in tuple(self.type_mappings.keys()):
            upgraded_obj = self.type_mappings[old_obj]
        elif old_obj in self.upgrade_rules:
            upgraded_obj = self.upgrade_rules.get(old_obj).get(NEWCLASS)
        else:
            raise NotImplementedError(f"Upgrade of object {old_obj} failed, as it is not supported.")
        return upgraded_obj

    def upgrade(self, old_obj):
        old_obj_typ = type(old_obj)
        if old_obj_typ in self.not_supported_types_for_upgrade:
            raise NotImplementedError(f"Not supported type for upgrade: {old_obj_typ}")

        if self.is_type(old_obj):
            upgraded_obj = self.upgrade_type(old_obj)
        elif old_obj_typ in self.types_requiring_no_upgrade:
            upgraded_obj = old_obj
        elif old_obj_typ in self.dict_types:
            upgraded_obj = self._upgrade_dict(old_obj)
        elif old_obj_typ in self.iterable_types:
            upgraded_obj = self._upgrade_iterable(old_obj)
        elif old_obj_typ in self.upgrade_rules and VAL_EVAL in self.upgrade_rules[old_obj_typ]:
            upgraded_obj = eval(self.upgrade_rules[old_obj_typ][VAL_EVAL])
        elif old_obj_typ in self.upgrade_rules:
            upgraded_obj = self._upgrade_from_defined_rules(old_obj)
        else:
            raise NotImplementedError(f"Upgrade of object {old_obj} failed, as it is not supported.")
        return upgraded_obj

    def upgrade_obj_store(self):
        new_obj_store = model3.DictObjectStore()
        for old_obj in self.provider:
            if isinstance(old_obj, model2.aas.Asset):
                continue
            new_obj = self.upgrade(old_obj)
            new_obj_store.add(new_obj)
        return new_obj_store
