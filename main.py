#!./.venv python
# -*- coding: utf-8 -*-
"""
YouTube API Client: using official Google API to retrieve different statistics and content of YouTube
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

# statistics for my youtube channel
request = youtube_service.channels().list(
    part='statistics',
    forUsername='disooqi'
)
print(request.execute())
print()
# My channel ID UCtREr67WnhCuBIYuTMQca6A
# Calculate the duration of videos in a specific playlist
playlists_req = youtube_service.playlists().list(
    part='contentDetails, snippet',
    channelId='UCtREr67WnhCuBIYuTMQca6A'
)

playlists_response = playlists_req.execute()
for playlist in playlists_response['items']:
    print('Playlist Title:', playlist['snippet']['title'], ', ID', playlist['id'])
    videoId_list = list()
    next_page_token = None
    td = datetime.timedelta()
    while True:
        playlistItem_req = youtube_service.playlistItems().list(part='contentDetails',
                                                                playlistId=playlist['id'],
                                                                maxResults=5,
                                                                pageToken=next_page_token)
        playlistItems_response = playlistItem_req.execute()
        for item in playlistItems_response['items']:
            videoId = item['contentDetails']['videoId']
            videoId_list.append(videoId)
        else:
            video_req = youtube_service.videos().list(part='contentDetails', id=','.join(videoId_list))

            for video in video_req.execute()['items']:
                duration = video['contentDetails']['duration']
                m = re.match(r'PT((?P<hrs>\d+)H)?((?P<mins>\d+)M)?((?P<secs>\d+)S)?', duration)
                td += datetime.timedelta(hours=float(m.group('hrs')) if m.group('hrs') else 0,
                                         minutes=float(m.group('mins')) if m.group('mins') else 0,
                                         seconds=float(m.group('secs')) if m.group('secs') else 0
                                         )
        next_page_token = playlistItems_response.get('nextPageToken')
        if not next_page_token:
            break
    print("Playlist total duration is", td)
    print()
