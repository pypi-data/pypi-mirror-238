import os
import argparse
from pathlib import Path
from pytube import YouTube

# Constants
DOWNLOADS_PATH = str(Path.home() / "Downloads")
FETCH_VERSION = "1.0.0"


# Function to get the best video stream based on quality
def get_best_video_stream(url, preferred_quality="1080p", oauth=False):
    """
    Get the best video stream based on preferred quality.

    :param url: URL of the YouTube video
    :type url: str
    :param preferred_quality: Preferred video quality (e.g., '1080p')
    :type preferred_quality: str
    :param oauth: Use OAuth for authentication
    :type oauth: bool
    :returns: Best video stream or None if not found
    :rtype: pytube.Stream or None
    """
    try:
        yt = YouTube(url, use_oauth=oauth, allow_oauth_cache=oauth)
        available_streams = yt.streams.filter(file_extension='mp4', progressive=True)

        # Sort the streams by resolution in descending order
        sorted_streams = sorted(available_streams, key=lambda s: int(s.resolution[:-1]), reverse=True)

        for stream in sorted_streams:
            if int(stream.resolution[:-1]) <= int(preferred_quality[:-1]):
                return stream

        return None
    except Exception as e:
        print(f"An error occurred while finding the best video stream: {str(e)}")
        return None


# Function to get the best audio stream based on quality
def get_best_audio_stream(url, preferred_quality="128kbps", oauth=False):
    """
    Get the best audio stream based on preferred quality.

    :param url: URL of the YouTube video
    :type url: str
    :param preferred_quality: Preferred audio quality (e.g., '128kbps')
    :type preferred_quality: str
    :param oauth: Use OAuth for authentication
    :type oauth: bool
    :returns: Best audio stream or None if not found
    :rtype: pytube.Stream or None
    """
    try:
        yt = YouTube(url, use_oauth=oauth, allow_oauth_cache=oauth)
        available_streams = yt.streams.filter(only_audio=True, file_extension='mp4')

        # Sort the streams by audio bitrate in descending order
        sorted_streams = sorted(available_streams, key=lambda s: int(s.abr[:-4]), reverse=True)

        for stream in sorted_streams:
            if int(stream.abr[:-4]) <= int(preferred_quality[:-4]):
                return stream

        return None
    except Exception as e:
        print(f"An error occurred while finding the best audio stream: {str(e)}")
        return None


# Function to download the best video stream
def download_video(url, output_path=DOWNLOADS_PATH, preferred_quality="1080p", oauth=False):
    """
    Download the best video stream based on preferred quality.

    :param url: URL of the YouTube video
    :type url: str
    :param output_path: Output directory for downloaded video
    :type output_path: str
    :param preferred_quality: Preferred video quality (e.g., '1080p')
    :type preferred_quality: str
    :param oauth: Use OAuth for authentication
    :type oauth: bool
    """
    try:
        yt = YouTube(url, use_oauth=oauth, allow_oauth_cache=oauth)
        selected_stream = get_best_video_stream(url, preferred_quality, oauth=oauth)

        if selected_stream:
            try:
                print(f"Downloading '{yt.title}' video in {selected_stream.resolution}...")
                selected_stream.download(output_path)
                print(f"'{yt.title}' video downloaded to {output_path}")
            except Exception as e:
                print(f"An error occurred while downloading: {str(e)}")
        else:
            print(f"No suitable video stream found for '{yt.title}' video.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Function to download the best audio stream
def download_audio(url, output_path=DOWNLOADS_PATH, preferred_quality="128kbps", oauth=False):
    """
    Download the best audio stream based on preferred quality.

    :param url: URL of the YouTube video
    :type url: str
    :param output_path: Output directory for downloaded audio
    :type output_path: str
    :param preferred_quality: Preferred audio quality (e.g., '128kbps')
    :type preferred_quality: str
    :param oauth: Use OAuth for authentication
    :type oauth: bool
    """
    try:
        yt = YouTube(url, use_oauth=oauth, allow_oauth_cache=oauth)
        selected_stream = get_best_audio_stream(url, preferred_quality, oauth=oauth)

        if selected_stream:
            try:
                print(f"Downloading '{yt.title}' audio in {selected_stream.abr}...")
                audio_file_path = selected_stream.download(output_path)
                # Rename the file with a .mp3 extension
                os.rename(audio_file_path, os.path.splitext(audio_file_path)[0] + '.mp3')
                print(f"'{yt.title}' audio downloaded to {output_path}")
            except Exception as e:
                print(f"An error occurred while downloading: {str(e)}")
        else:
            print(f"No suitable audio stream found for '{yt.title}' video.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Function to get available video and audio qualities
def get_qualities(url, oauth=False):
    """
    Get available video and audio qualities for a YouTube video.

    :param url: URL of the YouTube video
    :type url: str
    :param oauth: Use OAuth for authentication
    :type oauth: bool
    :returns: Video and audio qualities
    :rtype: dict or None
    """
    try:
        yt = YouTube(url, use_oauth=oauth, allow_oauth_cache=oauth)
        available_video_streams = yt.streams.filter(file_extension='mp4', progressive=True)
        available_audio_streams = yt.streams.filter(only_audio=True, file_extension='mp4')

        video_qualities = [stream.resolution for stream in available_video_streams]
        audio_qualities = [stream.abr for stream in available_audio_streams]

        return {
            "Video Qualities": video_qualities,
            "Audio Qualities": audio_qualities,
        }
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


# Function to display available video and audio qualities
def display_qualities(qualities):
    """
    Display available video and audio qualities.

    :param qualities: Video and audio qualities
    :type qualities: dict
    """
    if qualities is not None:
        print("Available Video Qualities:")
        for quality in qualities["Video Qualities"]:
            print(f"  - {quality}")

        print("Available Audio Qualities:")
        for quality in qualities["Audio Qualities"]:
            print(f"  - {quality}")
    else:
        print("No qualities available.")


# Main function for command-line interface
def main():
    parser = argparse.ArgumentParser(description="Fetch - YouTube Video and Audio Downloader")

    parser.add_argument("url", help="url of the YouTube video to download")
    parser.add_argument("-o", "--output", help="specify the output directory for downloaded files")
    parser.add_argument("-v", "--video", action="store_true", help="download video")
    parser.add_argument("-a", "--audio", action="store_true", help="download audio")
    parser.add_argument("-q", "--quality", help="preferred quality (e.g., '1080p' or '128kbps')")
    parser.add_argument("-l", "--list-qualities", action="store_true", help="list available video and audio qualities")
    parser.add_argument("--oauth", action="store_true", help="use OAuth for authentication")

    args = parser.parse_args()

    output_path = args.output if args.output else DOWNLOADS_PATH  # Use Downloads folder if no output directory is provided

    if args.list_qualities:
        qualities = get_qualities(args.url, oauth=args.oauth)
        if qualities:
            display_qualities(qualities)
    else:
        if args.video:
            preferred_quality = args.quality if args.quality else "1080p"
            oauth = args.oauth if args.oauth else False
            download_video(args.url, output_path, preferred_quality, oauth=oauth)
        elif args.audio:
            preferred_quality = args.quality if args.quality else "128kbps"
            oauth = args.oauth if args.oauth else False
            download_audio(args.url, output_path, preferred_quality, oauth=oauth)
