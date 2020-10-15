#!./.venv python
# -*- coding: utf-8 -*-
"""
YouTube API Client: using official Google API to retrieve different statistics and content of YouTube.
"""
__author__ = "Mohamed Eldesouki"
__copyright__ = "Copyright 2020-29, GINA CODY SCHOOL OF ENGINEERING AND COMPUTER SCIENCE, CONCORDIA UNIVERSITY"
__credits__ = ["Mohamed Eldesouki"]
__email__ = "mohamed@eldesouki.ca"
__created__ = "2020-10-02"

import re
import datetime
from googleapiclient.discovery import build

api_key = 'AIzaSyCz175-8M4WQKEmBLow55UkEVr6Qvr9kmI'

service_name = 'youtube'
service_ver = 'v3'

youtube_service = build(service_name, service_ver, developerKey=api_key, http=None)


def get_playlists_of_specific_channel(channel_id):
    # statistics for my youtube channel
    # request = youtube_service.channels().list(
    #     part='statistics',
    #     forUsername='disooqi'
    # )
    # print(request.execute())
    # print()
    # My channel ID UCtREr67WnhCuBIYuTMQca6A
    # Calculate the duration of videos in a specific playlist
    playlists_req = youtube_service.playlists().list(
        part='contentDetails, snippet',
        channelId=channel_id
    )
    playlists_response = playlists_req.execute()
    playlist_ids = list()
    for playlist in playlists_response['items']:
        playlist_ids.append(playlist['id'])
        # print('Playlist Title:', playlist['snippet']['title'], ', ID', playlist['id'])
    return playlist_ids


def get_videos_of_specific_playlist(playlist_id):
    # for playlist in playlists_response['items']:
    #     print('Playlist Title:', playlist['snippet']['title'], ', ID', playlist['id'])
    videoId_list = list()
    next_page_token = None

    while True:
        playlistItem_req = youtube_service.playlistItems().list(part='contentDetails', playlistId=playlist_id,
                                                                maxResults=50, pageToken=next_page_token)
        playlistItems_response = playlistItem_req.execute()
        for item in playlistItems_response['items']:
            videoId = item['contentDetails']['videoId']
            videoId_list.append(videoId)

        next_page_token = playlistItems_response.get('nextPageToken')
        if not next_page_token:
            break
    return videoId_list


def get_duration_of_video_list(video_ids):
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    td = datetime.timedelta()
    for fifty_video_ids in chunks(video_ids, 50):
        video_req = youtube_service.videos().list(part='contentDetails', id=','.join(fifty_video_ids))
        videos_response = video_req.execute()
        for video in videos_response['items']:
            duration = video['contentDetails']['duration']
            m = re.match(r'PT((?P<hrs>\d+)H)?((?P<mins>\d+)M)?((?P<secs>\d+)S)?', duration)
            td += datetime.timedelta(hours=float(m.group('hrs')) if m.group('hrs') else 0,
                                      minutes=float(m.group('mins')) if m.group('mins') else 0,
                                      seconds=float(m.group('secs')) if m.group('secs') else 0)
    else:
        return td


def get_the_most_popular_video_in_specific_playlist(playlist_id):
    pass


if __name__ == '__main__':
    my_channel_id ='UCtREr67WnhCuBIYuTMQca6A'
    channel_id = 'UC98CzaYuFNAA_gOINFB0e4Q'
    playlist_ids = get_playlists_of_specific_channel(channel_id=channel_id)
    playlist_ids = ['PL8uoeex94UhHFRew8gzfFJHIpRFWyY4YW']

    for playlist in playlist_ids:
        # get_the_most_popular_video_in_specific_playlist(playlist)
        videos_ids = get_videos_of_specific_playlist(playlist_id=playlist)
        print(len(videos_ids))
        playlist_duration = get_duration_of_video_list(videos_ids)
        print(f"Playlist '{playlist}' has total duration of", playlist_duration)
        print()

