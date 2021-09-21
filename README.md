# Python YouTube Playlist to CSV
Python script for exporting a YouTube playlist to a CSV file or providing a summary within the terminal.

## Getting Started
### Prerequisities
* [Python 3.9.7](https://www.python.org/downloads/release/python-397/) or higher
* [Google API Python Client 2.22.0](https://github.com/googleapis/google-api-python-client)
* [Python Slugify 5.0.2](https://github.com/un33k/python-slugify)

#### Google API Console
In order for this script to query the YouTube API, an API key is required via the [Google API Console](https://console.developers.google.com/). The following resources provide documentation on creating a Google API Console project and generating an API key:
* [Google API Python Client - Getting Started: Setup](https://github.com/googleapis/google-api-python-client/blob/main/docs/start.md#setup)
* [Google API Python Client - Getting Started: Simple API access (API keys)](https://github.com/googleapis/google-api-python-client/blob/main/docs/start.md#1-simple-api-access-api-keys)

### Installation
Download the repository files and run the command below to install the necessary packages:
```
pip install google-api-python-client python-slugify
```

### Configuration
The YouTube API key must be supplied to the **apiKey** variable at the top of the **"youtube-playlist-to-csv.py"** script file.
```
apiKey = '[YOUTUBE API KEY]'
```

## Built with
* [Python 3.9.7](https://www.python.org/downloads/release/python-397/)
* [Google API Python Client 2.22.0](https://github.com/googleapis/google-api-python-client)
* [Python Slugify 5.0.2](https://github.com/un33k/python-slugify)

## Usage
#### Minimum requirements / generating a CSV file
```
# Using long-form arguments
python youtube-playlist-to-csv.py --playlist "[YOUTUBE PLAYLIST ID]"

# Using short-form arguments
python youtube-playlist-to-csv.py -p "[YOUTUBE PLAYLIST ID]"
```
Upon completion, a CSV file will be generated adjacent to the other script files containing all of the relevant data from querying the YouTube API.

#### Terminal summary
```
# Using long-form arguments
python youtube-playlist-to-csv.py --playlist "[YOUTUBE PLAYLIST ID]" --summary

# Using short-form arguments
python youtube-playlist-to-csv.py -p "[YOUTUBE PLAYLIST ID]" -s

# Output
# [Playlist title] - [x] videos | [x]h [y]m [z]s
```

### API
#### Script arguments
* ***--playlist | -p*** (string) (Default: "" | Required)\
The ID for the target YouTube playlist. This is the only value required for the script to operate. The playlist ID can be obtained from a YouTube playlist's URL following the **"list="** query string parameter.

* ***--summary | -s*** (switch) (Default: false)\
Switches the default behavior of generating a CSV file to simply outputting a summary to the terminal. The summary includes the playlist's title, total video count, and the total playlist duration time.

* ***--trace | -t*** (switch) (Default: false)\
Enables stack tracing in the terminal for debugging errors.