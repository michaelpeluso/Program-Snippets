# Video Motion Detection

This project is a simple implementation of real-time video motion detection using JavaScript and HTML5. It utilizes either an uploaded video or the user's webcam to capture video feed, processes each frame, and highlight areas where motion is detected.

## Usage

1. Clone this repository to your local machine.
2. Open the `index.html` file in a modern web browser that supports HTML5 and JavaScript.
3. Grant necessary permissions for accessing your webcam when prompted by the browser.
4. The video feed will start automatically, and the application will highlight areas where motion is detected in real-time.

## Features

-   Real-time video motion detection using the webcam.
-   Customizable parameters for motion detection sensitivity and frame processing.
-   Highlights areas of motion with a red rectangle and logs motion events.

## Files Included

-   `index.html`: HTML file containing the structure of the web page and necessary elements for video display and motion detection.
-   `index.js`: JavaScript file containing the logic for accessing the webcam, processing video frames, detecting motion, and updating the UI.

## Customization

You can customize the following parameters in `index.js`:

-   `Frame Delay Interval`: Interval in milliseconds between each calculation.
-   `Pixel Change Threshold`: Threshold for detecting pixel changes between frames..
-   `Minimum Pixel Group Size`: Minimum number of adjacent marked pixels to trigger movement.
-   `Minimum Box Separation Distance`: Minimum distance between motion boxes to consider them separate.
-   `Pixel Count Threshold`: Percentage of marked vs total pixels required to trigger movement.
-   `Gaussian Filter Radius`: Radius of Gaussian filter map for image processing.

Additionally, you can switch between black and white mode (`isBlack`) and upload a video file for motion detection.

## Dependencies

This project has no external dependencies other than a modern web browser with webcam support.
