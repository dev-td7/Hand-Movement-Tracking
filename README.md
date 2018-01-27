# Hand Movement Tracking

## Description
This program can track your hand movements. An ellipse will follow your hand wherever it goes and reports directions if your hand is moving.

Directions (total 8): North, South, East, West, North-East, North-West, South-East, South-West

__Please note that the horizontal directions that you see in the display are opposite of what you are doing. That means, when you move your hand in the left direction, you see your hand moving in the right direction.__

So, do not feel that it is reporting you opposite directions.

## Usage
1. Run `track.py`
2. Place your hand in a window provided to you. Make sure your hand is completely inside the window. It is not necessary to touch your hand's boundaries to the window.
3. Press 's' key on your keyboard. Tracking starts.
4. If in a case when the ellipse tracking goes wrong, or you see an error message, press the 's' key again. It will reset the program and do Step 2,3 again.
5. At last, have fun!

## Results

An example of movement can be seen from these two frames:

![Hand is still in this case, no movement](https://github.com/dev-td7/Hand-Movement-Tracking/blob/master/results/still.PNG?raw=true)

![Hand has moved in the north direction](https://github.com/dev-td7/Hand-Movement-Tracking/blob/master/results/north.PNG?raw=true)

### Constraints
* Good lighting conditions are needed.
* __Do not bring your hand over your face. The program won't work as expected in such conditions__
* A full-sleeve shirt gives the best results. Without a full-sleeve shirt, results may be less accurate and hand tracking may get affected, but would still work fairly.
* Don't move your hand too fast. Keep the speed normal for best results. Also, very slow motion is not recommended.

### A small note
_CamShift algorithm was used to locate my hand in the next frame. I don't rely only on CamShift though, some post-processing has been done_