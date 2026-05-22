import paho.mqtt.client as mqtt
import time
from random import *

broker='test.mosquitto.org'
topic='tombola/numbers'

def on_connect(client, userdata, flags, rc):
	print(f'{mqtt.connack_string(rc)}')

def on_publish(client, userdata, mid):
	print(f'Estratti: {mid} numeri')

def main():
	client = mqtt.Client()

	client.on_connect = on_connect
	client.on_publish = on_publish

	print('MQTT client connection....')
	client.connect(broker)
	time.sleep(2)
	client.loop_start()

	n = list(range(1, 91))
	m = sample(n, len(n))

	try:
		for i in range(0,90):
			msg=m[i]
			client.publish(topic, msg)
			time.sleep(1)
	except KeyboardInterrupt:
		print('MQTT client disconnection...')
	finally:
		client.disconnect()
		client.loop_stop()

if __name__ == '__main__':
	main()