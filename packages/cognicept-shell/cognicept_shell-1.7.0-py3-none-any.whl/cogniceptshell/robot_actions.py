# coding=utf8
# Copyright 2023 Cognicept Systems
# Author: Kenneth Chow (kenneth.chow@kabam.ai)
# --> RobotActions class handles on demand custom robot actions on cognicept-shell

import getpass
import json
import requests
import jwt
import io 
import base64
from cogniceptshell.common import bcolors
from cogniceptshell.configuration import Configuration
from cogniceptshell.agent_life_cycle import AgentLifeCycle

class RobotActions:
    """
    A class to manage robot
    ...

    Parameters
    ----------
    None

    Methods
    -------
    login(username, password):
        API call to login the user to smart+

    get_organization(org_id, headers):
        API call to retrieve organization details

    get_robot(robot_id, org_id, headers):
        API call to retrieve robot details
    
    create_robot(robot_details, headers):
        API call to create robot

    get_robot_missions(robot_id, headers):
        API call to retrieve missions associated with robot_id
    
    get_mission_instances(mission_id, headers):
        API call to retrieve instances associated with mission_id
    
    create_mission(mission_details, headers):
        API call to create mission
    
    create_waypoint(waypoint_details, headers):
        API call to create waypoint

    get_map(map_id, headers):
        API call to retrieve map 

    create_map(map_details, headers):
        API call to create map

    get_schedules(schedule_id, headers):
        API call to retrieve schedule

    create_schedule(schedule_details, headers):
        API call to create schedule

    get_property_by_id(property_id, headers):
        API call to retrieve property by property_id

    get_property_by_filter(filters, headers):
        API call to retrieve property by filters

    create_property(property_details, headers):
        API call to create property

    switch_org(org_id, headers):
        API call to switch organizations

    rollback(created_data, headers):
        Deletes any created data if an error occurs 
    
    move(args):
        Main entry point for moving robots from one org to another

    """

    def login(self, username, password):
        login_base_uri = self.api_uri + "user/login"
        login_resp = requests.post(login_base_uri, json={"username": str(username), "password": str(password)}, timeout=5)
        if json.loads(login_resp.content.decode()).get('message', '') == "Username and password combination not valid":
            print(bcolors.FAIL + "Error in logging in: Wrong credentials" + bcolors.ENDC)
            raise SystemExit(1)
        return json.loads(login_resp.content.decode())['access_token']

    def mfa_verfication(self, auth_key, headers):
        mfa_verification_base_uri = self.api_uri + "user/mfa/verify"
        otp_trial = 3
        loop = True
        while loop:
            if otp_trial == 0:
                key = auth_key
                loop = False
            else:
                otp = getpass.getpass('OTP from Authenticator: ')
                x = requests.post(mfa_verification_base_uri, headers=headers, json={'otp': otp})
                if 'access_token' not in x.json():
                    print('Invalid OTP! Please try again...')
                else:
                    key = x.json()["access_token"]
                    loop = False
            otp_trial -= 1
        return key
    
    def get_organization_by_id(self, org_id, headers):
        org_base_uri = self.api_uri + "organization/"
        get_org_uri = org_base_uri + '?filter={{"organization_id":"{org_id}"}}'.format(org_id=org_id)
        get_org_resp = requests.get(get_org_uri, headers=headers, timeout=5)
        json_resp = json.loads(get_org_resp.content.decode())
        if get_org_resp.status_code != 200 or (isinstance(json_resp.get('data', ''), dict) and 'psycopg2.errors' in json_resp['data'].get('Message', '')):
             print(bcolors.FAIL + "Error in getting organization {org_id}".format(org_id=org_id) + bcolors.ENDC)
             raise SystemExit(1)
        elif len(json.loads(get_org_resp.content.decode())['data']) == 0:
             print(bcolors.FAIL + "No such organization {org_id}".format(org_id=org_id) + bcolors.ENDC)
             raise SystemExit(1)
        return json.loads(get_org_resp.content.decode())['data'][0]
    
    def get_organization_by_org_code(self, org_code, headers):
        org_base_uri = self.api_uri + "organization/"
        get_org_uri = org_base_uri + '?filter={{"organization_code":"{org_code}"}}'.format(org_code=org_code)
        get_org_resp = requests.get(get_org_uri, headers=headers, timeout=5)
        if get_org_resp.status_code != 200:
             print(bcolors.FAIL + "Error in getting organization" + bcolors.ENDC)
             raise SystemExit(1)
        elif len(json.loads(get_org_resp.content.decode())['data']) == 0:
             print(bcolors.FAIL + "No such organization {org_code}".format(org_code=org_code) + bcolors.ENDC)
             raise SystemExit(1)           
        return json.loads(get_org_resp.content.decode())['data'][0]

    def get_robot_by_id(self, robot_id, org_id, headers):
        get_robot_uri = self.api_uri + "robot/organization?robot_id={robot_id}&organization_id={org_id}".format(robot_id=robot_id, org_id=org_id)
        get_robot_resp = requests.get(get_robot_uri, headers=headers, timeout=5)
        if get_robot_resp.status_code != 200:
            print(bcolors.FAIL + "Error in retrieving robot" + bcolors.ENDC)
            raise SystemExit(1)
        elif len(get_robot_resp.content.decode()) == 0 or json.loads(get_robot_resp.content.decode()).get('message', '') == 'Bad request. Invalid input':
            print(bcolors.FAIL + "No such robot {robot_id} in organization {org_id}".format(robot_id=robot_id, org_id=org_id) + bcolors.ENDC)
            raise SystemExit(1)
        return json.loads(get_robot_resp.content.decode())

    def get_robot_by_code(self, robot_code, org_code, headers):
        get_robot_uri = self.api_uri + "robot/organization_code?robot_code={robot_code}&organization_code={org_code}".format(robot_code=robot_code, org_code=org_code)
        get_robot_resp = requests.get(get_robot_uri, headers=headers, timeout=5)
        if get_robot_resp.status_code != 200:
             print(bcolors.FAIL + "Error in retrieving robot. Message: {err}".format(err=json.loads(get_robot_resp.content.decode()).get('message', '')) + bcolors.ENDC)
             raise SystemExit(1)
        elif len(json.loads(get_robot_resp.content.decode())) == 0 or json.loads(get_robot_resp.content.decode()).get('message', '') == 'Bad request. Invalid input':
            print(bcolors.FAIL + "No such robot {robot_code} in organization {org_code}".format(robot_code=robot_code, org_code=org_code) + bcolors.ENDC)
            raise SystemExit(1)
        return json.loads(get_robot_resp.content.decode())

    def create_robot(self, robot_details, headers):
        create_robot_uri = self.api_uri + "robot/"
        create_robot_resp = requests.post(create_robot_uri, json=robot_details, headers=headers, timeout=5)
        if create_robot_resp.status_code != 200:
             raise Exception(bcolors.FAIL + "Error in creating robot" + bcolors.ENDC)
        return json.loads(create_robot_resp.content.decode())['robot_id']

    def delete_robot(self, robot_id, organization_id, headers):
        delete_robot_uri = self.api_uri + "robot/organization"
        delete_robot_resp = requests.delete(delete_robot_uri, params={"robot_id": "{robot_id}".format(robot_id=robot_id), "organization_id": "{organization_id}".format(organization_id=organization_id)}, headers=headers, timeout=5)
        if delete_robot_resp.status_code != 200:
             print(bcolors.FAIL + "Error in deleting robot {robot_id}. Please manually delete it".format(robot_id=robot_id) + bcolors.ENDC)
             return None
        return json.loads(delete_robot_resp.content.decode()).get('message', None)

    def get_robot_missions(self, robot_id, headers):
        mission_base_uri = self.api_uri + "mission/"
        get_mission_uri = mission_base_uri + '?filter={{"robot_id": "{robot_id}"}}'.format(robot_id=robot_id)
        get_mission_resp = requests.get(get_mission_uri, headers=headers, timeout=5)
        if get_mission_resp.status_code != 200:
             print(bcolors.FAIL + "Error in retrieving missions" + bcolors.ENDC)
             raise SystemExit(1)
        mission_list = json.loads(get_mission_resp.content.decode())['data']
        return mission_list
    
    def create_mission(self, mission_details, headers, tries=0):
        create_mission_uri = self.api_uri + "mission/"
        create_mission_resp = requests.post(create_mission_uri, json=mission_details, headers=headers, timeout=5)
        if create_mission_resp.status_code != 200:
            if 'UniqueViolation' in json.loads(create_mission_resp.content.decode())['message'] and tries < 50: 
                return self.create_mission(mission_details, headers, tries)
            else:
                raise Exception(bcolors.FAIL + "Error in creating mission" + bcolors.ENDC)
        return json.loads(create_mission_resp.content.decode())['mission_id']
    
    def delete_mission(self, mission_id, headers):
        delete_mission_uri = self.api_uri + "mission/{mission_id}".format(mission_id=mission_id)
        delete_mission_resp = requests.delete(delete_mission_uri, headers=headers, timeout=5)
        if delete_mission_resp.status_code != 200:
            print(bcolors.FAIL + "Failed to delete mission {mission_id}. Please manually delete it".format(mission_id=mission_id) + bcolors.ENDC)
            return None
        else:
            print("successfully deleted mission {mission_id}".format(mission_id=mission_id))
            return json.loads(delete_mission_resp.content.decode()).get('mission_id', None)
    
    def get_mission_instances(self, mission_id, headers):
        mission_instance_base_uri = self.api_uri + "mission-instance/"
        get_mission_instance_uri = mission_instance_base_uri + '?filter={{"mission_id": "{mission_id}"}}'.format(mission_id=mission_id)
        get_mission_instance_resp = requests.get(get_mission_instance_uri, headers=headers, timeout=5)
        if get_mission_instance_resp.status_code != 200:
            print(bcolors.FAIL + "Error retrieving mission instance" + bcolors.ENDC)
            raise SystemExit(1)
        return json.loads(get_mission_instance_resp.content.decode())['data']

    def create_mission_instance(self, mission_instance_details, headers):
        create_mission_instance_uri = self.api_uri + "mission-instance/"
        create_mission_instance_resp = requests.post(create_mission_instance_uri, json=mission_instance_details, headers=headers)
        if create_mission_instance_resp.status_code != 200:
            raise Exception(bcolors.FAIL + "Error in creating mission instance" + bcolors.ENDC)
        return json.loads(create_mission_instance_resp.content.decode())['mission_instance_id']

    def delete_mission_instance(self, mission_instance_id, headers):
        delete_mission_instance_uri = self.api_uri + "mission-instance/" + str(mission_instance_id)
        delete_mission_instance_resp = requests.delete(delete_mission_instance_uri, headers=headers, timeout=5)
        if delete_mission_instance_resp.status_code != 200:
            print(bcolors.FAIL + "Failed to delete mission_instance {mission_instance_id}. Please manually delete it".format(mission_instance_id=mission_instance_id) + bcolors.ENDC)
        else:
            print("successfully deleted mission_instance {mission_instance_id}".format(mission_instance_id=mission_instance_id))
    
    def get_waypoints_from_map_id(self, map_id, headers):
        waypoint_base_uri = self.api_uri + "waypoint/"
        get_waypoint_uri = waypoint_base_uri + '?filter={{"map_id": "{map_id}"}}'.format(map_id=map_id)
        get_waypoint_resp = requests.get(get_waypoint_uri, headers=headers, timeout=5)
        if get_waypoint_resp.status_code != 200:
            print(bcolors.FAIL + "Error retrieving waypoint" + bcolors.ENDC)
            raise SystemExit(1)
        return json.loads(get_waypoint_resp.content.decode())['data']

    def create_waypoint(self, waypoint_details, headers):
        waypoint_base_uri = self.api_uri + "waypoint/"
        create_waypoint_uri = waypoint_base_uri
        create_waypoint_resp = requests.post(create_waypoint_uri, json=waypoint_details, headers=headers, timeout=5)
        if create_waypoint_resp.status_code != 200:
            raise Exception(bcolors.FAIL + "Error in creating waypoint" + bcolors.ENDC)
        return json.loads(create_waypoint_resp.content.decode())['waypoint_id']
    
    def delete_waypoint(self, waypoint_id, headers):
        delete_waypoint_uri = self.api_uri + "waypoint/"
        delete_waypoint_uri += str(waypoint_id)
        delete_waypoint_resp = requests.delete(delete_waypoint_uri, headers=headers, timeout=5)
        if delete_waypoint_resp.status_code != 200:
            print(bcolors.FAIL + "Failed to delete waypoint {waypoint_id}. Please manually delete it".format(waypoint_id=waypoint_id) + bcolors.ENDC)
        else:
            print("successfully deleted waypoint {waypoint_id}".format(waypoint_id=waypoint_id))
    
    def get_map_image(self, map_id, headers):
        map_base_uri = self.api_uri + "map/"
        get_map_uri = map_base_uri + "{map_id}".format(map_id=map_id)
        get_map_resp = requests.get(get_map_uri, headers=headers, timeout=5)
        if get_map_resp.status_code != 200:
            print(bcolors.FAIL + "Error retrieving map {map_id}".format(map_id=map_id) + bcolors.ENDC)
            raise SystemExit(1)
        try:
            image_file = io.BytesIO(get_map_resp.content)
            image_data = image_file.read()
            b64_string = base64.b64encode(image_data).decode('utf-8')
        except Exception as err:
            print("Failed to decode image file")
            raise SystemExit(1)
        
        # remove padding
        last_index = len(b64_string) - 1
        while b64_string[last_index] == "=":
            b64_string = b64_string[:-1]
            last_index -= 1
        return b64_string
    
    def get_maps_from_robot_id(self, robot_id, headers):
        map_base_uri = self.api_uri + "map/"
        get_map_uri = map_base_uri + '?filter={{"robot_id":"{robot_id}"}}'.format(robot_id=robot_id)
        get_map_resp = requests.get(get_map_uri, headers=headers, timeout=5)
        if get_map_resp.status_code != 200:
            print(bcolors.FAIL + "Error retrieving maps associated to robot {robot_id}".format(robot_id=robot_id) + bcolors.ENDC)
            raise SystemExit(1)
        return json.loads(get_map_resp.content.decode())['data']
    
    def create_map(self, map_details, headers):
        create_map_uri = self.api_uri + "map/"
        create_map_resp = requests.post(create_map_uri, json=map_details, headers=headers, timeout=5)
        if create_map_resp.status_code != 200:
            raise Exception(bcolors.FAIL + "Error in creating map" + bcolors.ENDC)
        return json.loads(create_map_resp.content.decode())['map_id']

    def delete_map(self, map_id, headers):
        delete_map_uri = self.api_uri + "map/"
        delete_map_uri += str(map_id)
        delete_map_resp = requests.delete(delete_map_uri, headers=headers, timeout=5)
        if delete_map_resp.status_code != 200:
            print(bcolors.FAIL + "Failed to delete map {map_id}. Please manually delete it".format(map_id=map_id) + bcolors.ENDC)
            return None
        else:
            print("successfully deleted map {map_id}".format(map_id=map_id))
            return json.loads(delete_map_resp.content.decode()).get('map_id', None)

    def get_schedules(self, schedule_id, headers):
        schedule_base_uri = self.api_uri + "schedule/"
        get_schedule_uri = schedule_base_uri + 'metadata/{schedule_id}'.format(schedule_id=schedule_id)
        get_schedule_resp = requests.get(get_schedule_uri, headers=headers, timeout=5)
        if get_schedule_resp.status_code != 200:
            print(bcolors.FAIL + "Error in retrieving schedule {schedule_id}".format(schedule_id=schedule_id) + bcolors.ENDC)
            raise SystemExit(1)
        return json.loads(get_schedule_resp.content.decode())
    
    def create_schedule(self, schedule_details, headers):
        create_schedule_uri = self.api_uri + "schedule/"
        create_schedule_resp = requests.post(create_schedule_uri, json=schedule_details, headers=headers, timeout=5)
        if create_schedule_resp.status_code != 200:
            raise Exception(bcolors.FAIL + "Error in creating schedule. Error: {err}".format(err=json.loads(create_schedule_resp.content.decode()).get('message', '')) + bcolors.ENDC)
        return json.loads(create_schedule_resp.content.decode())['schedule_id']
    
    def delete_schedule(self, schedule_id, headers):
        delete_schedule_uri = self.api_uri + "schedule/" + str(schedule_id)
        delete_schedule_resp = requests.delete(delete_schedule_uri, headers=headers, timeout=5)
        if delete_schedule_resp.status_code != 200:
            print(bcolors.FAIL + "Failed to delete schedule {schedule_id}. Please manually delete it".format(schedule_id=schedule_id) + bcolors.ENDC)
            return None
        else:
            print("successfully deleted schedule {schedule_id}".format(schedule_id=schedule_id))
            return json.loads(delete_schedule_resp.content.decode()).get('schedule_id', None)
    
    def get_property_by_id(self, property_id, headers):
        property_base_uri = self.api_uri + "property/"
        get_property_uri = property_base_uri + "{property_id}".format(property_id=property_id)
        get_property_resp = requests.get(get_property_uri, headers=headers, timeout=5)
        if get_property_resp.status_code != 200:
            print(bcolors.FAIL + "Error in retrieving property {property_id} of robot".format(property_id=property_id) + bcolors.ENDC)
            raise SystemExit(1)
        return json.loads(get_property_resp.content.decode())
    
    def get_property_by_filter(self, filters, headers):
        property_base_uri = self.api_uri + "property/"
        filter_string = '?filter={'
        index = 0
        for key, value in filters.items():
            filter_string += '"{key}": "{value}"'.format(key=key, value=value)
            if index != len(filters) - 1:
                filter_string += ', '
            index += 1
        filter_string += '}'
        
        get_property_uri = property_base_uri + filter_string
        get_property_resp = requests.get(get_property_uri, headers=headers, timeout=5)
        if get_property_resp.status_code != 200:
            print(bcolors.FAIL + "Error in retrieving property of robot" + bcolors.ENDC)
            raise SystemExit(1)
        get_property_data = json.loads(get_property_resp.content.decode())['data']
        return get_property_data
    
    def create_property(self, property_details, headers):
        property_base_uri = self.api_uri + "property/"
        create_property_resp = requests.post(property_base_uri, json=property_details, headers=headers, timeout=5)
        if create_property_resp.status_code != 200: 
            raise Exception(bcolors.FAIL + "Error in creating property for new organization. Error: {err}"
                            .format(err=json.loads(create_property_resp.content.decode()).get('message', None)) + bcolors.ENDC)
        return json.loads(create_property_resp.content.decode())['property_id'] 

    def delete_property(self, property_id, headers):
        delete_property_uri = self.api_uri + "property/{property_id}".format(property_id=property_id)
        delete_property_resp = requests.delete(delete_property_uri, headers=headers, timeout=5)
        if delete_property_resp.status_code != 200:
            print(bcolors.FAIL + "Failed to delete property {property_id}. Please manually delete it".format(property_id=property_id) + bcolors.ENDC)
            return None
        else:
            print("successfully deleted property {property_id}".format(property_id=property_id))
            return json.loads(delete_property_resp.content.decode()).get('property_id', None)
        
    def get_robot_config(self, org_id, robot_id, headers):
        get_config_uri = self.api_uri + f'robot_config/config/{org_id}/{robot_id}'
        get_config_resp = requests.get(get_config_uri, headers=headers, timeout=5)
        if get_config_resp.status_code != 200:
            print(get_config_resp.content)
            print(bcolors.FAIL + "Failed to fetch new robot config file" + bcolors.ENDC)
            return None
        return json.loads(get_config_resp.content.decode())

    def switch_org(self, org_id, headers):
        switch_org_uri = self.api_uri + "user/switch_org"
        switch_org_payload = {
             'organization_id': org_id,
             "blacklist": True
        }   
        switch_org_resp = requests.post(switch_org_uri, json=switch_org_payload, headers=headers, timeout=5)
        if switch_org_resp.status_code != 200:
            print(bcolors.FAIL + "Error in switching organization" + bcolors.ENDC)
            raise SystemExit(1)
        new_access_token = json.loads(switch_org_resp.content.decode())['access_token']
        return new_access_token
    
    def rollback(self, created_data, headers):
        for key, value in created_data.items():
            if key == 'property_id':
                self.delete_property(value, headers)
            if key == 'robot':
                if value.get('robot_id', None):
                    self.delete_robot(robot_id=value.get('robot_id'), organization_id=value.get('organization_id', ''), headers=headers)
            if key == 'missions':
                for mission_id in value:
                    self.delete_mission(mission_id, headers=headers)
            if key == 'waypoints':
                for waypoint_id in value:
                    self.delete_waypoint(waypoint_id, headers=headers)
            if key == 'schedules':
                for schedule_id in value:
                    self.delete_schedule(schedule_id, headers=headers)
            if key == 'maps':
                for map_id in value:
                    if map_id:
                        self.delete_map(map_id, headers=headers)
            if key == 'mission_instances':
                for mission_instance_id in value:
                    self.delete_mission_instance(mission_instance_id, headers=headers)

    def move(self, args):
        """
        Main entrypoint to move a robot from one organization to another.

                Parameters:
                        args: populated argument namespace returned by `argparse.parse_args()`
        """
        if not hasattr(args.config, "config") or (hasattr(args.config, "config") and not args.config.config.get("COGNICEPT_USER_API_URI", None)): 
            print(bcolors.FAIL + "Failed to load API URL. Please contact our tech support team for assistance" + bcolors.ENDC)
            raise SystemExit(1)

        self.api_uri = args.config.config.get("COGNICEPT_USER_API_URI")

        if "/v1" in self.api_uri:
            print(bcolors.FAIL + "The cognicept move command is not available with version 1 of cognicept's api. Please contact our tech support team for assistance. " + bcolors.ENDC)
            raise SystemExit(1)
        
        if args.robot_id is None and args.robot_code is None:
            print("Please provide a robot id or robot code")
            raise SystemExit(1)
        elif args.old_org_id is None and args.old_org_code is None:
            print("Please provide the old organization id or code you wish to move the robot from")
            raise SystemExit(1)
        elif args.new_org_id is None and args.new_org_code is None:
            print("Please provide the new organization id or code you wish to move the robot to")
            raise SystemExit(1)
            
        if args.robot_id and args.robot_code:
            print("Please only provide either robot_id or robot_code")
            raise SystemExit(1)

        if (args.old_org_code and args.old_org_id) or (args.new_org_code and args.new_org_id):
            print("Please only provide organization details either as id or org_code")
            raise SystemExit(1)
        
        skip_schedule = False
        skip_map = False
        skip_waypoint = False
        if args.skip:
            arguments = args.skip
            for argument in arguments:
                if argument not in ['schedule', 'map', 'waypoint']:
                    print('Arguments for skip are invalid. Accepted arguments are schedule, map and waypoint')
                    raise SystemExit(1)
                if argument == 'schedule':
                    skip_schedule = True
                elif argument == 'map':
                    skip_map = True
                else:
                    skip_waypoint = True
    
        print(bcolors.HEADER + "Please login to your smart+ account to perform this operation" + bcolors.ENDC)

        username = input('Username: ')
        password = getpass.getpass('Password: ')

        access_token = self.login(username=username, password=password)
        if access_token is None:
             print(bcolors.FAIL + "Error in loading credentials. Please initialise the robot by running robot init" + bcolors.ENDC)
             raise SystemExit(1)
        headers = {
            'Authorization': 'Bearer ' + access_token
        }


        decode_json = jwt.decode(access_token, verify=False, algorithms=["HS256"])
        # False means 2FA Verification is activated by the user
        if decode_json['user_claims']['authorized'] == False:
            new_key = self.mfa_verfication(auth_key=access_token, headers=headers)
            if new_key == access_token:    
                print("Failed to move robot: Invalid OTP entered 3 times")
                raise SystemExit(1)
            else:
                access_token=new_key
                headers = {
                    'Authorization': 'Bearer ' + access_token
                }
        

        print(bcolors.OKBLUE + "Successfully logged in! Proceeding to fetch robot data..." + bcolors.ENDC)

        #### Check if both organizations exist ####
        if args.old_org_id:
            old_org_data = self.get_organization_by_id(org_id=args.old_org_id, headers=headers)
            args.old_org_code = old_org_data['organization_code']
        else:
            old_org_data = self.get_organization_by_org_code(org_code=args.old_org_code, headers=headers)
            args.old_org_id = old_org_data['organization_id']
        
        if args.new_org_id:
            new_org_data = self.get_organization_by_id(org_id=args.new_org_id, headers=headers)
            args.new_org_code = new_org_data['organization_code']
        else:
            new_org_data = self.get_organization_by_org_code(org_code=args.new_org_code, headers=headers)
            args.new_org_id = new_org_data['organization_id']


        # Switch to old_org_id if the default logged in org is not old_org_id #
        access_token = self.switch_org(args.old_org_id, headers=headers)
        headers = {
            'Authorization': 'Bearer ' + access_token
        }

        #### Check if robot exists in old organization ####
        if args.robot_id:
            old_robot_data = self.get_robot_by_id(robot_id=args.robot_id, org_id=args.old_org_id, headers=headers)
            args.robot_code = old_robot_data.get('robot_code', '')
        else:
            old_robot_data = self.get_robot_by_code(robot_code=args.robot_code, org_code=args.old_org_code, headers=headers)
            args.robot_id = old_robot_data.get('robot_id', '')

        print(bcolors.OKBLUE + "Successfully retrieved the old robot. Trying to move the robot to the new organization..." + bcolors.ENDC)

        #### Retrieve Missions associated with robot in old organization #####
        old_mission_list = self.get_robot_missions(robot_id=args.robot_id, headers=headers)

        #### Retrieve all maps associated with robot and waypoints associated to maps - including those not associated to a mission #### 
        map_dict = {}
        waypoint_dict = {}

        if not skip_map:
            maps = self.get_maps_from_robot_id(robot_id=args.robot_id, headers=headers)
            for map in maps:
                map_id = map.get('map_id', None)
                map_image = self.get_map_image(map_id, headers=headers)
                map['map_image'] = 'data:image/png;base64,' + str(map_image)
                if map_id is not None:
                    map_dict[map_id] = map
                
                if not skip_waypoint:
                    waypoints = self.get_waypoints_from_map_id(map_id, headers=headers)
                    for waypoint in waypoints:
                        waypoint_id = waypoint.get('waypoint_id', '')
                        waypoint_dict[waypoint_id] = waypoint

        #### Retrieve mission instances and schedules associated with robot in old organization #####
        if not skip_schedule:
            for mission in old_mission_list:
                mission_id = mission['mission_id']
                schedules = mission['schedules']
        
                mission_instances = self.get_mission_instances(mission_id=mission_id, headers=headers)
                mission_instances_without_schedules = []
                mission_instances_with_schedules = []
                
                if len(mission_instances) > 0 and mission_instances is not None:
                    mission_instances_dict = {}
                    for mission_instance in mission_instances:
                        schedule_id = mission_instance['schedule_id']
                        if schedule_id is None:
                            mission_instances_without_schedules.append(mission_instance)
                        else:
                            mission_instances_dict[schedule_id] = mission_instance
                    mission['schedule_to_mission_instance_dict'] = mission_instances_dict  
                    mission['mission_instances_without_schedules'] = mission_instances_without_schedules

                for index, schedule in enumerate(schedules):
                    schedule_id = schedule['schedule_id']
                    schedules[index] = self.get_schedules(schedule_id=schedule_id, headers=headers)
               
        #### Retrieve property id ####
        old_property_id = old_robot_data['property_id']
        old_property_data = self.get_property_by_id(property_id=old_property_id, headers=headers)

        new_property_id = None
        if old_property_data['phone_number'] is not None and old_property_data is not None:
            # Assumption - phone number and address are unique identifiers of a property 
            # if the property exists within the new organization then use that property id. Else create a new property
            check_property_data = self.get_property_by_filter(filters={"phone_number": old_property_data['phone_number'], "address": old_property_data['address']}, headers=headers)
            if len(check_property_data) == 1:
                new_property_id = check_property_data['data'][0]['property_id']
    

        #### Switch to new organization ####
        new_access_token = self.switch_org(args.new_org_id, headers)
        headers['Authorization'] = 'Bearer ' + new_access_token
        
        newly_created_data = {}

        try:
            #### Create property in new organization - if required ####
            if new_property_id is None:
                old_property_data.pop('created_at', None)
                old_property_data.pop('modified_at', None)
                old_property_data.pop('is_default', None)
                old_property_data.pop('property_id', None)
                old_property_data.pop('is_deleted', None)
            
                new_property_id = self.create_property(property_details=old_property_data, headers=headers)
                newly_created_data['property_id'] = new_property_id

            #### Create robot in new organization ####
            # Modify the data to create the robot in the new organization
            old_robot_data.pop("robot_id", None)
            old_robot_data.pop("pilot_config", None)
            old_robot_data.pop("robot_code", None)
            old_robot_data.pop("modified_at", None)
            old_robot_data.pop("robot_url", None)
            old_robot_data.pop("is_deleted", None)
            old_robot_data.pop("last_heartbeat_at", None)
            old_robot_data.pop("last_health_update", None)
            old_robot_data.pop("model_code", None)
            old_robot_data.pop("organization_id", None)
            old_robot_data.pop("status_details", None)
            old_robot_data.pop("adapter_url", None)
            old_robot_data.pop("aws_role_id", None)
            old_robot_data.pop("aws_channel_arn", None)
            
            old_robot_data['status'] = "Offline"
            old_robot_data['property_id'] = new_property_id

            # Remove any keys in robot data with value as None #
            delete_keys = []
            for key, value in old_robot_data.items():
                if value is None or value == 'None':
                    delete_keys.append(key)
            for key in delete_keys:
                old_robot_data.pop(key)
            
            # oem_id is required even tho it is null
            if old_robot_data.get('oem_id', None) is None: 
                old_robot_data['oem_id'] = None

            new_robot_id = self.create_robot(robot_details=old_robot_data, headers=headers)
            newly_created_data['robot'] = {
                "robot_id": new_robot_id,
                "organization_id": args.new_org_id
            }
            
            print(bcolors.OKBLUE + "Porting over robot details..." + bcolors.ENDC)

            #### Create maps ####     
            map_count = 0
            to_delete_map_id = []
            old_to_new_map_dict = {}
            for map_id, map_data in map_dict.items():
                # Prep data for creating map
                old_map_id = map_data.pop('map_id', None)
                to_delete_map_id.append(old_map_id)
                
                map_data['robot_id'] = new_robot_id
                new_map_id = self.create_map(map_details=map_data, headers=headers) 
                old_to_new_map_dict[map_id] = new_map_id
                if new_map_id is not None:
                        maps = newly_created_data.get('maps', [])
                        maps.append(new_map_id)
                        map_count += 1
                
                # log created map ids in case of rollback
                maps = newly_created_data.get('maps', [])
                maps.append(new_map_id)
                newly_created_data['maps'] = maps
                     
            #### Create waypoints - alternative ####
            waypoint_count = 0
            to_delete_waypoint_id = []
            for waypoint_id, waypoint_data in waypoint_dict.items():
                old_waypoint_id = waypoint_data.pop('waypoint_id', None)
                to_delete_waypoint_id.append(old_waypoint_id)

                old_map_id = waypoint_data.pop('map_id', None)
                waypoint_data['map_id'] = old_to_new_map_dict[old_map_id]
                waypoint_data.pop('map', None)
                waypoint_data['waypoint_name'] = waypoint_data.get('name', '')

                new_waypoint_id = self.create_waypoint(waypoint_details=waypoint_data, headers=headers)
                waypoint_count += 1
                
                created_waypoints = newly_created_data.get('waypoints', [])
                created_waypoints.append(new_waypoint_id)
                newly_created_data['waypoints'] = created_waypoints

                waypoint_data['waypoint_id'] = new_waypoint_id
            
            # associate newly created waypoints with missions #
            for mission in old_mission_list:
                tasks = mission.get('mission_json')['tasks']

                # Used to exclude missions with waypoints - only applicable when skip_waypoint or skip_map is True
                indexes_to_del = []
                curr_index = 0
                for task in tasks:
                    if task.get('parameter', {}).get('waypoint_id', None):
                        if skip_waypoint or skip_map:
                            indexes_to_del.append(curr_index)
                        else:
                            old_waypoint_id = task['parameter']['waypoint_id']
                            task['parameter']['waypoint_id'] = waypoint_dict[old_waypoint_id]['waypoint_id']
                        curr_index += 1

                if skip_waypoint or skip_map:
                    count = 0
                    for idx in indexes_to_del: 
                        del tasks[idx-count]
                        count += 1

            #### Create mission, schedule and mission instances ####     
            schedule_count = 0
            mission_count = 0
            mission_instance_count = 0
            old_mission_ids = []
            for mission in old_mission_list:
                mission_data = mission
                old_mission_id = mission_data.pop('mission_id', None)
                old_mission_ids.append(old_mission_id)
                tasks = mission_data.pop('mission_json')['tasks']
                schedules = mission_data.pop('schedules', {})
                schedule_to_mission_instance_dict = mission_data.pop('schedule_to_mission_instance_dict', {})
                mission_instances_without_schedules = mission_data.pop('mission_instances_without_schedules', [])

                mission_data['robot_id'] = new_robot_id

                if skip_waypoint or skip_map:
                    new_task_list = []
                    for task in tasks:
                        # If task requires waypoint then skip
                        if task.get('type', '') == 'NAV2POINT' or task.get('type', '') == 'MOV2POINT':
                            continue
                        else:
                            new_task_list.append(task)
                    tasks = new_task_list

                mission_data['task_list'] = tasks                    

                new_mission_id = self.create_mission(mission_details=mission_data, headers=headers)
                mission_count += 1
                new_missions = newly_created_data.get('missions', [])
                new_missions.append(new_mission_id)
                newly_created_data['missions'] = new_missions

                if not skip_schedule:
                    for schedule in schedules:
                        old_schedule_id = schedule.pop('schedule_id', None)
                        schedule_json = schedule.pop('schedule_json', None)
                        if schedule_json is not None:
                            timestamp = schedule_json.get('timestamp', None)
                            schedule_cron = schedule_json.get('cron', None)

                            if timestamp is not None:
                                schedule['schedule_timestamp'] = timestamp
                            else:
                                schedule['schedule_cron'] = schedule_cron

                            schedule['loop_count'] = schedule_json.get('loop_count', None)

                        schedule['mission_id'] = new_mission_id
                        if '.' in schedule['start_timestamp']:
                            schedule['start_timestamp'] = schedule['start_timestamp'].split('.')[0] 
                        new_schedule_id = self.create_schedule(schedule_details=schedule, headers=headers)
                        schedule_count += 1
                        schedules = newly_created_data.get('schedules', [])
                        schedules.append(new_schedule_id)
                        newly_created_data['schedules'] = schedules

                        mission_instance = schedule_to_mission_instance_dict.get(old_schedule_id, None)
                        if mission_instance is not None:
                            mission_instance['mission_id'] = new_mission_id
                            mission_instance['schedule_id'] = new_schedule_id
                            mission_instance['robot_id'] = new_robot_id
                        schedule_to_mission_instance_dict[old_schedule_id] = mission_instance

                    for key, mission_instance in schedule_to_mission_instance_dict.items():
                        if mission_instance is None:
                            continue
                        mission_instance.pop("last_updated_at", None)
                        mission_instance.pop("mission_instance_id", None)
                        mission_instance.pop("waypoints", None)
                        # mission_instance.get("schedule_id", None) = null if mission_instance['schedule_id'] = None or there is no schedule_id
                        schedule_id = mission_instance.get("schedule_id", None)
                        if schedule_id is None:
                            mission_instance.pop("schedule_id", None)

                        new_mission_instance_id = self.create_mission_instance(mission_instance_details=mission_instance, headers=headers)
                        mission_instance_count += 1
                        new_mission_instances = newly_created_data.get('mission_instances', [])
                        new_mission_instances.append(new_mission_instance_id)
                        newly_created_data['mission_instances'] = new_mission_instances

                    for mission_instance in mission_instances_without_schedules:
                        mission_instance.pop("last_updated_at", None)
                        mission_instance.pop("mission_instance_id", None)
                        mission_instance.pop("waypoints", None)
                        mission_instance.pop("schedule_id", None)
                        mission_instance['robot_id'] = new_robot_id
                        mission_instance['mission_id'] = new_mission_id

                        new_mission_instance_id = self.create_mission_instance(mission_instance_details=mission_instance, headers=headers)
                        mission_instance_count += 1
                        new_mission_instances = newly_created_data.get('mission_instances', [])
                        new_mission_instances.append(new_mission_instance_id)
                        newly_created_data['mission_instances'] = new_mission_instances

        except Exception as err:
            print(bcolors.FAIL + 'Error occurred while porting over robot to new organization. Details: ' + str(err) + bcolors.ENDC)
            print("Preparing to delete any created data...")
            self.rollback(created_data=newly_created_data,headers=headers)
            raise SystemExit(1)
    

        print(bcolors.OKGREEN + "Successfully ported robot to new organization!\n"
            "-------------- Summary ----------------\n"
            "New robot_id: {robot_id}\n"
            "Number of missions moved over: {mission_move_count} \n"
            "Number of mission instances moved over: {mission_instance_count}\n"
            "Number of schedules moved over: {schedule_move_count}\n"
            "Number of maps moved over: {map_move_count}\n"
            "Number of waypoints moved over: {waypoint_move_count}\n"
            .format(robot_id=new_robot_id, mission_move_count=mission_count, schedule_move_count=schedule_count,
                    map_move_count=map_count, waypoint_move_count=waypoint_count, mission_instance_count=mission_instance_count) \
            + bcolors.ENDC)
        
        new_robot_config = self.get_robot_config(org_id=args.new_org_id, robot_id=new_robot_id, headers=headers)
        config = args.config
        if new_robot_config and config:
            for key in new_robot_config:
                config.config[key] = new_robot_config[key]
        Configuration.save_config(config)

        if args.restart:
            # To run cognicept restart -d 
            args.detach = True
            agent_lifecycle = AgentLifeCycle()
            agent_lifecycle.restart(args)

        if args.delete_robot:
            # Should/Can only be done if the shell is connected to the robot because the restart will only work if the docker images are started inside the robot
            access_token = self.switch_org(org_id=args.old_org_id, headers=headers)
            headers = {
                'Authorization': 'Bearer ' + access_token
            }
            self.delete_robot(robot_id=args.robot_id, organization_id=args.old_org_id, headers=headers)
            for mission_id in old_mission_ids:
                if mission_id:
                    self.delete_mission(mission_id=mission_id, headers=headers)
            for map_id in to_delete_map_id:
                self.delete_map(map_id, headers=headers)
