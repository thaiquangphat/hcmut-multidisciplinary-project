import sys
from Adafruit_IO import MQTTClient
from Adafruit_IO import Client
import random
import time
import serial.tools.list_ports

def pushing_command(adadevice, value):
    AIO_FEED_ID = adadevice
    AIO_USERNAME = '<YOUR_USERNAME>'
    AIO_KEY = '<YOUR_API_KEY>'

    def connected(client): 
        client.subscribe(AIO_FEED_ID)
        # print('Kết nối thành công.')

    def subscribe(client, userdata, mid, granted_qos):
        # print('Subscribe thành công.')
        pass

    def disconnected(client):
        sys.exit(1)
        # print('Ngắt kết nối thành công.')

    def message(client, feed_id, payload):
        # print('Nhận dữ liệu ' + payload)
        pass
    
    client = MQTTClient(AIO_USERNAME , AIO_KEY)
    client.on_connect = connected
    client.on_disconnect = disconnected
    client.on_message = message
    client.on_subscribe = subscribe
    client.connect()
    client.loop_background()

    # print("Cập nhật:", value)
    try:
        time.sleep(5)
        client.publish(adadevice, value)
        print(f'Cập nhật thành công. {adadevice} = {value}.')
        time.sleep(5)
        return True
    except Exception as e:
        return e
    
def get_value_from_feed(feed: str): 
    AIO_USERNAME = 'YOUR_USERNAME'
    AIO_KEY = 'YOUR_API_KEY'

    aio = Client(username=AIO_USERNAME, key=AIO_KEY)

    recive_value = aio.receive(feed).value

    return recive_value