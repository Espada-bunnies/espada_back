import pytest
from unittest.mock import patch


@pytest.fixture
def mock_send_mail():
    with patch("myapp.services.send_mail") as send_mail_mock:
        yield send_mail_mock
