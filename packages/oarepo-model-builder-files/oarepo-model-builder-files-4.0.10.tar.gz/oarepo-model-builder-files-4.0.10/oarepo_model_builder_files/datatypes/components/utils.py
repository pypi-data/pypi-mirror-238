from oarepo_model_builder.datatypes import DataType
def get_metadata_record(datatype, context):
    if datatype.root.profile == "files":
        return context["published_record"]
    elif datatype.root.profile == "draft_files":
        return context["draft_record"]
