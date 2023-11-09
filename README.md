# Cursor Controller Using Computer Vision

## Setup
- Create virtual environment using `virtualenv`
```
virtualenv venv
```
- Activate the venv
```
source venv/bin/activate
```
or (for windows)
```
"venv/scripts/activate"
```
- Install the requirements
```
pip install -r requirements.txt
```
- Then run the script
```
python hand.py
```

## hand.py
Control computer cursor using your hand.

### Landmarks
- Thumb tip
- Index base (for the cursor movement)
- Middle tip
- Ring tip
- Pingky tip

### Gestures
Bring the following 2 fingers closer together.
- Left click = thumb tip & middle tip
- Right click = thumb tip & ring tip
- Double left click = thumb tip & pingky tip
