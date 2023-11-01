import json
import uuid
import pytest
import requests
from datetime import datetime
from unittest.mock import Mock, patch
from requests.exceptions import Timeout,TooManyRedirects

from cogniceptshell.agent_life_cycle import AgentLifeCycle

@pytest.fixture
def mock_object():
    # Mock the object instance and its methods
    mock_obj = Mock()
    mock_obj._docker_images = {
        'image1': 'ecr/image1:latest',
        'image2': 'ecr/image2:latest',
    }
    return mock_obj

@pytest.fixture
def mock_args():
    # Mock the args object returned by argparse.parse_args()
    mock_args = Mock()
    mock_args.config.config = {
        'AGENT_POST_API': 'http://example.com/api',
        'AGENT_ID': 'agent123',
        'ROBOT_CODE': 'robot456',
        'SITE_CODE': 'site789',
    }
    return mock_args

def test_successful_update(mock_object, mock_args):
    # Mock the get_version_tag_from_latest method for a successful update
    mock_object.get_version_tag_from_latest.return_value = 'v1.0'

    # Call the function with the mocked objects
    result = True
    AgentLifeCycle._update_event_log(mock_object, result, mock_args)

    # Assert the payload values after the function call
    expected_payload = {
        "agent_id": "",
        "compounding": False,
        "create_ticket": False,
        "description": "Null",
        "error_code": "Null",
        "event_id": "",
        "level": "2",
        "message": "Update is successful! Current images are: image1: 'latest:v1.0' ; image2: 'latest:v1.0'",
        "module": "Updater",
        "property_id": "",
        "resolution": "Null",
        "robot_id": "",
        "source": "auto_updater",
        "timestamp": ""
    }

    assert mock_object.post_event_log.call_count == 1
    actual_payload = mock_object.post_event_log.call_args[0][0]
    assert actual_payload == expected_payload

def test_failed_update(mock_object, mock_args):
    # Mock the get_version_tag_from_latest method for a failed update
    mock_object.get_version_tag_from_latest.return_value = None

    # Call the function with the mocked objects
    result = False
    AgentLifeCycle._update_event_log(mock_object, result, mock_args)

    # Assert the payload values after the function call
    expected_payload = {
        "agent_id": "",
        "compounding": False,
        "create_ticket": True,
        "description": "Null",
        "error_code": "Null",
        "event_id": "",
        "level": "16",
        "message": "Update has failed due to lack of disk space or error in updating images. Current images are: image1: 'latest' ; image2: 'latest'",
        "module": "Updater",
        "property_id": "",
        "resolution": "Null",
        "robot_id": "",
        "source": "auto_updater",
        "timestamp": ""
    }

    assert mock_object.post_event_log.call_count == 1
    actual_payload = mock_object.post_event_log.call_args[0][0]
    assert actual_payload == expected_payload


def test_successful_post(mock_args):
    # Mock the requests.post method for a successful request
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'status': 'success'}

    def mock_post(*args, **kwargs):
        return mock_response

    # Mock the datetime.utcnow and uuid.uuid4 functions
    fixed_timestamp = '2023-07-24T13:09:42.434015'
    fixed_event_id = '7fca97c9-17b3-488c-815f-b62adce155d7'
    with patch('requests.post', side_effect=mock_post) as mock_post_request, \
         patch('cogniceptshell.agent_life_cycle.datetime') as mock_datetime, \
         patch('cogniceptshell.agent_life_cycle.uuid') as mock_uuid:
        
        # Configure the mock datetime and uuid
        mock_datetime.utcnow.return_value = datetime.fromisoformat(fixed_timestamp)
        mock_uuid.uuid4.return_value = uuid.UUID(fixed_event_id)
        
        # Call the function with the mocked objects
        payload = {
            "agent_id": "",
            "compounding": False,
            "create_ticket": False,
            "description": "Null",
            "error_code": "Null",
            "event_id": "",
            "level": "2",
            "message": "Update is successful! Current images are: image1: 'latest' ; image2: 'latest'",
            "module": "Updater",
            "property_id": "",
            "resolution": "Null",
            "robot_id": "",
            "source": "auto_updater",
            "timestamp": ""
        }
        agent = AgentLifeCycle()
        result = agent.post_event_log(payload, mock_args)

        # Define the expected payload format
        expected_payload = {
            'agent_id': 'agent123',
            'compounding': False,
            'create_ticket': False,
            'description': 'Null',
            'error_code': 'Null',
            'event_id': fixed_event_id,
            'level': '2',
            'message': "Update is successful! Current images are: image1: 'latest' ; image2: 'latest'",
            'module': 'Updater',
            'property_id': 'site789',
            'resolution': 'Null',
            'robot_id': 'robot456',
            'source': 'auto_updater',
            'timestamp': fixed_timestamp
        }

        # Assert the result and compare the payload format
        assert result is True
        # Ensure the 'data' argument contains the correct payload
        _, actual_args = mock_post_request.call_args  # Get the call arguments of requests.post
        actual_payload = actual_args['json']  # Convert 'data' back to a dictionary
        assert actual_payload == expected_payload

def test_timeout_exception(mock_args):
    # Mock the requests.post method to raise Timeout exception
    def mock_post(*args, **kwargs):
        raise Timeout

    requests.post = mock_post

    # Call the function with the mocked objects
    payload = {
        'message': 'Test message',
        'level': '2',
    }
    agent = AgentLifeCycle()
    result = agent.post_event_log(payload, mock_args)

    # Assert the result
    assert result is False

def test_redirects_exception(mock_args):
    # Mock the requests.post method to raise TooManyRedirects exception
    def mock_post(*args, **kwargs):
        raise TooManyRedirects

    requests.post = mock_post

    # Call the function with the mocked objects
    payload = {
        'message': 'Test message',
        'level': '2',
    }
    agent = AgentLifeCycle()
    result = agent.post_event_log(payload, mock_args)

    # Assert the result
    assert result is False

def test_other_exceptions(mock_args):
    # Mock the requests.post method to raise other exceptions
    def mock_post(*args, **kwargs):
        raise ValueError('Some error occurred')

    requests.post = mock_post

    # Call the function with the mocked objects
    payload = {
        'message': 'Test message',
        'level': '2',
    }
    agent = AgentLifeCycle()
    result = agent.post_event_log(payload, mock_args)

    # Assert the result
    assert result is False
