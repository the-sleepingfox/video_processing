import os, subprocess, re
from datetime import timedelta
from .models import Video, Subtitle
from django.http import JsonResponse
from django.conf import settings


def process_subtitle(video_id, video_path,subtitle_output_path):
    video= Video.objects.get(id= video_id)
    
    # subtitle_output_path = f"{os.path.splitext(video_path)[0]}.srt"
    command= ['ffmpeg', '-i', video_path, '-map', '0:s:0', subtitle_output_path]
    # print(f"Running command: {command}")


    try:
        subprocess.run(command, check=True)
        if os.path.exists(subtitle_output_path):
            with open(subtitle_output_path, 'r') as f:
                content=f.read()

            subtitles = parse_subtitles(content)

            # LOOP is used tp Save each subtitle with its timestamp and text
            for subtitle in subtitles:
                Subtitle.objects.create(
                    video=video,
                    timestamp=subtitle['timestamp'],
                    content=subtitle['content']
                )

            subtitle_url = f"{settings.MEDIA_URL}subtitles/{os.path.basename(subtitle_output_path)}"
            return JsonResponse({
                "message": "Subtitles processed successfully.",
                "subtitle_url": subtitle_url  # Return the subtitle URL
            })

    except subprocess.CalledProcessError as e:
        print(f"Error Extracting Subtitles: {e}")
        return JsonResponse({"error": "Error extracting subtitles."}, status=500)


def parse_subtitles(content):
    """this
    Returns a list of dictionaries with 'timestamp' and 'content' keys.
    """
    pattern = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})')
    subtitles = []
    lines = content.splitlines()
    current_text = []
    current_timestamp = None

    for line in lines:
        if pattern.match(line):
            # When a new timestamp is found, save the previous subtitle (if any)
            if current_timestamp:
                subtitles.append({
                    'timestamp': current_timestamp,
                    'content': '\n'.join(current_text)
                })
                current_text = []

            # Extract the start timestamp (for simplicity)
            start_time = pattern.match(line).group(1)
            # Convert the start timestamp to a timedelta object
            current_timestamp = convert_srt_timestamp_to_timedelta(start_time)

        elif line.strip() == '':
            # End of a subtitle block
            continue
        else:
            # Collect subtitle lines
            current_text.append(line)

    # Add the last subtitle if any
    if current_timestamp:
        subtitles.append({
            'timestamp': current_timestamp,
            'content': '\n'.join(current_text)
        })

    return subtitles

def convert_srt_timestamp_to_timedelta(timestamp):
    """
    Convert an SRT timestamp to a timedelta object.
    """
    hours, minutes, seconds = timestamp.split(':')
    seconds, milliseconds = seconds.split(',')
    return timedelta(
        hours=int(hours),
        minutes=int(minutes),
        seconds=int(seconds),
        milliseconds=int(milliseconds)
    )