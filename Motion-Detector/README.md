# Video Motion Detection

This project is a simple implementation of real-time video motion detection using JavaScript and HTML5. It utilizes the user's webcam to capture live video feed, processes each frame, and highlights areas where motion is detected.

## Usage

1. Clone this repository to your local machine.
2. Open the `index.html` file in a modern web browser that supports HTML5 and JavaScript.
3. Grant necessary permissions for accessing your webcam when prompted by the browser.
4. The video feed will start automatically, and the application will highlight areas where motion is detected in real-time.

## Features

- Real-time video motion detection using the webcam.
- Customizable parameters for motion detection sensitivity and frame processing.
- Highlights areas of motion with a red rectangle and logs motion events.

## Files Included

- `index.html`: HTML file containing the structure of the web page and necessary elements for video display and motion detection.
- `index.js`: JavaScript file containing the logic for accessing the webcam, processing video frames, detecting motion, and updating the UI.

## Customization

You can customize the following parameters in `index.js`:

- `frameDelayMilliseconds`: Adjust the frame processing rate in milliseconds.
- `pixelChangeThreshold`: Set the threshold for pixel intensity change to detect motion.
- `pixelCountThreshold`: Define the minimum number of changed pixels to consider as motion.
- `medianFilterRadius`: Control the radius of the median filter for noise reduction.
- `minPixelGroup`: Define the minimum number of pixels in a motion group to be considered significant.
- `maxBoxDistance`: Set the maximum distance between bounding boxes to consider them as part of the same motion.

## Dependencies

This project has no external dependencies other than a modern web browser with webcam support.
