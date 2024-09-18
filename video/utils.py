import os, subprocess, re
from pydub import AudioSegment
from datetime import timedelta
from .models import Video, Subtitle

# def extract_audio_from_video(video_path, audio_output_path):
#     """Extract audio from video file using FFmpeg"""
#     command= f"ffmpeg -i {video_path} -q:a 0 -map a {audio_output_path}"
#     subprocess.run(command, shell=True, check=True)

# def transcribe_audio_to_subtitles(audio_file, video_id):
#     """subtitle generation from audio using speechrecognition library"""
#     recognizer= sr.Recognizer()

#     # Load audio file using pydub
#     audio= AudioSegment.from_file(audio_file)
#     audio.export('temp.wav', format='wav')

#     with sr.AudioFile('temp.wav') as source:
#         audio_data= recognizer.record(source)
    
#     try:
#         text= recognizer.recognize_google(audio_data)
#         process_subtitle_text(text, video_id)
#     except sr.UnknownValueError:
#         print("Speech recognition cannot understand the audio")
#     except sr.RequestError as e:
#         print(f"could not request results from Google Speech Recognition service: {e}")

# def process_subtitle_text(text, video_id):
#     """Save the extracted subtitle"""
#     lines= text.splitlines()
#     for idx, line in enumerate(lines):
#         Subtitle.objects.create(
#             video_id= video_id,
#             timestamp= timedelta(seconds=idx * 5),
#             text= lines
#         )

def process_subtitle(video_id, video_path,subtitle_output_path):
    video= Video.objects.get(id= video_id)
    
    # subtitle_output_path = f"{os.path.splitext(video_path)[0]}.srt"
    command= ['ffmpeg', '-i', video_path, '-map', '0:s:0', subtitle_output_path]
    print(f"Running command: {command}")


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

                # Subtitle.objects.create(
                #     video= video,
                #     text=content
                # )

                # lines=content.splitlines()
                # for idx, line in enumerate(lines):
                #     Subtitle.objects.create(
                #         video_id= video_id,
                #         timestamp= timedelta(seconds=idx * 5),
                #         text= lines
                #     )

    except subprocess.CalledProcessError as e:
        print(f"Error Extracting Subtitles: {e}")


def parse_subtitles(content):
    """
    Parse subtitle content in SRT format and extract timestamps and text.
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
    Convert an SRT timestamp (e.g., '00:00:01,000') to a timedelta object.
    """
    hours, minutes, seconds = timestamp.split(':')
    seconds, milliseconds = seconds.split(',')
    return timedelta(
        hours=int(hours),
        minutes=int(minutes),
        seconds=int(seconds),
        milliseconds=int(milliseconds)
    )