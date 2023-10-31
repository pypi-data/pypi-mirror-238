import cv2
import os
import numpy as np 
from imutils.object_detection import non_max_suppression 
import pyautogui

def navigate_to_typeracer():

    pyautogui.hotkey("command", "tab", interval=0.25 )

    pyautogui.hotkey("command","t", intterval=1 ) 

    pyautogui.typewrite("play.typeracer.com")

    pyautogui.press("enter")

    pyautogui.sleep(5)

    pyautogui.click(250,550)

    pyautogui.sleep(1)

def process_and_type():

    letter_path = os.path.join(os.getcwd(), "typeracerbot/letters")

    # take screenshot using pyautogui 
    image = pyautogui.screenshot() 
    
    # since the pyautogui takes as a  
    # PIL(pillow) and in RGB we need to  
    # convert it to numpy array and BGR  
    # so we can write it to the disk 
    image = cv2.cvtColor(np.array(image), 
                        cv2.COLOR_RGB2BGR) 
    
    # writing it to the disk using opencv 
    # cv2.imwrite("typeracerbot/app/typeracerbot/typeracer.png", image)

    letter_positions = []
    line_values = []

    # Reading the image and the template 
    # img = cv2.imread("typeracerbot/app/typeracerbot/typeracer.png") 


    for file_name in os.listdir(letter_path):

        thresh = .91

        if file_name == '.DS_Store':
            continue
        
        if file_name[0]=='"' and file_name[2]=='"':
            current_letter = file_name[1]
            thresh = 0.85
        else:
            current_letter = file_name[0]

        if current_letter == '*':
            current_letter = ":"

        temp = cv2.imread(letter_path+"/"+file_name) 
        
        # Define a minimum threshold 
        if current_letter == "w":
            thresh = .82
        if current_letter == "m":
            thresh = .84
        if current_letter == "v":
            thresh = .91
        if current_letter == ".":
            thresh = 0.985
        if current_letter == ',' or current_letter == '-' or current_letter == '1':
            thresh = 0.96
        
        # Converting them to grayscale 
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
        temp_gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY) 
        
        # Passing the image to matchTemplate method 
        match = cv2.matchTemplate(image=img_gray, templ=temp_gray, method=cv2.TM_CCOEFF_NORMED) 
        
        # Select occurances with greater value than threshhold
        (y_points, x_points) = np.where(match >= thresh) 

        for (x, y) in zip(x_points, y_points): 
            found = False
            for row_y in line_values:
                if abs(row_y-y)<=8:
                    y = row_y
                    found = True
                    break
            if found == False:
                line_values.append(y)
            letter_positions.append((x,y,current_letter))

    def rowOrder(tuple):
        return tuple[0]+tuple[1]*10

    # Use the sorted() function to sort the list of tuples using the key function
    letter_positions = sorted(letter_positions, key=(lambda tuple: (tuple[1],tuple[0])))

    #print(letter_positions)

    typeString = ""
    lastX = 0
    for tuple in letter_positions:
        if abs(tuple[0]-lastX)>16:
            typeString += " " 
        lastX = tuple[0]
        typeString += tuple[2]

    typeString = typeString.replace(" Type the above text here when the race begins","")
    print(typeString)
    pyautogui.write(typeString)