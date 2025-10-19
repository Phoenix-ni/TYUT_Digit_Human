# Description: 语音合成服务
# Author: TYUT创新学社
# Date: 2025-10-4 19：44
import requests
from config import TTS_CONFIG

class TTSService:
    def __init__(self):
        self.api_key = TTS_CONFIG["api_key"]
        self.reference_id = TTS_CONFIG["reference_id"]
        self.url = TTS_CONFIG["url"]
    
    def text_to_speech(self, text, speed=1.0):
        """将文本转换为语音"""
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            data = {
                "reference_id": self.reference_id,
                "text": text,
                "speed": speed,
                "volume": 0,
                "version": "s1",
                "format": "mp3",
                "cache": False
            }

            response = requests.post(self.url, headers=headers, json=data)

            if response.status_code == 200:
                print("✅ 语音生成成功")
                return response.content
            else:
                print(f"❌ TTS API出错: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            print(f"❌ TTS转换出错: {e}")
            return None