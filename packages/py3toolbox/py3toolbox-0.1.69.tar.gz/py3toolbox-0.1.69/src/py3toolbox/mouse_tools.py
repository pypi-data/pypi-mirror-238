import pyautogui
import time


def get_mouse_pos():
  pos = pyautogui.position()
  return (pos.x, pos.y)
  
if __name__ == "__main__":
  while 1:
    print (get_mouse_pos())
    

