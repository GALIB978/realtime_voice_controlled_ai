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
- Windows built-in System.Speech.Synthesis.SpeechSynthesizer

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

## Project Limitations
The current version does not support real-time interruption while the AI is speaking. The system starts listening again after the TTS response has finished.

Speech recognition can also make mistakes when the speech is unclear or there is background noise.

## How to Run

Install the required Python packages:

```bash
pip install faster-whisper sounddevice soundfile numpy ollama