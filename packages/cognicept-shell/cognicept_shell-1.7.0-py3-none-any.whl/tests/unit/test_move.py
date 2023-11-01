from cogniceptshell.robot_actions import RobotActions
from cogniceptshell.common import bcolors
from unittest.mock import patch
import pytest
import json
from uuid import UUID

robot_actions = RobotActions()
robot_actions.api_uri = "https://dev.cognicept.systems/api/web/v2/"

""" Class for mocking fake data"""
class MockConfig():
    config = {
        "COGNICEPT_USER_API_URI": "https://dev.cognicept.systems/api/web/v2/"
    }

class MockArgs():
    config = MockConfig()
    # user details
    username = 'test_move_robot@kabam.ai'
    password = 'Kabam123#'
    access_token = 'askodaslkdmalskmd1231==asd'
    headers = {
        'Authorization': 'Bearer ' + str(access_token)
    }


    # org details
    old_org_id = '0a3ec88a-4fe0-40f6-8c94-5b074eac24b2'
    old_org_code = 'cognicept_systems_125'
    new_org_id = '169ef896-07fb-402d-ac4a-b1cd825e8745'
    new_org_code = 'org_to_move_robot_to_1'
    wrong_organization_id = '0a3ec88a-4fe0-40f6-8c94-5b074eac24b5'
    wrong_organization_code = 'this_is_wrong'

    # robot details
    robot_id = '9d834f2a-5993-4a84-99b4-943d2b4cce29'
    robot_code = 'DoNotMove'
    robot_details = { "robot_name": "Test" }
    wrong_robot_id = '9d834f2a-5993-4a84-99b4-943d2b4cce22'
    wrong_robot_code = 'This_is_wrong'

    # map details
    map_ids = ['f2dae02a-8f73-460a-989d-2540598b3a1a']
    map_image = 'iVBORw0KGgoAAAANSUhEUg'
    map_details = {"map_image": "asdasd"}
    b64_encoded_map_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'

    waypoint_id = '2af2cbeb-7b50-40d1-8692-559eda719e74'

    # mission details
    mission_id = 'fe23e302-209d-4bf5-a669-6ecf441511cd'
    wrong_mission_id = 'fe23e302-209d-4bf5-a669-6ecf441511ce'
    mission_details = {"mission_name": "Test"}
    
    # schedule details
    schedule_id = '323fa670-d991-4ba5-871a-668f190f71e2'
    wrong_schedule_id = '323fa670-d991-4ba5-871a-668f190f71e3'
    schedule_details = {"address": "123"}
    
    property_id = '7b4c8067-7c41-41ce-ba43-366cdc69fc2b'
    property_code = 'MY_SITE'
    property_details = {"address": "123"}
    wrong_property_id = '7b4c8067-7c41-41ce-ba43-366cdc69fc22'

mock_args = MockArgs()

@pytest.fixture
def mock_positive_login_request():
    with patch("cogniceptshell.robot_actions.requests.post") as fake_resp:    
        fake_return_value = json.dumps({"access_token": "123123123123",
                                        "refresh_token": "123123123123"
                                        }).encode()        
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp
    
def test_login_positive(capsys, mock_positive_login_request):
    access_token = robot_actions.login(username=mock_args.username, password=mock_args.password)
    assert access_token == "123123123123"

