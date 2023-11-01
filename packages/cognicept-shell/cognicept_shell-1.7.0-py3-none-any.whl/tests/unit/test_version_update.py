import pytest
from unittest.mock import patch, MagicMock
from cogniceptshell.agent_life_cycle import AgentLifeCycle as agent

@pytest.fixture
def mock_response():
    response = MagicMock()
    response.json.return_value = {'info': {'version': '1.2.3'}}
    return response

@pytest.fixture
def mock_requests_get(mock_response):
    with patch('requests.get') as mock_get:
        mock_get.return_value = mock_response
        yield mock_get

@pytest.fixture
def mock_input_yes():
    with patch('builtins.input', return_value='y'):
        yield

@pytest.fixture
def mock_input_no():
    with patch('builtins.input', return_value='n'):
        yield

def test_version_update_skip_true(mock_requests_get, mock_input_yes, capsys):
    args = MagicMock(skip=True)
    agent.cognicept_version_update(None, args)
    captured = capsys.readouterr()
    assert "cognicept-shell current version" in captured.out
    assert "Installing Version 1.2.3" in captured.out

def test_version_update_skip_false_input_yes(mock_requests_get, mock_input_yes, capsys):
    args = MagicMock(skip=False)
    agent.cognicept_version_update(None, args)
    captured = capsys.readouterr()
    assert "cognicept-shell current version" in captured.out
    assert "Installing Version 1.2.3" in captured.out

def test_version_update_skip_false_input_no(mock_requests_get, mock_input_no, capsys):
    args = MagicMock(skip=False)
    agent.cognicept_version_update(None, args)
    captured = capsys.readouterr()
    assert "cognicept-shell was not updated" in captured.out
