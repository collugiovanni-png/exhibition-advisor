import os
import requests
import hashlib
import shutil
import subprocess
import tempfile
from typing import Optional

def _amplify_mp3_inplace(filepath: str, gain_db: float) -> None:
    """Alza il livello del file MP3 con ffmpeg (se installato). gain_db=0 non fa nulla."""
    if gain_db == 0:
        return
    if not shutil.which("ffmpeg"):
        print(
            "ffmpeg non trovato: installalo (es. brew install ffmpeg) per applicare "
            "ELEVENLABS_TITLE_GAIN_DB, oppure lascia il gain a 0."
        )
        return
    fd, tmp_path = tempfile.mkstemp(suffix=".mp3")
    os.close(fd)
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                filepath,
                "-af",
                f"volume={gain_db}dB",
                "-c:a",
                "libmp3lame",
                "-b:a",
                "192k",
                tmp_path,
            ],
            check=True,
            capture_output=True,
        )
        os.replace(tmp_path, filepath)
    except (subprocess.CalledProcessError, OSError) as e:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        print(f"Amplificazione ffmpeg fallita, uso audio ElevenLabs grezzo: {e}")


def generate_title_audio(title: str) -> Optional[str]:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("ElevenLabs API Key non impostata!")
        return None
        
    voice_id = "bcqm9BaLLWpCajP9LJI5"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    data = {
        "text": title,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            # Può aumentare un po' chiarezza/presenza rispetto al raw output
            "use_speaker_boost": True,
        }
    }
    
    # Generate a safe filename based on a hash of the title
    title_hash = hashlib.md5(title.encode()).hexdigest()
    filename = f"title_{title_hash}.mp3"
    filepath = os.path.join("static", "audio", filename)
    
    # If it already exists, don't regenerate to save ElevenLabs credits
    if os.path.exists(filepath):
        return filename
        
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            # Guadagno in dB dopo il download (default ~9 dB). 0 = disattivato.
            # Esporta ELEVENLABS_TITLE_GAIN_DB=12 per più volume, o 0 per file grezzi.
            try:
                gain = float(os.environ.get("ELEVENLABS_TITLE_GAIN_DB", "9"))
            except ValueError:
                gain = 9.0
            _amplify_mp3_inplace(filepath, gain)
            return filename
        else:
            print(f"Errore ElevenLabs: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Eccezione durante la chiamata a ElevenLabs: {e}")
        return None
