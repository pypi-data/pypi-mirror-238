import os
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import json
from dotenv import load_dotenv
from logger_local import Logger
from profile_local.comprehensive_profile import ComprehensiveProfile
from .constans_zoominfo import OBJECT_FOR_LOGGER_CODE
from zoomus import ZoomClient

load_dotenv()

logger_local = Logger.Logger.create_logger(object=OBJECT_FOR_LOGGER_CODE)

ZOOMINFO_APPLICATION_CLIENT_ID = os.getenv("ZOOMINFO_APPLICATION_CLIENT_ID")
ZOOMINFO_APPLICATION_CLIENT_SECRET = os.getenv(
    "ZOOMINFO_APPLICATION_CLIENT_SECRET")
ZOOMINFO_APPLICATION_ACCOUNT_ID = os.getenv("ZOOMINFO_APPLICATION_ACCOUNT_ID")

zoom_info_client = ZoomClient(
    client_id=ZOOMINFO_APPLICATION_CLIENT_ID, client_secret=ZOOMINFO_APPLICATION_CLIENT_SECRET, api_account_id=ZOOMINFO_APPLICATION_ACCOUNT_ID)


class ZoomInfo:

    @staticmethod
    def set_client(client_id: str, client_secret: str, account_id: str):
        """
        Sets the ZoomInfo client with the given credentials.

        Args:
            client_id (str): The client ID.
            client_secret (str): The client secret.
            account_id (str): The account ID.

        Returns:
            ZoomClient: The configured ZoomClient instance.
        """
        logger_local.start(object={
                           'client_id': client_id, 'client_secret': client_secret, 'account_id': account_id})
        logger_local.end()
        return ZoomClient(client_id, client_secret, account_id)

    @staticmethod
    def get_user_by_email(email: str):
        """
        Gets a ZoomInfo user by their email address.

        Args:
            email (str): The email address to search for.

        Returns:
            dict: The user dict if found, else None.
        """
        logger_local.start(object={'email': email})
        users = ZoomInfo.get_all_users()
        for user in users['users']:
            if user['email'] == email:
                user = ZoomInfo.get_user_by_id(user['id'])
                compatible_json = ZoomInfo.generate_compatible_json(user)
                ComprehensiveProfile.insert(compatible_json)
                logger_local.end(object=user)
                return user
        return None

    @staticmethod
    def _get_next_page(next_page_token: str):
        """
        Internal method to get the next page of results.

        Args:
            next_page_token (str): The next page token.

        Returns:
            dict: The next page of results.
        """
        logger_local.start(object={'next_page_token': next_page_token})
        try:
            response = zoom_info_client.user.list(page_token=next_page_token)
            users_list = response.json()
        except Exception as e:
            logger_local.exception("Exception in _get_next_page", object=e)
            raise (e)
        logger_local.end(object=users_list)
        return users_list

    @staticmethod
    def get_all_users():
        """
        Gets all ZoomInfo users.

        Returns:
            dict: The response containing users.
        """
        logger_local.start()
        try:
            response = zoom_info_client.user.list()
            users_list = response.json()
            print(json.dumps(users_list, indent=4, sort_keys=True))
            while users_list['page_number'] <= users_list['page_count']:
                for user in users_list['users']:
                    user = ZoomInfo.get_user_by_id(user['id'])
                    compatible_json = ZoomInfo.generate_compatible_json(user)
                    ComprehensiveProfile.insert(compatible_json)
                if users_list['next_page_token'] == "":
                    break
                users_list = ZoomInfo._get_next_page(
                    users_list['next_page_token'])
        except Exception as e:
            logger_local.exception("Exception in get_all_users", object=e)
            raise (e)
        logger_local.end(object=users_list)
        return users_list

    @staticmethod
    def get_all_users_emails():
        """
        Gets all ZoomInfo users emails.

        Returns:
            list: The list of emails.
        """
        logger_local.start()
        users = ZoomInfo.get_all_users()
        emails = []
        for user in users['users']:
            emails.append(user['email'])
        logger_local.end(object={'emails': emails})
        return emails

    @staticmethod
    def get_user_by_phone_number(phone_number: str):
        """
        Gets a ZoomInfo user by their phone number.

        Args:
            phone_number (str): The phone number to search for.

        Returns:
            dict: The user dict if found, else None.
        """
        logger_local.start(object={'phone_number': phone_number})
        users = ZoomInfo.get_all_users()

        while users['page_number'] <= users['page_count']:
            for user in users['users']:
                user = ZoomInfo.get_user_by_id(user['id'])
                if phone_number in user['phone_number']:
                    compatible_json = ZoomInfo.generate_compatible_json(user)
                    ComprehensiveProfile.insert(compatible_json)
                    logger_local.end(object=user)
                    return user
            if users['next_page_token'] == "":
                break
            users = ZoomInfo._get_next_page(users['next_page_token'])
        logger_local.end(object={'user': None})
        return None

    @staticmethod
    def get_user_by_name(first_name: str, last_name: str):
        """
        Gets a ZoomInfo user by their name.

        Args:
            first_name (str): The first name to search for.
            last_name (str): The last name to search for.

        Returns:
            dict: The user dict if found, else None.
        """
        logger_local.start(
            object={'first_name': first_name, 'last_name': last_name})
        users = ZoomInfo.get_all_users()
        users_by_name = []
        while users['page_number'] <= users['page_count']:
            for user in users['users']:
                if user['first_name'] == first_name and user['last_name'] == last_name:
                    user = ZoomInfo.get_user_by_id(user['id'])
                    compatible_json = ZoomInfo.generate_compatible_json(user)
                    ComprehensiveProfile.insert(compatible_json)
                    logger_local.end(object=user)
                    users_by_name.append(user)
            if users['next_page_token'] == "":
                return users_by_name
            users = ZoomInfo._get_next_page(users['next_page_token'])
        logger_local.end(object={'user': None})
        return None

    @staticmethod
    def get_user_by_id(user_id: str):
        """
        Gets a ZoomInfo user by their ID.

        Args:
            user_id (str): The user ID to search for.

        Returns:
            dict: The user dict if found, else None.
        """
        logger_local.start(object={'user_id': user_id})
        try:
            user = zoom_info_client.user.get(id=user_id)
            user_json = json.loads(user.content)
            print(json.dumps(user_json, indent=4, sort_keys=True))
            compatible_json = ZoomInfo.generate_compatible_json(user_json)
            ComprehensiveProfile.insert(compatible_json)
        except Exception as e:
            logger_local.exception("Exception in get_user_by_id", object=e)
            raise (e)
        logger_local.end(object={'user': user_json})
        return user_json

    @staticmethod
    def get_all_users_by_location(location: str):
        """
        Gets all ZoomInfo users by their location.

        Args:
            location (str): The location to search for.
            format: "country(Israel, USA, etc.))"

        Returns:
            list: The list of users.
        """
        logger_local.start(object={'location': location})
        users = ZoomInfo.get_all_users()
        users_by_location = []
        while users['page_number'] <= users['page_count']:
            for user in users['users']:
                user = ZoomInfo.get_user_by_id(user['id'])
                if str(user['location']).lower() == location.lower():
                    compatible_json = ZoomInfo.generate_compatible_json(user)
                    ComprehensiveProfile.insert(compatible_json)
                    users_by_location.append(user)
            if users['next_page_token'] == "":
                break
            users = ZoomInfo._get_next_page(users['next_page_token'])
        logger_local.end(object={'response': users_by_location})
        return users_by_location

    @staticmethod
    def get_all_users_by_job_title(job_title: str):
        """
        Gets all ZoomInfo users by their job title.

        Args:
            job_title (str): The job title to search for.

        Returns:
            list: The list of users.
        """
        logger_local.start(object={'job_title': job_title})
        users = ZoomInfo.get_all_users()
        users_by_job_title = []

        while users['page_number'] <= users['page_count']:
            for user in users['users']:
                user = ZoomInfo.get_user_by_id(user['id'])
                if str(user['job_title']).lower() == job_title.lower():
                    compatible_json = ZoomInfo.generate_compatible_json(user)
                    ComprehensiveProfile.insert(compatible_json)
                    users_by_job_title.append(user)
            if users['next_page_token'] == "":
                break
            users = ZoomInfo._get_next_page(users['next_page_token'])
        logger_local.end(object={'response': users_by_job_title})
        return users_by_job_title

    @staticmethod
    def generate_compatible_json(user_info: dict):

        plan_type_dict = {
            1: "Basic",
            2: "Licensed",
            99: "None (can only be set with ssoCreate)"
        }

        person = {

        }

        profile = {
            'profile_name': user_info['display_name'],
            'name_approved': True,
            'lang_code': user_info['language'],
            'user_id': user_info['id'],
            'is_approved': True,
            'profile_type_id': plan_type_dict[user_info['type']],
            'preferred_lang_code': user_info['language'],
            'main_phone_id': user_info['phone_number'],
        }

        location = {
            'address_local_language': user_info['language'],
            'coordinate': {},
            'plus_code': user_info['phone_numbers'][0]['code'],
            'country': user_info['location']
        }

        storage = {
            'path': user_info['pic_url'],
            'url': user_info['pic_url'],
            'file_extension': 'jpg',
            'file_type': 'Profile Image'
        }

        entry = {
            "person": person,
            "location": location,
            "profile": profile,
            "storage": storage,
        }

        return json.dumps({'results': entry})
