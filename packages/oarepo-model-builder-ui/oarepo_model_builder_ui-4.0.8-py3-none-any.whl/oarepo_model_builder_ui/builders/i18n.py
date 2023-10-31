from collections import defaultdict
from pathlib import Path
from oarepo_model_builder.builders import OutputBuilder

from oarepo_model_builder.datatypes import DataType
from oarepo_model_builder_ui.config import UI_ITEMS

from oarepo_model_builder.utils.python_name import module_to_path

class InvenioI18nBuilder(OutputBuilder):
    TYPE = "invenio_i18n"
    output_file_type = "po"

    def build_node(self, datatype: DataType):
        translation_config = datatype.section_translations.config

        path = module_to_path(translation_config['module'])
        self.output = self.builder.get_output("po", path)

        for node in datatype.deep_iter():
            if node != datatype:
                self.process_node(node)

    def process_node(self, node):
        ui_items = defaultdict(dict)

        for k in node.definition:
            split_key = k.split('.')
            if len(split_key) < 2:
                continue
            ui_type = split_key[0]
            lang = split_key[-1]
            prefix = '.'.join(split_key[:-1])
            if ui_type in UI_ITEMS or ui_type == 'enum':
                ui_items[prefix][lang] = node.definition[k]

        key_proto = node.definition.get("i18n.key")
        for ui in UI_ITEMS:
            if "key" not in ui_items[ui]:
                if key_proto:
                    ui_items[ui]["key"] = f"{key_proto}.{ui}"
                else:
                    ui_items[ui]["key"] = (
                            node.path.replace('.', '/') + f".{ui}"
                    )

        # add translation for enums
        enum_keys = node.definition.get("enum", [])
        for en in enum_keys:
            if key_proto:
                ui_items[f"enum.{en}"]["key"] = f"{key_proto}.enum.{en}"
            else:
                ui_items[f"enum.{en}"]["key"] = (
                        node.path.replace('.', '/') + f".enum.{en}"
                )

        for ui, langs in ui_items.items():
            key = langs.pop("key")
            for lang, val in langs.items():
                self.output.add(key, val, language=lang)
            self.output.add(key)
