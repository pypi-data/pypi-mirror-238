import marshmallow as ma
from oarepo_model_builder.datatypes import (
    DataType,
    DataTypeComponent,
    ModelDataType,
    Section,
)
from oarepo_model_builder.datatypes.components import DefaultsModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default
from oarepo_model_builder.datatypes.model import Link
from oarepo_model_builder.utils.links import url_prefix2link
from oarepo_model_builder.utils.python_name import Import

def get_file_schema():
    from ..file import FileDataType

    return FileDataType.validator()


class FileComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    affects = [DefaultsModelComponent]

    class ModelSchema(ma.Schema):
        files = ma.fields.Nested(get_file_schema)

    def process_links(self, datatype, section: Section, **kwargs):
        url_prefix = url_prefix2link(datatype.definition["resource-config"]["base-url"])

        if datatype.root.profile == "record":
            has_files = "files" in datatype.definition
            if not has_files:
                return
            try:
                files_url_prefix = url_prefix2link(
                    datatype.definition["files"]["resource-config"]["base-url"]
                )
            except KeyError:
                files_url_prefix = f"{url_prefix}{{id}}/"
            # add files link item
            has_files = False
            for link in section.config["links_item"]:
                if link.name == "files":
                    has_files = True
            if not has_files:
                # todo these should actually refer to file resource url prefixe
                section.config["links_item"].append(
                    Link(
                        name="files",
                        link_class="RecordLink",
                        link_args=[f'"{{+api}}{files_url_prefix}files"'],
                        imports=[
                            Import(
                                import_path="invenio_records_resources.services.RecordLink"  # NOSONAR
                            )
                        ],
                    )
                )
        if datatype.root.profile == "files":
            if "links_search" in section.config:
                section.config.pop("links_search")
            # remove normal links and add
            section.config["file_links_list"] = [
                Link(
                    name="self",
                    link_class="RecordLink",
                    link_args=[f'"{{+api}}{url_prefix}files"'],
                    imports=[Import("invenio_records_resources.services.RecordLink")],
                ),
            ]

            section.config.pop("links_item")
            section.config["file_links_item"] = [
                Link(
                    name="self",
                    link_class="FileLink",
                    link_args=[f'"{{+api}}{url_prefix}files/{{key}}"'],
                    imports=[
                        Import("invenio_records_resources.services.FileLink")
                    ],  # NOSONAR
                ),
                Link(
                    name="content",
                    link_class="FileLink",
                    link_args=[f'"{{+api}}{url_prefix}files/{{key}}/content"'],
                    imports=[Import("invenio_records_resources.services.FileLink")],
                ),
                Link(
                    name="commit",
                    link_class="FileLink",
                    link_args=[f'"{{+api}}{url_prefix}files/{{key}}/commit"'],
                    imports=[Import("invenio_records_resources.services.FileLink")],
                ),
            ]

    def process_mb_invenio_record_service_config(self, *, datatype, section, **kwargs):
        if datatype.root.profile == "files":
            # override class as it has to be a parent class
            section.config.setdefault("record", {})[
                "class"
            ] = datatype.parent_record.definition["record"]["class"]

    def before_model_prepare(self, datatype, *, context, **kwargs):
        if not datatype.root.profile == "files":
            return

        parent_record_datatype: DataType = context["published_record"]
        datatype.parent_record = parent_record_datatype

        set_default(datatype, "search-options", {}).setdefault("skip", True)
        set_default(datatype, "facets", {}).setdefault("skip", True)
        set_default(datatype, "json-schema-settings", {}).setdefault("skip", True)
        set_default(datatype, "mapping-settings", {}).setdefault("skip", True)
        set_default(datatype, "record-dumper", {}).setdefault("skip", True)
