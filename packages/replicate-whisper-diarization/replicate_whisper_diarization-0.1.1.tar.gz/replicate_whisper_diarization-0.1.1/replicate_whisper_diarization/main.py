from replicate_whisper_diarization.whisper import transcribe
from replicate_whisper_diarization.diarization import run_diarization


def extract_word_timestamps(segments: list[dict]) -> list[dict]:
    word_timestamps = []

    for segment in segments:
        for word in segment["words"]:
            word_timestamps.append(word.update({"text": word["word"]}) or word)
    return word_timestamps


def run_transcript_with_diarization(
    audio_url: str, whisper_model: str = "base"
) -> list[dict]:
    transcript = transcribe(audio_url=audio_url, model=whisper_model)
    segments = transcript["segments"]
    language = transcript["detected_language"]
    word_timestamps = extract_word_timestamps(segments)
    return run_diarization(audio_url, word_timestamps, language)
