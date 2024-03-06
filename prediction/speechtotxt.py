import assemblyai as aai
import librosa


#kei bolena vane -18 ani len(transcript.text) == 0
def silence_or_not(path):
    aai.settings.api_key = "35a8354414cb4377b5e108561148d0f1"
    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe(path)
    #transcript = transcriber.transcribe("./my-local-audio-file.wav")
    print(transcript.text)
    print(len(transcript.text))

    y, sr = librosa.load(path)

    # Calculate the maximum amplitude in decibels (dB)
    db_values = librosa.amplitude_to_db(y)
    max_db = max(db_values)
    print(max_db)
    if len(transcript.text) == 0 and max_db <= -18:
        return False
    else:
        return True

def text_from_speech(path):
    aai.settings.api_key = "35a8354414cb4377b5e108561148d0f1"
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(path)
    return transcript.text

