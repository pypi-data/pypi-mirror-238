# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
A module for sending control request of sensors.
"""

import json
import logging
import os
import sys
import time
from typing import Union, Optional
import uuid
import pandas
import pandas
import requests
from ._constants import IOT_RESPONSE_ERROR, IOT_RESPONSE_SUCCESS, WS_DEFAULT_PORT, WS_MQTT_CONNECTION_TIMEOUT, WS_MQTT_DEFAULT_MAX_TIMEOUT, WS_MQTT_WAIT_TIME_INTERVAL
from ._mqtt import SwitchMQTT
from .._utils._utils import ApiInputs, _with_func_attrs, is_valid_uuid

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler(stream=sys.stdout)
consoleHandler.setLevel(logging.INFO)

logger.addHandler(consoleHandler)
formatter = logging.Formatter('%(asctime)s  %(name)s.%(funcName)s  %(levelname)s: %(message)s',
                              datefmt='%Y-%m-%dT%H:%M:%S')
consoleHandler.setFormatter(formatter)

global _control_api_endpoint
global _control_ws_host
global _control_ws_port
global _control_ws_username
global _control_ws_password
global _control_ws_max_timeout

_control_api_endpoint = ''
_control_ws_host = ''
_control_ws_port = WS_DEFAULT_PORT
_control_ws_username = ''
_control_ws_password = ''
_control_ws_max_timeout = WS_MQTT_DEFAULT_MAX_TIMEOUT


def set_control_variables(api_endpoint: str, ws_host: str, user_name: str, password: str,
                          ws_port: int = WS_DEFAULT_PORT, max_timeout: int = WS_MQTT_DEFAULT_MAX_TIMEOUT):
    """Set Control Variables

    Set Control Variables needed to enable control request to MQTT Broker when running locally.

    In Production, these are pulled from the deployment environment variables.

    Parameters
    ----------
    api_endpoint : str
        Platform IoT API Endpoint.
    host : str
        Host URL for MQTT connection. This needs to be datacenter specfic URL.
    port : int
        MQTT message broker port. Defaults to 443.
    user_name : str
        Username for MQTT connection
    password: str
        Password for MQTT connection
    max_timeout : int
        Max timeout set for the controls module. Defaults to 30 seconds.
    """
    global _control_api_endpoint
    global _control_ws_host
    global _control_ws_port
    global _control_ws_username
    global _control_ws_password
    global _control_ws_max_timeout

    # Check if endpoint is a valid URL
    if not api_endpoint.startswith('https://'):
        raise ValueError(
            "Invalid IoT API Endpoint. The IoT host should start with 'https://'.")

    # Check if host is a valid URL
    if not ws_host.startswith('wss://'):
        raise ValueError(
            "Invalid IoT Websocket MQTT Host. The IoT host should start with 'wss://'.")

    # Check if user_name and password are not empty
    if not user_name:
        raise ValueError("user_name cannot be empty.")
    if not password:
        raise ValueError("password cannot be empty.")

    # Check if max_timeout is greated than 0
    if max_timeout < 1:
        raise ValueError("max_timeout should be greater than 0.")

    # Set global variables
    _control_api_endpoint = api_endpoint
    _control_ws_host = ws_host
    _control_ws_port = ws_port
    _control_ws_username = user_name
    _control_ws_password = password
    _control_ws_max_timeout = max_timeout


@_with_func_attrs(df_required_columns=['ObjectPropertyId', 'Value', 'TTL'])
def submit_control(api_inputs: ApiInputs, installation_id: Union[uuid.UUID, str], df: DataFrame, has_priority: bool, session_id: uuid.UUID = uuid.uuid4(), timeout: int = WS_MQTT_CONNECTION_TIMEOUT):
    """Submit control of sensor(s)

    Required fields are:

    - ObjectPropertyId
    - Value
    - TTL

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.
    df : pandas.DataFrame
        List of Sensors for control request.
    has_priority : bool
        Flag if dataframe passes contains has_priority column.
    session_id : uuid.UUID., Optional
        Session Id to reuse when communicating with IoT Endpoint and MQTT Broker
    timeout : int, Optional:
        Default value is 30 seconds. Value must be between 1 and max control timeout set in the control variables.
            When value is set to 0 it defaults to max timeout value.
            When value is above max timeout value it defaults to max timeout value.

    Returns
    -------
    tuple
        control_response  = is the list of sensors that are acknowledged and process by the MQTTT message broker
        missing_response = is the list of sensors that are sensors that were caught by the connection time_out
            default to 30 secs - meaning the response were no longer waited to be received by the python package. 
            Increasing the time out can potentially help with this.
    """
    global _control_api_endpoint
    global _control_ws_host
    global _control_ws_port
    global _control_ws_username
    global _control_ws_password
    global _control_ws_max_timeout

    data_frame = df.copy()

    if api_inputs.api_base_url == '' or api_inputs.bearer_token == '':
        logger.error("You must call initialize() before using the API.")
        return 'Invalid api_inputs.', pandas.DataFrame()

    if not is_valid_uuid(installation_id):
        logger.error("Installation Id is not a valid UUID.")
        return 'Invalid installation_id.', pandas.DataFrame()

    if data_frame.empty:
        logger.error("Dataframe is empty.")
        return 'Empty dataframe.', pandas.DataFrame()

    if timeout < 0:
        logger.error(
            f"Invalid timeout value. Timeout should be between 0 and {_control_ws_max_timeout}. Setting to zero will default to max timeout.")
        return 'Invalid timeout.', pandas.DataFrame()

    if timeout > _control_ws_max_timeout:
        logger.critical(
            f'Timeout is greater than Max Timeout value. Setting timeout to Max Timeout Value instead.')
        timeout = _control_ws_max_timeout

    if timeout == 0:
        timeout = _control_ws_max_timeout

    required_columns = getattr(submit_control, 'df_required_columns')
    proposed_columns = data_frame.columns.tolist()

    if not set().issubset(data_frame.columns):
        logger.exception('Missing required column(s): %s', set(
            required_columns).difference(proposed_columns))
        return 'control.submit_control(): dataframe must contain the following columns: ' + ', '.join(
            required_columns), pandas.DataFrame()

    # We convert these columns to the required payload property names
    data_frame = data_frame.rename(columns={'ObjectPropertyId': 'id',
                                            'Value': 'v', 'TTL': 'dsecs'})

    if has_priority:
        if not 'Priority' in data_frame:
            logger.error(
                f"has_priority is set to True, but the dataframe does not have the column 'Priority'.")
            return 'Missing Priority column', pandas.DataFrame()
        else:
            data_frame = data_frame.rename(columns={'Priority': 'p'})

    json_payload = {
        "sensors": data_frame.to_dict(orient='records'),
        "email": api_inputs.email_address,
        "userid": api_inputs.user_id,
        "sessionId": str(session_id)
    }

    url = f"{_control_api_endpoint}/api/gateway/{str(installation_id)}/log-control-request"

    headers = api_inputs.api_headers.default

    logger.info("Sending Control Request to IoT API: POST %s", url)
    logger.info("Control Request Session Id: %s", str(session_id))
    logger.info("Control Request for User: %s=%s",
                api_inputs.email_address, api_inputs.user_id)

    response = requests.post(url, json=json_payload, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    response_object = json.loads(response.text)

    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.",
                     response.status_code, response.reason)
        logger.error(response_object[IOT_RESPONSE_ERROR])
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s',
                     response.request.url)
        return response_status, pandas.DataFrame()

    if not response_object[IOT_RESPONSE_SUCCESS]:
        logger.error(response_object[IOT_RESPONSE_ERROR])
        return response_object[IOT_RESPONSE_SUCCESS], pandas.DataFrame()

    # Proceeds when the control request is successful
    logger.info('IoT API Control Request is Successful.')

    data_frame = df.copy()

    logger.info(
        "Renaming columns to match Control Request Payload for MQTT Broker.")
    data_frame = data_frame.rename(columns={'ObjectPropertyId': 'sensorId',
                                            'Value': 'controlValue', 'TTL': 'duration'})

    if has_priority:
        if not 'Priority' in data_frame:
            logger.error(
                f"The dataframe does not have the column 'Priority'.")
        else:
            data_frame = data_frame.rename(columns={'Priority': 'priority'})

    switch_mqtt = SwitchMQTT(host_address=_control_ws_host, host_port=_control_ws_port,
                             username=_control_ws_username, password=_control_ws_password,
                             session_id=session_id, client_id=api_inputs.user_id, email=api_inputs.email_address,
                             project_id=api_inputs.api_project_id, installation_id=str(installation_id))

    is_connected = switch_mqtt.connect(timeout=timeout)

    if not is_connected:
        logger.info("Could not connect to MQTT Broker.")
        return 'Could not connect to MQTT Broker.', pandas.DataFrame()

    control_response, missing_response = switch_mqtt.send_control_request(
        sensors=data_frame.to_dict(orient='records'))

    return control_response, missing_response
