# ¿Cómo funcionan las OLN en Chile? — video Remotion

Video explicativo animado de unos 3 minutos sobre las **Oficinas Locales de la Niñez** (Ley 21.430). Está hecho con código, en estilo Kurzgesagt: ilustraciones SVG planas, colores saturados, fondo nocturno y animaciones sincronizadas con la narración.

## Estructura

| Archivo | Qué contiene |
|---|---|
| `script.md` | Guion completo, notas de ritmo y fuentes |
| `src/constants.ts` | Texto narrado (`NARRATION`), paleta y cálculo de tiempos |
| `src/scenes/*.tsx` | Las 10 escenas (intro → cierre) |
| `src/components/` | Fondo, subtítulos, personajes, edificios e íconos SVG |
| `src/audio-manifest.json` | Duraciones reales de la voz (vacío = tiempos estimados) |
| `scripts/generate-tts.mjs` | Genera la voz y actualiza el manifiesto |

## Uso

```bash
npm i
npm run dev      # Remotion Studio: vista previa interactiva
npm run tts      # (opcional) genera la voz con edge-tts
npm run render   # exporta out/oln-chile.mp4
```

### Voz

`npm run tts` necesita `pip install edge-tts` y ffmpeg. Usa por defecto la voz chilena `es-CL-CatalinaNeural`; para la masculina, ejecuta `npm run tts -- --voice es-CL-LorenzoNeural`.

El script mide cada audio y los subtítulos y las animaciones se ajustan solos. Las animaciones usan `cue()` para aparecer cuando la narración dice la palabra que les corresponde.

Mientras `src/audio-manifest.json` esté vacío (`{}`), el video sale sin voz y con tiempos estimados según la longitud del texto.

### Cambiar el guion

Edita `NARRATION` en `src/constants.ts`. Si borras una frase que alguna escena usa como `cue("escena", "fragmento")`, TypeScript no lo detecta, pero la vista previa muestra el error con el fragmento que falta.
