# Description: 音频播放服务
# Author: TYUT创新学社
# Date: 2025-10-4 19：44
import pygame
import tempfile
import os
import time

class AudioService:
    def __init__(self):
        pygame.mixer.init()
    
    def play_audio(self, audio_data):
        """播放音频数据"""
        try:
            # 创建临时文件保存音频
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            # 加载并播放音频
            pygame.mixer.music.load(temp_file_path)
            pygame.mixer.music.play()
            
            # 等待播放完成
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
            # 删除临时文件
            os.unlink(temp_file_path)
            print("✅ 音频播放完成")
            
        except Exception as e:
            print(f"❌ 音频播放出错: {e}")