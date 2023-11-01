from oarepo_model_builder.datatypes import ModelDataType
from oarepo_model_builder.datatypes.components import RecordModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default


class DraftRecordModelComponent(RecordModelComponent):
    eligible_datatypes = [ModelDataType]
    dependency_remap = RecordModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        if datatype.root.profile not in {"record", "draft"}:
            return
        record = set_default(datatype, "record", {})

        if datatype.root.profile == "draft":
            record.setdefault(
                "base-classes",
                ["invenio_drafts_resources.records.api.Draft{InvenioDraft}"],
            )
            record.setdefault(
                "imports",
                [],
            )
            is_record_preset = record.get("class", None)
            super().before_model_prepare(datatype, context=context, **kwargs)
            if not is_record_preset and record["class"][-6:] == "Record":
                record["class"] = record["class"][:-6]
        if datatype.root.profile == "record":
            record.setdefault(
                "base-classes",
                ["invenio_drafts_resources.records.api.Record{InvenioRecord}"],
            )
            super().before_model_prepare(datatype, context=context, **kwargs)
