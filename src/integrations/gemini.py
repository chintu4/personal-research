"""Gemini integration helpers (supports new and legacy SDKs).

Tries the new SDK (`from google import genai`, `Client`) first, then falls back to
legacy (`import google.generativeai as genai`, `configure` + `GenerativeModel`).
"""
from typing import List, Tuple, Any
import os


def _get_key() -> str:
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("GEMINI_API_KEY not set.")
    return key


def have_gemini() -> bool:
    key_ok = bool(os.getenv("GEMINI_API_KEY"))
    if not key_ok:
        return False
    try:
        # Prefer new API
        from google import genai as _new  # type: ignore
        _ = getattr(_new, "Client", None)
        if _ is not None:
            return True
    except Exception:
        pass
    try:
        # Fallback legacy API
        import google.generativeai as _legacy  # type: ignore
        # If import works, assume usable
        return True
    except Exception:
        return False


def _get_backend():
    """Return (backend, module) where backend is 'new' or 'legacy'."""
    try:
        from google import genai as _new  # type: ignore
        if getattr(_new, "Client", None) is not None:
            return "new", _new
    except Exception:
        pass
    import google.generativeai as _legacy  # type: ignore
    return "legacy", _legacy


def _clamp_join(texts: List[str], max_chars: int = 60000) -> str:
    buf, total = [], 0
    for t in texts:
        if not t:
            continue
        t = t.strip()
        if total + len(t) + 1 > max_chars:
            remaining = max_chars - total
            if remaining > 0:
                buf.append(t[:remaining])
                total += remaining
            break
        buf.append(t)
        total += len(t) + 1
    return "\n\n".join(buf)


def _resp_text(resp: Any) -> str:
    # Try .text first (new SDK convenience property)
    try:
        t = getattr(resp, "text", None)
        if t:
            return str(t)
    except Exception:
        pass
    # Fallback to candidates -> content.parts[].text
    try:
        candidates = getattr(resp, "candidates", None)
        if candidates:
            parts = getattr(candidates[0], "content", None)
            parts = getattr(parts, "parts", []) if parts else []
            texts = []
            for p in parts:
                pt = getattr(p, "text", None)
                if pt:
                    texts.append(str(pt))
            if texts:
                return "\n".join(texts)
    except Exception:
        pass
    # Last resort
    try:
        return str(resp)
    except Exception:
        return ""


def gemini_summarize(texts: List[str], model_name: str = "gemini-1.5-flash", max_chars: int = 60000) -> str:
    backend, mod = _get_backend()
    content = _clamp_join(texts, max_chars=max_chars)
    prompt = (
        "You are a helpful research assistant. Summarize the following documents "
        "into a clear, concise abstract with bullet points for key contributions."
    )
    if backend == "new":
        Client = getattr(mod, "Client")  # type: ignore
        client = Client(api_key=_get_key())
        resp = client.models.generate_content(model=model_name, contents=f"{prompt}\n\n{content}")
    else:
        configure = getattr(mod, "configure")  # type: ignore
        GenerativeModel = getattr(mod, "GenerativeModel")  # type: ignore
        configure(api_key=_get_key())
        model = GenerativeModel(model_name)
        resp = model.generate_content(f"{prompt}\n\n{content}")
    return _resp_text(resp)


def gemini_answer(
    question: str,
    texts: List[str],
    model_name: str = "gemini-1.5-flash",
    max_chars: int = 60000,
) -> Tuple[str, float]:
    backend, mod = _get_backend()
    content = _clamp_join(texts, max_chars=max_chars)
    prompt = (
        "Answer the question based strictly on the provided documents. "
        "If unknown, say you don't know. Provide a brief, direct answer."
    )
    if backend == "new":
        Client = getattr(mod, "Client")  # type: ignore
        client = Client(api_key=_get_key())
        resp = client.models.generate_content(
            model=model_name,
            contents=f"{prompt}\n\nQUESTION: {question}\n\nDOCUMENTS:\n{content}",
        )
    else:
        configure = getattr(mod, "configure")  # type: ignore
        GenerativeModel = getattr(mod, "GenerativeModel")  # type: ignore
        configure(api_key=_get_key())
        model = GenerativeModel(model_name)
        resp = model.generate_content(
            f"{prompt}\n\nQUESTION: {question}\n\nDOCUMENTS:\n{content}"
        )
    answer = _resp_text(resp).strip()
    return answer, (1.0 if answer else 0.0)
