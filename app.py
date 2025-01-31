import streamlit as st
from gtts import gTTS
import tempfile
import speech_recognition as sr

# Predefined keywords and responses
keywords_responses = {
    "account balance": "Your account balance is fifty thousand rupees.",
    "open account": "You can open a new account by scanning your ID card and proof of salary.",
    "nearest atm location": "The nearest ATM is 3 kilometers down kheban-e-jinnah, open 24/7.",
    "loan inquiry": "You can check you loan eligibility by scanning your QR code here or ask a customer service representative on the counter.",
    "credit card": "You can apply for a credit card here, press 5 for assistance.",
    "customer support": "You can contact our customer support at 1-800-123-4567."
}

# Function to recognize speech from the microphone
def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak into your microphone.")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError:
            return "Error with the speech recognition service."
        except sr.WaitTimeoutError:
            return "You didn't say anything."

# Function to get a response based on keyword matching
def get_response(user_input):
    for keyword, response in keywords_responses.items():
        if keyword in user_input:  # Check if keyword exists in user input
            return response
    return "Sorry, I don't have an answer for that."

# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        tts.save(temp_audio.name)
        return temp_audio.name

# Streamlit App
st.title("AI Voice Assistant with Live Audio Input and Keyword-Based Responses")
st.write("Click the button below to record your voice or type your question.")

# Text input for fallback
user_input_text = st.text_input("Type your question here (optional):")

# Add a button for live audio input
if st.button("Record Voice"):
    user_input = recognize_speech_from_mic()  # Capture live audio input
    st.write(f"You said: {user_input}")

    # Get the response based on keyword matching
    response = get_response(user_input)
    st.write(f"AI: {response}")

    # Convert the response to audio
    audio_file = text_to_speech(response)
    st.audio(audio_file, format="audio/mp3")

# Process text input if provided
if user_input_text:
    response = get_response(user_input_text.lower())  # Case-insensitive
    st.write(f"AI: {response}")
    audio_file = text_to_speech(response)
    st.audio(audio_file, format="audio/mp3")
