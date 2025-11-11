import cv2
import numpy as np
from mss import mss
import pyautogui
from ultralytics import YOLO
import torch
import os
import time
import keyboard  # <-- (NEW) IMPORT FOR GLOBAL KEYPRESS


DEBUG = True 
MODEL_PATH = 'v8n-pokidata.pt'

MONITOR_REGION = {
    'top': 130,
    'left': 1107,
    'width': 793,
    'height': 447
}
FRUIT_NAMES = ['banana', 'coconut', 'greenapple', 'kiwi', 'lemon', 'mango', 'orange', 'peach', 'pineapple', 'watermelon']
BOMB_NAME = 'bomb'

CONF_THRESHOLD = 0.2

BOMB_SAFETY_MARGIN_PIXELS = 35
SAFE_POSITION = (MONITOR_REGION['left'] + 10, MONITOR_REGION['top'] + 10)

REL_SAFE_POS = (10, 10) 

TARGET_LEAD_PIXELS = 13


pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

try:
    import torch_directml
    if torch_directml.is_available():
        device = torch_directml.device()
        print(f"Using device: torch_directml (AMD GPU)")
    elif torch.cuda.is_available():
        device = 'cuda'
        print(f"Using device: cuda (NVIDIA GPU)")
    else:
        device = 'cpu'
        print(f"Using device: cpu")
except ImportError:
    print("torch_directml not found.")
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Falling back to device: {device}")


model = YOLO(MODEL_PATH)
sct = mss()

FRUIT_NAMES_LOWER = [name.lower() for name in FRUIT_NAMES]
BOMB_NAME_LOWER = BOMB_NAME.lower()

# --- HELPER FUNCTIONS FOR PATH CHECKING ---
def is_point_in_rect(point, rect):
    """Checks if a (x, y) point is inside a (x1, y1, x2, y2) rect."""
    px, py = point
    r_x1, r_y1, r_x2, r_y2 = rect
    return (r_x1 < px < r_x2) and (r_y1 < py < r_y2)

def is_path_safe(start, end, bomb_zones, pixel_step=20):
    """
    Checks if the straight-line path from start to end intersects any bomb zones
    by checking one point every 'pixel_step' pixels.
    """
    start_v = np.array(start)
    end_v = np.array(end)
    path_vector = end_v - start_v
    path_length = np.linalg.norm(path_vector)

    if path_length < 1: #no movement
        return True

    num_steps = max(2, int(path_length / pixel_step)) 

    for i in range(1, num_steps + 1):
        t = i / num_steps
        check_x = start[0] * (1 - t) + end[0] * t
        check_y = start[1] * (1 - t) + end[1] * t
        
        # check if this interpolated point is in any bomb zone
        for zone in bomb_zones:
            if is_point_in_rect((check_x, check_y), zone):
                return False # Path is blocked!
    return True # Path is clear


print("Starting Fruit Ninja auto-player. Press 'ESC' to stop.")

prev_frame_time = 0
new_frame_time = 0

try:
    pyautogui.mouseDown(button='left')
    print("Left mouse button held down for smooth slicing.")
    
    cv2.namedWindow('Fruit Ninja Detection', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Fruit Ninja Detection', 800, 500)

    while True:
        if keyboard.is_pressed('esc'):
            print("\n[INFO] 'ESC' pressed. Exiting...")
            break
        
        screenshot = sct.grab(MONITOR_REGION)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        results = model.predict(img, verbose=False, conf=CONF_THRESHOLD, device=device, imgsz=640)

        annotated_img = results[0].plot()
        if annotated_img.shape[2] == 4: 
            annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_BGRA2BGR)
            
        new_frame_time = time.time()
        if (new_frame_time - prev_frame_time) > 0:
            fps = 1 / (new_frame_time - prev_frame_time)
        else:
            fps = 0
        prev_frame_time = new_frame_time
        
        fps_text = f"FPS: {int(fps)}"
        cv2.putText(annotated_img, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        cv2.imshow('Fruit Ninja Detection', annotated_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass # 'q' is disabled, use 'ESC'

        boxes = results[0].boxes
        bomb_zones = []
        fruit_targets = []
        class_names = results[0].names  

        if boxes is not None:
            for box in boxes:
                cls_id = int(box.cls[0].item())
                cls_name = class_names[cls_id].lower()
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

                if cls_name == BOMB_NAME_LOWER:
                    z_x1 = max(0, x1 - BOMB_SAFETY_MARGIN_PIXELS)
                    z_y1 = max(0, y1 - BOMB_SAFETY_MARGIN_PIXELS)
                    z_x2 = min(MONITOR_REGION['width'], x2 + BOMB_SAFETY_MARGIN_PIXELS)
                    z_y2 = min(MONITOR_REGION['height'], y2 + BOMB_SAFETY_MARGIN_PIXELS)
                    bomb_zones.append((z_x1, z_y1, z_x2, z_y2))

                elif cls_name in FRUIT_NAMES_LOWER:
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2
                    fruit_targets.append(((center_x, center_y), (x1, y1, x2, y2)))

        
        current_pos = pyautogui.position()
        rel_current_pos = (
            current_pos[0] - MONITOR_REGION['left'],
            current_pos[1] - MONITOR_REGION['top']
        )

        mouse_is_in_danger = False
        for zone in bomb_zones:
            if is_point_in_rect(rel_current_pos, zone):
                mouse_is_in_danger = True
                break
        
        if mouse_is_in_danger:
            pyautogui.mouseUp(button='left')
            pyautogui.moveTo(*SAFE_POSITION, duration=0)
            pyautogui.mouseDown(button='left')
            continue 

        path_safe_fruits = []
        for center, box in fruit_targets:
            center_is_safe = True
            for zone in bomb_zones:
                if is_point_in_rect(center, zone):
                    center_is_safe = False 
                    break
            
            if center_is_safe and is_path_safe(rel_current_pos, center, bomb_zones):
                path_safe_fruits.append((center, box)) # Good to go!

        if path_safe_fruits:
            closest_target_center = None
            min_distance = float('inf')

            for center, box in path_safe_fruits:
                center_x, center_y = center
                distance = ((center_x - rel_current_pos[0]) ** 2 + (center_y - rel_current_pos[1]) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    closest_target_center = center
            
            if closest_target_center:
                swipe_x, swipe_y = closest_target_center
                swipe_y -= TARGET_LEAD_PIXELS # Apply lead
                
                abs_swipe = (
                    int(MONITOR_REGION['left'] + swipe_x),
                    int(MONITOR_REGION['top'] + swipe_y)
                )
                pyautogui.moveTo(*abs_swipe, duration=0)
        
        else:
            pass


except KeyboardInterrupt:
    print("\nStopped by user (KeyboardInterrupt).")
except Exception as e:
    print(f"Error during gameplay: {e}")
finally:
    pyautogui.mouseUp(button='left')
    cv2.destroyAllWindows()
    print("Auto-player stopped.")