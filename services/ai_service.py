# Description: AI服务类，用于调用大语言模型API
# Author: TYUT创新学社
# Date: 2025-10-4 19：44
from openai import OpenAI
from config import OPENAI_CLIENTS

class AIService:
    def __init__(self):
        self.clients = {
            "client2": OpenAI(**OPENAI_CLIENTS["client2"])
        }
    
    def get_client(self, model_name="LongCat-Flash-Chat"):
        if model_name == "LongCat-Flash-Chat":
            return self.clients["client2"]
        else:
            # 默认返回client2
            return self.clients["client2"]
    
    def call_api(self, messages, model_name, stream=False):
        """调用API模型"""
        try:
            client = self.get_client(model_name)
            print(f"调用API，模型: {model_name}, 消息长度: {len(messages)}")
            
            if stream:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    stream=True
                )
                return response
            else:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    stream=False
                )
                result = response.choices[0].message.content
                print(f"API响应: {result}")
                return result
        except Exception as e:
            print(f"调用API模型时出错: {e}")
            # 返回错误信息而不是抛出异常
            return f"抱歉，AI服务暂时不可用: {str(e)}"