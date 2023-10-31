import marshmallow as ma
from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.datatypes.components import (
    DefaultsModelComponent,
    RecordDumperModelComponent,
    RecordModelComponent,
    ServiceModelComponent,
)
from oarepo_model_builder.datatypes.components.model.utils import (
    append_array,
    set_default,
)


class CustomFieldsSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    element = ma.fields.String(required=False)
    config = ma.fields.String(required=True)


class CustomFieldsModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [ServiceModelComponent]

    class ModelSchema(ma.Schema):
        custom_fields = ma.fields.List(
            ma.fields.Nested(CustomFieldsSchema),
            attribute="custom-fields",
            data_key="custom-fields",
        )

        @ma.post_load(pass_many=False)
        def post_load(self, data, **kwargs):
            custom_fields = data.get("custom_fields", [])
            seen_inlined = False
            for cf in custom_fields:
                if not cf.get("element"):
                    if seen_inlined:
                        raise ma.ValidationError(
                            "Only one inline custom field is allowed"
                        )
                    seen_inlined = True
            return data

    def before_model_prepare(self, datatype, **kwargs):
        append_array(datatype, "service-config", "components", "DataComponent")
        append_array(
            datatype,
            "service-config",
            "imports",
            {
                "import": "invenio_records_resources.services.records.components.DataComponent"
            },
        )

    def process_marshmallow(self, datatype, section=None, **kwargs):
        for cf in datatype.definition.get("custom-fields", []):
            element = cf.get("element", None)
            config = cf.get("config", None)
            if not element:
                section.config["base-classes"] = [
                    "oarepo_runtime.cf.InlinedCustomFieldsSchemaMixin"
                ] + section.config["base-classes"]
                section.config.setdefault("extra-fields", []).append(
                    {"name": "CUSTOM_FIELDS_VAR", "value": f'"{config}"'}
                )


class CustomFieldsElementModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [
        DefaultsModelComponent,
        RecordModelComponent,
        RecordDumperModelComponent,
    ]

    def before_model_prepare(self, datatype, **kwargs):
        for cf in datatype.definition.get("custom-fields", []):
            element = cf.get("element", None)
            config = cf.get("config", None)

            if element:
                # add this element to the model and let the rest of the framework generate the schema etc.
                datatype.definition["properties"][element] = {
                    "type": "object",
                    "jsonschema": {"additionalProperties": True},
                    "mapping": {"type": "object", "dynamic": True},
                    "marshmallow": {
                        "field": f'{{{{marshmallow_utils.fields.NestedAttribute}}}}({{{{functools.partial}}}}({{{{invenio_records_resources.services.custom_fields.CustomFieldsSchema}}}}, fields_var="{config}"))',
                        "generate": False,
                    },
                    "ui": {
                        "marshmallow": {
                            "field": f'{{{{marshmallow_utils.fields.NestedAttribute}}}}({{{{functools.partial}}}}({{{{invenio_records_resources.services.custom_fields.CustomFieldsSchema}}}}, fields_var="{config}"))',
                            "generate": False,
                        }
                    },
                    "sample": {"skip": True},
                }

                already_imported = [
                    imp["import"] for imp in datatype.definition["record"]["imports"]
                ]

                datatype.definition["record-dumper"]["extensions"].append(
                    f"{{{{invenio_records_resources.records.dumpers.CustomFieldsDumperExt}}}}('{config}')"
                )
            else:
                # just make the schema and mapping extensible
                set_default(datatype, "jsonschema", {}).setdefault(
                    "additionalProperties", True
                )
                set_default(datatype, "mapping", "os-v2", "mappings", {}).setdefault(
                    "dynamic", True
                )


COMPONENTS = [CustomFieldsModelComponent, CustomFieldsElementModelComponent]
