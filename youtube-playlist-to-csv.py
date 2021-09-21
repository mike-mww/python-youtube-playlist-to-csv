import sys, getopt, csv, traceback
from datetime import datetime
from slugify import slugify
from YouTubeApiClass import YouTubeApi

# Supply the YouTube service API key...
apiKey = ''

def main():
    # Prepare logic for command line arguments...    
    playlistId = None
    summaryOnly = False
    stackTrace = False
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:st", ['playlist=', 'summary', 'trace'])
    except getopt.GetoptError as err:
        print(err)
        opts = []
    
    for opt, arg in opts:
        if opt in ['-p', '--playlist']:
            playlistId = arg
        elif opt in ['-s', '--summary']:
            summaryOnly = True
        elif opt in ['-t', '--trace']:
            stackTrace = True
    
    # If the YouTube playlist ID was supplied...
    if playlistId:
        try:
            # Instatiate the YouTubeAPI class...
            yt = YouTubeApi(apiKey, playlistId)
            
            # Get the playlist title...
            playlistTitle = yt.getPlaylistTitle()
            
            # Loop through each set of playlist video results...
            # Prepare CSV data by default...
            currentPage = 1
            nextPageToken = None
            videosData = []
            totalSeconds = 0
            
            while True:
                playlistItems = yt.getPlaylistItems(nextPageToken)
                videos = yt.getPlaylistVideos(playlistItems)

                for index, video in enumerate(videos):
                    if currentPage == 1 and not index:
                        videosData.append([key for key in video])
                        
                    rowData = []
                    for key in video:
                        rowData.append(video.get(key))
                        
                        if 'duration' in key:
                            totalSeconds += video.get(key)
                
                    videosData.append(rowData)

                nextPageToken = playlistItems.get('nextPageToken')
                if not nextPageToken:
                    break
                
                currentPage = (currentPage + 1)
            
            # If the "summary" command is present...
            if summaryOnly:
                playlistItemCount = yt.getPlaylistItemCount()
                playlistMinutes, playlistSeconds = divmod(totalSeconds, 60)
                playlistHours, playlistMinutes = divmod(playlistMinutes, 60)
                
                print(f'{playlistTitle} - {playlistItemCount} videos | {playlistHours}h {playlistMinutes}m {playlistSeconds}s')
            
            # ...othewrise, create the CSV file...
            else:
                timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
                playlistTitleSlug = slugify(playlistTitle)
                
                csvFilename = f"{playlistTitleSlug}-results-{timestamp}.csv"
                csvFile = open(csvFilename, mode = 'w', newline = '')
                csvWriter = csv.writer(csvFile, delimiter = ',')
            
                csvWriter.writerows(videosData)
            
                csvFile.close()
                
        # If an error occurred...
        except Exception as e:
            print(f'An error occurred when trying to query playlist {playlistId}')
            
            if stackTrace:
                print()
                traceback.print_exc()
                
    # If the YouTube playlist ID wasn't supplied...
    else:
        print('Playlist ID is required')
    
    
if __name__ == "__main__":
    main()