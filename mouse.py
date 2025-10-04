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
import platform

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

# Function to download msedgedriver automatically
def download_msedgedriver(dest_path):
    print("msedgedriver.exe not found. Downloading...")
    # Get latest version number
    version_url = "https://msedgedriver.azureedge.net/LATEST_STABLE"
    version = requests.get(version_url).text.strip()
    print(f"Latest EdgeDriver version: {version}")

    # Construct download URL based on OS
    system_os = platform.system()
    if system_os == "Windows":
        url = f"https://msedgedriver.azureedge.net/{version}/edgedriver_win64.zip"
    else:
        print("Only Windows is supported in this script.")
        sys.exit(1)

    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extract("msedgedriver.exe", os.path.dirname(dest_path))
    print("msedgedriver.exe downloaded successfully.")

# Download driver if not found
if not os.path.isfile(driver_path):
    download_msedgedriver(driver_path)

# Edge profile for WhatsApp
edge_profile = r"D:\whatsapp_profile"

# Selenium headless setup
options = Options()
options.add_argument("--headless")  # run without GUI
options.add_argument("--disable-gpu")
options.add_argument(f"--user-data-dir={edge_profile}")
options.add_argument("--profile-directory=Default")

# Use Service object
service = Service(driver_path)
driver = webdriver.Edge(service=service, options=options)

# Open WhatsApp Web
driver.get("https://web.whatsapp.com")
time.sleep(10)  # wait for session to load

# -----------------------------
# Mouse tracking settings
# -----------------------------
interval = 60           # check every 1 minute
monitor_duration = 300  # total monitoring duration = 5 minutes

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
