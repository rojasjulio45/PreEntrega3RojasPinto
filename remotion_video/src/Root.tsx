import { Composition } from "remotion";
import { FPS, HEIGHT, WIDTH, getTotalDuration } from "./constants";
import { OLNVideo } from "./OLNVideo";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="OLNChile"
      component={OLNVideo}
      durationInFrames={getTotalDuration()}
      fps={FPS}
      width={WIDTH}
      height={HEIGHT}
    />
  );
};
