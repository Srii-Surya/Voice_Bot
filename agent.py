import asyncio
import os
import tempfile
from dotenv import load_dotenv
from livekit import Room, AudioSource, LocalAudioTrack
from openai import OpenAI
from faster_whisper import WhisperModel
import edge_tts
import wave

load_dotenv()

LIVEKIT_URL = os.getenv("LIVEKIT_URL")
TOKEN = input("Paste your generated token: ")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_KEY)
whisper = WhisperModel("base")

async def transcribe_audio(file_path):
    segments, _ = whisper.transcribe(file_path)
    text = ""
    for segment in segments:
        text += segment.text
    return text

async def generate_reply(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": text}]
    )
    return response.choices[0].message.content

async def text_to_speech(text, output_file):
    communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
    await communicate.save(output_file)

async def main():
    room = Room()
    await room.connect(LIVEKIT_URL, TOKEN)
    print("Connected to room")

    audio_source = AudioSource(48000, 1)
    track = LocalAudioTrack.create_audio_track("bot-voice", audio_source)
    await room.local_participant.publish_track(track)

    @room.on("track_subscribed")
    async def on_track(track, publication, participant):
        print("Subscribed to user audio")

        while True:
            frame = await track.recv()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                wf = wave.open(tmp.name, 'wb')
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(48000)
                wf.writeframes(frame.data)
                wf.close()

                text = await transcribe_audio(tmp.name)
                print("User said:", text)

                reply = await generate_reply(text)
                print("Bot reply:", reply)

                tts_file = tmp.name + "_tts.wav"
                await text_to_speech(reply, tts_file)

                with wave.open(tts_file, 'rb') as wf:
                    audio_data = wf.readframes(wf.getnframes())
                    await audio_source.capture_frame(audio_data)

    await asyncio.Event().wait()

asyncio.run(main())