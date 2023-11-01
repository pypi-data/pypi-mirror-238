from cf.proxies import current_service as cf_service
from invenio_access.permissions import system_identity


def test_invenio_relation(app, db, search_clear, installed_custom_fields):
    rec = cf_service.create(
        system_identity,
        {
            "metadata": {"title": "title"},
            "hello": "world",
            "custom_fields": {
                "blah": "123",
            },
        },
    )
    assert rec.data["hello"] == "world"
    assert rec.data["custom_fields"]["blah"] == "123"
    assert rec.data["metadata"]["title"] == "title"
