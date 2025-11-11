import cv2
import pyautogui
import numpy as np

print("--- Visual Region Selector (GUI) ---")
print("\nInstructions:")
print("1. A screenshot of your entire screen will appear.")
print("2. CLICK and DRAG your mouse to draw a box around the game area.")
print("3. Once the box is correct, press 'ENTER' or 'SPACE' to confirm.")
print("4. Press 'c' to cancel and re-draw.")
print("\nTaking screenshot...")

# 1. Take a screenshot of the entire screen
screenshot = pyautogui.screenshot()
img = np.array(screenshot)
# Convert from RGB (pyautogui) to BGR (OpenCV)
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

# 2. Create a resizable window
window_name = "Select Game Area (Drag box, then press ENTER)"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
# Move window to top-left
cv2.moveWindow(window_name, 0, 0)
# Set to fullscreen so coordinates are 1:1 with your monitor
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


# 3. Use OpenCV's built-in Region of Interest (ROI) selector
# It handles all the mouse dragging and drawing logic
try:
    # showCrosshair=True, fromCenter=False are defaults but good to be explicit
    roi = cv2.selectROI(window_name, img, fromCenter=False, showCrosshair=True)
    cv2.destroyAllWindows()

    # 4. Unpack the (x, y, w, h) from the ROI
    left, top, width, height = roi

    if width == 0 or height == 0:
        print("\nSelection Canceled. No region selected.")
    else:
        # 5. Print the result in the format you need
        print("\n--- ✂️ COPY AND PASTE THIS INTO YOUR SCRIPT ✂️ ---")
        print("\nMONITOR_REGION = {")
        print(f"    'top': {top},")
        print(f"    'left': {left},")
        print(f"    'width': {width},")
        print(f"    'height': {height}")
        print("}")
        print("\n")

except Exception as e:
    print(f"\nAn error occurred. Did you close the window? Error: {e}")
finally:
    cv2.destroyAllWindows()