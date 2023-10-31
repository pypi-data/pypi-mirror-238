
from marshmallow import fields as ma_fields
import marshmallow as ma

class UISettingsSchema(ma.Schema):
    i18n_languages = ma_fields.List(
        ma_fields.String(), default=["en"], data_key="i18n-languages", attribute='i18n-languages'
    )

