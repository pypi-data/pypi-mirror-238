from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioRecordCFBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_record_cf"
    section = "record"
    template = "record_cf"
