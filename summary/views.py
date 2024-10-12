from django.shortcuts import render

from moviepy.editor import VideoFileClip
import os
import requests
from django.core.files.base import ContentFile
from moviepy.editor import VideoFileClip
import speech_recognition as sr
from pydub import AudioSegment
import yt_dlp as youtube_dl


def generate_summary(video_link, lang='en-US'):
    video_path = "temp_video.mp4"
    audio_path = "temp_audio.wav"

    ydl_opts = {
        'format': 'best',
        'outtmpl': video_path,
        'noplaylist': True,
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_link])

        if not os.path.exists(video_path) or os.path.getsize(video_path) == 0:
            return "The video file is invalid or empty."

        # Load the video and extract audio
        with VideoFileClip(video_path) as video:
            video.audio.write_a
            
        # Initialize recognizer class for recognizing the speech
        recognizer = sr.Recognizer()

        # Load the audio file and convert it to text
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            try:
                summary_text = recognizer.recognize_google(audio_data, language=lang)
            except sr.UnknownValueError:
                summary_text = "Speech was unintelligible."
            except sr.RequestError:
                summary_text = "Could not request results from Google Speech Recognition service."
    except youtube_dl.utils.DownloadError as de:
        return f"Download error: {str(de)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)

    return summary_text




def summarize_video(request):
    summary = ""
    if request.method == "POST":
        video_link = request.POST.get("video_link")
        language = request.POST.get("language")
        summary = generate_summary(video_link, lang=language)

    return render(request, "summarizer.html", {"summary": summary})
