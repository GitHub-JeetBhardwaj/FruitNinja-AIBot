# FruitNinja-AIBot

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Ultralytics](https://img.shields.io/badge/Ultralytics-000000?style=for-the-badge&logo=ultralytics&logoColor=white)

## Overview

This project is an AI-powered bot designed to play the game Fruit Ninja. It utilizes real-time object detection through a YOLOv8 model to identify fruits and bombs on the screen. The bot automates mouse movements to slice fruits while implementing sophisticated logic to avoid bombs and ensure the slicing path is safe.

## Features

* **Real-time Object Detection**: Employs a YOLOv8 model (`v8n-pokidata.pt`) to detect various fruits and bombs in real-time.
* **Intelligent Bomb Avoidance**: Creates a configurable safety margin around detected bombs and prevents the cursor from entering these zones.
* **Safe Path-finding**: Before moving to a fruit, the bot checks if the straight-line path from the current cursor position to the target is clear of any bomb "danger zones".
* **Cursor Safety**: If the cursor finds itself within a bomb's danger zone, it automatically retreats to a predefined safe position.
* **Target Prioritization**: Identifies the closest, path-safe fruit to maximize slicing efficiency.
* **Hardware Acceleration**: Automatically detects and utilizes NVIDIA (CUDA) or AMD (DirectML) GPUs via PyTorch, with a fallback to CPU if no compatible GPU is found.
* **Visual Debugging**: Provides a live OpenCV window (`Fruit Ninja Detection`) showing the game capture with detection boxes and FPS.
* **Easy Configuration**: A helper script (`window-size.py`) is included to visually select and configure the game's screen region.

## Dependencies

The script requires the following Python libraries:

* `opencv-python`
* `numpy`
* `mss`
* `pyautogui`
* `ultralytics`
* `torch`
* `keyboard`
* `torch_directml` (Optional, for AMD GPU acceleration)

You can install the primary dependencies using pip:
```bash
pip install opencv-python numpy mss pyautogui ultralytics torch keyboard
````

## Setup and Configuration

1.  **Install Dependencies**: Run the pip install command listed above.
2.  **Configure Game Region**:
      * Before running the main bot, you must define the area of your screen where the game is played.
      * Run the `window-size.py` script:
        ```bash
        python window-size.py
        ```
      * A full-screen screenshot will appear. Click and drag a box around the active game area (where fruits appear).
      * Press `ENTER` to confirm your selection.
      * The script will print a `MONITOR_REGION` dictionary to your console.
      * Copy this dictionary and paste it into `final-path.py`, replacing the existing `MONITOR_REGION` variable.
3.  **Model File**: Ensure the `v8n-pokidata.pt` model file is located in the same directory as `final-path.py`, or update the `MODEL_PATH` variable in the script to point to its location.

## How to Use

1.  Complete the **Setup and Configuration** steps.
2.  Open and run your Fruit Ninja game in the region you defined.
3.  Run the main bot script:
    ```bash
    python final-path.py
    ```
4.  The bot will initialize, print the device it is using (e.g., `cuda`, `cpu`), and hold down the left mouse button to begin slicing.
5.  A window titled 'Fruit Ninja Detection' will appear, showing the bot's view.
6.  To stop the bot at any time, press the **ESC** key.

## License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2025 Jeet Bhardwaj

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
