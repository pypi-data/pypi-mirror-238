# FetchTube - Simple YouTube Video and Audio Downloader

FetchTube is a lightweight Python package that allows you to easily download YouTube videos and audio using simple command-line commands.

## Installation

You can install FetchTube using pip:

```bash
pip install fetchtube
```
## Usage
FetchTube provides two straightforward command-line commands:


## Download Video
To download a video from YouTube, use the -v command followed by the video's URL:

``` bash
fetchtube -v "https://www.youtube.com/watch?v=VIDEO_ID"
```

This command will download the best available video up to 1080p resolution to your current working directory.

## Download Audio
To download audio from a YouTube video, use the -a command followed by the video's URL:

``` bash
fetchtube -a "https://www.youtube.com/watch?v=VIDEO_ID" 
```

This command will download the best quality audio stream to your current working directory.

## License
This package is open-source and released under the MIT License. Feel free to use and modify it according to your needs.

## Acknowledgments
FetchTube is built on the Pytube library.

## Author
Caleb Smith

## Contribute
If you'd like to contribute to this project or report issues, please visit the GitHub repository.

Happy downloading!