import whisper
import torch
import numpy as np
import redis
import json
import time

# use command before run: redis-server

# Whisper modelini yükle
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("large-v3-turbo", device=device)

# Redis ile bağlantı kur (FastAPI ile haberleşmek için)
redis_conn = redis.Redis(host='localhost', port=6379, db=0)

print("🎤 Whisper worker başlatıldı... FastAPI'den ses bekleniyor.")

while True:
    _, message = redis_conn.blpop("audio_queue")  # Kuyruktan ses al
    print(f"Mesaj tipi: {type(message)}, Uzunluk: {len(message)}")
    if len(message) % 4 != 0:
        raise ValueError(f"Geçersiz veri uzunluğu: {len(message)}. float32 için 4 byte'ın katı olmalı!")
    audio_data = np.frombuffer(message, dtype=np.float32)

    # Eğer veri gelmişse işleyelim
    if len(audio_data) > 0:
        result = model.transcribe(audio_data, language="en", task="transcribe", temperature=0.5)
        text = result["text"]
        print(f"📜 Transkript: {text}")

        # Çıktıyı FastAPI'ye göndermek için Redis'e yaz
        redis_conn.set("transcript_result", json.dumps({"text": text}))

    time.sleep(0.1)  # Küçük bir bekleme süresi ekleyelim