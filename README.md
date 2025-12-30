🤟 Sign Language Recognition Web App

This project is a real-time sign language recognition system that translates hand gestures into text and speech using computer vision. The main idea behind this project is to reduce the communication gap between sign language users and non-signers through a simple and interactive application.

The project was built step by step with a strong focus on accuracy, real-time performance, and a smooth user experience rather than just visual output.

✨ What this app does

The application detects hand gestures in real time using a webcam. It identifies finger positions and hand orientation, recognizes selected sign language alphabets, forms words from continuous gestures, and converts the recognized text into speech. All of this runs inside an interactive web application.

🛠️ Tech stack used

The system is built using Python as the core language. OpenCV is used for video capture and image processing, MediaPipe is responsible for hand landmark detection, Streamlit is used to create the web interface, and pyttsx3 is used for text-to-speech conversion.

🔍 How it works

The webcam captures live video input, after which MediaPipe detects 21 hand landmarks. Finger states are calculated using geometric relationships and joint angles. These finger patterns are then mapped to corresponding letters. Over time, recognized letters are combined to form words, which are finally displayed on the screen and spoken aloud.

Special attention was given to thumb detection, as it is one of the most challenging aspects of hand gesture recognition due to its rotational movement.

▶️ How to run the project

Install the required dependencies using the requirements file. Once installed, start the Streamlit application and open the local web address in your browser to access the app.

📌 Usage notes

For best accuracy, the palm (white side) of the hand should face the camera. Each gesture should be held steadily for a short moment to allow proper recognition. Making a fist is used to separate words or trigger speech output.

🚧 Current limitations

Only selected alphabets are supported using logic-based gesture detection. Very complex sign language gestures may require advanced shape analysis or depth-based information. The performance of the system also depends on lighting conditions and camera quality.

🚀 Future improvements

The project can be extended to support more sign language alphabets, sentence-level recognition, language translation, and a mobile-friendly interface. Cloud deployment can also be added to make the application publicly accessible.

👨‍💻 About the project

This project was developed as a hands-on learning experience in computer vision and human–computer interaction. It serves as a foundation for building more advanced sign language translation systems in the future.

📫 Author

Srivathsan GMS
B.Tech Artificial Intelligence & Data Science
K.L.N. College of Engneering, Madurai.
