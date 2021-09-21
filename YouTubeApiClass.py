import re
from datetime import timedelta
from googleapiclient.discovery import build

class YouTubeApi():
    def __init__(self, apiKey:str, playlistId:str):
        self.playlistId = playlistId
        
        self.service = build('youtube', 'v3', developerKey=apiKey)
        
        
    # Public methods
    # --------------------------------------------------
    
    # getPlaylistTitle
    # Returns the playlist title
    def getPlaylistTitle(self):
        playlistInfo    = self.__getPlaylistInfo()
        playlistTitle   = playlistInfo['items'][0]['snippet']['title']
        
        return playlistTitle if playlistTitle else None
    # /getPlaylistTitle  
            
    
    # getPlaylistItemCount
    # Returns the total count of playlist items
    def getPlaylistItemCount(self):
        playlistInfo        = self.__getPlaylistInfo()
        playlistItemCount   = playlistInfo['items'][0]['contentDetails']['itemCount']
        
        return playlistItemCount if playlistItemCount else None
    # /getPlaylistItemCount
        
        
    # getPlaylistItems
    # @param    str nextPageToken
    # Returns playlist items of the current page request
    def getPlaylistItems(self, nextPageToken:str):
        req = self.service.playlistItems().list(
            part = 'contentDetails',
            playlistId = self.playlistId,
            maxResults = 50,
            pageToken = nextPageToken
        )
        
        res = req.execute()
        return res
    # /getPlaylistItems
    
    
    # getPlaylistVideos
    # @param    str playlistItems
    # Returns the playlist videos of the current page request
    def getPlaylistVideos(self, playlistItems):
        videoIds = [item['contentDetails']['videoId'] for item in playlistItems['items']]
        
        req = self.service.videos().list(
            part = 'contentDetails,snippet',
            id = ','.join(videoIds)
        )
        
        res = req.execute()
        
        videosData = []
        for video in res['items']:
            videosData.append({
                'id':               video['id'],
                'title':            video['snippet']['title'],
                'video_url':        f"https://youtu.be/{video['id']}",
                'duration_seconds': self.__calculateVideoTotalDuration(video['contentDetails']['duration']),
            })
            
        return videosData
    # /getPlaylistVideos
        
        
    # Private methods
    # --------------------------------------------------
    
    # __getPlaylistInfo
    # Returns playlist information
    def __getPlaylistInfo(self):
        req = self.service.playlists().list(
            part = 'contentDetails,snippet',
            id = self.playlistId
        )
        
        res = req.execute()
        return res
    # /__getPlaylistInfo
    
    
    # __calculateVideoTotalDuration
    # @param    str duration
    # Returns a video's calculated total number of seconds
    def __calculateVideoTotalDuration(self, duration:str):
        hours   = re.compile(r'(\d+)H').search(duration)
        minutes = re.compile(r'(\d+)M').search(duration)
        seconds = re.compile(r'(\d+)S').search(duration)
            
        hours   = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0
            
        videoTotalSeconds = timedelta(
            hours = hours, 
            minutes = minutes, 
            seconds = seconds
        ).total_seconds()
        videoTotalSeconds = int(videoTotalSeconds)
            
        return videoTotalSeconds
    # /__calculateVideoTotalDuration
    