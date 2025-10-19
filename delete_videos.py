from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import os
from youtube import YouTube
from create_playlist import read_ids_from_file

# Read video IDs to be deleted from the text file
def read_video_ids(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip().split(',')[0] for line in file.readlines()[1:]]

# Fetch all videos in the playlist
def get_playlist_videos(playlist_id):
    video_ids = []
    next_page_token = None

    while True:
        try:
            playlist_items_response = youtube.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()
        except HttpError as e:
            print(f"An error occurred while fetching playlist items: {e}")
            break

        for item in playlist_items_response['items']:
            video_ids.append({
                "id": item["id"],  # ID of the video in the playlist
                "videoId": item['snippet']['resourceId']['videoId'],  # Actual video ID
                "title": item['snippet']['title']  # Optional: for debugging or logging
            })

        next_page_token = playlist_items_response.get('nextPageToken')
        if not next_page_token:
            break

    return video_ids

# Delete a video from the playlist by its playlist item ID
def delete_playlist_video(playlist_item_id):
    try:
        yt.service.playlistItems().delete(
            id=playlist_item_id
        ).execute()
        print(f"Deleted playlist item ID: {playlist_item_id}")
    except HttpError as e:
        print(f"An error occurred while deleting playlist item ID {playlist_item_id}: {e}")

def main():
    # Step 1: Read video IDs to delete
    video_ids_to_delete = read_ids_from_file(video_ids_file)
    print(f"Video IDs to delete: {video_ids_to_delete}")

    # Step 2: Get all videos in the playlist
    playlist_videos = get_playlist_videos(playlist_id)
    print(f"Found {len(playlist_videos)} videos in the playlist.")

    output_file = f"NewIDS/NewIDS_VideoDetails.txt"
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("id,videoId\n")
        for video in playlist_videos:
            line = f"{video['id']},{video['videoId']}\n"
            file.write(line)
    
    print(f"Details for channel have been saved to '{output_file}'.")

    # Step 3: Match and delete videos
    for video in playlist_videos:
        if video["videoId"] in video_ids_to_delete:
            print(f"Deleting video: {video['title']} (Video ID: {video['videoId']})")
            delete_playlist_video(video["id"])

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    client_file = os.getenv("CLIENT_FILE")
    yt = YouTube(client_file)
    yt.init_service()

    # Access the API key and other variables
    api_key = os.getenv("API_KEY")
    playlist_id = os.getenv("PLAYLIST")  # The ID of the playlist
    video_ids_file = 'videos_to_delete.txt'

    # Initialize YouTube API client
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
    except HttpError as e:
        print(f"An error occurred while initializing the YouTube API client: {e}")
        exit()

    main()
