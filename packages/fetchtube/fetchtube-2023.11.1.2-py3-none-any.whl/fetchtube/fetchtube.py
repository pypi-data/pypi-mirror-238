import os
import argparse
from pathlib import Path
from pytube import YouTube

DOWNLOADS_PATH = str(Path.home() / "Downloads")
FETCH_VERSION = "2023.11.1.2"


def download_video(url, output_path=DOWNLOADS_PATH, preferred_quality="1080p", oauth=False):
    try:
        yt = YouTube(url, use_oauth=oauth, allow_oauth_cache=oauth)
        selected_stream = yt.streams.filter(file_extension='mp4', progressive=True).desc().first()

        if selected_stream:
            print(f"Downloading '{yt.title}' video in {selected_stream.resolution}...")
            selected_stream.download(output_path)
            print(f"'{yt.title}' video downloaded to {output_path}")
        else:
            print(f"No suitable video stream found for '{yt.title}' video.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def download_audio(url, output_path=DOWNLOADS_PATH, preferred_quality="128kbps", oauth=False):
    try:
        yt = YouTube(url, use_oauth=oauth, allow_oauth_cache=oauth)
        selected_stream = yt.streams.filter(only_audio=True, file_extension='mp4').desc().first()

        if selected_stream:
            print(f"Downloading '{yt.title}' audio in {selected_stream.abr}...")
            os.rename(selected_stream.download(output_path), os.path.splitext(selected_stream.download(output_path))[0] + '.mp3')

            print(f"'{yt.title}' audio downloaded to {output_path}")
        else:
            print(f"No suitable audio stream found for '{yt.title}' video.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def get_qualities(url, oauth=False):
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


def display_qualities(qualities):
    if qualities is not None:
        print("Available Video Qualities:")
        for quality in qualities["Video Qualities"]:
            print(f"  - {quality}")

        print("Available Audio Qualities:")
        for quality in qualities["Audio Qualities"]:
            print(f"  - {quality}")
    else:
        print("No qualities available.")


def main():
    parser = argparse.ArgumentParser(description="Fetch - YouTube Video and Audio Downloader")

    parser.add_argument("url", help="URL of the YouTube video to download")
    parser.add_argument("-o", "--output", help="Specify the output directory for downloaded files")
    parser.add_argument("-v", "--video", action="store_true", help="Download video")
    parser.add_argument("-a", "--audio", action="store_true", help="Download audio")
    parser.add_argument("-q", "--quality", help="Preferred quality (e.g., '1080p' or '128kbps')")
    parser.add_argument("-l", "--list-qualities", action="store_true", help="List available video and audio qualities")
    parser.add_argument("--oauth", action="store_true", help="Use OAuth for authentication")

    args = parser.parse_args()

    if args.list_qualities:
        qualities = get_qualities(args.url)
        if qualities:
            display_qualities(qualities)
    else:
        output_path = args.output if args.output else DOWNLOADS_PATH  # Use Downloads folder if no output directory is provided

        if args.video:
            preferred_quality = args.quality if args.quality else "1080p"
            oauth = args.oauth if args.oauth else False
            download_video(args.url, output_path, preferred_quality, oauth=oauth)
        elif args.audio:
            preferred_quality = args.quality if args.quality else "128kbps"
            oauth = args.oauth if args.oauth else False
            download_audio(args.url, output_path, preferred_quality, oauth=oauth)


if __name__ == "__main__":
    main()