import pyautogui
import pywhatkit
import time
 
phone_number = "+94762797637"   
message = "Hey, I have been idle for 5 minutes."
 
idle_limit = 10   
last_mouse_pos = pyautogui.position()
last_move_time = time.time()

while True:
    current_pos = pyautogui.position()

    if current_pos != last_mouse_pos: 
        last_move_time = time.time()
        last_mouse_pos = current_pos
 
    if time.time() - last_move_time > idle_limit:
        print("Idle for 5 minutes! Sending WhatsApp message...")
 
        pywhatkit.sendwhatmsg_instantly(phone_number, message, 15, True)

        break   

    time.sleep(5)  
