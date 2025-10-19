# Description: 语音合成服务
# Author: TYUT创新学社
# Date: 2025-10-4 19：44
import requests
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))
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
if __name__ == "__main__":
    tts_service = TTSService()
    audio_data = tts_service.text_to_speech("太原理工大学创新学社开始招新啦！想和一群爱动手、爱钻研的同学一起参与有价值的科研与开发项目，并把学习成果真正落地？参与丰富的竞赛吗?来这里就对了！我们提供真实的项目实践、系统的成长路径和丰富的学习资源，帮你把兴趣化为实力，将想法真正落地！在这里你能够参与丰富的竞赛，与志同道合的同学一起提升自己。", speed=1)
    if audio_data:
        with open("output.mp3", "wb") as f:
            f.write(audio_data)
        print("语音已保存为 output.mp3")