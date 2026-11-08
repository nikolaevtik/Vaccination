
#tests/test_utils.py
import pytest
import requests
from src.utils import get_random_number, get_data, log_message


def test_random_number(mocker):
    mocker.patch('src.utils.random.randint', return_value=42)
    assert get_random_number() == 42


def test_get_data_connection_error(mocker):
    mocker.patch(
        'src.utils.requests.get',
        side_effect=requests.exceptions.ConnectionError
    )
    with pytest.raises(requests.exceptions.ConnectionError):
        get_data()


def test_log_message(mocker):
    mock_send = mocker.patch("src.utils.external_logger.send")
    log_message("hello")
    mock_send.assert_called_once_with("hello")