document.addEventListener("DOMContentLoaded", () => {
    const topicInput = document.getElementById("topic");
    const ageSelect = document.getElementById("age-range");
    const voiceSelect = document.getElementById("voice");
    const rateSelect = document.getElementById("rate");
    const generateBtn = document.getElementById("generate-btn");
    const loading = document.getElementById("loading");
    const result = document.getElementById("result");
    const storyText = document.getElementById("story-text");
    const audioPlayer = document.getElementById("audio-player");
    const downloadBtn = document.getElementById("download-btn");
    const editBtn = document.getElementById("edit-btn");
    const regenerateTtsBtn = document.getElementById("regenerate-tts-btn");

    // Suggestion tags
    document.querySelectorAll(".suggestion-tag").forEach((tag) => {
        tag.addEventListener("click", () => {
            topicInput.value = tag.dataset.topic;
            topicInput.focus();
        });
    });

    // Generate story
    generateBtn.addEventListener("click", async () => {
        const topic = topicInput.value.trim();
        if (!topic) {
            alert("请输入故事题材");
            topicInput.focus();
            return;
        }

        generateBtn.disabled = true;
        loading.classList.remove("hidden");
        result.classList.add("hidden");

        try {
            const response = await fetch("/api/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    topic: topic,
                    age_range: ageSelect.value,
                    voice: voiceSelect.value,
                    rate: rateSelect.value,
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "生成失败");
            }

            storyText.textContent = data.story;
            audioPlayer.src = data.audio_url;
            downloadBtn.href = data.audio_url;

            result.classList.remove("hidden");
            result.scrollIntoView({ behavior: "smooth" });
        } catch (err) {
            alert(err.message);
        } finally {
            generateBtn.disabled = false;
            loading.classList.add("hidden");
        }
    });

    // Edit story toggle
    let isEditing = false;
    editBtn.addEventListener("click", () => {
        isEditing = !isEditing;
        storyText.contentEditable = isEditing ? "true" : "false";
        editBtn.textContent = isEditing ? "完成编辑" : "编辑故事";
        regenerateTtsBtn.classList.toggle("hidden", !isEditing && !storyText.dataset.edited);

        if (!isEditing && storyText.dataset.edited) {
            regenerateTtsBtn.classList.remove("hidden");
        }
        if (isEditing) {
            storyText.focus();
            storyText.dataset.edited = "true";
        }
    });

    // Regenerate TTS for edited story
    regenerateTtsBtn.addEventListener("click", async () => {
        const text = storyText.textContent.trim();
        if (!text) {
            alert("故事内容不能为空");
            return;
        }

        regenerateTtsBtn.disabled = true;
        regenerateTtsBtn.textContent = "生成中...";

        try {
            const response = await fetch("/api/tts", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    text: text,
                    voice: voiceSelect.value,
                    rate: rateSelect.value,
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "语音合成失败");
            }

            audioPlayer.src = data.audio_url;
            downloadBtn.href = data.audio_url;
        } catch (err) {
            alert(err.message);
        } finally {
            regenerateTtsBtn.disabled = false;
            regenerateTtsBtn.textContent = "重新生成语音";
        }
    });

    // Enter key to generate
    topicInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            generateBtn.click();
        }
    });
});
