import cv2
import face_recognition
import smtplib
import datetime

# Load the database of known faces
known_face_encodings = []
known_face_names = []

# Load the image of each known face and get its encoding
for name in known_face_names:
    image = face_recognition.load_image_file("known_faces/" + name + ".jpg")
    encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(encoding)

# Set up the email server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

# Log in to the email account
sender = "my@email.com"
password = "mypassword"
server.login(sender, password)

# Initialize the video capture
video_capture = cv2.VideoCapture(0)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face encodings in the frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop through each face in this frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
	cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

# If an unknown face was detected, send an email with the image attached
if name == "Unknown":
    # Send the email with the image attached
    receiver = "andy20030520@gmail.com"
    subject = "Unknown Face Detected"
    body = "A new face was detected at " + str(datetime.datetime.now())

    # Set the headers for the email
    headers = ["from: " + sender,
               "subject: " + subject,
               "to: " + receiver,
               "mime-version: 1.0",
               "content-type: image/jpg"]
    headers = "\r\n".join(headers)

    # Create the image file
    cv2.imwrite("unknown_face.jpg", frame)

    # Open the image file in binary mode
    binary_image = open("unknown_face.jpg", 'rb')

    # Combine the headers and body into the payload
    payload = headers + "\r\n\r\n" + body

    # Send the email
    server.sendmail(sender, receiver, payload)
    binary_image.close()

# Close the server
server.quit()