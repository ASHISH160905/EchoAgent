import re
from urllib.parse import urlparse
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from youtube_transcript_api import YouTubeTranscriptApi

def is_valid_syntax(url):
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False
        
        # Check for YouTube domains
        domain = result.netloc.lower()
        if domain.startswith('www.'):
            domain = domain[4:]
        
        return domain in ['youtube.com', 'youtu.be']
    except Exception:
        return False
 
# Used for Checking if the Url is live or not
def is_link_live(url):
    ydl_opts = {
        'extract_flat': True,   
        'playlist_items': 0,
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=False)
        return True
    except DownloadError:
        return False

def extract_video_id(url):
    """
    Extract the video ID from a YouTube URL.
    Handles standard, shortened, and mobile URLs.
    """
    regex = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None

def get_transcrpt(url):
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Could not extract a valid YouTube video ID from the provided link.")

    try:
        # Instantiate the API and fetch transcript list
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        
        # Attempt to find English transcript (manual or generated)
        transcript = transcript_list.find_transcript(['en'])
        snippets = transcript.fetch()
        
        txt = [snippet.text for snippet in snippets]
        return " ".join(txt)
        
    except Exception as e:
        raise RuntimeError(f"Failed to fetch YouTube transcript: {e}")





    
