#import pyttsx3
import speech_recognition as sr

#engine = pyttsx3.init()
#voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[0].id)

#def greeting():
#    speak('Hello. Have a good day!')

#def speak(audio):
#    engine.say(audio)
#    engine.runAndWait()

def voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        recognizer.pause_threshold = 0.6
        recognizer.energy_threshold = 500
        recognizer.adjust_for_ambient_noise(source, 0.8)
        audio = recognizer.listen(source)
    try:
        print('Recognizing..')
        query = recognizer.recognize_vosk(audio, language='en')
        print(query.split(" : ")[1].strip()[1:-3])
        return query.split(" : ")[1].strip()[1:-3]
    except Exception as e:
        print(e)
        print('Record failed')
        return None