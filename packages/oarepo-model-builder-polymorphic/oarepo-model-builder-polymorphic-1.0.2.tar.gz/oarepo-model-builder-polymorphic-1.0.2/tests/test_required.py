import pytest
from invenio_access.permissions import system_identity
from marshmallow.exceptions import ValidationError
from mock_record.proxies import current_service


# test for required fields across polymorphic datatypes
def test_person_data(app, db, search_clear, lang_data):
    current_service.create(
        system_identity,
        {
            "metadata": {
                "creator": {"type": "person", "name": "test", "birthdate": "1980-01-01"}
            }
        },
    )
    with pytest.raises(
        ValidationError,
        match=r".*'birthdate': \['Missing data for required field.'\].*",
    ):
        current_service.create(
            system_identity,
            {"metadata": {"creator": {"type": "person", "name": "test"}}},
        )


def test_organization_data(app, db, search_clear, lang_data):
    current_service.create(
        system_identity,
        {"metadata": {"creator": {"type": "org", "name": "test", "ror": "1234"}}},
    )
    with pytest.raises(
        ValidationError, match=r".*'ror': \['Missing data for required field.'\].*"
    ):
        current_service.create(
            system_identity, {"metadata": {"creator": {"type": "org", "name": "test"}}}
        )
