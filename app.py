"""Flask application for the Children's Audiobook Generator."""

import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, send_file

from backend.tts_engine import get_available_voices, text_to_speech

load_dotenv()

DEMO_MODE = not os.getenv("OPENAI_API_KEY")

if DEMO_MODE:
    from backend.preset_stories import find_matching_story
else:
    from backend.story_generator import generate_story

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static",
)

AGE_RANGES = [
    {"value": "3-6", "label": "3-6岁（幼儿）"},
    {"value": "7-9", "label": "7-9岁（小学低年级）"},
    {"value": "10-12", "label": "10-12岁（小学高年级）"},
]

TOPIC_SUGGESTIONS = [
    "小兔子的冒险", "勇敢的小狮子", "友谊的魔法",
    "会飞的小象", "海底世界探险", "森林音乐会",
    "小星星的愿望", "恐龙乐园", "太空旅行",
    "善良的小精灵", "彩虹桥的故事", "小熊学分享",
]


@app.route("/")
def index():
    """Render the main page."""
    voices = get_available_voices()
    return render_template(
        "index.html",
        voices=voices,
        age_ranges=AGE_RANGES,
        suggestions=TOPIC_SUGGESTIONS,
        demo_mode=DEMO_MODE,
    )


@app.route("/api/generate", methods=["POST"])
def api_generate():
    """Generate a story and convert it to audio."""
    data = request.get_json()
    topic = data.get("topic", "").strip()
    age_range = data.get("age_range", "3-6")
    voice = data.get("voice", "")
    rate = data.get("rate", "-10%")

    if not topic:
        return jsonify({"error": "请输入故事题材"}), 400

    try:
        if DEMO_MODE:
            matched = find_matching_story(topic, age_range)
            story_text = matched["text"]
        else:
            story_text = generate_story(topic, age_range)

        audio_path = text_to_speech(story_text, voice_key=voice, rate=rate)
        audio_filename = os.path.basename(audio_path)

        return jsonify({
            "story": story_text,
            "audio_url": f"/audio/{audio_filename}",
            "demo_mode": DEMO_MODE,
        })
    except Exception as e:
        return jsonify({"error": f"生成失败: {str(e)}"}), 500


@app.route("/api/tts", methods=["POST"])
def api_tts():
    """Convert provided text to audio (for edited stories)."""
    data = request.get_json()
    text = data.get("text", "").strip()
    voice = data.get("voice", "")
    rate = data.get("rate", "-10%")

    if not text:
        return jsonify({"error": "请输入文本内容"}), 400

    try:
        audio_path = text_to_speech(text, voice_key=voice, rate=rate)
        audio_filename = os.path.basename(audio_path)
        return jsonify({"audio_url": f"/audio/{audio_filename}"})
    except Exception as e:
        return jsonify({"error": f"语音合成失败: {str(e)}"}), 500


@app.route("/audio/<filename>")
def serve_audio(filename):
    """Serve generated audio files."""
    audio_dir = os.path.join(os.path.dirname(__file__), "output")
    filepath = os.path.join(audio_dir, filename)
    if not os.path.isfile(filepath):
        return jsonify({"error": "音频文件不存在"}), 404
    return send_file(filepath, mimetype="audio/mpeg")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
