#!/usr/bin/env python3

import os
import redis
import json
import crowdai_api
import timeout_decorator
import base64

# Gather Variables
REDIS_HOST = os.getenv("CROWDAI_REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("CROWDAI_REDIS_PORT", "6379")
REDIS_DB = os.getenv("CROWDAI_REDIS_DB", 0)
REDIS_PASSWORD = os.getenv("CROWDAI_REDIS_PASSWORD", False)

CROWDAI_REDIS_COMMUNICATION_CHANNEL = os.getenv(
                                    "CROWDAI_REDIS_COMMUNICATION_CHANNEL",
                                    "CROWDAI_REDIS_COMMUNICATION_CHANNEL"
                                    )
CROWDAI_ORACLE_COMMUNICATION_CHANNEL = os.getenv(
                                    "CROWDAI_ORACLE_COMMUNICATION_CHANNEL",
                                    "CROWDAI_ORACLE_COMMUNICATION_CHANNEL"
                                    )

MODEL_SERVER = os.getenv("MODEL_SERVER", "127.0.0.1")
MODEL_PORT = os.getenv("MODEL_PORT", 8989)
CROWDAI_TIMEOUT = os.getenv("CROWDAI_TIMEOUT", "600")
CROWDAI_TIMEOUT = float(CROWDAI_TIMEOUT)
REDIS_SOCKET_TIMEOUT = float(os.getenv("REDIS_SOCKET_TIMEOUT", 60))
REDIS_SOCKET_CONNECT_TIMEOUT = float(os.getenv("REDIS_SOCKET_CONNECT_TIMEOUT", 60))


REDIS_POOL = redis.ConnectionPool(host=REDIS_HOST,
                            port=REDIS_PORT,
                            password=REDIS_PASSWORD,
                            db=REDIS_DB,
                            socket_timeout=REDIS_SOCKET_TIMEOUT,
                            socket_connect_timeout=REDIS_SOCKET_CONNECT_TIMEOUT
                            )
DATA = []
while True:
    redis_conn = redis.Redis(connection_pool=REDIS_POOL)
    response = redis_conn.rpop(CROWDAI_ORACLE_COMMUNICATION_CHANNEL)
    if response:
        try:
            response = response.decode("utf8")
            _object = json.loads(response)
        except:
            _object = {}
            _object["event_type"] = crowdai_api.CrowdAIEvents.CROWDAI_EVENT_ERROR
            _object["message"] = "Malformed Event receieved"
            _object["payload"] = {
                "corrupted-data" : response
            }

        DATA.append(_object)
    else:
        break

DATA = json.dumps(DATA)
DATA = base64.b64encode(DATA.encode('utf-8'))
print(DATA.decode('utf-8'))
