from unittest.mock import call, mock_open, patch
from clfill.config_handler import config_exists, create_config


def test_config_exists():
    with patch('clfill.config_handler.exists') as mock_exists:
        config_exists()
    mock_exists.assert_called_once_with('config/config.ini')


def test_create_config():
    with patch('clfill.config_handler.exists', return_value=False):
        with patch('clfill.config_handler.mkdir') as mock_mkdir:
            with patch('clfill.config_handler.input', side_effect=['mocked_email', 'mocked_name']):
                with patch('clfill.config_handler.open', mock_open()) as mock_file:
                    create_config()

    mock_mkdir.assert_called_once_with('config/')
    mock_file.assert_called_once_with('config/config.ini', 'w', encoding='utf8')

    calls = []
    calls.append(call('[Tracker]\n'))
    calls.append(call('trackerid = \n'))
    calls.append(call('\n'))
    calls.append(call('[Mailer]\n'))
    calls.append(call('myemail = mocked_email\n'))
    calls.append(call('myname = mocked_name\n'))
    calls.append(call('\n'))
    mock_file().write.assert_has_calls(calls)
