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


def generate_synthesis_audio(text: str) -> Optional[str]:
    """Genera l'audio per la sintesi critica usando ElevenLabs."""
    return _generate_elevenlabs_audio(text, prefix="synthesis")

def generate_title_audio(title: str) -> Optional[str]:
    """Genera l'audio per il titolo della mostra usando ElevenLabs."""
    return _generate_elevenlabs_audio(title, prefix="title")

def _generate_elevenlabs_audio(text: str, prefix: str = "audio") -> Optional[str]:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("ElevenLabs API Key non impostata!")
        return None
        
    # ID Voce (Intellettuale/Narratore)
    voice_id = "bcqm9BaLLWpCajP9LJI5"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "use_speaker_boost": True,
        }
    }
    
    # Filename basato su hash del testo per il caching
    text_hash = hashlib.md5(text.encode()).hexdigest()
    filename = f"{prefix}_{text_hash}.mp3"
    filepath = os.path.join("static", "audio", filename)
    
    if os.path.exists(filepath):
        return filename
        
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            # Guadagno audio (default ~18 dB per titoli, 6 per sintesi)
            gain_val = "18" if prefix == "title" else "6"
            try:
                gain = float(os.environ.get(f"ELEVENLABS_{prefix.upper()}_GAIN_DB", gain_val))
            except ValueError:
                gain = float(gain_val)
            _amplify_mp3_inplace(filepath, gain)
            
            return filename
        else:
            print(f"Errore ElevenLabs ({prefix}): {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Eccezione ElevenLabs ({prefix}): {e}")
        return None
