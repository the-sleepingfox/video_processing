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







