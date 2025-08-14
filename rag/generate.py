import os
import openai
from typing import List, Tuple
from dotenv import load_dotenv

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_KEY:
    openai.api_key = OPENAI_KEY

def format_timestamp(seconds: float) -> str:
    s = int(seconds)
    h, m, s = s // 3600, (s % 3600) // 60, s % 60
    if h > 0:
        return f"{h:d}:{m:02d}:{s:02d}"
    return f"{m:d}:{s:02d}"

def extractive_answer(hits: List[Tuple[str, str, dict]], max_chunks: int = 3) -> str:
    # hits: list of tuples (_id, doc, meta)
    chosen = hits[:max_chunks]
    lines = []
    for _id, doc, meta in chosen:
        ts = f"{format_timestamp(meta['start'])}–{format_timestamp(meta['end'])}"
        ep = meta.get("episode_id", "episode")
        # limit doc length for UI
        snippet = doc.strip()
        lines.append(f"- **{ep}** [{ts}]: {snippet}")
    return "\n".join(lines)

def build_context_for_llm(hits: List[Tuple[str, str, dict]], max_chars: int = 3000) -> str:
    """
    Turn top hits into a context block for the LLM with timestamps and episode IDs.
    Truncate if needed to respect token limits.
    """
    ctx_parts = []
    current_len = 0
    for _id, doc, meta in hits:
        part = f"[{meta.get('episode_id','ep')}] {format_timestamp(meta['start'])}-{format_timestamp(meta['end'])}: {doc.strip()}"
        if current_len + len(part) > max_chars:
            break
        ctx_parts.append(part)
        current_len += len(part)
    return "\n\n".join(ctx_parts)

def abstractive_answer(
    query: str,
    hits: List[Tuple[str, str, dict]],
    model: str = "gpt-4o-mini",
    max_tokens: int = 256,
    temperature: float = 0.2
) -> str:
    """
    Create an abstractive answer using OpenAI chat completion. The reply will include short summary,
    and explicit citations to chunks with episode and timestamps.
    """
    if not OPENAI_KEY:
        return "Abstractive mode requires OPENAI_API_KEY to be set. Set it in .env or environment."

    context = build_context_for_llm(hits, max_chars=4000)
    system = (
        "You are an assistant that answers queries about podcast transcripts. "
        "Use the provided context (transcript snippets with episode IDs and timestamps) to produce a concise answer. "
        "Always include short citations in the form (episode_id HH:MM:SS) or (episode_id M:SS) when you reference specific facts. "
        "If context doesn't contain the answer, say you couldn't find it in the audio and suggest related topics from the context."
    )
    user_prompt = (
        f"Query: {query}\n\n"
        "Context:\n"
        f"{context}\n\n"
        "Instructions: Answer concisely (2-5 sentences). When you mention a fact from the context, append a citation with episode id and timestamp, e.g. (episode1 0:12)."
    )

    try:
        # ChatCompletion or Chat API usage
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        ans = resp["choices"][0]["message"]["content"].strip()
        return ans
    except Exception as e:
        return f"[LLM error] {e}"
