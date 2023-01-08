# Face-Detection
This program uses the OpenCV and face_recognition libraries to detect faces in a live video feed and compare them to a database of known faces. If a known face is detected, the program displays the name of the user. If an unknown face is detected, the program sends an email with a timestamp and attached image to a specified email address.

## Requirements

- Python 3
- OpenCV
- face_recognition
- smtplib

## Installation

1. Clone or download the repository.
2. Install the required libraries: `pip install opencv-python face_recognition smtplib`
3. Add images of known faces to the "known_faces" folder. The images should be named with the corresponding name and the file extension ".jpg".
4. Edit the `known_face_names` list in the main program file to include the names of the known faces.
5. Edit the `sender` and `password` variables in the main program file to include the email address and password of the account that will be used to send the emails.
6. Edit the `receiver` variable in the main program file to include the email address that will receive the emails.

## Usage

Run the main program file: `python face_detection.py`

Press 'q' on the keyboard to quit the program.
