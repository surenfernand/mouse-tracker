import pyautogui
import time
import math
import os
import requests
import zipfile
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import io
import sys

# -----------------------------
# WhatsApp / Selenium settings
# -----------------------------
contact_name = "Suren Dialog"
low_activity_msg = "Hey, mouse activity is low (less than 1000px in 1 minute)."
high_activity_msg = "Hey, mouse activity is unusually high (over 5000px in 1 minute)."

# -----------------------------
# Edge WebDriver setup
# -----------------------------
driver_path = r"D:\msedgedriver.exe"
temp_profile = r"D:\edge_temp_profile"

# Download msedgedriver if not found
def download_msedgedriver(path):
    if os.path.exists(path):
        return
    print("msedgedriver.exe not found. Downloading...")
    version_url = "https://msedgedriver.azureedge.net/LATEST_STABLE"
    version = requests.get(version_url).text.strip()
    system_os = "win64" if sys.maxsize > 2**32 else "win32"
    download_url = f"https://msedgedriver.azureedge.net/{version}/edgedriver_{system_os}.zip"
    r = requests.get(download_url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extract("msedgedriver.exe", os.path.dirname(path))
    print("msedgedriver.exe downloaded.")

download_msedgedriver(driver_path)

# Selenium Edge options
options = Options()
options.add_argument(f"--user-data-dir={temp_profile}")  # temp profile
options.add_argument("--disable-gpu")
options.add_argument("start-minimized")
# options.add_argument("--headless")  # optional, headless often crashes with WhatsApp Web

# Use Service object
service = Service(driver_path)
driver = webdriver.Edge(service=service, options=options)

# Open WhatsApp Web
driver.get("https://web.whatsapp.com")
time.sleep(5)  # scan QR on first run

# -----------------------------
# Mouse tracking settings
# -----------------------------
interval = 10           # check every 10 seconds
monitor_duration = 30  # total monitoring duration = 5 minutes

print("Monitoring mouse movement continuously...")

while True:
    start_time = time.time()
    last_pos = pyautogui.position()
    movement_distance = 0
    next_check_time = start_time + interval

    while time.time() - start_time < monitor_duration:
        current_pos = pyautogui.position()
        distance = math.dist(last_pos, current_pos)
        movement_distance += distance
        last_pos = current_pos

        # Check once every 'interval' seconds
        if time.time() >= next_check_time:
            print(f"Mouse moved {movement_distance:.2f} pixels in the past {interval} seconds.")

            try:
                # Open the chat
                search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
                search_box.clear()
                search_box.send_keys(contact_name)
                time.sleep(2)
                contact = driver.find_element(By.XPATH, f'//span[@title="{contact_name}"]')
                contact.click()
                time.sleep(1)
                msg_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')

                if movement_distance < 1000:
                    print("Low movement detected — sending alert.")
                    msg_box.send_keys(low_activity_msg + "\n")
                elif movement_distance > 5000:
                    print("High movement detected — sending alert.")
                    msg_box.send_keys(high_activity_msg + "\n")
            except Exception as e:
                print(f"Error sending message: {e}")

            # Reset movement and update next check time
            movement_distance = 0
            next_check_time = time.time() + interval

        time.sleep(1)

    print("Completed one 5-minute monitoring cycle — restarting...\n")
