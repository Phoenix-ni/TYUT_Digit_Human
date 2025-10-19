# Author: TYUT创新学社
# Date: 2025-19-42
OPENAI_CLIENTS = {
    "client2": {
        "api_key": "ak_10a9lj0jQ2xq33Y47c2CE3IV1Bm7g", 
        "base_url": "https://api.longcat.chat/openai"
    }
}

# TTS配置
TTS_CONFIG = {
    "api_key": "04ae05260c06dda9cc63e7175fe20902de568afe80e4392377d81113941b275a",
    "reference_id": "5bc7fb18-a5c4-469f-8473-4bf24dde5b96",
    "url": "https://fishspeech.net/api/open/tts"
}

# 模型配置
MODEL_CONFIG = {
    "whisper_model": "small",
    "embedding_model": "/home/zyb/.cache/huggingface/hub/models--sentence-transformers--all-MiniLM-L6-v2/snapshots/c9745ed1d9f207416be6d2e6f8de32d1f16199bf/",
    "knowledge_base_path": "/home/zyb/百度飞桨领航团/组织/TYUT_Digit/知识库.md"
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