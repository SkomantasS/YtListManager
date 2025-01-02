from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import os

load_dotenv()
channel_handles = os.getenv("CHANNEL_HANDLES").split(',')
api_key = os.getenv("API_KEY")

# Initialize YouTube API client
try:
    youtube = build('youtube', 'v3', developerKey=api_key)
except HttpError as e:
    print(f"An error occurred while initializing the YouTube API client: {e}")
    exit()

# Fetch all video IDs from the uploads playlist of a channel
def get_video_ids(playlist_id):
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
            video_ids.append(item['snippet']['resourceId']['videoId'])

        next_page_token = playlist_items_response.get('nextPageToken')
        if not next_page_token:
            break

    return video_ids

# Fetch video details including duration
def get_video_details(video_ids):
    video_details = []
    for i in range(0, len(video_ids), 50):  # API supports up to 50 IDs per request
        try:
            videos_response = youtube.videos().list(
                part='contentDetails,snippet',
                id=','.join(video_ids[i:i+50])
            ).execute()
        except HttpError as e:
            print(f"An error occurred while fetching video details: {e}")
            continue

        for video in videos_response['items']:
            video_details.append({
                "ID": video['id'],
                "PublishedAt": video['snippet']['publishedAt'],
                "Duration": video['contentDetails']['duration']
            })

    return video_details

# Fetch uploads playlist ID for a given channel handle
def get_uploads_playlist_id(channel_handle):
    try:
        request = youtube.channels().list(
            part='contentDetails',
            forHandle=channel_handle.strip()
        )
        response = request.execute()

        if 'items' not in response or not response['items']:
            print(f"No items found for channel: {channel_handle}")
            return None

        return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    except HttpError as e:
        print(f"An error occurred while fetching channel details for {channel_handle}: {e}")
        return None

def main():
    for channel_handle in channel_handles:
        print(f"Processing channel: {channel_handle}")
        
        # Step 1: Get the uploads playlist ID for the channel
        playlist_id = get_uploads_playlist_id(channel_handle)
        if not playlist_id:
            continue

        # Step 2: Get video IDs
        video_ids = get_video_ids(playlist_id)

        # Step 3: Get video details (including durations)
        video_details = get_video_details(video_ids)

        # Step 4: Save details to a separate file for each channel
        output_file = f"video_details/{channel_handle.strip()}_VideoDetails.txt"
        with open(output_file, "w", encoding="utf-8") as file:
            file.write("ID,PublishedAt,Duration\n")
            for video in video_details:
                line = f"{video['ID']},{video['PublishedAt']},{video['Duration']}\n"
                file.write(line)
        
        print(f"Details for channel '{channel_handle}' have been saved to '{output_file}'.")

if __name__ == "__main__":
    main()