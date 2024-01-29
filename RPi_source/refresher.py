"""
Name: refresh.py
Desc: run scripts after a button press is detected to refresh data
Auth: Ance Strazdina
Date: 11/12/2023
"""

# imports
import subprocess

BUTTON_DEV_PATH = "/dev/button_dev" # button character device path

def main():
    with open(BUTTON_DEV_PATH, "rb") as char_device:
        # print("Button app started. Waiting for button press...")
        while True:
            message = char_device.read(1)
            if message == b'B': # 'B' is the signal message for button press in the button module LKM
                # print("Button pressed!")
                subprocess.run(['python3', '/home/pi/nordpool_scrape/elspot.py'])
                subprocess.run(['python3', '/home/pi/nordpool_scrape/hourlyTariff.py'])

if __name__ == "__main__":
    main()
