from invenio_access.permissions import system_identity
from mock_record.proxies import current_service
from mock_record.records.api import MockRecordRecord


def test_service(app, db, search_clear, lang_data):
    created_record_a = current_service.create(
        system_identity,
        {"metadata": {"a": {"disc": "1", "a": "a field", "c": {"id": "en"}}}},
    )
    created_record_reread_a = current_service.read(
        system_identity, created_record_a["id"]
    )
    assert created_record_a.data["metadata"] == created_record_reread_a.data["metadata"]
    assert "c" in created_record_a.data["metadata"]["a"]
    assert created_record_a.data["metadata"]["a"]["c"]["title"] == {"en": "English"}

    created_record_b = current_service.create(
        system_identity, {"metadata": {"a": {"disc": "2", "b": "b field"}}}
    )

    MockRecordRecord.index.refresh()

    # search by field directly
    by_field = current_service.search(
        system_identity, params={"q": 'metadata.a.a:"a field"'}
    )
    hits = list(by_field.hits)
    assert len(hits) == 1
    assert hits[0]["id"] == created_record_a["id"]

    by_field = current_service.search(
        system_identity, params={"q": 'metadata.a.b:"b field"'}
    )
    hits = list(by_field.hits)
    assert len(hits) == 1
    assert hits[0]["id"] == created_record_b["id"]

    # TODO: search by facet
    # by_facet = current_service.search(system_identity, params={'facets': 'metadata.a.a:"a field"'})
    # hits = list(by_facet.hits)
    # assert len(hits) == 1
    # assert hits[0]['id'] == created_record_a["id"]
