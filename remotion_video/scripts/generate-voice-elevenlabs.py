"""Narration for the reel with ElevenLabs v3 (voice "Jessica", playful/bright).

Each beat has a performance version of its NARRATION text: same words, plus
v3 audio tags and punctuation that drive the delivery. The API key is added
to requests by the environment's network secret (header xi-api-key), so this
script never reads it. Writes public/reel/narration/<beat>.mp3 and
src/reel/audio-manifest.json.

Usage: python3 scripts/generate-voice-elevenlabs.py [--stability 0.0]
"""

import argparse
import json
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOICE = "cgSgspJ2msm6clMCkdW9"  # Jessica
PERFORMANCE = {
    "hookLinkedIn": "[excited] ¡Hasta 300 casos por cada profesional! [curious] Así trabaja la oficina que protege a los niños de... ¡tu comuna!",
    "hookInstagram": "[curious] Si un niño de tu comuna está en riesgo... ¿esta oficina? [excited] ¡Debe actuar primero! Se llama... ¡o-ele-ene!",
    "ley": "[excited] Nacieron con la Ley veintiún mil cuatrocientos treinta, de 2022, [playfully] ¡y reemplazan a las antiguas o-pe-de!",
    "mision": "[confident] Su misión: ¡promover derechos, prevenir... y proteger!",
    "puertas": "[curious] Un caso llega por... ¡tres puertas! [excited] La familia, una alerta del colegio o del consultorio... ¡o un tribunal!",
    "proceso": "[warm] Un gestor de casos evalúa, arma un plan con la familia... [excited] ¡y la conecta con el consultorio, el colegio y apoyo social!",
    "grave": "[serious] ¿Si es grave? Deriva a Protección Especializada... o al tribunal de familia.",
    "reto": "[determined] El reto: ¡cubrir las 346 comunas a más tardar en 2027! [sighs] Con gestores que en algunas comunas cargan... ¡300 casos!",
    "ctaLinkedIn": "[curious] ¿En tu comuna ya funciona la o-ele-ene? [cheerful] ¡Te leo en comentarios!",
    "ctaInstagram": "[excited] ¡Guárdalo! [warm] Y compártelo con alguien que trabaje con niños.",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stability", type=float, default=0.0, help="v3: 0.0 creative, 0.5 natural, 1.0 robust")
    parser.add_argument("--tempo", type=float, default=1.2, help="speed-up without pitch change, keeps the reel under 60 s")
    args = parser.parse_args()
    out_dir = ROOT / "public/reel/narration"
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for key, text in PERFORMANCE.items():
        body = json.dumps({
            "text": text,
            "model_id": "eleven_v3",
            "language_code": "es",
            "voice_settings": {"stability": args.stability},
        }).encode()
        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128",
            data=body, headers={"Content-Type": "application/json"}, method="POST",
        )
        raw = urllib.request.urlopen(req, timeout=120).read()
        mp3 = out_dir / f"{key}.mp3"
        # Trim edge silence and even out loudness so beats cut tightly.
        subprocess.run(
            ["ffmpeg", "-loglevel", "error", "-y", "-i", "-", "-af",
             f"silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,atempo={args.tempo},loudnorm=I=-16:TP=-1.5",
             "-ar", "44100", "-b:a", "128k", str(mp3)],
            input=raw, check=True,
        )
        duration = float(subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)],
            capture_output=True, text=True, check=True).stdout)
        manifest[key] = {"file": f"reel/narration/{key}.mp3", "durationInSeconds": round(duration, 3)}
        print(f"🎙  {key}: {duration:.2f} s")
    (ROOT / "src/reel/audio-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
