# myapp/views.py
from django.shortcuts import render
from django.http import HttpResponse
import base64
from django.core.files.base import ContentFile
from .models import Photo
import easyocr #image recog
import cohere # ai
from gtts import gTTS
import os


def capture_photo(request):
    if request.method == 'POST':
        photo_data = request.POST.get('photo')
        format, imgstr = photo_data.split(';base64,')
        ext = format.split('/')[-1]
        photo = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        # Save the photo to the model
        photo_model = Photo(image=photo)
        photo_model.save()

        # Process the photo with EasyOCR
        reader = easyocr.Reader(['en'])
        image_path = photo_model.image.path
        result = reader.readtext(image_path)

        fragment = ""
        print("This is the fragment:")
        for detection in result:
            print(detection[1])
            fragment += " " + detection[1]
        print(fragment)

        # Rephrase text using Cohere
        co = cohere.Client('ESBqFLmeJp7AmsFEYSKkshNOEc8jGGxGtp20IKzO')
        prompt = f"The following is a sign. Tell people what the sign is saying, in one sentence.'{fragment}'"
        response = co.generate(
            model='command-r-plus',
            prompt=prompt,
            max_tokens=100,
            temperature=0.7,
        )
        meaningful_sentence = response.generations[0].text.strip()
        photo_model.rephrased_text = meaningful_sentence
        print(meaningful_sentence)

        # Convert rephrased text to speech
        tts = gTTS(text=meaningful_sentence, lang='en', slow=False)
        audio_path = f"audio/{photo_model.id}.mp3"
        audio_full_path = os.path.join('media', audio_path)
        tts.save(audio_full_path)
        photo_model.audio = audio_path
        photo_model.save()
        audio_play_script = f"<script>var audio = new Audio('/media/{audio_path}'); audio.play();" + "function handleAudioEnd() {window.history.back();}; audio.onended = handleAudioEnd; </script>"

        return HttpResponse(
            "Photo captured, text processed, and audio generated successfully."
            + audio_play_script)
    return render(request, 'camera/camera.html')
