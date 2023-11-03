import logging
import json

from .RestFunctions import do_POST, do_GET
from .KodiakGlobals import KodiakGlobals
from .kodiak_endpoints import *


class KodiakSession:
    def __init__(self):
        """
        Kodiak session class is designed to control the login / authentication aspects of the Kodiak.
        Separated this from the main code so that program can store all these identifiers in isolated location.

        """
        pass

    def get_lock_status(self, kw) -> str:
        """
        Send a GET request to the Kodiak to see its current lock status.

        :param kw: Kodiak wrapper containing credentials
        :param session_token: Login session token

        :return: Response from get lock stats request
        """

        # Header to include in POST request
        headers = {
            'x-api-key': kw.key
        }

        endpoint = KodiakGlobals.url_prefix + kw.ipaddress + endpoint_status

        # Do the get request to lock endpoint
        response = self.send_get_request(endpoint, headers)

        return response

    def lock(self, kw, lock_name):
        """
        Locking the system so we can control it without interference

        :param kw: Kodiak wrapper containing credentials
        :param lock_name: Name you wish to give the lock session
        :param session_token: Login session token

        :return: boolean for success
        """

        message_to_send = {
            "lock_name": lock_name,
            # "owner": kw.username,
            "force": True
        }
        headers = {
            # "X-Auth-Token": session_token
            'x-api-key': kw.key
        }

        endpoint = KodiakGlobals.url_prefix + kw.ipaddress + endpoint_lock

        try:
            response = self.send_post_command(message_to_send, endpoint, headers)

            if not response:
                logging.debug("No valid response from the kodiak IP address")
                return None

            if 'key' in response.keys():
                return response['key']

            return None

        except KeyError:
            logging.warning(f'No lock key was returned from lock post request! : {response}')
            return None

        except Exception as err:
            logging.error(err)
            return None

    def unlock(self, kw, lock_key):
        """
        Sending a post request to unlock the Kodiak device

        :param kw: Kodiak wrapper containing credentials
        :param lock_key: Key that locked the module.

        :return: False if unlock failed, true if success
        """

        # Creating the message to send to the endpoint
        message_to_send = {
            "key": lock_key
        }
        headers = {
            'x-api-key': kw.key
        }

        # Endpoint location
        endpoint = KodiakGlobals.url_prefix + kw.ipaddress + endpoint_unlock

        # A post request to the API
        response = self.send_post_command(message_to_send, endpoint, headers)

        if not response:
            logging.debug("No valid response from Kodiak IP address")
            return None

        # TODO: Check what happens if this fails to unlock

        return True

    def send_post_command(self, command, endpoint, header):
        """
        Creating a post command wrapper to make teh json object and examine the response for HTTP errors
        :param command:
        :param endpoint:
        :param header:
        :return: Dict - Json data returned
        """
        # converting the msg to json
        json_object = json.dumps(command, indent=4)

        # Post the command
        response = do_POST(command, endpoint, header)

        # if not self._check_response(response):
        #     self._handle_invalid_response(response)

        try:
            json_data = json.loads(str(response.text))

            return json_data
        except Exception as err:
            logging.warning('Error attempting to parse response into json string : ' + str(err))
            return None

    def send_get_request(self, endpoint, header):
        """
        Creating a wrapper for sending GET requests to examine the response return for HTTP errors
        :param endpoint:
        :param header:
        :return:
        """

        # Do get request
        response = do_GET(endpoint, header)

        # if not self._check_response(response):
        #     self._handle_invalid_response(response)

        try:
            json_data = json.loads(str(response.text))

            return json_data
        except Exception as err:
            logging.warning('Error attemtping to parse response into json string : ' + str(err))
            return None

    def _check_response(self, response):
        """
        Checking if the response from the module is valid.
        Will Warn if the response was invalid.

        :param response: Response object
        :return: Boolean - true if valid, else false
        """
        if 200 <= int(response.status_code) <= 229:
            return True

        logging.warning(response.text)

        return False

    # def _handle_invalid_response(self, response):
    #
    #     if int(response.status_code) == 401:
    #         # Indicates the user is not logged authenticated - a login / refresh token is required.
    #         if self.logged_in:
    #             self.refresh_required = True
    #         self.logged_in = False
