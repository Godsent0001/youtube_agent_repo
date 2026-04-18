import re


# =========================
# CLEAN LLM OUTPUT
# =========================
def clean_llm_text(text: str):
    """
    Removes unwanted formatting artifacts from LLM output
    """

    if not text:
        return ""

    text = text.strip()

    # remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    # remove markdown artifacts
    text = text.replace("```", "")
    text = text.replace("**", "")

    return text.strip()


# =========================
# SPLIT INTO SCENES
# =========================
def split_into_scenes(script: str):
    """
    Converts script into structured scenes
    """

    if not script:
        return []

    # split by sentence groups
    sentences = re.split(r"(?<=[.!?]) +", script)

    scenes = []

    for i, sentence in enumerate(sentences):
        scenes.append({
            "scene_id": i,
            "text": sentence.strip()
        })

    return scenes


# =========================
# GENERATE TITLE (YOUTUBE STYLE)
# =========================
def extract_hook(title: str):
    """
    Extracts attention hook from script or topic
    """

    words = title.split()

    if len(words) <= 6:
        return title

    return " ".join(words[:6]) + "..."


# =========================
# FORMAT SUBTITLES
# =========================
def format_subtitles(script: str):
    """
    Converts script into subtitle chunks
    """

    sentences = split_into_scenes(script)

    subtitles = []

    for item in sentences:
        subtitles.append({
            "text": item["text"],
            "start": item["scene_id"] * 3,
            "end": (item["scene_id"] + 1) * 3
        })

    return subtitles


# =========================
# REMOVE EXTRA WHITESPACE
# =========================
def normalize_text(text: str):
    return re.sub(r"\s+", " ", text).strip()