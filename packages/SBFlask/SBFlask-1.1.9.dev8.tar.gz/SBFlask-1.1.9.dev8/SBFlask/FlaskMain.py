import logging
import os
import signal
import sys
import ipaddress

from flask import Flask, redirect, url_for, request
from flask_cors import CORS, cross_origin
import json
from SBKodiak.KodiakControl import KodiakControlClass, KodiakWrapper
from SBKodiak.KodiakMDNsLocate import find_kodiak_ip_addresses
from SBFlask.tests.frigged_server_responses import *

app = Flask(__name__)
CORS(app)

# Kodiak Controller object
KodiakController = KodiakControlClass()


logger = logging.getLogger("logging_tryout")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
# logging.basicConfig(level=logging.DEBUG)

# Fake the responses
frigg_responses = False
frigg_responses_port_counter = 0


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


def check_if_json(tmp_request, response):
    # Checking the request is JSON
    if not tmp_request.content_type:
        response['Error'] = 'Request not of type JSON'
        return

    # Checking the JSON is actual json.
    if 'application/json' not in tmp_request.content_type:
        response['Error'] = 'Request not of type JSON'
        return

    if not tmp_request.get_json():
        response['Error'] = 'Request missing args'
        return


def check_json_for_ip(data, response):
    if not isinstance(data, dict):
        response['Error'] = 'Request not of correct JSON format'
        return
    if 'ipaddress' not in data:
        response['Error'] = 'Missing IP address'
        return


@app.route(f"/kodiak/port/discover", methods=['POST'])
def kodiak_endpoint_discover():
    """
    Discover endpoint.

    The function will first try to get the login credentials.

    This endpoint will start the discovery of the Kodiak Module against the SB ports
    After posting to the endpoint, the client should then send a 'get' request to the /kodiak/port to discover the port.

    :return: JSON - With an appropriate success / Error message.
    """
    global KodiakController
    global frigg_responses

    response = {}

    if request.method == 'POST':
        # Checking the request is JSON
        check_if_json(request, response)
        if 'Error' in response:
            return json.dumps(response, indent=4)

        data = request.get_json()

        check_json_for_ip(data, response)
        if 'Error' in response:
            return json.dumps(response, indent=4)

        elif not check_valid_ip(data['ipaddress']):
            response['Error'] = 'Badly formatted IP address'
        elif 'key' not in data:
            response['Error'] = "Missing API key"
        else:
            ipaddress = data['ipaddress']
            key = data['key']

            # If we're faking it, just do to here
            if frigg_responses:
                response['Success'] = 'Started auto discovery'
                return json.dumps(response, indent=4)

            # Create a wrapper and attempt to start the auto locate
            kw = KodiakWrapper(ipaddress, None, None, key)
            try:
                errors = KodiakController.start_auto_locate_port(kw)

                # If there's an Error starting the discovery, add the Error message
                if not errors:
                    response['Success'] = 'Started auto discovery'
                else:
                    response['Error'] = errors
            except Exception as err:
                response['Error'] = err

        return json.dumps(response, indent=4)


@app.route(f"/kodiak/locate", methods=['GET'])
def kodiak_endpoint_locate():
    """
    Get endpoint for scanning MDNs for Kodiak Ipaddresses.

    This function will attempt to get the port the Kodiak is attached to

    :return: JSON - With an appropriate success / Error message.
    """
    global KodiakController
    global frigg_responses
    response = {}

    if request.method == 'GET':
        try:
            if frigg_responses:
                response['Success'] = ['192.168.1.2', '192.168.1.3']
                # print(json.dumps(response, indent=4))
                return json.dumps(response, indent=4)

            # call to MDNS scan function which will return a list of discovered IPAddresses
            ip_address_list = find_kodiak_ip_addresses()
            logging.debug(f"List of found ip's : {ip_address_list}")
            response['Success'] = ip_address_list
            # print(json.dumps(response, indent=4))
        except Exception as err:
            response['Error'] = "Error whilst starting MDNS discovery!"

        return json.dumps(response, indent=4)


@app.route(f"/kodiak/database", methods=['POST'])
def kodiak_endpoint_database():
    """
    Get endpoint for scanning MDNs for Kodiak Ipaddresses.

    This function will attempt to get the port the Kodiak is attached to

    :return: JSON - With an appropriate success / Error message.
    """
    global KodiakController
    global frigg_responses
    response = {}

    if request.method == 'POST':
        # Checking the request is JSON
        check_if_json(request, response)
        if 'Error' in response:
            return json.dumps(response, indent=4)

        data = request.get_json()

        check_json_for_ip(data, response)
        if 'Error' in response:
            return json.dumps(response, indent=4)

        tmp_ip = data['ipaddress']

        if not check_valid_ip(tmp_ip):
            response['Error'] = 'Badly formatted IP address value'
            return json.dumps(response, indent=4)

        query_response = KodiakController.db.get_kodiak_db(tmp_ip)

        if frigg_responses:
            response['Success'] = ('192.168.1.2', '192.168.1.3')
            # print(json.dumps(response, indent=4))
            return json.dumps(response, indent=4)

        # if the response is missing then add an appropriate Error message
        if not query_response:
            response['Error'] = "Missing Kodiak from DB"
            return json.dumps(response, indent=4)

        response['Success'] = query_response

        return json.dumps(response, indent=4)


