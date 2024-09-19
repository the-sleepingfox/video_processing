# Video Upload and Subtitle Search Application

This project is a Django web application that allows users to upload videos, extract subtitles using FFmpeg, search for specific phrases within the subtitles, and play the video from a specific timestamp with closed captions.

## Features

- **Video Upload**: Users can upload videos.
- **Subtitle Extraction**: Subtitles are automatically extracted using FFmpeg.
- **Search Subtitles**: Users can search for specific phrases in the subtitles and jump to the corresponding timestamp in the video.
- **Closed Captions**: Subtitles are shown as closed captions on the video.
- **Video Deletion**: Users can delete videos and their corresponding subtitle files.

## Prerequisites

- **Docker** and **Docker Compose**
- **FFmpeg**
- **PostgreSQL**

## Project Setup (Withou Docker)

Before setting up the project, ensure that the following tools are installed on your machine:

1. **Python** (3.8+ recommended)
2. **Django** (5.1.1)
3. **FFmpeg** (for subtitle extraction)
4. **PostgreSQL**

Run the following command in terminal
```bash
pip install -r requirements.txt
```
After environment is setup completly
```bash
python manage.py runserver
```

## Project Setup (Using Docker)

- Plese ensure Docker is installed in your system.
- Follow these steps to get the project up and running using Docker and Docker Compose.

### Step 1: Clone the repository

```bash
git clone https://github.com/the-sleepingfox/video_processing.git
```
```bash
cd video_processing
```

Run the command in bash of root folder where .yml file is available.

```bash
cmd docker-compose up -d --build
``` 
Navigate_to 127.0.0.1:8000
```bash
run_migrations docker-compose exec web python manage.py migrate
```

```bash
create_superuser docker-compose exec web python manage.py createsuperuser
```







