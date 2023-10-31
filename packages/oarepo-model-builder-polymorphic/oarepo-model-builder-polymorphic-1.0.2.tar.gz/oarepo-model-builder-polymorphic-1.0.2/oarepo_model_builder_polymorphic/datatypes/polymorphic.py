import marshmallow as ma
from oarepo_model_builder.datatypes import (DataTypeComponent, ModelDataType,
                                            ObjectDataType, Section, datatypes)
from oarepo_model_builder.datatypes.components import (
    MarshmallowModelComponent, UIMarshmallowModelComponent)
from oarepo_model_builder.datatypes.containers.object import \
    ObjectPropertiesField


class PolymorphicDataType(ObjectDataType):
    model_type = "polymorphic"

    class ModelSchema(ObjectDataType.ModelSchema):
        schemas = ObjectPropertiesField()
        discriminator = ma.fields.String(default="type")

    def prepare(self, context):
        super().prepare(context)
        self.polymorphic_children = {}
        self.discriminator = self.definition.get("discriminator", "type")

        # marshmallow uses one-of, others use union - so create the union here
        # but keep the polymorphic children somewhere
        for schema_key, schema in self.definition["schemas"].items():
            dt = datatypes.get_datatype(
                self, schema, schema_key, self.model, self.schema
            )
            dt.skip_in_path = True
            dt.prepare(context)
            self.polymorphic_children[schema_key] = dt
            self.children.update(dt.children)

    def deep_iter(self):
        # skip direct children in deepiter and go to polymorphic instead
        yield from super(ObjectDataType, self).deep_iter()
        for c in self.polymorphic_children.values():
            yield from c.deep_iter()

    def _process_marshmallow(self, section: Section):
        section.children = self.polymorphic_children


class PolymorphicComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [MarshmallowModelComponent, UIMarshmallowModelComponent]

    def after_model_prepare(self, datatype, **kwargs):
        for dt in datatype.deep_iter():
            if isinstance(dt, PolymorphicDataType):
                self.patch_base_classes(dt)

    def patch_base_classes(self, datatype):
        base_classes = []
        config = datatype.section_marshmallow.config
        if "base-classes" in config:
            for bc in config["base-classes"]:
                if bc == "marshmallow.Schema":
                    base_classes.append("oarepo_runtime.services.schema.polymorphic.PolymorphicSchema")
                else:
                    base_classes.append(bc)
            config["base-classes"] = base_classes
        else:
            config["base-classes"] = ["oarepo_runtime.services.schema.polymorphic.PolymorphicSchema"]

        extra_fields = config.setdefault("extra-fields", [])
        extra_fields.append(
            {"name": f"type_field", "value": repr(datatype.discriminator)}
        )
