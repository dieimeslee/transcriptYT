# transcriptYT
 transform audio to text from YT based on subtitles
---

# YouTube Caption Extractor  

A simple and efficient tool for extracting captions and transcripts from YouTube videos.  

## Description  

YouTube Caption Extractor is a Python application designed to extract closed captions from YouTube videos quickly and accurately. This tool eliminates the need to download the entire video or audio to obtain transcripts, resulting in a faster and more precise process.  

## Features  

- Extraction of manual and automatic captions from YouTube videos  
- Support for multiple languages (pt, en, es, fr, etc.)  
- Automatic detection of available captions  
- Cleaning and formatting of extracted text  
- Removal of duplicates and HTML formatting  
- Saving transcripts to text files  
- Simple command-line interface  

## Requirements  

- Python 3.6 or higher  
- yt-dlp library  

## Installation  

1. Clone this repository:  
```
git clone https://github.com/your-username/youtube-caption-extractor.git
cd youtube-caption-extractor
```  

2. Install dependencies:  
```
pip install yt-dlp
```  

## How to use  

### Basic method  
```
python extract_captions.py https://www.youtube.com/watch?v=VIDEO_ID
```  

### Specify language  
```
python extract_captions.py https://www.youtube.com/watch?v=VIDEO_ID -i en
```  

### Display only, without saving to file  
```
python extract_captions.py https://www.youtube.com/watch?v=VIDEO_ID --no-log
```  

### Interactive mode  
```
python extract_captions.py
```  

## Parameters  

- `url`: YouTube video URL (required)  
- `-i`, `--language`: Desired language code (default: pt)  
- `-nl`, `--no-log`: Do not save the transcript to a file  

## Language codes examples  

- `pt`: Portuguese  
- `en`: English  
- `es`: Spanish  
- `fr`: French  
- `de`: German  
- `it`: Italian  
- `ja`: Japanese  

## Advantages over other methods  

- Does not require FFmpeg or other audio processing libraries  
- Does not rely on speech recognition services  
- Extracts text directly from official or auto-generated YouTube captions  
- Much faster process compared to downloading and transcribing audio  
- Higher accuracy, especially for videos with manual captions  

## Limitations  

- Depends on the availability of captions in the video  
- The quality of automatic transcripts may vary  
- Some videos may not have available captions  

## Contributions  

Contributions are welcome! Feel free to open issues or submit pull requests.  

## License  

This project is licensed under the MIT License - see the LICENSE file for details.