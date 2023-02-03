import serial
import requests
import time


URL = 'http://YOUR_IP_ADDRESS/device/rgb/'
ser = serial.Serial('COM7', 9600)


while True:
    r, g, b = ser.readline().strip().split()
    print(r, g, b)
    print("-----------------------------------")

    with requests.Session() as s:
        s.get(URL, timeout=60)
        response = s.post(URL, data={'red': r, 'green': g, 'blue': b}, timeout=60,
                          headers={'X-CSRFToken': s.cookies.get('csrftoken'),
                                   'Referer': URL})
        if response.status_code != 200:
            print(f"{response.status_code}: Can not send the rgb data")
    time.sleep(1.5)
