import os
from dotenv import load_dotenv
from livekit.api import AccessToken
from livekit.api.video_grant import VideoGrant

load_dotenv()

api_key = os.getenv("LIVEKIT_API_KEY")
api_secret = os.getenv("LIVEKIT_API_SECRET")

grant = VideoGrant(
    room_join=True,
    room="test-room"
)

token = (
    AccessToken(api_key, api_secret)
    .with_identity("voice-bot-user")
    .with_name("Voice Bot")
    .with_grants(grant)
)

print("\nYour LIVEKIT_TOKEN:\n")
print(token.to_jwt())