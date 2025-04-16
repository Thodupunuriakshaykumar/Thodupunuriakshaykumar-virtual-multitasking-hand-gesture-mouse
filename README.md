# Hand Gesture Control System 🖐️

## Introduction
This project lets you control your computer using hand gestures! Think of it as magic - you can move your mouse and adjust your computer's volume just by moving your hand in the air. No need to touch your computer.

## What Can It Do? 🎯
1. **Control Your Mouse** 👆
   - Move the cursor by pointing your finger
   - Click by showing two fingers

2. **Control Volume** 🔊
   - Adjust volume by pinching your thumb and index finger
   - The more you spread your fingers, the louder it gets

## How It Works? 🤔
The program uses your computer's camera to:
1. Detect your hand in real-time
2. Track specific points on your hand (like fingertips)
3. Convert your hand movements into computer controls

## Requirements 📋
- A computer with Windows
- A webcam
- Python 3.7 or newer
- Some free space to install required packages

## Step-by-Step Setup Guide 🚀

### 1. Setting Up Your Computer
1. Install Python from [python.org](https://www.python.org/downloads/)
2. Download this project's files
3. Open Command Prompt (CMD)
   - Press `Windows + R`
   - Type `cmd` and press Enter

### 2. Installing the Project
```bash
# Go to project folder
cd path_to_your_folder

# Create a virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 3. Running the Program
```bash
python CombinedHandControl.py
```

### 4. Using the Program 🎮

#### Mouse Control:
- **To Move Mouse**: 
  1. Show your palm to the camera
  2. Raise only your index finger
  3. Move your finger to control the cursor

- **To Click**: 
  1. Raise both index and middle fingers
  2. Bring them close together

#### Volume Control:
1. Show your palm to the camera
2. Raise your thumb and index finger
3. Change the distance between them:
   - Bring them closer = Lower volume
   - Move them apart = Higher volume

### 5. Tips for Best Results 💡
- Make sure you have good lighting
- Keep your hand about 1-2 feet from the camera
- Keep your movements slow and steady
- Face your palm towards the camera
- Wear plain sleeves (no patterns) for better detection

### 6. Troubleshooting 🔧

#### Camera Not Working?
- Check if your webcam is connected
- Try restarting the program
- Make sure no other app is using your camera

#### Hand Not Detected?
- Improve lighting in your room
- Keep your hand in the camera's view
- Move your hand slower

#### Volume Control Not Working?
- Make sure you're on Windows
- Check if your system audio is working
- Try restarting the program

## Code Explanation 📝

### Main Components:

1. **HandController Class**
   - The brain of the program
   - Handles all hand tracking and gesture recognition

2. **Hand Detection**
```python
def findHands(self, img, draw=True):
    # Converts image to RGB for hand detection
    # Draws hand landmarks if found
```

3. **Finger Position Tracking**
```python
def fingersUp(self):
    # Checks which fingers are raised
    # Returns list of 5 values (1 for up, 0 for down)
```

4. **Mouse Control**
```python
def controlMouse(self, img, fingers):
    # Uses index finger for movement
    # Uses index + middle fingers for clicking
```

5. **Volume Control**
```python
def controlVolume(self, length, img, draw=True):
    # Uses distance between thumb and index finger
    # Maps distance to volume level
```

## Project Structure 📁
```
Hand-Gesture-Control/
│
├── CombinedHandControl.py   # Main program file
├── requirements.txt         # Required packages
└── README.md               # This guide
```

## Credits and References 🙏
- Built using OpenCV and MediaPipe libraries
- Inspired by computer vision and gesture recognition technology
- Created for easy computer control without physical contact

## Future Improvements 🚀
- Add more gestures for different controls
- Support for custom gesture mapping
- Add support for other operating systems
- Improve accuracy in low light conditions

---
Made with ❤️ for making technology more interactive and accessible 