import datetime
import importlib
import json
import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libs'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'agent'))

import coverage
import requests
#
from agent.footprint_service import FootprintService
from agent.footprint_model import FootprintModel, FootprintExecutionHit, FootprintExecution, FootprintMeta
from agent.agent_config import AgentConfig

cov = coverage.Coverage(data_file='/tmp/.coverage')

orig_lambda_handler = os.environ.get('ORIG_NAME', '')
orig_module_name, orig_function_name = orig_lambda_handler.rsplit('.', 1)
orig_module = importlib.import_module(orig_module_name)
orig_function = getattr(orig_module, orig_function_name)
sl_debug = os.environ.get('SL_DEBUG', 'false').lower() == 'true'


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (FootprintExecutionHit, FootprintExecution, FootprintModel, FootprintMeta, AgentConfig)):
            return obj.__dict__
        return super().default(obj)


def send_collector(url, data_object: FootprintModel):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        data_json = json.dumps(data_object, cls=CustomEncoder, indent=4)
        debug(f'Footprints JSON: {data_json}')
        response = requests.post(url, data=data_json, headers=headers)
        response.raise_for_status()
    except requests.HTTPError as http_err:
        error(f'HTTP error occurred: {http_err}')
    except requests.ConnectionError as conn_err:
        error(f'Connection error occurred: {conn_err}')
    except requests.Timeout as timeout_err:
        error(f'Timeout error occurred: {timeout_err}')
    except requests.RequestException as req_err:
        error(f'An error occurred during the request: {req_err}')
    except json.JSONDecodeError:
        error('Failed to decode JSON response from server.')
    except Exception as e:
        error(f'An unexpected error occurred: {e}')


def lambda_handler(event, context):
    info("Starting Sealights lambda wrapper handler")
    debug("Debug mode is on")
    is_valid_config = False
    agent_config = AgentConfig()
    try:
        agent_config.load_from_env_or_file('sl_lambda_config.json')
        debug(f'Agent config: {agent_config}')
        agent_config.validate()
        is_valid_config = True
    except Exception as e:
        error(e)

    if is_valid_config:
        debug("Starting Sealights Coverage")
        cov.start()

    debug("Calling original lambda function")
    start_time = int(time.time())
    lambda_response = orig_function(event, context)
    end_time = int(time.time())
    debug("Original lambda function returned")
    if is_valid_config:
        debug("Stopping Sealights Coverage")
        cov.stop()
        footprints_service = FootprintService(agent_config)
        fm = footprints_service.get_footprints_model(cov.get_data(), start_time, end_time)
        post_url = "%s/api/v6/agents/%s/footprints" % (agent_config.collectorUrl, agent_config.buildSessionId)
        debug(f'Posting footprints to {post_url}')
        send_collector(post_url, fm)
        cov.erase()
        debug("Erased Sealights Coverage")
    info("Finished Sealights lambda wrapper handler")
    return lambda_response


def info(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} [SEALIGHTS-AGENT] - INFO: {message}')


def error(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} [SEALIGHTS-AGENT] - ERROR: {message}')


def debug(message):
    if not sl_debug:
        return
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestamp} [SEALIGHTS-AGENT] - DEBUG: {message}')
