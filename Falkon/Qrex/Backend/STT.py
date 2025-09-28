import speech_recognition as sr

def recognize_speech(callback=None, timeout=5, phrase_time_limit=8):
    """
    Capture speech from microphone with sensible timeouts so UI doesn't hang.

    Args:
        callback: optional function to call with recognized text
        timeout: max seconds to wait for phrase start
        phrase_time_limit: max seconds for phrase length
    """
    recognizer = sr.Recognizer()

    try:
        mic = sr.Microphone()
    except Exception as e:
        print(f"Microphone initialization error: {e}")
        return None

    with mic as source:
        print("🎤 Listening...")
        try:
            recognizer.adjust_for_ambient_noise(source, duration=0.8)
        except Exception:
            pass
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            print("⏱️ No speech detected within timeout.")
            return None
        except Exception as e:
            print(f"Listening error: {e}")
            return None

    try:
        text = recognizer.recognize_google(audio, language='en-IN')
        print(f"🗣️  Mr. Rishi : {text}")
        if callback:
            callback(text)
        return text
    except sr.UnknownValueError:
        print("🤖 Could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"🔌 Could not request results; {e}")
        return None
    except Exception as e:
        print(f"Recognition error: {e}")
        return None