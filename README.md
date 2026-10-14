# Real-Time Voice-Controlled AI Application

## Group

Cronous

## Members

- Prova Zarin
- Akther Rubina
- Islam K
- Bin Mahamud Galib

## Project Description

This project is a real-time voice-controlled AI assistant. The user speaks through a microphone, the speech is converted into text, the local AI model generates a response, and the response is spoken through the computer speaker.

The application is designed to provide a simple hands-free interaction with an AI assistant using voice.

## System Architecture

Microphone → Speech-to-Text → AI Model → Text-to-Speech → Speaker

## Models and Technologies

### Speech-to-Text

- faster-whisper Base model
- CPU
- int8 computation

### AI Language Model

- Ollama
- Llama 3.2 3B (`llama3.2:3b`)
- Runs locally on the computer

### Text-to-Speech

- Windows built-in `System.Speech.Synthesis.SpeechSynthesizer`

## Main Features

- Voice input through microphone
- Automatic speech detection using silence detection
- Speech-to-text transcription
- Local AI response generation
- Spoken AI responses
- Continuous voice interaction
- Stop, exit, and quit commands
- Response latency measurement
- Basic error handling

## How the System Works

1. The microphone captures the user's speech.
2. Silence detection detects when the user has finished speaking.
3. Faster-Whisper converts the speech into text.
4. Ollama Llama 3.2 3B generates an AI response locally.
5. Windows Speech Synthesizer converts the response into speech.
6. The response is played through the computer speaker.
7. The system continues listening for the next question.

## Latency Measurement

The application measures:

- Speech-to-text processing time
- AI response generation time
- Text-to-speech time
- Total response latency

This allows the performance of each part of the voice interaction pipeline to be evaluated.

## Error Handling

The application includes basic error handling for:

- Microphone errors
- Audio recording errors
- Speech recognition errors
- Ollama/AI errors
- Text-to-speech errors
- Empty speech input

## Project Limitations

The current version does not support real-time interruption while the AI is speaking. The system starts listening again after the TTS response has finished.

Speech recognition can also make mistakes when the speech is unclear or there is background noise.

## Installation

Install the required Python packages:

```bash
pip install faster-whisper sounddevice soundfile numpy ollama

Make sure Ollama is installed on the computer.

Download the required AI model:

```bash
ollama pull llama3.2:3b

## How to Run

Start the application with:

```bash
python voice_ai.py

After starting the application:

1. Speak into the microphone.
2. Wait until the system detects that you have finished speaking.
3. The application transcribes your speech.
4. Ollama generates a short AI response.
5. The response is spoken through the computer speaker.
6. The system waits for the next voice input.

To stop the application, say:

```text
Stop