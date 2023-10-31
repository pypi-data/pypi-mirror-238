import os

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.datatypes.components import SavedModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default
import marshmallow as ma

from oarepo_model_builder.utils.python_name import module_to_path


class TranslationsSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    module = ma.fields.Str()
    alias = ma.fields.Str()


class UISchema(ma.Schema):
    """
    registered in entry points to the ui.model group
    """
    class Meta:
        unknown = ma.RAISE

    module = ma.fields.Str()
    file = ma.fields.Str()
    alias = ma.fields.Str()


class UIModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on=[SavedModelComponent]

    class ModelSchema(ma.Schema):
        translations = ma.fields.Nested(TranslationsSchema)

    def before_model_prepare(self, datatype, *, context, **kwargs):
        translations = set_default(datatype, 'translations', {})
        translations.setdefault('module', f"{datatype.definition['module']['qualified']}.translations")
        translations.setdefault('alias', datatype.definition['module']['alias'])

        ui = set_default(datatype, 'ui', {})
        module = ui.setdefault('module', datatype.definition['saved-model']['module'])
        ui.setdefault('file', os.path.join(module_to_path(module), "ui.json"))
        ui.setdefault('alias', datatype.definition['module']['alias'])
