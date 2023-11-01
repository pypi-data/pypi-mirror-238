import os
import pytest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError
from cogniceptshell.configuration import Configuration

def test_pull_config_templates_success(capsys, tmpdir, monkeypatch):
    # 1. Setup tmpdir with a templates folder inside
    templates_folder = tmpdir.mkdir("templates")
    
    # 2. Mock args.config.config and path
    mock_args = MagicMock()
    mock_args.config.config = {
        'ECS_ROBOT_MODEL': 'robot_model'
    }
    mock_args.path = str(tmpdir)
    
    # 3. Mock the list_objects_v2 response
    mock_s3_client = MagicMock()
    mock_s3_client.list_objects_v2.return_value = {
        'Contents': [
            {'Key': 'robot_model/template1.yaml'},
            {'Key': 'robot_model/template2.yml'},
            {'Key': 'robot_model/other_file.txt'}
        ]
    }
    
    # 4. Mock download_file
    def mock_download_file(bucket, key, destination):
        # Simulate file download by creating an empty file in the templates folder
        template_filename = os.path.basename(key)
        destination_path = os.path.join(templates_folder, template_filename)
        open(destination_path, 'a').close()

    mock_s3_client.download_file = mock_download_file
    
    # Patch the necessary objects with the mocks
    monkeypatch.setattr('boto3.client', lambda service: mock_s3_client)
    monkeypatch.setattr('os.path.expanduser', lambda path: str(tmpdir))
    
    # Call the function
    object = Configuration()
    object.pull_config_templates(mock_args)
    
    # Assert the download message
    assert "All robot configuration templates have been successfully downloaded." in capsys.readouterr().out
    
    # Assert the correct files in the templates directory
    assert templates_folder.join("template1.yaml").check(file=True)
    assert templates_folder.join("template2.yml").check(file=True)
    assert not templates_folder.join("other_file.txt").check()


def test_pull_config_templates_list_objects_error(capsys, tmpdir, mocker):
    # 1. Setup tmpdir with a templates folder inside
    templates_folder = tmpdir.mkdir("templates")

    # 2. Mock the necessary objects and functions
    mock_args = mocker.MagicMock()
    mock_args.config.config = {
        'ECS_ROBOT_MODEL': 'robot_model'
    }
    mock_args.path = str(tmpdir)

    mock_s3_client = mocker.MagicMock()
    mocker.patch("boto3.client", return_value=mock_s3_client)

    mock_error = ClientError({'Error': {'Code': 'SomeErrorCode', 'Message': 'SomeErrorMessage'}}, 'ListObjectsV2')
    mock_s3_client.list_objects_v2.side_effect = mock_error

    # Create an instance of Configuration
    config = Configuration()

    # Call the function
    config.pull_config_templates(mock_args)

    # Assert the correct behavior
    assert "Failed to retrieve template config files" in capsys.readouterr().out

    assert not os.listdir(templates_folder)


def test_pull_config_templates_download_file_error(capsys, tmpdir, mocker):
    # 1. Setup tmpdir with a templates folder inside
    templates_folder = tmpdir.mkdir("templates")

    # 2. Mock the necessary objects and functions
    mock_args = mocker.MagicMock()
    mock_args.config.config = {
        'ECS_ROBOT_MODEL': 'robot_model'
    }
    mock_args.path = str(tmpdir)

    mock_s3_client = mocker.MagicMock()
    mocker.patch("boto3.client", return_value=mock_s3_client)

    mock_response = {
        'Contents': [
            {'Key': 'robot_model/template1.yaml'},
            {'Key': 'robot_model/template2.yml'},
            {'Key': 'robot_model/other_file.txt'}
        ]
    }
    mock_s3_client.list_objects_v2.return_value = mock_response

    mock_error = ClientError({'Error': {'Code': 'SomeErrorCode', 'Message': 'SomeErrorMessage'}}, 'DownloadFile')
    mock_s3_client.download_file.side_effect = mock_error

    # Create an instance of Configuration
    config = Configuration()

    # Call the function
    config.pull_config_templates(mock_args)

    # Assert the correct behavior
    assert "Failed to retrieve template config files" in capsys.readouterr().out

    assert not os.listdir(templates_folder)