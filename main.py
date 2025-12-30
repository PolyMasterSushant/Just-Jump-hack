import pyautogui as pg
import time
import subprocess

def jump_needed():
    # Tells if jump is needed

    #Shruken
    try:
        shruken = pg.locateOnScreen('shruken.png', confidence=0.7)
        print(f"Shruken located at: {shruken}")
    except Exception as e:
        print(f"Error locating shruken: {e}")
        shruken = None
    #Player
    try:
        player = pg.locateOnScreen('player.png', confidence=0.7)
        print(f"Player located at: {player}")
    except Exception as e:
        print(f"Error locating player: {e}")
        player = None
    
    if shruken is not None and player is not None:
        if abs(shruken[0] - player[0]) < 20:
            print("Jump")
            return True
        else:
            return False
    return None


subprocess.Popen(['Just Jump.exe'])
time.sleep(3)  # Wait for the game to load
pg.press('space')  # Start the game
while True:
    needed = jump_needed()
    if needed is None:
        print("Could not locate player or shruken.")
    elif needed:
        pg.press('space')
    time.sleep(0.1)  # Small delay to prevent excessive CPU usage