@app.route(f"/kodiak/database/remove", methods=['POST'])
def kodiak_endpoint_database_remove():
    """
    Get endpoint for scanning MDNs for Kodiak Ipaddresses.

    This function will attempt to get the port the Kodiak is attached to

    :return: JSON - With an appropriate success / Error message.
    """
    global KodiakController
    global frigg_responses
    response = {}

    if request.method == 'POST':
        # Checking the request is JSON
        check_if_json(request, response)
        if 'Error' in response:
            return json.dumps(response, indent=4)

        data = request.get_json()

        check_json_for_ip(data, response)
        if 'Error' in response:
            return json.dumps(response, indent=4)

        tmp_ip = data['ipaddress']

        if not check_valid_ip(tmp_ip):
            response['Error'] = 'Badly formatted IP address value'
            return json.dumps(response, indent=4)

        # Stop here if we're doing testing as rest of function can be tested independently elsewhere
        if frigg_responses:
            response['Success'] = 'Successfully deleted kodiak'
            return json.dumps(response, indent=4)

        if not KodiakController.db.remove_kodiak_from_db(tmp_ip):
            response['Error'] = "Could not delete kodiak from db"
            return json.dumps(response, indent=4)

        response['Success'] = 'Successfully deleted kodiak'

        return json.dumps(response, indent=4)


@app.route(f"/kodiak/port", methods=['POST'])
def kodiak_endpoint_port():
    """
    Get port endpoint.

    This function will attempt to get the port the Kodiak is attached to

    :return: JSON - With an appropriate success / Error message.
    """
    global KodiakController
    global frigg_responses
    global frigg_responses_port_counter
    response = {}

    if request.method == 'POST':
        # Checking the request is JSON
        check_if_json(request, response)
        if 'Error' in response:
            return json.dumps(response, indent=4)

        data = request.get_json()

        check_json_for_ip(data, response)
        if 'Error' in response:
            return json.dumps(response, indent=4)

        tmp_ip = data['ipaddress']

        if not check_valid_ip(tmp_ip):
            response['Error'] = 'Badly formatted IP address value'
            return json.dumps(response, indent=4)

        if frigg_responses:
            # If we're faking the responses, make sure we only do 1 port at a time, so we can test other ports work too
            response['Success'] = '0' + str(frigg_responses_port_counter)
            frigg_responses_port_counter += 1
            if frigg_responses_port_counter > 4:
                frigg_responses_port_counter = 0

            return json.dumps(response, indent=4)

        # Get the items from the database
        query_response = KodiakController.db.get_kodiak_db(tmp_ip)

        # if the response is missing then add an appropriate Error message
        if not query_response:
            response['Error'] = "Missing Kodiak from DB"

        else:
            # Create a wrapper and attempt to start the auto locate
            port_response = query_response[7]

            if port_response:
                response['Success'] = port_response
            else:
                # If there wasn't a return from the locate_kodiak_port function then no port was found
                response['Error'] = "Could not find port containing Kodiak Module!"

        return json.dumps(response, indent=4)


@app.route(f"/kodiak/status", methods=['POST'])
def kodiak_endpoint_get_status():
    """
    Get kodiak status for a given IP address.

    This function will attempt to get the status of the kodiak from the supplied IP

    :return: JSON - With an appropriate success / Error message.
    """
    global KodiakController
    global frigg_responses
    response = {}

    if request.method == 'POST':
        check_if_json(request, response)
        if 'Error' in response:
            return json.dumps(response, indent=4)

        data = request.get_json()

        check_json_for_ip(data, response)
        if 'Error' in response:
            return json.dumps(response, indent=4)

        ipaddress = request.json.get('ipaddress')

        if not check_valid_ip(ipaddress):
            response['Error'] = 'Badly formatted IP address value'
            return json.dumps(response, indent=4)

        # Stop here if we're just testing as the rest of this function will be tested elsewhere
        if frigg_responses:
            response['Success'] = status_response_good
            return json.dumps(response, indent=4)

        # Get the items from the database
        my_response = KodiakController.db.get_kodiak_db(ipaddress)
        kw = KodiakWrapper(my_response[0], None, None, my_response[3])
        query_response = KodiakController.get_module_status(kw)

        response["Success"] = query_response

        return json.dumps(response, indent=4)


