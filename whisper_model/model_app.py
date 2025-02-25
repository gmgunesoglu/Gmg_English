import time
import sounddevice as sd
import numpy as np
import whisper
import torch
from collections import deque


# Whisper modelini yükleyin (GPU kullanımı için cuda ile çalıştırın)
device = "cuda"
if not torch.cuda.is_available():
    print("gpu olmuyor")
    device = "cpu"
print(f"models: {whisper.available_models()}")
model = whisper.load_model("large-v3-turbo", device=device)

# Ses kaydı için parametreler
samplerate = 16000  # Ses örnekleme hızı (16kHz)
buffer_duration = 2  # Buffer'ın süresi 3 saniye
buffer_size = int(samplerate * buffer_duration)  # Buffer boyutunu hesaplayalım

# Anlık ses kaydı alınacak
buffer = deque(maxlen=buffer_size)

silence_threshold = 0.01

# Ses kaydını almak ve buffer'ı doldurmak için callback fonksiyonu
def audio_callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    # Buffer'a ses verisini ekle
    buffer.extend(indata[:, 0])  # Mono ses kanalını alıyoruz


def transcribe_audio(text: str):
    pre_text = text.split(" ")
    index = 0
    word_count = 10
    last_index = len(pre_text) - word_count

    while index <= last_index:
        if len(buffer) == buffer_size:
            audio_data = np.array(buffer, dtype=np.float32)  # Buffer'dan ses verisini al

            # Sessizlik kontrolü (ortalama mutlak değer)
            volume_norm = np.linalg.norm(audio_data) / np.sqrt(len(audio_data))

            if volume_norm < silence_threshold:
                # print("Sessizlik algılandı, model çalıştırılmadı.")
                time.sleep(0.5)  # 0.8 saniye bekle ve devam et
            else:
                # Model yalnızca yeterli ses seviyesi olduğunda çalıştırılır
                prompt = " ".join(pre_text[index:index+3])
                result = model.transcribe(audio_data, language="en", task="transcribe", temperature=.5, initial_prompt=prompt)
                print(f"prompt: {prompt}")

                print(f"Ön Metin: {pre_text[index:index + word_count]}")
                result_texts = result['text'].replace(',', "").replace('.', "")
                print(f"result_texts: {result_texts}")
                result_text_array = result_texts.split(" ")

                for result_text in result_text_array:
                    if result_text.lower() == pre_text[index].lower():
                        index += 1

        time.sleep(0.5)  # 0.2 saniye bekle ve devam et


# Ses kaydını başlatan fonksiyon
def start_recording(pre_text: str):
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=samplerate):
        print("Ses kaydı başlatıldı. Program kapanana kadar devam edecek...")
        transcribe_audio(pre_text)  # Ses kaydından sürekli metne dönüştürme işlemini başlat


# Kayıt başlat
with open("reading_text.txt", "r", encoding="utf-8") as file:
    reading_text = file.read()
reading_text = reading_text.replace(',', "").replace('.', "").replace('\n', " ")
# reading_text = reading_text.replace('\'', "")
print(reading_text)
start_recording(reading_text)
