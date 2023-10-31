from typing import Dict

from oarepo_model_builder.datatypes import DataTypeComponent
from oarepo_model_builder_ui.config import UI_ITEMS

import marshmallow as ma


class UIPropertySchema(ma.Schema):
    # just a model description, not displayed anywhere
    description = ma.fields.String()

    def load(
        self,
        data,
        *,
        many=None,
        partial=None,
        unknown=None,
    ):
        # remove UI_ITEMS from data
        if many:
            x: Dict
            ui_items = [self.remove_ui_items(x) for x in data]
            i18n_key = [x.pop('i18n.key', None) for x in data]
        else:
            ui_items = self.remove_ui_items(data)
            i18n_key = data.pop('i18n.key', None)

        # perform normal validation
        ret = super().load(data, many=many, partial=partial, unknown=unknown)
        # add UI_ITEMS to data
        if many:
            for ui_item, ret_item, i18n_key_item in zip(ui_items, ret, i18n_key):
                self.add_ui_items(ret_item, ui_item)
                if i18n_key_item:
                    ret_item['i18n.key'] = i18n_key_item
        else:
            self.add_ui_items(ret, ui_items)
            if i18n_key:
                ret['i18n.key'] = i18n_key
        return ret

    def remove_ui_items(self, data):
        if not data:
            return {}
        ui_items = {}
        for k in list(data.keys()):
            split_key = k.split('.')
            if len(split_key) < 2:
                continue
            if split_key[0] in UI_ITEMS or split_key[0] == 'enum':
                ui_items[k] = data.pop(k)
        return ui_items

    def add_ui_items(self, data, ui_items):
        data.update(ui_items)


class DataTypeUIComponent(DataTypeComponent):
    class ModelSchema(UIPropertySchema):
        pass


from .model import UIModelComponent
components = [
    DataTypeUIComponent,
    UIModelComponent
]