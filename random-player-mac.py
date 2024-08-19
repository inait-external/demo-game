import pyautogui
import time
import random

# List of arrow keys and a "middle" option
actions = ['right', 'left', 'middle']

# Function to randomly press an arrow key or do nothing every n seconds
def random_arrow_key_press():
    while True:
        # Choose a random action
        action = random.choice(actions)
        
        if action == 'middle':
            # Do nothing for this iteration
            print("Middle chosen: Doing nothing")
        else:
            # Press the chosen arrow key
            pyautogui.press(action)
            print(f"Pressed {action} arrow key")
        
        # Wait for n second(s) before the next action
        time.sleep(0.8)

# Run the function
random_arrow_key_press()

