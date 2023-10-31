import marshmallow as ma
import pytest
from mock_record.services.records.schema import MockRecordMetadataSchema


def test_schema(app):
    data = {"a": {"disc": "1", "a": "a field"}}
    assert MockRecordMetadataSchema().load(data) == data

    data = {"a": {"disc": "2", "a": "a field"}}
    with pytest.raises(ma.ValidationError):
        MockRecordMetadataSchema().load(data)

    data = {"a": {"disc": "2", "b": "b field"}}
    assert MockRecordMetadataSchema().load(data) == data
