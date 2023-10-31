import inflect

from oarepo_model_builder.builders.json_base import JSONBaseBuilder
from oarepo_model_builder.datatypes import Section

from oarepo_model_builder_ui.config import UI_ITEMS

"""
Will generate:
metadata: {
  // contents of ui child here
  label: <label.key>
  hint: <hint.key>
  help: <help.key>
  children: {
    k: child_def
  }, // or 
  child: {
    ...
  }

// invenio_stuff_here

it will be saved to package/model/ui.json
"""


class InvenioLayoutBuilder(JSONBaseBuilder):
    TYPE = "ui-layout"
    output_file_type = "json"
    output_file_name = ["ui", "file"]
    create_parent_packages = True

    def build_node(self, node):
        generated = self.generate_node(node)
        self.output.merge(generated)

    def generate_node(self, node):
        ui = {}
        section = node.section_ui
        data = node.definition
        facets = node.section_facets.config['facets']

        ui.update({k.replace("-", "_"): v for k, v in section.config.items()})
        ui.pop('marshmallow', None)
        if "type" in data:
            t = data["type"]
            if t in ("object", "nested"):
                t = inflect.engine().singular_noun(
                    node.path.split('.')[-1].lower()
                )
            ui.setdefault("detail", t)
            ui.setdefault("input", t)

        for fld in UI_ITEMS:
            ui[fld] = data.get(
                f"{fld}.key",
                node.path.replace('.', '/') + f".{fld}",
            )
        if 'enum' in data:
            ui['enum'] = data.get(f"enum.key",
                node.path.replace('.', '/') + ".enum",
            )

        if facets:
            ui["facet"] = facets[0].path

        if node.children:
            children = ui.setdefault('children', {})
            for c in node.children.values():
                children[c.key] = self.generate_node(c)
        if hasattr(node, 'item'):
            ui['child'] = self.generate_node(node.item)

        return ui