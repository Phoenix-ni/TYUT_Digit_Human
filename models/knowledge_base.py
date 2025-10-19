# Description: 知识库
# Author: TYUT创新学社
# Date: 2025-10-4 19：44
import faiss
from .embedding_model import EmbeddingModel

class KnowledgeBase:
    def __init__(self, file_path, embedder, chunk_size=200, overlap=50):
        self.file_path = file_path
        self.embedder = embedder
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.chunks = []
        self.index = None
        self.load_knowledge_base()
    
    def load_and_chunk_kb(self):
        """加载知识库文件并进行分块处理"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                text = f.read()
            
            paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
            chunks = []
            for para in paragraphs:
                if para.startswith("#"):
                    continue
                    
                for i in range(0, len(para), self.chunk_size - self.overlap):
                    chunk = para[i:i + self.chunk_size]
                    if chunk:
                        chunks.append(chunk)
            return chunks
        except Exception as e:
            print(f"加载知识库文件时出错: {e}")
            return []
    
    def load_knowledge_base(self):
        """加载知识库并建立索引"""
        try:
            self.chunks = self.load_and_chunk_kb()
            if not self.chunks:
                print("知识库为空")
                return
            
            kb_embs = self.embedder.encode(self.chunks, convert_to_numpy=True)
            kb_embs = self.embedder.normalize(kb_embs)
            
            self.index = faiss.IndexFlatIP(kb_embs.shape[1])
            self.index.add(kb_embs)
            print("知识库加载成功!")
            
        except Exception as e:
            print(f"加载知识库时出错: {e}")
            self.chunks = []
            self.index = None
    
    def retrieve(self, query_text, k=3):
        """检索相关知识"""
        if self.index is None or len(self.chunks) == 0:
            return []
        
        try:
            q = self.embedder.encode([query_text], convert_to_numpy=True)
            q = self.embedder.normalize(q)
            D, I = self.index.search(q, k)
            results = []
            for sim, idx in zip(D[0], I[0]):
                results.append({
                    "chunk": self.chunks[idx],
                    "score": float(sim)
                })
            return results
        except Exception as e:
            print(f"检索知识库时出错: {e}")
            return []