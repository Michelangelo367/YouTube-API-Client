# -*- coding: utf-8 -*-
from googleapiclient.discovery import build

api_key = 'AIzaSyCz175-8M4WQKEmBLow55UkEVr6Qvr9kmI'

service_name = 'youtube'
service_ver = 'v3'

youtube_service = build(service_name, service_ver, developerKey=api_key, http=None)

# statistics for my youtube channel
request = youtube_service.channels().list(part='statistics', forUsername='disooqi')
print(request.execute())

# Calculate the duration of videos in a specific playlist
