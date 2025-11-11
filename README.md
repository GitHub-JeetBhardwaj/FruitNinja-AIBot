# FruitNinja AI Bot

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## Overview

**FruitNinja AI Bot** is an automated system designed to play the popular *Fruit Ninja* game using artificial intelligence and computer vision.  
The bot detects fruits on the screen, tracks their motion, and performs swipe gestures programmatically to maximize the score—mimicking human gameplay with precision.

---

## Features

- Real-time screen capture and fruit detection  
- Object recognition using trained AI model  
- Automated mouse gestures for slicing fruits  
- Adjustable speed and accuracy for testing  
- Modular, easy-to-modify Python codebase  

---

## Tech Stack

- **Programming Language:** Python  
- **Core Libraries:** OpenCV, NumPy, PyTorch  
- **Automation:** PyAutoGUI (for mouse control)  
- **Model Type:** YOLO or CNN-based object detector  

---

## Project Structure

```

FruitNinja-AIBot/
│
├── model/               # Trained AI model weights
├── data/                # Sample game frames or datasets
├── src/                 # Core Python source code
│   ├── capture.py       # Screen capture and preprocessing
│   ├── detect.py        # Fruit detection logic
│   ├── action.py        # Swipe and interaction functions
│   └── main.py          # Entry point for the AI bot
│
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── LICENSE              # License information

````

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/FruitNinja-AIBot.git
   cd FruitNinja-AIBot


2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Place your trained model file (e.g., `best.pt`) in the `model/` directory.

---

## Usage

1. Launch the Fruit Ninja game (windowed mode recommended).
2. Run the AI bot:

   ```bash
   python src/main.py
   ```
3. The bot will automatically detect fruits and simulate slicing actions in real time.

---

## Configuration

You can modify parameters such as:

* Screen region for capture
* Detection confidence threshold
* Swipe speed and angle

All configuration options are located in the `config.py` file (if available).

---

## Results

* Average reaction time: ~50–100 ms per detection
* High accuracy fruit detection using trained AI model
* Smooth automation of swipe gestures

*(Add screenshots or GIFs showing the bot in action here)*

---

## Contributing

Contributions are welcome.

1. Fork the project
2. Create a new branch
3. Submit a pull request with detailed changes

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

* Inspired by the *Fruit Ninja* game by Halfbrick Studios
* Uses open-source computer vision and automation frameworks
