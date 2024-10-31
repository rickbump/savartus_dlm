import ffmpeg
import os
import wave
import json as json_parser  # Use json_parser to avoid confusion with the config file
import speech_recognition as sr
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer
from processors.text_cleaning import clean_up_transcript

# Extract metadata using FFmpeg
def process_audio(file_path):
    try:
        probe = ffmpeg.probe(file_path)
        format_info = probe['format']
        stream_info = probe['streams'][0]  # Assuming the first stream is audio

        metadata = {
            "filename": os.path.basename(file_path),
            "format": format_info.get('format_name'),
            "duration": float(format_info.get('duration', 0)),
            "bitrate": int(format_info.get('bit_rate', 0)),
            "sample_rate": int(stream_info.get('sample_rate', 0)),
            "channels": stream_info.get('channels', 0),
            "codec": stream_info.get('codec_name', ''),
            "size": int(format_info.get('size', 0))
        }
        return {
            'embedded_metadata': metadata}

    except ffmpeg.Error as e:
        print(f"Error extracting metadata from {file_path}: {e}")
        return {}

# Main processing function for transcript
def process_transcript(file_path):
    # Load config from config.json
    config = load_config()

    # Extract configuration variables
    output_path = config['audio_output_path']
    ai_process = config['ai_process']
    ai_model = config['ai_model']

    # Convert to WAV if necessary
    if not file_path.endswith(".wav"):
        file_path = convert_to_wav(file_path, output_path)

#    # Extract audio metadata
#    metadata = extract_audio_metadata(file_path)

    # Process based on ai_process and ai_model
    transcript = None
    if ai_process == 1:  # Use AI-based models
        if ai_model == 1:
            transcript = transcribe_audio_vosk(file_path)
        elif ai_model == 2:
            transcript = transcribe_audio_google(file_path)
        else:
            raise ValueError("Invalid AI model selection.")
    else:
        raise ValueError("Invalid AI process selection.")

    # Clean up the transcript using text_cleaning
    cleaned_transcript = clean_up_transcript(transcript)

    # Return the combined metadata and cleaned transcript
    return {
        'transcript': cleaned_transcript
    }

# Function to load configuration from a json file
def load_config(config_file='config.json'):
    try:
        with open(config_file, 'r') as f:
            config = json_parser.load(f)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
    except json_parser.JSONDecodeError as e:
        raise ValueError(f"Error reading the config file '{config_file}': {e}")

# Function to convert audio to WAV format (if needed)
def convert_to_wav(file_path, output_path):
    audio = AudioSegment.from_file(file_path)  # Automatically detects the file format (MP3, etc.)
    # Convert the audio to WAV format, mono, 16-bit PCM, 16000 Hz sample rate
    audio = audio.set_channels(1)  # Mono channel
    audio = audio.set_frame_rate(16000)  # 16kHz sample rate
    audio = audio.set_sample_width(2)  # 16-bit
    # Export as a WAV file
    audio.export(output_path, format="wav")
    return output_path


# Vosk-based transcription
def transcribe_audio_vosk(file_path):
    model_path = "/Users/rickbump/PycharmProjects/savartus_dlm/.venv/lib/speech_recog_models/voskenus0_22"
    model = Model(model_path)

    wf = wave.open(file_path, "rb")

    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        raise ValueError("Audio file must be WAV format, mono, 16-bit PCM, and 16kHz sample rate.")

    recognizer = KaldiRecognizer(model, wf.getframerate())

    transcript = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = json_parser.loads(recognizer.Result())
            transcript += result.get("text", "")

    final_result = json_parser.loads(recognizer.FinalResult())
    transcript += final_result.get("text", "")
    return transcript


# Google Speech Recognition-based transcription
def transcribe_audio_google(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio_data = recognizer.record(source)  # Process the entire file

    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand the audio."
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"


