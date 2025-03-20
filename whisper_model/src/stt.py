import redis
import pickle
import whisper
import torch
import time

# Redis bağlantısı
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Whisper modelini yükleyin (GPU destekli)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")
model = whisper.load_model("large-v3-turbo", device=device)

# Redis'ten veriyi al ve transkribe et
def transcribe_from_redis():
    while True:
        serialized_data = redis_client.get("audio_buffer")
        if serialized_data:
            audio_data = pickle.loads(serialized_data)
            print("Ses verisi alındı, işleniyor...")
            result = model.transcribe(audio_data, language="en", task="transcribe", temperature=0.5)
            print("Metin Çıktısı:", result['text'])
        time.sleep(0.5)  # Her 500ms'de bir kontrol et

if __name__ == "__main__":
    transcribe_from_redis()