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
                                                                maxResults=5, pageToken=next_page_token)
        playlistItems_response = playlistItem_req.execute()
        for item in playlistItems_response['items']:
            videoId = item['contentDetails']['videoId']
            videoId_list.append(videoId)

        next_page_token = playlistItems_response.get('nextPageToken')
        if not next_page_token:
            break
    return videoId_list


def get_duration_of_video_list(video_ids):
    video_req = youtube_service.videos().list(part='contentDetails', id=','.join(video_ids))
    td = datetime.timedelta()
    for video in video_req.execute()['items']:
        duration = video['contentDetails']['duration']
        m = re.match(r'PT((?P<hrs>\d+)H)?((?P<mins>\d+)M)?((?P<secs>\d+)S)?', duration)
        td += datetime.timedelta(hours=float(m.group('hrs')) if m.group('hrs') else 0,
                                  minutes=float(m.group('mins')) if m.group('mins') else 0,
                                  seconds=float(m.group('secs')) if m.group('secs') else 0)
    else:
        return td


if __name__ == '__main__':
    playlist_ids = get_playlists_of_specific_channel(channel_id='UCtREr67WnhCuBIYuTMQca6A')
    for playlist in playlist_ids:
        videos_ids = get_videos_of_specific_playlist(playlist_id=playlist)
        playlist_duration = get_duration_of_video_list(videos_ids)
        print(f"Playlist '{playlist}' has total duration of", playlist_duration)
        print()
