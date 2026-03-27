# Project Scaffold

Templates for setting up a new Remotion project for the overlay video pipeline.

## package.json

```json
{
  "name": "video-overlay",
  "private": true,
  "scripts": {
    "start": "npx remotion studio src/index.ts",
    "build:v1": "npx remotion render src/index.ts FinalV1 out/final_v1.mp4 --codec h264 --crf 18",
    "build:v2": "npx remotion render src/index.ts FinalV2 out/final_v2.mp4 --codec h264 --crf 18",
    "build:v3": "npx remotion render src/index.ts FinalV3 out/final_v3.mp4 --codec h264 --crf 18",
    "build:all": "npm run build:v1 && npm run build:v2 && npm run build:v3"
  },
  "dependencies": {
    "remotion": "^4.0.0",
    "@remotion/cli": "^4.0.0",
    "@remotion/google-fonts": "^4.0.0",
    "@remotion/transitions": "^4.0.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0"
  },
  "devDependencies": {
    "@types/react": "^18.3.0",
    "typescript": "^5.7.0"
  }
}
```

## tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true,
    "outDir": "dist"
  },
  "include": ["src"]
}
```

## src/index.ts

```typescript
import { registerRoot } from "remotion";
import { RemotionRoot } from "./Root";

registerRoot(RemotionRoot);
```

## .claude/launch.json

For previewing in Remotion studio during development:

```json
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "remotion-studio",
      "runtimeExecutable": "npx",
      "runtimeArgs": ["remotion", "studio", "src/index.ts"],
      "port": 3000
    }
  ]
}
```

## Setup commands

After creating the project files:

```bash
cd overlay
npm install

# Copy video (not symlink!) into public/
mkdir -p public
cp /path/to/video.MOV public/raw.MOV
```
