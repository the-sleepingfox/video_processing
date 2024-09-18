from django.shortcuts import render, redirect
from .forms import VideoForm
from .models import Video, Subtitle
from .utils import process_subtitle
# from .utils import extract_audio_from_video, transcribe_audio_to_subtitles
import os
# Create your views here.

def home(request):
    form= VideoForm()
    return render(request, 'upload.html', {'form':form})

def upload_video(request):
    if request.method == 'POST':
        form= VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video= form.save()
            video_path= video.video_file.path
            # audio_output_path= f"media/audio_{video.id}.mp3"

            subtitle_output_path= f"media/sub_{video.title}_{video.id}.srt"
            process_subtitle(video.id, video_path, subtitle_output_path)

            # extract_audio_from_video(video_path, audio_output_path)
            # transcribe_audio_to_subtitles(audio_output_path, video.id)

            return redirect('video_list')
    else:
        form= VideoForm()
    return render(request, 'upload.html', {'form':form})

def video_list(request):
    videos= Video.objects.all()
    return render(request, 'video_list.html', {'videos':videos})

def video_detail(request, video_id):
    video = Video.objects.get(id=video_id)
    subtitles = Subtitle.objects.filter(video=video)
    return render(request, 'video_detail.html', {'video': video, 'subtitles': subtitles})

def delete_video(request, video_id):
    video= Video.objects.get(id=video_id)
    video_path= video.video_file.path
    os.remove(video_path)
    video.delete()
    return redirect('video_list')