import datetime
import random
import sys
import time

import paho.mqtt.client as mqtt


DEVICE_ID = 'PythonAsMcu'
MQTT_HOSTNAME = 'localhost'
MQTT_PORT = 1883


def create_simple_payload():
    return ';'.join(['0'] * 10)


def create_temp_on_d5_payload():
    payload = ['0'] * 10
    payload[0] = str(random.randint(25, 30))
    return ';'.join(payload)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    topic = 'esp/{}/in'.format(DEVICE_ID)
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


def handle_pub_command():
    topic = 'esp/{}/out'.format(DEVICE_ID)
    client = mqtt.Client()
    client.connect(MQTT_HOSTNAME, MQTT_PORT, 60)  # keep alive 60s

    while True:
        now = datetime.datetime.now()
        print(now)

        try:
            payload = create_temp_on_d5_payload()
            client.publish(topic, payload)
        except KeyboardInterrupt:
            break
        time.sleep(5)


def handle_sub_command():
    topic = 'esp/{}/in'.format(DEVICE_ID)
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_HOSTNAME, MQTT_PORT, 60)  # keep alive 60s
    client.loop_forever()


def print_help():
    help_msg = '''python main.py [pub/sub]
        pub: act like an esp to send data to mqtt
        sub: act like an esp to recv data from mqtt
    '''
    print(help_msg)
    sys.exit(1)


def main():
    n = len(sys.argv)
    if n != 2:
        print_help()

    command = sys.argv[1]
    if command == 'pub':
        handle_pub_command()
    elif command == 'sub':
        handle_sub_command()
    else:
        print('Invalid command!')
        print_help()


if __name__ == '__main__':
    main()

