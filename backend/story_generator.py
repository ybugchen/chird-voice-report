"""Story generator module using OpenAI API to create children's stories."""

import os

from openai import OpenAI

SYSTEM_PROMPT = """你是一位专业的儿童故事作家，擅长为3-12岁的孩子创作有趣、富有教育意义的故事。
请根据用户提供的题材，创作一个适合儿童收听的语音读物故事。

要求：
1. 语言简洁生动，适合朗读
2. 故事有明确的开头、发展和结尾
3. 包含正面的价值观和教育意义
4. 使用儿童能理解的词汇和句子
5. 故事长度适中（约500-800字）
6. 可以包含对话，使故事更加生动
7. 不要包含任何暴力、恐怖或不适合儿童的内容"""


def generate_story(topic: str, age_range: str = "3-6") -> str:
    """Generate a children's story based on the given topic.

    Args:
        topic: The theme/subject for the story.
        age_range: Target age range (e.g., "3-6", "7-9", "10-12").

    Returns:
        The generated story text.
    """
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    user_prompt = f"请为{age_range}岁的孩子创作一个关于「{topic}」的儿童故事。"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.8,
        max_tokens=2000,
    )

    return response.choices[0].message.content
