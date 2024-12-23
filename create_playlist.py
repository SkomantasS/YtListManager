from youtube import YouTube
from dotenv import load_dotenv
import os

client_file = os.getenv("CLIENT_FILE")
yt = YouTube(client_file)
yt.init_service()

response_playlist = yt.create_playlist(title='TestT')
playlist_id = response_playlist.get('id')
playlist_title = response_playlist['snippet']['title']

video_ids = ['vfFW2SbvOOM']
for video_id in video_ids:
    request_body = {
        'snippet': {
            'playlistId': playlist_id,
            'resourceId': {
                'kind': 'youtube#video',
                'videoId': video_id
            }
        }
    }
    response = yt.service.playlistItems().insert(
        part='snippet',
        body=request_body
    ).execute()
    video_title = response['snippet']['title']
    print(f'Video "{video_title}" inserted to {playlist_title} playlist')