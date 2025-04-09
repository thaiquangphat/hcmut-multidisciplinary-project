import sys
from Adafruit_IO import MQTTClient
import random
import time
import serial.tools.list_ports

def pushing_command(adadevice, value):
    AIO_FEED_ID = adadevice
    AIO_USERNAME = 'Phat_Adafruit'
    AIO_KEY = 'aio_FpCw83QuD1wktNbwmwyGBBajuNEU'

    def connected(client): 
        client.subscribe(AIO_FEED_ID)
        print('Kết nối thành công.')

    def subscribe(client, userdata, mid, granted_qos):
        print('Subscribe thành công.')

    def disconnected(client):
        sys.exit(1)
        print('Ngắt kết nối thành công.')

    def message(client, feed_id, payload):
        print('Nhận dữ liệu ' + payload)

    client = MQTTClient(AIO_USERNAME , AIO_KEY)
    client.on_connect = connected
    client.on_disconnect = disconnected
    client.on_message = message
    client.on_subscribe = subscribe
    client.connect()
    client.loop_background()

    print("Cập nhật:", value)
    client.publish(adadevice, value)