@app.route(f"/kodiak/remove", methods=['POST'])
def kodiak_endpoint_remove():
    """
    Function to remove kodiak from the underlying database

    :return: JSON - With an appropriate success / Error message.
    """
    global KodiakController
    global frigg_responses
    response = {}

    # Checking if request is of type 'POST'
    if request.method == 'POST':

        check_if_json(request, response)
        if 'Error' in response:
            return json.dumps(response, indent=4)

        data = request.get_json()

        check_json_for_ip(data, response)
        if 'Error' in response:
            return json.dumps(response, indent=4)

        ipaddress = request.json.get('ipaddress')

        if not check_valid_ip(ipaddress):
            response['Error'] = 'Badly formatted IP address value'
            return json.dumps(response, indent=4)

        if frigg_responses:
            response['Success'] = 'Removed Successfully'
            return json.dumps(response, indent=4)

        response['Success'] = 'Removed Successfully'

        return json.dumps(response, indent=4)


@app.route(f"/kodiak/start", methods=['POST'])
def kodiak_endpoint_start():
    global KodiakController

    response = {}

    # Checking if request is of type 'POST'
    if request.method == 'POST':

        # Checking the request is JSON
        check_if_json(request, response)
        if 'Error' in response:
            return json.dumps(response, indent=4)

        data = request.get_json()

        check_json_for_ip(data, response)
        if 'Error' in response:
            return json.dumps(response, indent=4)

        # if 'key' not in data:
        #     response['Error'] = "Missing API key"
        #     return json.dumps(response, indent=4)

        ipaddress = data['ipaddress']

        # Checking the IP address is of the valid format
        if not check_valid_ip(ipaddress):
            response['Error'] = 'Badly formatted IP address value'
            return json.dumps(response, indent=4)

        # Stop here if we're doing testing as rest of function can be tested independently elsewhere
        if frigg_responses:
            response['Success'] = 'Successfully started kodiak stream'
            return json.dumps(response, indent=4)

        # Get the items from the database
        query_response = KodiakController.db.get_kodiak_db(ipaddress)

        # if the response is missing then add an appropriate Error message
        if not query_response:
            response['Error'] = "Could not locate this IP address, is this definitely connected?"

        else:
            # Create a wrapper and attempt to start the auto locate
            kw = KodiakWrapper(query_response[0], query_response[1], query_response[2], query_response[3])

            if not KodiakController.get_module_status(kw):
                response['Error'] = "No module located at location : " + kw.ipaddress
                return json.dumps(response, indent=4)

            # Need to lock the device before we can start streaming to it.
            KodiakController.lock(kw, 'SB_LOCK')
            started = KodiakController.start(kw, trigger=False)

            if started:
                response['Success'] = 'Successfully started kodiak stream'
            else:
                response['Error'] = started


        # else:
        #     response['Error'] = 'Missing IP address argument from post request'

        return json.dumps(response, indent=4)


@app.route(f"/kodiak/stop", methods=['POST'])
def kodiak_endpoint_stop():
    global KodiakController

    response = {}

    # Checking if request is of type 'POST'
    if request.method == 'POST':

        # Checking the request is JSON
        check_if_json(request, response)
        if 'Error' in response:
            return json.dumps(response, indent=4)

        data = request.get_json()

        check_json_for_ip(data, response)
        if 'Error' in response:
            return json.dumps(response, indent=4)

        # if 'key' not in data:
        #     response['Error'] = "Missing API key"
        #     return json.dumps(response, indent=4)

        ipaddress = data['ipaddress']

        # Checking the IP address is of the valid format
        if not check_valid_ip(ipaddress):
            response['Error'] = 'Badly formatted IP address value'
            return json.dumps(response, indent=4)

        # Stop here if we're doing testing as rest of function can be tested independently elsewhere
        if frigg_responses:
            response['Success'] = 'Successfully stopped kodiak stream'
            return json.dumps(response, indent=4)

        # Get the items from the database
        query_response = KodiakController.db.get_kodiak_db(ipaddress)

        # if the response is missing then add an appropriate Error message
        if not query_response:
            response['Error'] = "Could not locate this IP address, is this definitely connected?"

        else:
            # Create a wrapper and attempt to start the auto locate
            kw = KodiakWrapper(query_response[0], query_response[1], query_response[2], query_response[3])

            # call function to stop device from streaming
            started = KodiakController.stop(kw)

            KodiakController.unlock(kw)

            if started:
                response['Success'] = 'Successfully stopped kodiak stream'
            else:
                response['Error'] = started

        return json.dumps(response, indent=4)


def shutdown_application():
    """
    This function is a standalone way to kill the application

    It is called both via the endpoint @ :4201/shutdown or via the cli 'python -m SBFlask.run shutdown'

    :return: N/A
    """
    os.kill(os.getpid(), signal.SIGINT)


@app.route('/shutdown', methods=['GET'])
def shutdown():
    """
    This endpoint is used to terminate / kill the running flask server process.

    There will be no response to the server as a result of this.

    :return: N/A
    """
    shutdown_application()


def create_app():
    app.run(port=4201, host='0.0.0.0', debug=True)


def set_frigg_responses(frigg):
    global frigg_responses
    frigg_responses = frigg


if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) > 0:
        main_arg = args[0]
        if 'test' in main_arg:
            set_frigg_responses(True)

    # if frigg_responses:

    create_app()
