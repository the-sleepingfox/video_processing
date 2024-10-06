from django.shortcuts import render, redirect
from .forms import VideoForm
from .models import Video, Subtitle
from .utils import process_subtitle
import os
from django.conf import settings

# Create your views here.

def home(request):
    return render(request, 'home.html')

def upload_video(request):
    if request.method == 'POST':
        form= VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video= form.save()
            video_path= video.video_file.path
            
            subtitle_output_path= f"media/sub_{video.title}_{video.id}.srt"
            process_subtitle(video.id, video_path, subtitle_output_path)

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
    timestamp= float(request.GET.get('timestamp', 0))
    subtitleUrl = f"{settings.MEDIA_URL}sub_{video.title}_{video.id}.srt"
    context={
        'video': video,
        'subtitles': subtitles,
        'subtitleUrl': subtitleUrl,
        'timestamp': timestamp,
    }
    return render(request, 'video_detail.html', context)

def search_subtitle(request):
    query = request.GET.get('query', '')
    subtitles = []
    if query:
        subtitles = Subtitle.objects.filter(content__icontains=query)  # Case-insensitive search
    return render(request, 'search_results.html', {'subtitles': subtitles, 'query': query})

def delete_video(request, video_id):
    video= Video.objects.get(id=video_id)
    video_path= video.video_file.path
    subtitle_path= f"media/sub_{video.title}_{video.id}.srt"
    if os.path.isabs(video_path):
        os.remove(video_path)
    if os.path.isabs(subtitle_path):
        os.remove(subtitle_path)
    video.delete()
    return redirect('video_list')