import cv2
import mediapipe as mp
import time

from voice_alert import speak_alert

# MEDIAPIPE SETUP

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(

    refine_landmarks=True,

    max_num_faces=1,

    min_detection_confidence=0.5,

    min_tracking_confidence=0.5
)

# CAMERA SETUP

cap = cv2.VideoCapture(0)

# CAMERA QUALITY

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# CAMERA CHECK

if not cap.isOpened():

    print("❌ Camera Not Working")

    exit()

print("✅ AI Drowsiness Detection Started")

# VARIABLES

eyes_closed_start = None

drowsy_alert_sent = False

# MAIN LOOP

while True:

    success, frame = cap.read()

    if not success:

        print("❌ Camera Frame Error")

        break

    # FLIP CAMERA

    frame = cv2.flip(frame, 1)

    # RGB CONVERSION

    rgb_frame = cv2.cvtColor(

        frame,

        cv2.COLOR_BGR2RGB
    )

    # FACE PROCESSING

    results = face_mesh.process(

        rgb_frame
    )

    # FACE DETECTED

    if results.multi_face_landmarks:

        # FACE STATUS

        cv2.putText(

            frame,

            "Face Detected",

            (20, 40),

            cv2.FONT_HERSHEY_SIMPLEX,

            1,

            (0, 255, 0),

            2
        )

        for face_landmarks in results.multi_face_landmarks:

            # LEFT EYE LANDMARKS

            left_top = face_landmarks.landmark[159]

            left_bottom = face_landmarks.landmark[145]

            # RIGHT EYE LANDMARKS

            right_top = face_landmarks.landmark[386]

            right_bottom = face_landmarks.landmark[374]

            # EYE DISTANCE

            left_eye_distance = abs(

                left_top.y - left_bottom.y
            )

            right_eye_distance = abs(

                right_top.y - right_bottom.y
            )

            # DEBUG VALUES

            print(

                "Left Eye:",

                round(left_eye_distance, 4),

                "Right Eye:",

                round(right_eye_distance, 4)
            )

            # DROWSINESS DETECTION

            if (

                left_eye_distance < 0.024

                and

                right_eye_distance < 0.024

            ):

                # EYES CLOSED TIMER

                if eyes_closed_start is None:

                    eyes_closed_start = time.time()

                elapsed = time.time() - eyes_closed_start

                # DROWSINESS ALERT

                if elapsed > 3:

                    # DROWSINESS TEXT

                    cv2.putText(

                        frame,

                        "DROWSINESS DETECTED",

                        (50, 100),

                        cv2.FONT_HERSHEY_SIMPLEX,

                        1,

                        (0, 0, 255),

                        3
                    )

                    if not drowsy_alert_sent:

                        drowsy_alert_sent = True

                        print(

                            "🚨 Drowsiness Detected"
                        )

                        speak_alert(

                            "Warning. Driver drowsiness detected. Please wake up immediately."
                        )

            else:

                # RESET

                eyes_closed_start = None

                drowsy_alert_sent = False

    else:

        # NO FACE DETECTED

        cv2.putText(

            frame,

            "No Face Detected",

            (20, 40),

            cv2.FONT_HERSHEY_SIMPLEX,

            1,

            (0, 0, 255),

            2
        )

    # SHOW CAMERA

    cv2.imshow(

        "AI Driver Drowsiness Detection",

        frame
    )

    # EXIT

    if cv2.waitKey(1) & 0xFF == ord('q'):

        break

# RELEASE CAMERA

cap.release()

cv2.destroyAllWindows()