from collections import deque

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