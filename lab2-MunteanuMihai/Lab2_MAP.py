import pyautogui
import time
import keyboard

def cautare_google():
    time.sleep(3)
    if(pyautogui.locateOnScreen(r"C:\Users\munte\Desktop\lab2\s1.png")!=None):
      camp_cautare_google = pyautogui.locateOnScreen(r"C:\Users\munte\Desktop\lab2\s2.png")
      pyautogui.click(camp_cautare_google)
      time.sleep(3)
      pyautogui.write("http://youtube.com")
      time.sleep(1)
      pyautogui.press('enter')
      time.sleep(1)
      if(pyautogui.locateOnScreen(r"C:\Users\munte\Desktop\lab2\s1.png")!=None):
        camp_cautare_youtube = pyautogui.locateOnScreen(r"C:\Users\munte\Desktop\lab2\s2.png")
        pyautogui.click2(camp_cautare_youtube)
    else:
        print("NIMIC PE ECRAN")

def coordonate_mouse():
    while not keyboard.is_pressed('x'):
        print(pyautogui.position())
        time.sleep(0.2)

cautare_google()
coordonate_mouse()
pyautogui.click(868,228)
pyautogui.click2(351,397)

