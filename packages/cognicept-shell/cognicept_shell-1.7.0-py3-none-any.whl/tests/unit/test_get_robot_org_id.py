import pytest
from unittest.mock import patch
from cogniceptshell.configuration import Configuration

@pytest.fixture
def mock_requests_get():
    with patch('cogniceptshell.configuration.requests.get') as mock_get:
        yield mock_get

api_uri = 'https://dev.cognicept.systems/api/web/v2/'

def test_get_robot_id_success(mock_requests_get, capsys):
    mock_response = {
        'robot_id': '12345'
    }
    mock_requests_get.return_value.json.return_value = mock_response

    auth_key = 'test_auth_key'
    robot_code = 'r2'
    org_id = 'cognicept_systems_2'
    
    object = Configuration()
    robot_id = object.get_robot_id(api_uri, auth_key, robot_code, org_id)
    assert robot_id == '12345'

    captured = capsys.readouterr()
    assert "The robot_code input does not match a robot" not in captured.out

def test_get_robot_id_failure(mock_requests_get, capsys):
    mock_response = {
        'message': 'test_message'
    }
    mock_requests_get.return_value.json.return_value = mock_response

    auth_key = 'test_auth_key'
    robot_code = 'r2'
    org_id = 'cognicept_systems_2'
    
    object = Configuration()
    robot_id = object.get_robot_id(api_uri, auth_key, robot_code, org_id)
    assert robot_id is None

    captured = capsys.readouterr()
    assert "The robot_code input does not match a robot" in captured.out

def test_get_robot_id_exception(mock_requests_get, capsys):
    mock_requests_get.side_effect = Exception('API Error')

    auth_key = 'my_auth_key'
    robot_code = 'my_robot_code'
    org_id = 'my_org_id'

    object = Configuration()
    robot_id = object.get_robot_id(api_uri, auth_key, robot_code, org_id)
    assert robot_id is None

    captured = capsys.readouterr()
    assert "Cognicept API Error: API Error" in captured.out
    
def test_get_organization_id_success(mock_requests_get, capsys):
    mock_response = {
        'data': [
            {
                'organization_id': 'org123'
            }
        ]
    }
    mock_requests_get.return_value.json.return_value = mock_response

    auth_key = 'my_auth_key'
    org_code = 'my_org_code'
    
    object = Configuration()
    org_id = object.get_organization_id(api_uri, auth_key, org_code)
    assert org_id == 'org123'

    captured = capsys.readouterr()
    assert "The org_code input does not match any organization" not in captured.out

def test_get_organization_id_failure(mock_requests_get, capsys):
    mock_requests_get.return_value.json.return_value = {'data': []}

    auth_key = 'my_auth_key'
    org_code = 'my_org_code'
    
    object = Configuration()
    org_id = object.get_organization_id(api_uri, auth_key, org_code)
    assert org_id is None

    captured = capsys.readouterr()
    assert "The org_code input does not match any organization" in captured.out

def test_get_organization_id_exception(mock_requests_get, capsys):
    mock_requests_get.side_effect = Exception('API Error')

    auth_key = 'my_auth_key'
    org_code = 'my_org_code'

    object = Configuration()
    org_id = object.get_organization_id(api_uri, auth_key, org_code)
    assert org_id is None

    captured = capsys.readouterr()
    assert "Cognicept API Error: API Error" in captured.out
