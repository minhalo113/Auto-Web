import googleapiclient.discovery
import random
from datetime import datetime, timedelta
from config import API_YTB_KEY, YTB_CHANNEL_ID1

def read_video_ids(filename = 'already_use_video.txt'):
    try:
        with open(filename, 'r') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def get_video_from_playlist(api_service_name, api_version, playlist_id, api_key):
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
    videos = []
    next_page_token = None
    total_videos = 0
    video_count = 50

    # get total video of a channel
    request = youtube.playlistItems().list(
        part = 'snippet',
        playlistId = playlist_id,
        maxResults = 50
    )
    response = request.execute()
    total_videos = response['pageInfo']['totalResults']

    # find how many pages to skip
    pages_to_skip = (total_videos - video_count)//50

    # skip to the pages contain oldest 50 vid
    for _ in range(pages_to_skip):
        request = youtube.playlistItems().list(
            part = 'snippet',
            playlistId = playlist_id,
            maxResults = 50,
            pageToken = next_page_token
        )
        response = request.execute()
        next_page_token = response.get('nextPageToken')
    
    # get info of 50 oldest vid
    request = youtube.playlistItems().list(
        part = 'snippet',
        playlistId = playlist_id,
        maxResults = 50,
        pageToken = next_page_token
    )
    response = request.execute()

    # get 1 year ago time 
    one_year_ago = datetime.now() - timedelta(days = 365)
    # get selected vid
    selected_vid = read_video_ids()

    # get every one year or older vid of oldest 50 vid
    for item in response['items']:
        video_id = item['snippet']['resourceId']['videoId']
        title = item['snippet']['title']
        published_at = item['snippet']['publishedAt']

        published_date = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ')

        if (published_date < one_year_ago) and (video_id not in selected_vid):
            videos.append({'video_id': video_id, 'title': title, 'published_at': published_date})

    if len(videos) == 0:
        print("Already Get All Possible Video, Minus 1 To Page To Skip To Continue")
        return
    # mix videos up
    else:
        random_vid = random.choice(videos)
        return random_vid

def get_video_playlist_id(api_service_name, api_version, api_key):
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

    # get channel info
    request = youtube.channels().list(
        part="contentDetails",
        id= YTB_CHANNEL_ID1,
        maxResults=1
    )
    response = request.execute()
    uploads_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    return uploads_id

def return_videos_list():
    api_service_name = "youtube"
    api_version = "v3"
    api_key = API_YTB_KEY 

    playlist_id = get_video_playlist_id(api_service_name, api_version, api_key)
    random_videos = get_video_from_playlist(api_service_name, api_version, playlist_id, api_key)
    return random_videos

if __name__ == "__main__":
    return_videos_list()