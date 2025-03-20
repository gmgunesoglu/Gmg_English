import time
import sounddevice as sd
import numpy as np
import redis
import pickle
from collections import deque
import threading  # threading modülünü ekliyoruz

# Redis bağlantısı
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Ses kaydı için parametreler
samplerate = 16000  # 16kHz
buffer_duration = 3  # 3 saniyelik buffer
buffer_size = int(samplerate * buffer_duration)

# Anlık ses kaydı için buffer
buffer = deque(maxlen=buffer_size)


# Ses kaydını almak ve buffer'ı doldurmak için callback fonksiyonu
def audio_callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    buffer.extend(indata[:, 0])  # Mono ses


# Redis'e veriyi gönderme fonksiyonu
def send_audio_to_redis():
    while True:
        if len(buffer) == buffer_size:
            audio_data = np.array(buffer, dtype=np.float32)
            serialized_data = pickle.dumps(audio_data)
            redis_client.set("audio_buffer", serialized_data)
            print("Ses Redis'e gönderildi")
        time.sleep(0.5)  # Her 500ms'de bir güncelle


# Ses kaydını başlatan fonksiyon
def start_listener():
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=samplerate):
        print("Ses kaydedici çalışıyor...")
        # Redis'e veri gönderme işlemini ayrı bir thread olarak başlatıyoruz
        redis_thread = threading.Thread(target=send_audio_to_redis, daemon=True)
        redis_thread.start()

        # Bu blok sürekli çalışacak, ses kaydını sürekli dinleyecek
        while True:
            time.sleep(1)


if __name__ == "__main__":
    start_listener()
