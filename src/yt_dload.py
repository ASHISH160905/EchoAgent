from urllib.parse import urlparse
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from youtube_transcript_api import YouTubeTranscriptApi

def is_valid_syntax(url):
    try:
        result = urlparse(url)
        return all([result.scheme,result.netloc])
    except Exception :
        return False
 
# Used for Checking if the Url is live or not
def is_link_live(url):
    ydl_opts = {
        'extract_flat': True,   
        'playlist_items':0,
        'quiet': True,
        'no_warnings':True,
        'skip_download':True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url,download=False)
        return True
    except DownloadError:
        return False

def get_transcrpt (url):
    #getting the video code for Youtube Transcript Api
    url_list = url.split('=')
    video_id = url_list[1].strip()
    #print(f" code  : {video_id} and Type : {type(video_id)}")
    #print(dir(YouTubeTranscriptApi))

    #fetching the trans-script
    try:
        tsxapi = YouTubeTranscriptApi()
        transcrpt = tsxapi.fetch(video_id)
        txt = []
        for snippet in transcrpt:
            txt.append(snippet.text)
            transcripted_text = " ".join(txt)
        return transcripted_text
    except Exception as e:
        print(f"Some Error occured : {e}")
        return "could not get transcript - error occured"





    
