#!/usr/bin/env python3
"""
Transcribe a video or audio file into timestamped segments using OpenAI Whisper.

Usage:
    python transcribe.py <video_file> [model_size]

    model_size: tiny, base (default), small, medium, large
    Larger models are more accurate but slower.

Output:
    Creates <filename>_transcript.json with timestamped segments.

Requirements:
    pip install openai-whisper
"""

import sys
import json
import os


def transcribe(file_path: str, model_size: str = "base") -> dict:
    """Transcribe a video/audio file and return timestamped segments."""
    try:
        import whisper
    except ImportError:
        print("Error: openai-whisper is not installed.")
        print("Install it with: pip install openai-whisper")
        sys.exit(1)

    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    print(f"Loading Whisper model '{model_size}'...")
    model = whisper.load_model(model_size)

    print(f"Transcribing '{file_path}'...")
    result = model.transcribe(file_path)

    segments = []
    for seg in result["segments"]:
        segments.append({
            "start": round(seg["start"], 1),
            "end": round(seg["end"], 1),
            "text": seg["text"].strip(),
        })

    return {
        "text": result["text"].strip(),
        "segments": segments,
        "duration": round(segments[-1]["end"], 1) if segments else 0,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <video_file> [model_size]")
        print("  model_size: tiny, base (default), small, medium, large")
        sys.exit(1)

    file_path = sys.argv[1]
    model_size = sys.argv[2] if len(sys.argv) > 2 else "base"

    result = transcribe(file_path, model_size)

    # Write output
    base_name = os.path.splitext(file_path)[0]
    output_path = f"{base_name}_transcript.json"

    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\nTranscript saved to: {output_path}")
    print(f"Duration: {result['duration']}s")
    print(f"Segments: {len(result['segments'])}")
    print(f"\nFull text:\n{result['text'][:500]}{'...' if len(result['text']) > 500 else ''}")


if __name__ == "__main__":
    main()
