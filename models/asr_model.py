# Description: 语音识别模型
# Author: TYUT创新学社
# Date: 2025-10-4 19：44
import whisper
from opencc import OpenCC
import re

class ASRModel:
    def __init__(self, model_name="small"):
        self.model = whisper.load_model(model_name)
        self.cc = OpenCC('t2s')
        
    def correct_mixed_language_errors(self, text):
        """修正中英文混合识别的常见错误"""
        correction_rules = {
            r'爱人': 'i人',
            r'意人': 'e人', 
            r'爱人不爱社交': 'i人不爱社交',
            r'意人爱社交': 'e人爱社交',
            r'm比特': 'MBTI',
            r'm b t i': 'MBTI',
            r'十六型': '16型',
            r'十六型人格': '16型人格',
            r'm b t': 'MBT',
            r'爱意': 'IE',
            r'爱意人': 'IE人',
        }
        
        for wrong, correct in correction_rules.items():
            text = re.sub(wrong, correct, text, flags=re.IGNORECASE)
        
        return text
    
    def transcribe(self, audio_data):
        """转录音频数据为文本"""
        print("🔄 正在转写录音...")
        
        try:
            result = self.model.transcribe(
                audio_data,
                language=None,
                task="transcribe", 
                temperature=0.0,
                best_of=3,
                beam_size=3
            )
            
            text = result["text"]
            print(f"原始识别结果: {text}")
            
            if text and isinstance(text, str):
                simplified_text = self.cc.convert(text)
                print(f"简体中文转换结果: {simplified_text}")
                
                corrected_text = self.correct_mixed_language_errors(simplified_text)
                print(f"修正后结果: {corrected_text}")
                return corrected_text
            
            return text
            
        except Exception as e:
            print(f"语音识别出错: {e}")
            return "语音识别失败，请重试"