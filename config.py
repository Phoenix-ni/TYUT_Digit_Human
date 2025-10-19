# Author: TYUT创新学社
# Date: 2025-19-42
OPENAI_CLIENTS = {
    "client2": {
        "api_key": "***********************", # 请替换为你的大语言模型API Key 
        "base_url": "https://api.longcat.chat/openai"
    }
}

# TTS配置
TTS_CONFIG = {
    "api_key": "*******************************", # 请替换为你的TTS服务API Key
    "reference_id": "************************", # 请替换为你的TTS服务Reference ID
    "url": "https://fishspeech.net/api/open/tts"
}

# 模型配置
MODEL_CONFIG = {
    "whisper_model": "small",
    "embedding_model": "all-MiniLM-L6-v2",
    "knowledge_base_path": "/知识库.md" # 请替换为你的知识库文件路径
}

# 音频配置
AUDIO_CONFIG = {
    "rate": 16000,
    "chunk": 1024
}

# RAG配置
RAG_CONFIG = {
    "chunk_size": 200,
    "overlap": 50,
    "similarity_threshold": 0.75,
    "top_k": 3
}