\# Voice\_Bot



\*\*Voice\_Bot\*\* is a Python AI voice agent that joins a \*\*LiveKit room\*\*, listens to user audio, converts it to text (STT), generates AI responses using \*\*OpenAI\*\*, converts the response to speech (TTS), and plays it back in real-time.  



This project is \*\*audio-only\*\* — no UI is required.  



---



\## Features



\- Real-time subscription to user audio in LiveKit rooms

\- Speech-to-text (STT) using \*\*Whisper\*\*

\- AI response generation using \*\*OpenAI GPT\*\*

\- Text-to-speech (TTS) using \*\*Edge TTS\*\*

\- Publishes bot voice back to the room

\- Supports multiple users asynchronously



---



\## Requirements



\- Python 3.10+

\- LiveKit account (room + token)

\- OpenAI API key

\- Packages in `requirements.txt`:



