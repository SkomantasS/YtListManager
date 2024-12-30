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

for channel_handle in channel_handles:
    # Make a request to the YouTube API
    try:
        request = youtube.channels().list(
            part='contentDetails',
            forHandle=channel_handle
        )
        response = request.execute()
        print(response)  # Debug: print the API response
    except HttpError as e:
        print(f"An error occurred while making the API request: {e}")
        exit()

    # Check if 'items' key exists in the response
    if 'items' not in response or not response['items']:
        print("No items found in the response. Please check the channel username.")
        exit()

    # Retrieve the uploads playlist ID for the given channel
    playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Retrieve all videos from the uploads playlist
    videos = []
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

        videos += playlist_items_response['items']
        next_page_token = playlist_items_response.get('nextPageToken')

        if not next_page_token:
            break

    # Extract video URLs and titles
    video_IDs = [
        {
            'ID': video['snippet']['resourceId']['videoId'],
            'PublishedAt': video['snippet']['publishedAt'],
            'Duration': video['contentDetails']['duration']
        }
        for video in videos
    ]

    # Write video URLs and titles to a file
    with open(f"youtube_videos/{channel_handle}_YoutubeVideos.txt", "w", encoding="utf-8") as outFile:
        outFile.write("ID,PublishedAt,Duration\n")
        for video in video_IDs:
            line = f"{video['ID']},{video['PublishedAt']},{video['Duration']}\n"
            outFile.write(line)

    print(f"Video IDs, publish dates and durations have been saved to '{channel_handle}_YoutubeVideos.txt'.")