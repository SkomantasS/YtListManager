from youtube import YouTube
from dotenv import load_dotenv
import os
import csv

def read_ids_from_file(file_path):
    """
    Reads all IDs from a single .txt file into a list.
    
    Parameters:
        file_path (str): Path to the .txt file.
        
    Returns:
        list: A list of IDs from the file.
    """
    ids = []

    # Open and read the file
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)  # Read as dictionary
        for row in reader:
            ids.append(row["ID"])  # Append the ID to the list
    
    return ids

client_file = os.getenv("CLIENT_FILE")
yt = YouTube(client_file)
yt.init_service()

response_playlist = yt.create_playlist(title='TestT')
playlist_id = response_playlist.get('id')
playlist_title = response_playlist['snippet']['title']

video_ids = read_ids_from_file('youtube_videos_combined_list/combined_and_sorted_videos.txt')
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