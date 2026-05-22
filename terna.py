import paho.mqtt.client as mqtt
import time

BROKER = 'test.mosquitto.org'
topic = 'tombola/terna'

def on_connect(client, userdata, flags, rc):
	print(f'{mqtt.connack_string(rc)}')
	client.subscribe(topic)

def on_subscribe(client, userdata, mid, granted_qos):
	print(f'subscribed {topic} with qos {granted_qos[0]}\n')

def on_message(client, userdata, msg):
	print(f'Ha fatto terna: {msg.payload.decode()}')

def main():
	client = mqtt.Client()

	#associazione tra eventi e funzioni di callback
	client.on_connect = on_connect
	client.on_subscribe = on_subscribe
	client.on_message = on_message

	#connessione del client al broker
	print('MQTT client connection....')
	client.connect(BROKER)

	try:
		client.loop_forever()
	except KeyboardInterrupt:
		print('MQTT client disconnection...')
	finally:
		client.disconnect()
		client.loop_stop()

if __name__ == '__main__':
	main()