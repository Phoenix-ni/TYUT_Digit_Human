# Author: TYUT创新学社
# Date: 2025-10-4 19：44
# Description: 嵌入模型模块，用于将文本编码为向量
from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingModel:
    def __init__(self, model_path):
        self.model = SentenceTransformer(model_path)
    
    def encode(self, texts, convert_to_numpy=True):
        """编码文本为向量"""
        return self.model.encode(texts, convert_to_numpy=convert_to_numpy)
    
    def normalize(self, embeddings):
        """归一化向量"""
        return embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)