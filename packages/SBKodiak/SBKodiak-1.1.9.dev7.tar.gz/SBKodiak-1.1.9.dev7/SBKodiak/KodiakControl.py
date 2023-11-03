"""
Python module to handle control of the Kodiak modules.

This class will also do all necessary interaction with underlying Database.

Author : Matt Holsey
Date : 09-05-2023
"""
import logging
import time
import os
import paramiko
import ipaddress
import threading
from .sb_db import SimpleDB

from .kodiak_session_management import KodiakSession
from .KodiakGlobals import KodiakGlobals
from .kodiak_endpoints import *
from .kodiak_static_vars import *


def check_valid_ip(ip_addr):
    try:
        if not isinstance(ip_addr, str):
            return False
        ip = ipaddress.ip_address(ip_addr)
        return True
    except ValueError:
        return False
    except:
        return False


class KodiakControlClass:

    def __init__(self):

        # self.private_key = private_key if private_key else "gThV9h4LQmmSiYFNTcjBuvoRPvEC3LpW"
        self.db = SimpleDB(KodiakGlobals.database_name)

        # If the table doesn't already exist, then create a new one
        if not self.db.check_exists():
            self.db.create_table()

        self.kodiak_session = KodiakSession()

    def lock(self, kw, lock_name):
        """
        Attempts to lock the Kodiak Module

        :param kw: Kodiak Wrapper
        :param lock_name: Lock name to be used for lock

        :return: boolean : True if success, else False.
        """

        lock_response = self.kodiak_session.lock(kw, lock_name)
        if lock_response:
            # Use the 'lock_key' response and update the DB with the key.
            if not self.db.update_kodiak_db_lock_key(kw.ipaddress, lock_response):
                logging.warning('Failed to update database with lock')
                return False
            return True
        else:
            return False

    def unlock(self, kw):
        """
        Attempt to unlock the module.

        :param kw: Kodiak wrapper containing credentials

        :return: boolean: True if success, else False
        """

        # Check if the kodiak module present in database
        response = self.db.get_kodiak_db(kw.ipaddress)
        if response:
            if not response[-1]:
                logging.warning('Missing lock key from database query!')
                return False

            # Attempt to unlock the module based off of the current items in the DB
            if self.kodiak_session.unlock(kw, response[-1]):
                return True

        else:
            return False

    def get_lock_status(self, kw):
        """
        Function to get the current lock status of the kodiak module

        :param kw: Kodiak Wrapper containing credentials

        :return: Lock status or None if no response
        """

        return self.kodiak_session.get_lock_status(kw)

    def stop(self, kw):
        """
        Sending a POST request to stop the Kodiak capture

        :return: True if success, False if fail
        """

        query_response = self.db.get_kodiak_db(kw.ipaddress)
        if not query_response:
            logging.warning("Couldn't find kodiak login in database, have you logged into the module yet?")
            return False

        if not query_response[-1]:
            logging.warning("Invalid lock key returned from database")
            return False

        message_to_send = {
            "lock_key": query_response[-1]
        }
        headers = {
            'x-api-key': kw.key
        }

        endpoint = KodiakGlobals.url_prefix + kw.ipaddress + endpoint_stop

        # A post request to the API
        response = self.kodiak_session.send_post_command(message_to_send, endpoint, headers)

        # Checking that the response received was valid
        if not response:
            logging.warning('No response returned from kodiak module')
            return False

        # if not isinstance(response, dict):
        #     logging.warning('Kodiak response not of type json')
        #     return False

        if 'error' in response:
            logging.warning('Kodiak /stop returned an error: ' + str(response))
            return False

        return True

    def start(self, kw, trigger=False):
        """
        Sending a POST request to start the kodiak capture

        :return: Return True if start succeeded, else False
        """

        query_response = self.db.get_kodiak_db(kw.ipaddress)
        if not query_response:
            logging.warning("Database did not reply to get kodiak item")
            return "Database did not reply to get kodiak item"

        if not isinstance(query_response, tuple):
            logging.warning(f"Response from DB is not of type tuple ({type(query_response)}) : " + str(query_response) )
            return f"Response from DB is not of type tuple ({type(query_response)}) : " + str(query_response)

        # If trigger is set wrong, just set it to default off
        if not isinstance(trigger, bool):
            logging.warning('"trigger" argument not set properly, setting to default false')
            trigger = False

        message_to_send = start_dict

        message_to_send["mode"] = "trigger" if trigger else "manual"
        message_to_send["lock_key"] = query_response[-1]

        # If we want to trigger the kodiak module, then add the SB_trigger definition in.
        if trigger:
            message_to_send['trigger'] = trigger_dict

        headers = {
            'x-api-key': kw.key
        }

        endpoint = KodiakGlobals.url_prefix + kw.ipaddress + endpoint_start

        # A post request to the API
        response = self.kodiak_session.send_post_command(message_to_send, endpoint, headers)

        if not response:
            logging.warning('No response returned from sending "Start" to kodiak')
            return 'No response returned from sending "Start" to kodiak'

        # if not isinstance(response, dict):
        #     logging.warning('Invalid response from start to Kodiak : ' + str(response))
        #     return 'Invalid response from start to Kodiak : ' + str(response)

        if 'error' in response:
            logging.warning('Error returned from sending "Start" to kodiak : ' + str(response))
            return "Error returned from kodiak : " + str(response)

        return None

    def get_module_status(self, kw):
        """
        Send a GET request to the Kodiak to see its current lock status.

        :return: Response from get lock stats request
        """

        if not kw.key:
            logging.warning('No api key included for the module status, KW = ' + str(kw))
            return None

        # query_response = self.db.get_kodiak_db(kw.ipaddress)

        # if not query_response:
        #     logging.warning('No response returned from database query (get_kodaik_db) : ' + str(query_response))
        #     return None

        headers = {
            'x-api-key': kw.key
        }

        endpoint = KodiakGlobals.url_prefix + kw.ipaddress + endpoint_status

        # Do the get request to lock endpoint
        try:
            response = self.kodiak_session.send_get_request(endpoint, headers)
            logging.debug('Response from /module kodiak was : ' + str(response))
            return response
        except Exception as err:
            logging.warning('Error asking kodiak for a module update: ' + str(err))
            return None

    def get_module_capture_status(self, kw):
        """
        Send a GET request to the Kodiak to see its current lock status.

        :return: Response from get lock stats request
        """

        if not kw.key:
            logging.warning('No api key included for the capture status, KW = ' + str(kw))
            return None

        # Calling to the DB
        query_response = self.db.get_kodiak_db(kw.ipaddress)

        if not query_response:
            logging.warning('No response returned from database query (get_kodaik_db) : ' + str(query_response))
            return None

        headers = {
            'x-api-key': kw.key
        }

        # Creating the endpoint
        endpoint = KodiakGlobals.url_prefix + kw.ipaddress + endpoint_capture_status

        # Do the get request to lock endpoint
        try:
            response = self.kodiak_session.send_get_request(endpoint, headers)
            logging.debug('Response from /status kodiak was : ' + str(response))
            # return whatever was returned from the kodiak
            return response
        except Exception as err:
            logging.warning('Error asking kodiak for a status update: ' + str(err))
            return None

    def locate_kodiak_port(self, kw, remote_ip=None):
        """
        Go through and trigger the SB system to trigger the Analyser that should be running.
        :return:
        """

        ssh = None

        # If there's a remote IP specified, use this, else just execute the command on the current system.
        if remote_ip is not None:
            if not check_valid_ip(remote_ip):
                logging.warning('Passed a bad REMOTE ip when looking for kodiak port')
                return None

            try:
                # connect on ssh using paramiko
                ssh = self.paramiko_connect(remote_ip)

                # checking we're definitely connected
                if not ssh:
                    logging.warning('Error connecting to remote ip, paramiko didnt connect')
                    return None
            except Exception as err:
                # Catching anything 'bad' that might've resulted from a bad connection
                logging.warning('Error connecting to remote ip! : ' + str(err))
                return None

        for x in range(16):
            index = x
            if len(str(index)) < 2:
                index = "0" + str(index)

            os_cmd = f'sbecho trigger=1{index} > /proc/vlun/nvme'

            if remote_ip:
                try:
                    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(os_cmd)
                    if ssh_stderr:
                        logging.warning('Got warning from os cmd execution : ' + ''.join(ssh_stderr.readlines()))
                except Exception as err:
                    logging.warning('Got warning from remote os cmd execution : ' + str(err))
                    return None
            else:
                os.system(os_cmd)

            time.sleep(0.05)

            response = self.get_module_capture_status(kw)

            if response:
                if 'error' not in response:

                    if response[0]['triggered']:
                        # Adding the port located to the database.
                        self.db.update_kodiak_db_kodiak_port(kw.ipaddress, x)
                        return response[0]['triggered']

        return None

    def paramiko_connect(self, remote_ip):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remote_ip, 22, username='root', password='sb')
        return ssh

    def check_if_running(self, kw):
        response = self.get_module_capture_status(kw)

        # Checking for a bad response
        if not response:
            logging.warning('No response from module capture status!')
            return False

        # if 0 not in response:
        #     logging.warning('Missing "0" key from module capture status response ' + str(response))
        #     return False

        if 'recording' not in response[0]:
            logging.warning('Missing "recording" key from module capture status response[0]')
            return False

        # Checking if the kodiak is streaming
        if response[0]['recording']:
            logging.debug('Module already recording')
            return False

        # return True if the kodiak is in a state we can stream to
        return True

    def start_auto_locate_port(self, kw):

        # Checking if there's a module at the location before we add it to the database
        if not self.get_module_status(kw):
            return "No module located at location : " + kw.ipaddress

        self.db.insert_kodiak_db_standard(kw.ipaddress, kw.key)

        self.lock(kw, 'SB_LOCK')

        if not self.check_if_running(kw):
            return "Module is already recording!"

        # Start the kodiak, if it fails to start, return False
        response = self.start(kw, trigger=True)
        if response:
            return response

        # Start the locate port in another thread...
        # Done this because we don't want to hold the current request thread!
        thread = threading.Thread(target=self.locate_kodiak_port, args=(kw, '192.168.1.160', ))
        thread.start()

        # self.locate_kodiak_port(kw, '192.168.1.160')

        # If we get here, the kodiak has been started and we're attempting to locate the port
        return None


class KodiakWrapper:
    def __init__(self, kodiak_ip_address, username, password, private_key):
        self.password = password
        self.username = username
        self.key = private_key
        self.ipaddress = kodiak_ip_address
