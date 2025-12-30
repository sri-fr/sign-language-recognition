import cv2
import mediapipe as mp
import math

from recognizer import recognize_letter
from word_builder import WordBuilder
from tts import speak_async

# ---------- angle helper ----------
def angle(a, b, c):
    ab = (a[1] - b[1], a[2] - b[2])
    cb = (c[1] - b[1], c[2] - b[2])
    dot = ab[0]*cb[0] + ab[1]*cb[1]
    mag_ab = math.hypot(ab[0], ab[1])
    mag_cb = math.hypot(cb[0], cb[1])
    if mag_ab * mag_cb == 0:
        return 0
    return math.degrees(math.acos(dot / (mag_ab * mag_cb)))

# ---------- MediaPipe ----------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# ---------- Camera ----------
cap = cv2.VideoCapture(0)
word_builder = WordBuilder()

spoken = False

while True:
    success, img = cap.read()
    if not success:
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    detected_letter = ""
    fingers = []

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lm = []
            h, w, _ = img.shape

            for id, p in enumerate(handLms.landmark):
                lm.append((id, int(p.x * w), int(p.y * h)))

            # ---------- thumb ----------
            thumb_tip, thumb_ip, thumb_mcp, wrist = lm[4], lm[3], lm[2], lm[0]
            thumb_angle = angle(thumb_tip, thumb_ip, thumb_mcp)
            thumb_dist = math.hypot(thumb_tip[1]-wrist[1], thumb_tip[2]-wrist[2])
            mcp_dist = math.hypot(thumb_mcp[1]-wrist[1], thumb_mcp[2]-wrist[2])

            fingers.append(1 if (thumb_angle > 150 and thumb_dist > mcp_dist + 10) else 0)

            # ---------- other fingers ----------
            for tip in [8,12,16,20]:
                fingers.append(1 if lm[tip][2] < lm[tip-2][2] else 0)

            detected_letter = recognize_letter(fingers)
            word = word_builder.update(detected_letter, fingers)

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            cv2.putText(img, f"Fingers: {fingers}", (10,40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

            if detected_letter:
                cv2.putText(img, f"Letter: {detected_letter}", (10,80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0,0,255), 3)

            cv2.putText(img, f"Word: {word}", (10,130),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

            # ---------- speak on long fist ----------
            if fingers == [0,0,0,0,0] and len(word.strip()) > 0:
                if not spoken:
                    speak_async(word)
                    spoken = True
            else:
                spoken = False

    cv2.imshow("Sign Language Recognition", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