@pytest.fixture
def mock_negative_login_request():
    with patch("cogniceptshell.robot_actions.requests.post") as fake_resp:    
        fake_return_value = json.dumps({"message": "Username and password combination not valid"}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp

def test_login_negative_wrong_cred(capsys, mock_negative_login_request):
    with pytest.raises(SystemExit):
        access_token = robot_actions.login(username=123, password=mock_args.password+'123') 
    out, err = capsys.readouterr()
    assert out.replace("\n", "") == bcolors.FAIL + "Error in logging in: Wrong credentials" + bcolors.ENDC
    print(out, err)
    
@pytest.fixture
def mock_get_organization_by_id_positive():
    with patch("cogniceptshell.robot_actions.requests.get") as fake_resp:    
        fake_return_value = json.dumps({"data": [{"organization_id": mock_args.old_org_id,
                                    "organization_code": mock_args.old_org_code }]}).encode()        
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp

def test_get_organization_positive(capsys, mock_get_organization_by_id_positive):
    org_details = robot_actions.get_organization_by_id(org_id='correct_org_id', headers=mock_args.headers)
    assert org_details['organization_code'] == mock_args.old_org_code

    org_details = robot_actions.get_organization_by_org_code(org_code='correct_org_code', headers=mock_args.headers)
    assert org_details['organization_id'] == mock_args.old_org_id

@pytest.fixture
def mock_get_organization_by_id_negative():
    with patch("cogniceptshell.robot_actions.requests.get") as fake_resp:    
        fake_return_value = json.dumps({"data": []}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp

def test_get_organization_by_id_negative(capsys, mock_get_organization_by_id_negative):
    with pytest.raises(SystemExit):
        org_details = robot_actions.get_organization_by_id(org_id=mock_args.wrong_organization_id, headers=mock_args.headers)
    out, err = capsys.readouterr()
    assert out.replace("\n", "") == bcolors.FAIL + "No such organization {org_id}".format(org_id=mock_args.wrong_organization_id) + bcolors.ENDC
    print(out, err)

@pytest.fixture
def mock_get_organization_by_code_negative():
    with patch("cogniceptshell.robot_actions.requests.get") as fake_resp:    
        fake_return_value = json.dumps({"data": []}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp

def test_get_organization_by_code_negative(capsys, mock_get_organization_by_code_negative):
    with pytest.raises(SystemExit):
        org_details = robot_actions.get_organization_by_org_code(org_code=mock_args.wrong_organization_code, headers=mock_args.headers)
    out, err = capsys.readouterr()
    assert out.replace("\n", "") == bcolors.FAIL + 'No such organization {org_code}'.format(org_code=mock_args.wrong_organization_code) + bcolors.ENDC
    print(out, err)

@pytest.fixture
def mock_get_robot_positive():
    with patch("cogniceptshell.robot_actions.requests.get") as fake_resp:    
        fake_return_value = json.dumps({"robot_id": mock_args.robot_id, "robot_code": mock_args.robot_code}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp

def test_get_robot_by_id_positive(capsys, mock_get_robot_positive):
    robot_details = robot_actions.get_robot_by_id(mock_args.robot_id, mock_args.old_org_id, mock_args.headers)
    assert robot_details['robot_id'] == mock_args.robot_id
    assert robot_details['robot_code'] == mock_args.robot_code

@pytest.fixture
def mock_get_robot_by_id_negative():
    with patch("cogniceptshell.robot_actions.requests.get") as fake_resp:    
        fake_return_value = json.dumps({"message": "Bad request. Invalid input"}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp

def test_get_robot_by_id_negative(capsys, mock_get_robot_by_id_negative):    
    with pytest.raises(SystemExit):
        robot_details = robot_actions.get_robot_by_id(mock_args.wrong_robot_id, mock_args.old_org_id, mock_args.headers)
    out, err = capsys.readouterr()
    assert out.replace("\n", "") == bcolors.FAIL + "No such robot {robot_id} in organization {org_id}".format(robot_id=mock_args.wrong_robot_id, org_id=mock_args.old_org_id) + bcolors.ENDC
    print(out, err)

def test_get_robot_by_code_positive(capsys, mock_get_robot_positive):
    robot_details = robot_actions.get_robot_by_id(mock_args.robot_id, mock_args.old_org_id, mock_args.headers)
    assert robot_details['robot_id'] == mock_args.robot_id
    assert robot_details['robot_code'] == mock_args.robot_code

@pytest.fixture
def mock_get_robot_by_code_negative():
    with patch("cogniceptshell.robot_actions.requests.get") as fake_resp:    
        fake_return_value = json.dumps({"message": "Bad request. Invalid input"}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp

def test_get_robot_by_code_negative(capsys, mock_get_robot_by_code_negative):
    with pytest.raises(SystemExit):
        robot_details = robot_actions.get_robot_by_code(mock_args.wrong_robot_code, mock_args.old_org_code, mock_args.headers)
    out, err = capsys.readouterr()
    assert out.replace("\n", "") == bcolors.FAIL + "No such robot {robot_code} in organization {org_code}".format(robot_code=mock_args.wrong_robot_code, org_code=mock_args.old_org_code) + bcolors.ENDC
    print(out, err)

@pytest.fixture
def mock_create_robot_positive():
    with patch("cogniceptshell.robot_actions.requests.post") as fake_resp:    
        fake_return_value = json.dumps({"robot_id": mock_args.robot_id}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp

def test_create_robot_positive(capsys, mock_create_robot_positive):    
    new_robot_id = robot_actions.create_robot(robot_details=mock_args.robot_details, headers=mock_args.headers)
    assert new_robot_id == mock_args.robot_id

@pytest.fixture
def mock_create_robot_negative():
    with patch("cogniceptshell.robot_actions.requests.post") as fake_resp:    
        fake_return_value = json.dumps({"message": "Bad request"}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 400
        yield fake_resp

def test_create_robot_negative(capsys, mock_create_robot_negative):
    with pytest.raises(Exception) as excinfo:
        robot_actions.create_robot(robot_details=mock_args.robot_details, headers=mock_args.headers)    
    assert str(excinfo.value) == bcolors.FAIL + "Error in creating robot" + bcolors.ENDC

@pytest.fixture
def mock_delete_robot_positive():
    with patch("cogniceptshell.robot_actions.requests.delete") as fake_resp:    
        fake_return_value = json.dumps({"message": mock_args.robot_id}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp

def test_delete_robot_positive(capsys, mock_delete_robot_positive):
    delete_robot_payload = robot_actions.delete_robot(robot_id=mock_args.robot_id, organization_id=mock_args.old_org_id ,headers=mock_args.headers)
    assert delete_robot_payload == mock_args.robot_id

@pytest.fixture
def mock_delete_robot_negative():
    with patch("cogniceptshell.robot_actions.requests.delete") as fake_resp:    
        fake_return_value = json.dumps({"Message": "Invalid key to delete"}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 400
        yield fake_resp

def test_delete_robot_negative(capsys, mock_delete_robot_negative):
    delete_robot_payload = robot_actions.delete_robot(robot_id=mock_args.robot_id, organization_id=mock_args.old_org_id ,headers=mock_args.headers)
    out, err = capsys.readouterr()
    assert out.replace("\n", "") == bcolors.FAIL + "Error in deleting robot {robot_id}. Please manually delete it".format(robot_id=mock_args.robot_id) + bcolors.ENDC
    print(out, err)

@pytest.fixture
def mock_get_robot_missions_positive():
    with patch("cogniceptshell.robot_actions.requests.get") as fake_resp:    
        fake_return_value = json.dumps({"data": [{"mission_id": 1}, {"mission_id": 2}, {"mission_id": 3}]}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp

def test_get_robot_missions_positive(capsys, mock_get_robot_missions_positive):
    missions_data = robot_actions.get_robot_missions(robot_id=mock_args.robot_id, headers=mock_args.headers)
    assert len(missions_data) == 3
    
@pytest.fixture
def mock_get_robot_missions_negative():
    with patch("cogniceptshell.robot_actions.requests.get") as fake_resp:    
        fake_return_value = json.dumps({"message": "Invalid input"}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 400
        yield fake_resp

def test_get_robot_missions_negative(capsys, mock_get_robot_missions_negative):
    with pytest.raises(SystemExit):
        missions_data = robot_actions.get_robot_missions(mock_args.robot_id, headers=mock_args.headers)
    out, err = capsys.readouterr()
    assert out.replace("\n", "") == bcolors.FAIL + "Error in retrieving missions" + bcolors.ENDC
    
@pytest.fixture
def mock_create_mission_positive():
    with patch("cogniceptshell.robot_actions.requests.post") as fake_resp:    
        fake_return_value = json.dumps({"mission_id": mock_args.mission_id}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp

def test_create_mission_positive(capsys, mock_create_mission_positive):
    new_mission_id = robot_actions.create_mission(mock_args.mission_details, headers=mock_args.headers)
    assert new_mission_id == mock_args.mission_id

@pytest.fixture
def mock_create_mission_negative():
    with patch("cogniceptshell.robot_actions.requests.post") as fake_resp:    
        fake_return_value = json.dumps({"message": "Bad input"}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 400
        yield fake_resp

def test_create_mission_negative(capsys, mock_create_mission_negative):    
    with pytest.raises(Exception) as excinfo:
        new_mission_id = robot_actions.create_mission(mock_args.mission_details, headers=mock_args.headers)
    assert str(excinfo.value) == bcolors.FAIL + "Error in creating mission" + bcolors.ENDC

@pytest.fixture
def mock_delete_mission_positive():
    with patch("cogniceptshell.robot_actions.requests.delete") as fake_resp:    
        fake_return_value = json.dumps({"mission_id": mock_args.mission_id}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp

def test_delete_mission_positive(capsys, mock_delete_mission_positive):
    delete_payload = robot_actions.delete_mission(mission_id=mock_args.mission_id, headers=mock_args.headers)
    assert delete_payload == mock_args.mission_id

@pytest.fixture
def mock_delete_mission_negative():
    with patch("cogniceptshell.robot_actions.requests.delete") as fake_resp:    
        fake_return_value = json.dumps({"message": "Invalid input"}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 400
        yield fake_resp

def test_delete_mission_negative(capsys, mock_delete_mission_negative):
    delete_payload = robot_actions.delete_mission(mission_id=mock_args.wrong_mission_id, headers=mock_args.headers)   
    out, err = capsys.readouterr()
    assert out.replace("\n", "") == bcolors.FAIL + "Failed to delete mission {mission_id}. Please manually delete it".format(mission_id=mock_args.wrong_mission_id) + bcolors.ENDC

@pytest.fixture
def mock_get_map_positive():
    with patch("cogniceptshell.robot_actions.requests.get") as fake_resp:    
        fake_return_value = json.dumps({"data": [{"map_id": mock_args.map_ids[0]}]}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp
        
def test_get_map_positive(capsys, mock_get_map_positive):
    map_details = robot_actions.get_maps_from_robot_id(robot_id=mock_args.robot_id, headers=mock_args.headers)[0]
    assert map_details['map_id'] == mock_args.map_ids[0]

@pytest.fixture
def mock_get_map_negative():
    with patch("cogniceptshell.robot_actions.requests.get") as fake_resp:    
        fake_return_value = json.dumps({"message": "Invalid input"}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 400
        yield fake_resp
        
def test_get_map_negative(capsys, mock_get_map_negative):
    with pytest.raises(SystemExit):
        map_details = robot_actions.get_maps_from_robot_id(mock_args.robot_id, headers=mock_args.headers)
    out, err = capsys.readouterr()
    assert out.replace("\n", "") == bcolors.FAIL + "Error retrieving maps associated to robot {robot_id}".format(robot_id=mock_args.robot_id) + bcolors.ENDC

@pytest.fixture
def mock_get_map_image_positive():
    with patch("cogniceptshell.robot_actions.requests.get") as fake_resp:    
        fake_return_value = mock_args.b64_encoded_map_image
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp
        
def test_get_map_image_positive(mock_get_map_image_positive):
    map_image = robot_actions.get_map_image(map_id=mock_args.map_ids[0], headers=mock_args.headers)
    assert map_image == mock_args.map_image

@pytest.fixture
def mock_get_map_image_negative_400():
    with patch("cogniceptshell.robot_actions.requests.get") as fake_resp:    
        fake_return_value = mock_args.b64_encoded_map_image
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 400
        yield fake_resp
        
def test_get_map_image_negative_400(capsys, mock_get_map_image_negative_400):
    with pytest.raises(SystemExit):
        map_image = robot_actions.get_map_image(mock_args.map_ids[0], headers=mock_args.headers)
    out, err = capsys.readouterr()
    assert out.replace("\n", "") == bcolors.FAIL + "Error retrieving map {map_id}".format(map_id=mock_args.map_ids[0]) + bcolors.ENDC

@pytest.fixture
def mock_get_map_image_negative_decoding():
    with patch("cogniceptshell.robot_actions.requests.get") as fake_resp:    
        fake_return_value = "123"
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp
  
def test_get_map_image_negative_decoding(capsys, mock_get_map_image_negative_decoding):
    with pytest.raises(SystemExit):
        map_image = robot_actions.get_map_image(mock_args.map_ids[0], headers=mock_args.headers)
    out, err = capsys.readouterr()
    assert out.replace("\n", "") == "Failed to decode image file"

@pytest.fixture
def mock_create_map_positive():
    with patch("cogniceptshell.robot_actions.requests.post") as fake_resp:    
        fake_return_value = json.dumps({"map_id": mock_args.map_ids[0]}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp
  
def test_create_map_positive(capsys, mock_create_map_positive):
    new_map_id = robot_actions.create_map(mock_args.map_details, headers=mock_args.headers)
    assert new_map_id == mock_args.map_ids[0]

@pytest.fixture
def mock_create_map_negative():
    with patch("cogniceptshell.robot_actions.requests.post") as fake_resp:    
        fake_return_value = json.dumps({"message": "Invalid input"}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 400
        yield fake_resp

def test_create_map_negative(capsys, mock_create_map_negative):
    with pytest.raises(Exception) as excinfo:
        new_map_id = robot_actions.create_map(map_details=mock_args.map_details, headers=mock_args.headers)
    out, err = capsys.readouterr()
    assert str(excinfo.value) == bcolors.FAIL + "Error in creating map" + bcolors.ENDC
    
@pytest.fixture
def mock_delete_map_positive():
    with patch("cogniceptshell.robot_actions.requests.delete") as fake_resp:    
        fake_return_value = json.dumps({"map_id": mock_args.map_ids[0]}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp

def test_delete_map_positive(mock_delete_map_positive):
    delete_payload = robot_actions.delete_map(map_id=mock_args.map_ids[0], headers=mock_args.headers)
    assert delete_payload == mock_args.map_ids[0]

@pytest.fixture
def mock_delete_map_negative():
    with patch("cogniceptshell.robot_actions.requests.delete") as fake_resp:    
        fake_return_value = json.dumps({"message": "Invalid input"}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 400
        yield fake_resp

def test_delete_map_negative(capsys, mock_delete_map_negative):
    delete_payload = robot_actions.delete_map(map_id=mock_args.map_ids[0], headers=mock_args.headers)
    out, err = capsys.readouterr()
    assert out.replace("\n", "") == bcolors.FAIL + "Failed to delete map {map_id}. Please manually delete it".format(map_id=mock_args.map_ids[0]) + bcolors.ENDC
    
@pytest.fixture
def mock_get_schedules_positive():
    with patch("cogniceptshell.robot_actions.requests.get") as fake_resp:    
        fake_return_value = json.dumps({"schedule_id": mock_args.schedule_id, "robot_id": mock_args.robot_id}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp

def test_get_schedules_positive(capsys, mock_get_schedules_positive):
    schedule_details = robot_actions.get_schedules(mock_args.schedule_id, headers=mock_args.headers)
    assert schedule_details['schedule_id'] == mock_args.schedule_id

@pytest.fixture
def mock_get_schedules_negative():
    with patch("cogniceptshell.robot_actions.requests.get") as fake_resp:    
        fake_return_value = json.dumps({"message": "Invalid input"}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 400
        yield fake_resp

def test_get_schedules_negative(capsys, mock_get_schedules_negative):
    with pytest.raises(SystemExit):
        schedule_details = robot_actions.get_schedules(mock_args.wrong_schedule_id, headers=mock_args.headers)
    out, err = capsys.readouterr()
    assert out.replace("\n", "") == bcolors.FAIL + "Error in retrieving schedule {schedule_id}".format(schedule_id=mock_args.wrong_schedule_id) + bcolors.ENDC  
    
@pytest.fixture
def mock_create_schedule_positive():
    with patch("cogniceptshell.robot_actions.requests.post") as fake_resp:    
        fake_return_value = json.dumps({"schedule_id": mock_args.schedule_id}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp

def test_create_schedule_positive(capsys, mock_create_schedule_positive):
    new_schedule_id = robot_actions.create_schedule(mock_args.schedule_id, headers=mock_args.headers)
    assert new_schedule_id == mock_args.schedule_id

@pytest.fixture
def mock_create_schedule_negative():
    with patch("cogniceptshell.robot_actions.requests.post") as fake_resp:    
        fake_return_value = json.dumps({"message": "One of cron or timestamp are required"}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 400
        yield fake_resp

def test_create_schedule_negative(capsys, mock_create_schedule_negative):
    schedule_id = mock_args.schedule_id
    with pytest.raises(Exception) as excinfo:
        new_schedule_id = robot_actions.create_schedule(mock_args.schedule_details, headers=mock_args.headers)
    assert str(excinfo.value) == bcolors.FAIL + "Error in creating schedule. Error: {err}".format(err="One of cron or timestamp are required") + bcolors.ENDC 
   
@pytest.fixture
def mock_delete_schedule_positive():
    with patch("cogniceptshell.robot_actions.requests.delete") as fake_resp:    
        fake_return_value = json.dumps({"schedule_id": mock_args.schedule_id}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp

def test_delete_schedule_positive(capsys, mock_delete_schedule_positive):
    delete_payload = robot_actions.delete_schedule(schedule_id=mock_args.schedule_id, headers=mock_args.headers)
    assert delete_payload == mock_args.schedule_id

@pytest.fixture
def mock_delete_schedule_negative():
    with patch("cogniceptshell.robot_actions.requests.delete") as fake_resp:    
        fake_return_value = json.dumps({"message": "Invalid input"}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 400
        yield fake_resp

def test_delete_schedule_negative(capsys, mock_delete_schedule_negative):
    delete_payload = robot_actions.delete_schedule(schedule_id=mock_args.wrong_schedule_id, headers=mock_args.headers)
    out, err = capsys.readouterr()
    assert out.replace("\n", "") == bcolors.FAIL + "Failed to delete schedule {schedule_id}. Please manually delete it".format(schedule_id=mock_args.wrong_schedule_id) + bcolors.ENDC 
   
@pytest.fixture
def mock_get_property_by_id_positive():
    with patch("cogniceptshell.robot_actions.requests.get") as fake_resp:    
        fake_return_value = json.dumps({"property_id": mock_args.property_id, "property_code": mock_args.property_code}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp

def test_get_property_by_id_positive(capsys, mock_get_property_by_id_positive):
    property_details = robot_actions.get_property_by_id(mock_args.property_id, headers=mock_args.headers)
    assert property_details['property_id'] == mock_args.property_id

@pytest.fixture
def mock_get_property_by_id_negative():
    with patch("cogniceptshell.robot_actions.requests.get") as fake_resp:    
        fake_return_value = json.dumps({"message": "Invalid input"}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 400
        yield fake_resp

def test_get_property_by_id_negative(capsys, mock_get_property_by_id_negative):
    with pytest.raises(SystemExit):
        property_details = robot_actions.get_property_by_id(mock_args.wrong_property_id, headers=mock_args.headers)
    out, err = capsys.readouterr()
    assert out == bcolors.FAIL + "Error in retrieving property {property_id} of robot".format(property_id=mock_args.wrong_property_id) + bcolors.ENDC + "\n"
    print(out, err)

@pytest.fixture
def mock_get_property_by_filter_positive():
    with patch("cogniceptshell.robot_actions.requests.get") as fake_resp:    
        fake_return_value = json.dumps({"data": [{"property_id": mock_args.property_id, "property_code": mock_args.property_code}]}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp

def test_get_property_by_filter_positive(capsys, mock_get_property_by_filter_positive):
    filters = {"property_name": "My Site"}
    property_details = robot_actions.get_property_by_filter(filters, headers=mock_args.headers)[0]
    
    assert property_details['property_id'] == mock_args.property_id

@pytest.fixture
def mock_get_property_by_filter_negative():
    with patch("cogniceptshell.robot_actions.requests.get") as fake_resp:    
        fake_return_value = json.dumps({"message": "Invalid input"}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 400
        yield fake_resp

def test_get_property_by_filter_negative(capsys, mock_get_property_by_filter_negative):
    filters = {"property_name": "My Site"}
    
    with pytest.raises(SystemExit):
        property_details = robot_actions.get_property_by_filter(filters, headers=mock_args.headers)[0]
    out, err = capsys.readouterr()
    assert out == bcolors.FAIL + "Error in retrieving property of robot" + bcolors.ENDC + "\n"
    print(out, err)

@pytest.fixture
def mock_create_property_positive():
    with patch("cogniceptshell.robot_actions.requests.post") as fake_resp:    
        fake_return_value = json.dumps({"property_id": mock_args.property_id}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp

def test_create_property_positive(capsys, mock_create_property_positive):
    new_property_id = robot_actions.create_property(mock_args.property_details, headers=mock_args.headers)
    assert new_property_id == mock_args.property_id

@pytest.fixture
def mock_create_property_negative():
    with patch("cogniceptshell.robot_actions.requests.post") as fake_resp:    
        fake_return_value = json.dumps({"message": "Invalid input"}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 400
        yield fake_resp

def test_create_property_negative(capsys, mock_create_property_negative):
    with pytest.raises(Exception) as excinfo:
        new_property_id = robot_actions.create_property(mock_args.property_details, headers=mock_args.headers)
    assert str(excinfo.value) == bcolors.FAIL + "Error in creating property for new organization. Error: {err}".format(err="Invalid input") + bcolors.ENDC 

@pytest.fixture
def mock_delete_property_positive():
    with patch("cogniceptshell.robot_actions.requests.delete") as fake_resp:    
        fake_return_value = json.dumps({"property_id": mock_args.property_id}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp

def test_delete_property_positive(capsys, mock_delete_property_positive):
    delete_payload = robot_actions.delete_property(property_id=mock_args.property_id, headers=mock_args.headers)
    assert delete_payload == mock_args.property_id

@pytest.fixture
def mock_delete_property_negative():
    with patch("cogniceptshell.robot_actions.requests.delete") as fake_resp:    
        fake_return_value = json.dumps({"message": "Invalid input"}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 400
        yield fake_resp

def test_delete_property_negative(capsys, mock_delete_property_negative):
    delete_payload = robot_actions.delete_property(property_id=mock_args.wrong_property_id, headers=mock_args.headers)
    out, err = capsys.readouterr()
    assert out.replace("\n", "") == bcolors.FAIL + "Failed to delete property {property_id}. Please manually delete it".format(property_id=mock_args.wrong_property_id) + bcolors.ENDC
    print(out, err)

@pytest.fixture
def mock_switch_org_positive():
    with patch("cogniceptshell.robot_actions.requests.post") as fake_resp:    
        fake_return_value = json.dumps({"access_token": "123123", "refresh_token": "123123"}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 200
        yield fake_resp

def test_switch_org_positive(capsys, mock_switch_org_positive):
    new_access_token = robot_actions.switch_org(mock_args.new_org_id, headers=mock_args.headers)
    assert new_access_token == "123123"

@pytest.fixture
def mock_switch_org_negative():
    with patch("cogniceptshell.robot_actions.requests.post") as fake_resp:    
        fake_return_value = json.dumps({"message": "Invalid input"}).encode()
        fake_resp.return_value.content = fake_return_value
        fake_resp.return_value.status_code = 400
        yield fake_resp

def test_switch_org_negative(capsys, mock_switch_org_negative):
    with pytest.raises(SystemExit):
        new_access_token = robot_actions.switch_org(mock_args.new_org_id, headers=mock_args.headers)
    out, err = capsys.readouterr()
    assert out == bcolors.FAIL + "Error in switching organization" + bcolors.ENDC + "\n"
    print(out, err)

def test_move_no_robot_details(capsys):
    args_without_robot_details = MockArgs()
    args_without_robot_details.robot_id = None
    args_without_robot_details.robot_code = None
    with pytest.raises(SystemExit):
        robot_actions.move(args_without_robot_details)
    out, err = capsys.readouterr()
    assert out.replace("\n", "") == 'Please provide a robot id or robot code'
    print(out, err)

def test_move_no_old_org_details(capsys):
    args_without_old_organization_details = MockArgs()
    args_without_old_organization_details.old_org_code = None
    args_without_old_organization_details.old_org_id = None
    with pytest.raises(SystemExit):
        robot_actions.move(args_without_old_organization_details)
    out, err = capsys.readouterr()
    assert out.replace("\n", "") == "Please provide the old organization id or code you wish to move the robot from"
    print(out, err)

def test_move_no_new_org_details(capsys):
    args_without_new_organization_details = MockArgs()
    args_without_new_organization_details.new_org_code = None
    args_without_new_organization_details.new_org_id = None
    with pytest.raises(SystemExit):
        robot_actions.move(args_without_new_organization_details)
    out, err = capsys.readouterr()
    assert out.replace("\n", "") == "Please provide the new organization id or code you wish to move the robot to"
    print(out, err)

def test_move_both_robot_details(capsys):
    args_with_both_robot_details = MockArgs()
    with pytest.raises(SystemExit):
        robot_actions.move(args_with_both_robot_details)
    out, err = capsys.readouterr()
    assert out.replace("\n", "") == "Please only provide either robot_id or robot_code"
    print(out, err)

def test_move_both_old_org_details(capsys):
    args_with_both_old_org_details = MockArgs()
    args_with_both_old_org_details.robot_id = None
    with pytest.raises(SystemExit):
        robot_actions.move(args_with_both_old_org_details)
    out, err = capsys.readouterr()
    assert out.replace("\n", "") == "Please only provide organization details either as id or org_code"
    print(out, err)

def test_move_both_new_org_details(capsys):
    args_with_both_new_org_details = MockArgs()
    args_with_both_new_org_details.robot_id = None
    args_with_both_new_org_details.old_org_id = None
    with pytest.raises(SystemExit):
        robot_actions.move(args_with_both_new_org_details)
    out, err = capsys.readouterr()
    assert out.replace("\n", "") == "Please only provide organization details either as id or org_code"
    print(out, err)
