import logging

from openai import AsyncOpenAI
from typing import Dict, Optional

from decouple import config


logger = logging.getLogger(__name__)


client = AsyncOpenAI(
    base_url='https://openrouter.ai/api/v1',
    api_key=config('DEEPSEEK_API_KEY'),  
)

async def ai_generate(text: str, model: str = 'deepseek/deepseek-r1-distill-llama-70b') -> Optional[Dict]:

    try:
        completion = await client.chat.completions.create(
            model=model,
            messages=[{'role': 'user', 'content': text}],
            temperature=0.7,  # Параметр для креативности
            max_tokens=2000   # Максимальное количество токенов
        )
        
        return {
            'response': completion.choices[0].message.content,
            'usage': completion.usage.total_tokens
        }
        
    except Exception as e:
        logger.error(f"DeepSeek API error: {e}", exc_info=True)
        return None