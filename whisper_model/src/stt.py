import redis
import pickle
import whisper
import torch
import time

# Redis bağlantısı
redis_host = "192.168.1.102"
# redis_client = redis.Redis(host=redis_host, port=6379, db=0)
redis_client = redis.Redis(host=redis_host, port=6379, decode_responses=False)

# Whisper modelini yükleyin (GPU destekli)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")
model = whisper.load_model("large-v3-turbo", device=device)

# Redis'ten veriyi al ve transkribe et
def transcribe_from_redis():
    while True:
        redis_message = redis_client.rpop("reading")
        if redis_message:
            data = pickle.loads(redis_message)
            audio_data = data["audio_data"]
            print("Message:", data["message"])
            result = model.transcribe(audio_data, language="en", task="transcribe", temperature=0.5, initial_prompt=data["message"])
            print("Model result:", result['text'])
        else:
            time.sleep(0.1)

if __name__ == "__main__":
    transcribe_from_redis()