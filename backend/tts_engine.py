"""Text-to-Speech engine using Edge TTS for generating children's audiobooks."""

import asyncio
import logging
import os
import uuid

import edge_tts

logger = logging.getLogger(__name__)

# Voice options suitable for children's stories
VOICE_OPTIONS = {
    "xiaoxiao": "zh-CN-XiaoxiaoNeural",       # 女声，温柔活泼
    "xiaoyi": "zh-CN-XiaoyiNeural",           # 女声，亲切自然
    "yunxi": "zh-CN-YunxiNeural",             # 男声，阳光少年
    "yunyang": "zh-CN-YunyangNeural",          # 男声，沉稳温和
    "xiaoxuan": "zh-CN-XiaoxuanNeural",        # 女声，甜美可爱
}

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")


async def _synthesize(text: str, voice: str, output_path: str, rate: str) -> str:
    """Internal async function to perform TTS synthesis."""
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_path)
    return output_path


def text_to_speech(
    text: str,
    voice_key: str = "",
    rate: str = "-10%",
) -> str:
    """Convert text to speech and save as MP3 file.

    Args:
        text: The story text to convert.
        voice_key: Key from VOICE_OPTIONS or a full voice name.
        rate: Speech rate adjustment (e.g., "-10%" for slower).

    Returns:
        Path to the generated MP3 file.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    default_voice = os.getenv("TTS_VOICE", "zh-CN-XiaoxiaoNeural")
    voice = VOICE_OPTIONS.get(voice_key, default_voice) if voice_key else default_voice

    filename = f"story_{uuid.uuid4().hex[:8]}.mp3"
    output_path = os.path.join(OUTPUT_DIR, filename)

    try:
        asyncio.run(_synthesize(text, voice, output_path, rate))
    except Exception as e:
        logger.error("Edge TTS synthesis failed: %s", e)
        raise RuntimeError(
            "语音合成失败，请检查网络连接。Edge TTS 需要访问微软服务器。"
        ) from e

    return output_path


def get_available_voices() -> dict:
    """Return available voice options."""
    return {
        key: {"name": value, "label": _voice_label(key)}
        for key, value in VOICE_OPTIONS.items()
    }


def _voice_label(key: str) -> str:
    labels = {
        "xiaoxiao": "晓晓 - 温柔活泼女声",
        "xiaoyi": "晓伊 - 亲切自然女声",
        "yunxi": "云希 - 阳光少年男声",
        "yunyang": "云扬 - 沉稳温和男声",
        "xiaoxuan": "晓萱 - 甜美可爱女声",
    }
    return labels.get(key, key)
