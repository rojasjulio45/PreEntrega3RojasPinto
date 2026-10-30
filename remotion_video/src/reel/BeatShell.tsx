import React from "react";
import { AbsoluteFill, Html5Audio, Sequence, interpolate, staticFile, useCurrentFrame } from "remotion";
import { BeatKey, LEAD, getBeatAudio } from "./script";
import { BeatBg, Captions, Sfx, enter } from "./kit";

// Every beat: animated background, a punch-in cut with a white flash and a
// whoosh, the illustration, word-by-word captions and (once generated) voice.
export const BeatShell: React.FC<{
  beat: BeatKey;
  bg: string;
  children: React.ReactNode;
  captionsY?: number;
  // false for the opening beat: frame 0 must already show the hook, never a flash.
  cut?: boolean;
}> = ({ beat, bg, children, captionsY, cut = true }) => {
  const frame = useCurrentFrame();
  const punch = cut ? 1 + 0.12 * (1 - enter(frame, 0, 300)) : 1;
  const flash = cut ? interpolate(frame, [0, 3], [0.7, 0], { extrapolateRight: "clamp" }) : 0;
  const audio = getBeatAudio(beat);
  return (
    <AbsoluteFill>
      <BeatBg color={bg} />
      <AbsoluteFill style={{ transform: `scale(${punch})` }}>{children}</AbsoluteFill>
      <Captions beat={beat} y={captionsY} />
      <AbsoluteFill style={{ background: "white", opacity: flash }} />
      {cut ? <Sfx name="whoosh" at={0} volume={0.35} /> : null}
      {audio ? (
        <Sequence from={LEAD} name="voz" layout="none">
          <Html5Audio src={staticFile(audio.file)} />
        </Sequence>
      ) : null}
    </AbsoluteFill>
  );
};
