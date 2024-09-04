from flask import Flask, request, render_template, send_file
import wikipedia
import speech_recognition as sr
from gtts import gTTS
import os

app = Flask(__name__)

# Set a custom user agent
wikipedia.set_lang('en')
wikipedia.set_user_agent('WaterScarcityApp/1.0 (your-email@example.com)')

# Define the topic
TOPIC = "Water scarcity"

def fetch_summary(query):
    """Fetch Wikipedia summary based on the query or fallback to the default topic."""
    try:
        # Try to get summary for the user's query
        summary = wikipedia.summary(query)
        if TOPIC.lower() in summary.lower():
            return summary
        else:
            return summary
    except wikipedia.exceptions.PageError:
        # If page not found, provide information about the default topic
        return get_topic_summary()
    except wikipedia.exceptions.DisambiguationError:
        # Handle disambiguation by showing relevant topic information
        return f"Multiple results found for '{query}'. Showing details on '{TOPIC}' instead."

def get_topic_summary():
    """Get the summary of the default topic."""
    try:
        return wikipedia.summary(TOPIC)
    except wikipedia.exceptions.PageError:
        return "Page not found for the topic."
    except wikipedia.exceptions.DisambiguationError:
        return "Disambiguation error occurred."

def text_to_speech(text, filename='static/result.mp3'):
    """Convert text to speech and save it as an MP3 file."""
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    return filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    result = fetch_summary(query)
    audio_file = text_to_speech(result)
    return render_template('result.html', result=result, audio_file=audio_file)

@app.route('/voice_search', methods=['POST'])
def voice_search():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            result = fetch_summary(query)
            audio_file = text_to_speech(result)
        except sr.UnknownValueError:
            result = "Sorry, I could not understand the audio."
            audio_file = text_to_speech(result)
        except sr.RequestError:
            result = "Sorry, there was an error with the speech recognition service."
            audio_file = text_to_speech(result)
    return render_template('result.html', result=result, audio_file=audio_file)

@app.route('/audio/<filename>')
def audio(filename):
    return send_file(os.path.join('static', filename))

if __name__ == '__main__':
    app.run(debug=True)
