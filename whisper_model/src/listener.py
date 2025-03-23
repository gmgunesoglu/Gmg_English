import time
import sounddevice as sd
import numpy as np
import redis
import pickle
from collections import deque
import threading

# Redis bağlantısı
redis_host = "192.168.1.102"
redis_client = redis.Redis(host=redis_host, port=6379, decode_responses=False)

reading_text = "Helloo my friend, My name's David."
silence_threshold = 0.01

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

            # Sessizlik kontrolü (ortalama mutlak değer)
            audio_data = np.array(buffer, dtype=np.float32)
            volume_norm = np.linalg.norm(audio_data) / np.sqrt(len(audio_data))

            if volume_norm < silence_threshold:
                print("Sessizlik algılandı, kuyruğa mesaj eklenmiyor.")
                time.sleep(0.2)
            else:
                serialized_data = pickle.dumps({"message": reading_text, "audio_data": audio_data})
                redis_client.lpush("reading", serialized_data)
                print(f"Redis'e gönderildi...\nserialized_data: {serialized_data}")
                time.sleep(0.1)
        else:
            time.sleep(0.5)  # Her 500ms'de bir güncelle


# Ses kaydını başlatan fonksiyon
def start_listener():
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=samplerate):
        print("Ses kaydedici çalışıyor...")
        # Redis'e veri gönderme işlemini ayrı bir thread olarak başlatıyoruz
        redis_thread = threading.Thread(target=send_audio_to_redis, daemon=True)
        redis_thread.start()

        while True:
            time.sleep(1)


if __name__ == "__main__":
    start_listener()
