from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

api_key='ADD_YOUR_API_KEY_HERE'
youtube=build(
    'youtube',
    'v3',
    developerKey=api_key
)

#Make a request to youtube api
request = youtube.channels().list(
    part='contentDetails',
    forUsername='DisneyMusicVEVO' 
  #you can change the channel name here
)


#get a response for api
response=request.execute()
print(response)

# Retrieve the uploads playlist ID for the given channel
playlist_id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

# Retrieve all videos from uploads playlist
videos = []
next_page_token = None

while True:
    playlist_items_response=youtube.playlistItems().list(
                #part='contentDetails',
                part='snippet',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
    ).execute()

    videos += playlist_items_response['items']

    next_page_token = playlist_items_response.get('nextPageToken')

    if not next_page_token:
        break

# Extract video URLs
video_urls = []

for video in videos:
    #video_id = video['contentDetails']['videoId']
    video_id = video['snippet']['resourceId']['videoId']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    video_title=video['snippet']['title']
    #video_urls.append(video_url)
    video_urls.append({'URL':video_url,'Title':video_title})

#return video_urls

#open file
outFile=open("YoutubeVideos.txt", "w",encoding="utf-8")
outFile.write("URL,Title\n")
# Print the extracted video URLs
for key in video_urls:
    line=key['URL']+","+key['Title']+"\n"
    outFile.write(line)