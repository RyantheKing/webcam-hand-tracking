# webcam-hand-tracking
A python program that uses OpenCV to track the position of your hands using an ordinary webcam.
This is the code I created as my contribution to the Webcam Theremin project. (https://github.com/RyantheKing/webcam-theremin)
I have isolated it here so it can be used for other purposes.

## Example
![](https://i.ibb.co/kDbR7Sd/unknown.png)
![](https://i.ibb.co/9h6mZ4p/unknown.png)

## Installation
#### Standalone
Download the file and run `py hand-tracking.py`

#### As a python module
Download the `handtracking.py` file. It has two functions, `findHandPos_standalone` which runs the video loop inside the function and `findHandPos_frame` which find the hand countours and position using the given frame and a background model.
