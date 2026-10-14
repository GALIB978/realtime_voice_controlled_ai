import sounddevice as sd
import soundfile as sf
import ollama
import subprocess
import os
import numpy as np
import time
from faster_whisper import WhisperModel


# ============================================================
# SETTINGS
# ============================================================

SAMPLE_RATE = 16000
BLOCK_DURATION = 0.1
SILENCE_DURATION = 1.2
MAX_RECORDING_TIME = 10
SILENCE_THRESHOLD = 0.015
MODEL_SIZE = "base"


# ============================================================
# LOAD SPEECH RECOGNITION MODEL
# ============================================================

print("Loading speech recognition model...")

try:
    model = WhisperModel(
        MODEL_SIZE,
        device="cpu",
        compute_type="int8"
    )
except Exception as e:
    print("Error loading speech recognition model:", e)
    exit()


# ============================================================
# RECORD UNTIL SILENCE
# ============================================================

def record_until_silence():

    print("\nSpeak now...")

    audio_data = []
    speech_started = False
    silence_time = 0
    total_time = 0

    block_size = int(SAMPLE_RATE * BLOCK_DURATION)

    try:

        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            blocksize=block_size
        ) as stream:

            while total_time < MAX_RECORDING_TIME:

                audio_block, overflowed = stream.read(block_size)

                audio_block = audio_block.copy()

                volume = np.sqrt(np.mean(audio_block ** 2))

                audio_data.append(audio_block)

                total_time += BLOCK_DURATION

                if volume > SILENCE_THRESHOLD:

                    speech_started = True
                    silence_time = 0

                elif speech_started:

                    silence_time += BLOCK_DURATION

                    if silence_time >= SILENCE_DURATION:
                        break

    except Exception as e:

        print("Microphone error:", e)
        return None

    if not audio_data:
        return None

    return np.concatenate(audio_data, axis=0)


# ============================================================
# TEXT TO SPEECH - WINDOWS
# ============================================================

def speak_text(text):

    try:

        powershell_script = """
Add-Type -AssemblyName System.Speech

$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer

$synth.Volume = 100
$synth.Rate = 0

$synth.Speak($env:TTS_TEXT)

$synth.Dispose()
"""

        environment = os.environ.copy()
        environment["TTS_TEXT"] = text

        subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                powershell_script
            ],
            env=environment,
            check=True
        )

        return True

    except Exception as e:

        print("Text-to-speech error:", e)
        return False


# ============================================================
# MAIN VOICE ASSISTANT
# ============================================================

while True:

    # --------------------------------------------------------
    # RECORD USER SPEECH
    # --------------------------------------------------------

    audio = record_until_silence()

    if audio is None:

        print("No audio detected or microphone error.")
        continue


    # --------------------------------------------------------
    # SAVE AUDIO
    # --------------------------------------------------------

    try:

        sf.write(
            "test_audio.wav",
            audio,
            SAMPLE_RATE
        )

    except Exception as e:

        print("Error saving audio:", e)
        continue


    # User finished speaking
    end_of_speech = time.perf_counter()

    print("Recording finished.")
    print("Transcribing...")


    # --------------------------------------------------------
    # SPEECH TO TEXT
    # --------------------------------------------------------

    try:

        stt_start = time.perf_counter()

        segments, info = model.transcribe(
            "test_audio.wav"
        )

        text = ""

        for segment in segments:
            text += segment.text

        text = text.strip()

        stt_time = time.perf_counter() - stt_start

    except Exception as e:

        print("Speech recognition error:", e)
        continue


    print("You said:", text)
    print(f"STT time: {stt_time:.3f} seconds")


    # --------------------------------------------------------
    # EMPTY SPEECH
    # --------------------------------------------------------

    if not text:

        print("I didn't hear anything.")
        continue


    # --------------------------------------------------------
    # STOP COMMAND
    # --------------------------------------------------------

    if text.lower().startswith(
        ("stop", "exit", "quit")
    ):

        print("Goodbye!")
        break


    # --------------------------------------------------------
    # OLLAMA AI
    # --------------------------------------------------------

    print("Thinking...")

    try:

        ai_start = time.perf_counter()

        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a voice assistant. "
                        "Answer the user briefly in "
                        "1 or 2 short sentences. "
                        "Keep the response concise because "
                        "it will be spoken aloud. "
                        "Do not give long explanations."
                    )
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        ai_time = time.perf_counter() - ai_start

        answer = response["message"]["content"].strip()

    except Exception as e:

        print("AI error. Please make sure Ollama is running.")
        print("Details:", e)
        continue


    print("AI:", answer)
    print(f"AI time: {ai_time:.3f} seconds")


    # --------------------------------------------------------
    # TEXT TO SPEECH
    # --------------------------------------------------------

    print("Speaking...")

    tts_start = time.perf_counter()

    success = speak_text(answer)

    tts_time = time.perf_counter() - tts_start

    if not success:

        print("Could not speak the answer.")
        continue


    # --------------------------------------------------------
    # TOTAL LATENCY
    # --------------------------------------------------------

    total_response_time = (
        time.perf_counter() - end_of_speech
    )

    print(f"TTS time: {tts_time:.3f} seconds")
    print(
        f"Total response time: "
        f"{total_response_time:.3f} seconds"
    )