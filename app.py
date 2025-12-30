import streamlit as st
import cv2
import mediapipe as mp
import math

from recognizer import recognize_letter
from word_builder import WordBuilder
from tts import speak_async
st.warning("⚠️ Webcam access works only on local machine. Online demo shows UI & logic.")


# ---------- Angle helper ----------
def angle(a, b, c):
    ab = (a[1] - b[1], a[2] - b[2])
    cb = (c[1] - b[1], c[2] - b[2])
    dot = ab[0]*cb[0] + ab[1]*cb[1]
    mag_ab = math.hypot(ab[0], ab[1])
    mag_cb = math.hypot(cb[0], mag_cb := math.hypot(cb[0], cb[1]))
    if mag_ab * mag_cb == 0:
        return 0
    return math.degrees(math.acos(dot / (mag_ab * mag_cb)))

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Sign Language Recognition", layout="wide")
st.title("🤟 Real-Time Sign Language Recognition")
st.markdown("Show **palm (white side)** to the camera")

run = st.checkbox("▶ Start Camera")

# Layout: camera on left, text on right
left_col, right_col = st.columns([2, 1])

FRAME_WINDOW = left_col.image([])

# Right side placeholders (EMPTY by default)
letter_placeholder = right_col.empty()
word_placeholder = right_col.empty()

# ---------- MediaPipe ----------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
word_builder = WordBuilder()
spoken = False

while run:
    ret, frame = cap.read()
    if not ret:
        st.error("Camera not accessible")
        break

    frame = cv2.flip(frame, 1)
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    detected_letter = ""
    fingers = []

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lm = []
            h, w, _ = frame.shape

            for id, p in enumerate(handLms.landmark):
                lm.append((id, int(p.x * w), int(p.y * h)))

            # ---------- Thumb (calibrated) ----------
            thumb_tip, thumb_ip, thumb_mcp, wrist = lm[4], lm[3], lm[2], lm[0]
            thumb_angle = angle(thumb_tip, thumb_ip, thumb_mcp)
            thumb_dist = math.hypot(thumb_tip[1]-wrist[1], thumb_tip[2]-wrist[2])
            mcp_dist = math.hypot(thumb_mcp[1]-wrist[1], thumb_mcp[2]-wrist[2])

            fingers.append(1 if (thumb_angle > 150 and thumb_dist > mcp_dist + 10) else 0)

            # ---------- Other fingers ----------
            for tip in [8, 12, 16, 20]:
                fingers.append(1 if lm[tip][2] < lm[tip - 2][2] else 0)

            detected_letter = recognize_letter(fingers)
            word = word_builder.update(detected_letter, fingers)

            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            # ---------- Speak ----------
            if fingers == [0,0,0,0,0] and word.strip():
                if not spoken:
                    speak_async(word)
                    spoken = True
            else:
                spoken = False

    # ---------- UI UPDATE ----------
    FRAME_WINDOW.image(frame, channels="BGR")

    # ✅ Show letter ONLY if recognised
    if detected_letter:
        letter_placeholder.markdown(
            f"## 🅰️ Detected Letter\n# **{detected_letter}**"
        )
    else:
        letter_placeholder.empty()

    # ✅ Show word ONLY if not empty
    if word_builder.word.strip():
        word_placeholder.markdown(
            f"## 🧾 Recognized Word\n### **{word_builder.word}**"
        )
    else:
        word_placeholder.empty()

cap.release()
