import json
import time
from threading import Event
from typing import Any, Optional

import paho.mqtt.client as mqtt
import requests

# Feel free to add more libraries (e.g.: The REST Client library)

mqtt_client: Optional[mqtt.Client] = None

mqtt_connection_event = Event()

secret = -1


def send_secret_rest(secret_value: int):
    # Add the logic to send this secret value to the REST server.
    # We want to send a JSON structure to the endpoint `/secret_number`, using
    # a POST method.
    #
    # Assuming secret_value = 50, then the request will contain the following
    # body: {"value": 50}
    headers = {
        'Content-Type': 'application/json'
    }
    data = json.dumps({"value": secret_value})
    try:
        requests.post("http://server:80/secret_number",
                      data=data, headers=headers)
    except Exception as err:
        print(err)


def on_mqtt_connect(client, userdata, flags, rc):
    print('Connected to MQTT broker')
    client.subscribe("secret/number")
    mqtt_connection_event.set()


def on_mqtt_message(client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage):
    # Implement the logic to parse the received secret (we receive a json, but
    # we are interested just on the value) and send this value to the REST
    # server... or maybe the sending to REST should be done somewhere else...
    # do you have any idea why?
    global secret
    secret = json.loads(msg.payload.decode(encoding="utf-8"))["value"]
    send_secret_rest(secret)


def connect_mqtt() -> mqtt.Client:
    client = mqtt.Client(
        clean_session=True,
        protocol=mqtt.MQTTv311
    )
    client.on_connect = on_mqtt_connect
    client.on_message = on_mqtt_message
    client.loop_start()
    client.connect('mqtt-broker', 1883)
    return client


def main():
    global mqtt_client

    mqtt_client = connect_mqtt()
    mqtt_connection_event.wait()
    
    time.sleep(1)

    # At this point, we have our MQTT connection established, now we need to:
    # 1. Subscribe to the MQTT topic: secret/number
    # 2. Parse the received message and extract the secret number
    # 3. Send this number via REST to the server, using a POST method on the
    # resource `/secret_number`, with a JSON body like: {"value": 50}
    # 4. (Extra) Check the REST resource `/secret_correct` to ensure it was
    # properly set
    # 5. Terminate the script, only after at least a value was sent


    try:
        mqtt_client.disconnect()
    except Exception:
        pass
    try:
        mqtt_client.loop_stop()
    except Exception:
        pass


if __name__ == '__main__':
    main()
