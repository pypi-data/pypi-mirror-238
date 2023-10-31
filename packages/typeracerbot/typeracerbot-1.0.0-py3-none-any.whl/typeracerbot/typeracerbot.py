import cv2
import os
import numpy as np 
from imutils.object_detection import non_max_suppression 
import pyautogui

def run_auto_typer():

    pyautogui.hotkey("command", "tab", interval=0.25 )

    pyautogui.hotkey("command","t", intterval=1 ) 

    pyautogui.typewrite("play.typeracer.com")

    pyautogui.press("enter")

    pyautogui.sleep(5)

    pyautogui.click(250,550)

    pyautogui.sleep(1)

    letter_path = os.path.join(os.getcwd(), "typeracerbot/letters")

    type_string = ""

    image = pyautogui.screenshot() 

    image = cv2.cvtColor(np.array(image), 
                        cv2.COLOR_RGB2BGR) 
    y_change = 0
    last_character = "."
    x_change = 0

    while x_change < 80:
        width = 14
        offset = 12
        crop_img = image[372+y_change*23:396+y_change*23,182+x_change*offset:182+width+x_change*offset]

        bestFit = "0"
        best_character = " "

        for file_name in os.listdir(letter_path):

            if file_name == '.DS_Store':
                continue
   
            img_gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY) 
            temp_gray = cv2.cvtColor(cv2.imread(letter_path+"/"+file_name), cv2.COLOR_BGR2GRAY) 

            height, width= img_gray.shape

            height, width = temp_gray.shape

            match = cv2.matchTemplate(image=img_gray, templ=temp_gray, method=cv2.TM_CCOEFF_NORMED)

            (y_points, x_points) = np.where(match >= 0.75) 

            for (y,x) in zip(y_points,x_points): 
                if float(bestFit) < float(match[y,x]):
                    bestFit = match[y,x]
                    best_character = file_name

        if best_character[0]=='"' and best_character[2]=='"':
            current_letter = best_character[1]
        else:
            current_letter = best_character[0]
        if current_letter == '*':
            current_letter = ":"

        if x_change == 0 and best_character == " ":
            break

        x_change += 1

        if last_character == " " and best_character == " ":
            x_change = 0
            y_change+=1
            last_character == "."
        else:
            type_string += current_letter
            last_character = current_letter

    print(type_string)

    pyautogui.write(type_string) 

        
