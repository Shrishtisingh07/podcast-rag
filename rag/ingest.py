import json
import math
import pathlib
from typing import List, Dict
from tqdm import tqdm
from rich import print as rprint

# We use faster-whisper for speed; fall back to whisper if needed.
def transcribe_file(audio_path: str, model_size: str = "base") -> Dict:
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel(model_size)
        segments, info = model.transcribe(audio_path, word_timestamps=False)
        segs = []
        for seg in segments:
            segs.append({"start": float(seg.start), "end": float(seg.end), "text": seg.text})
        return {"segments": segs}
    except Exception as e:
        rprint(f"[yellow]faster-whisper failed ({e}). Falling back to whisper...[/yellow]")
        import whisper
        model = whisper.load_model(model_size)
        result = model.transcribe(audio_path, word_timestamps=False)
        # normalize to same structure
        segs = []
        for seg in result.get("segments", []):
            segs.append({"start": float(seg["start"]), "end": float(seg["end"]), "text": seg["text"]})
        return {"segments": segs}

def build_chunks_from_segments(
    segments: List[Dict],
    max_chars: int = 1200,
    overlap_chars: int = 200
) -> List[Dict]:
    chunks = []
    buf = ""
    buf_start = None
    last_end = None

    for seg in segments:
        text = seg["text"].strip()
        start, end = float(seg["start"]), float(seg["end"])
        if not text:
            continue
        if buf == "":
            buf_start = start
        if len(buf) + len(text) + 1 <= max_chars:
            buf = (buf + " " + text).strip()
            last_end = end
        else:
            if buf:
                chunks.append({"text": buf, "start": buf_start, "end": last_end})
            tail = buf[-overlap_chars:] if len(buf) > overlap_chars else buf
            buf = (tail + " " + text).strip()
            buf_start = max(buf_start if buf_start is not None else start, start)
            last_end = end

    if buf:
        chunks.append({"text": buf, "start": buf_start, "end": last_end})
    return chunks

def ingest_directory(
    input_dir: str = "data/raw",
    transcripts_dir: str = "data/transcripts",
    index_after: bool = True,
    collection_name: str = "podcasts",
    persist_dir: str = "vectorstore",
    model_size: str = "base"
):
    from .index import build_index
    input_p = pathlib.Path(input_dir)
    transcripts_p = pathlib.Path(transcripts_dir)
    transcripts_p.mkdir(parents=True, exist_ok=True)

    all_chunks = []

    audio_files = sorted(list(input_p.glob("*.mp3")) + list(input_p.glob("*.wav")) + list(input_p.glob("*.m4a")))
    if not audio_files:
        rprint("[red]No audio files found in data/raw/. Add .mp3/.wav and try again.[/red]")
        return

    for audio in tqdm(audio_files, desc="Transcribing"):
        episode_id = audio.stem
        out_json = transcripts_p / f"{episode_id}.json"

        rprint(f"[cyan]Transcribing {audio.name}...[/cyan]")
        result = transcribe_file(str(audio), model_size=model_size)
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        # chunk
        segments = result.get("segments", [])
        chunks = build_chunks_from_segments(segments, max_chars=1200, overlap_chars=200)

        # attach metadata
        for ch in chunks:
            ch["episode_id"] = episode_id

        all_chunks.extend(chunks)

    rprint(f"[green]Built {len(all_chunks)} chunks from {len(audio_files)} files.[/green]")

    if index_after and all_chunks:
        rprint("[cyan]Indexing into Chroma...[/cyan]")
        build_index(all_chunks, collection_name=collection_name, persist_dir=persist_dir)
        rprint("[green]Index built successfully.[/green]")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Ingest audio → transcripts → chunks → index")
    parser.add_argument("--input", default="data/raw", help="Folder with audio files")
    parser.add_argument("--transcripts", default="data/transcripts", help="Where to store JSON transcripts")
    parser.add_argument("--no-index", action="store_true", help="Skip indexing into Chroma")
    parser.add_argument("--model", default="base", help="Whisper model size (tiny, base, small, medium, large-v3)")
    parser.add_argument("--collection", default="podcasts", help="Chroma collection name")
    parser.add_argument("--persist", default="vectorstore", help="Chroma persist directory")
    args = parser.parse_args()

    ingest_directory(
        input_dir=args.input,
        transcripts_dir=args.transcripts,
        index_after=not args.no_index,
        collection_name=args.collection,
        persist_dir=args.persist,
        model_size=args.model,
    )
