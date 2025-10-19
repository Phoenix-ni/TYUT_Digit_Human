# Description: 主程序
# Author: TYUT创新学社
# Date: 2025-10-4 19：44
from flask import Flask, request, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import numpy as np
import threading
import traceback
from config import MODEL_CONFIG, RAG_CONFIG
from models.asr_model import ASRModel
from models.embedding_model import EmbeddingModel
from models.knowledge_base import KnowledgeBase
from services.ai_service import AIService
from services.tts_service import TTSService
from services.audio_service import AudioService
from utils.text_utils import create_rag_prompt, format_retrieved_context

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# 初始化服务
asr_service = ASRModel(MODEL_CONFIG["whisper_model"])
embedder = EmbeddingModel(MODEL_CONFIG["embedding_model"])
knowledge_base = KnowledgeBase(
    MODEL_CONFIG["knowledge_base_path"], 
    embedder,
    RAG_CONFIG["chunk_size"],
    RAG_CONFIG["overlap"]
)
ai_service = AIService()
tts_service = TTSService()
audio_service = AudioService()

# 全局状态管理
audio_buffers = {}
abort_flags = {}
client_models = {}

@app.route('/')
def index():
    return render_template('index.html')

def transcribe_audio(audio_data):
    """转录音频数据为文本"""
    return asr_service.transcribe(audio_data)

def retrieve_kb(user_text, k=3):
    """向量检索知识库"""
    return knowledge_base.retrieve(user_text, k)

def answer_by_rag(user_text, model_name="LongCat-Flash-Chat", threshold=0.75):
    """基于RAG的回答逻辑"""
    print(f"RAG处理开始，用户文本: {user_text}")
    
    retrieved = retrieve_kb(user_text, RAG_CONFIG["top_k"])
    print(f"检索到 {len(retrieved)} 条相关知识")
    
    if not retrieved:
        print("未检索到相关知识，使用直接问答")
        try:
            messages = [
                {"role": "system", "content": "你是一个智能助手"},
                {"role": "user", "content": user_text}
            ]
            response = ai_service.call_api(messages, model_name, stream=False)
            print(f"直接问答结果: {response}")
            return response
        except Exception as e:
            error_msg = f"❌ 发生错误: {e}"
            print(error_msg)
            return error_msg
    
    top = retrieved[0]
    print(f"最高相似度: {top['score']}, 阈值: {threshold}")
    
    if top["score"] >= threshold:
        print("使用最高相似度片段作为回答")
        return top["chunk"]
    
    context = format_retrieved_context(retrieved)
    system_prompt, user_prompt = create_rag_prompt(context, user_text)

    try:    
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        response = ai_service.call_api(messages, model_name, stream=False)
        print(f"RAG增强回答结果: {response}")
        return response
    except Exception as e:
        error_msg = f"❌ 发生错误: {e}"
        print(error_msg)
        return error_msg

# WebSocket事件处理
@socketio.on('connect')
def handle_connect():
    print(f'客户端已连接: {request.sid}')

@socketio.on('start_recording')
def start_recording(data):
    client_id = request.sid
    audio_buffers[client_id] = []
    abort_flags[client_id] = False
    
    selected_model = data.get('model', 'LongCat-Flash-Chat')
    client_models[client_id] = selected_model
    
    emit('recording_started', {'message': '录音已开始，请说话...'})

@socketio.on('audio_data')
def handle_audio_data(data):
    client_id = request.sid
    if client_id in audio_buffers:
        try:
            audio_chunk = np.array(data['chunk'], dtype=np.float32)
            audio_buffers[client_id].extend(audio_chunk)
        except Exception as e:
            print(f'处理音频数据时出错: {str(e)}')
            emit('error', {'message': f'处理音频数据时出错: {str(e)}'})

@socketio.on('stop_recording')
def stop_recording():
    client_id = request.sid
    if client_id in audio_buffers:
        audio_data = np.array(audio_buffers[client_id], dtype=np.float32)
        del audio_buffers[client_id]
        
        if len(audio_data) > 0:
            text = transcribe_audio(audio_data)
            
            if text.strip():
                emit('transcription_result', {'text': text})
                # 不再自动触发AI响应，等待用户确认文本
            else:
                emit('transcription_result', {'error': '未检测到有效语音'})
        else:
            emit('transcription_result', {'error': '录音为空'})

@socketio.on('user_confirmed_text')
def handle_user_confirmed_text(data):
    """处理用户确认的文本"""
    client_id = request.sid
    text = data.get('text', '')
    selected_model = data.get('model', 'LongCat-Flash-Chat')
    
    print(f"收到用户确认文本: {text}, 模型: {selected_model}")
    
    if text.strip():
        try:
            emit('user_confirmed_text_ack', {'message': '文本已确认，正在生成回复'}, room=client_id)
            # 直接调用生成响应函数
            generate_rag_response_and_emit(text, client_id, selected_model)
        except Exception as e:
            print(f"处理用户确认文本时出错: {str(e)}")
            emit('error', {'message': f'处理请求时出错: {str(e)}'}, room=client_id)
    else:
        emit('error', {'message': '文本为空，请重新输入'}, room=client_id)

@socketio.on('abort_response')
def handle_abort_response():
    client_id = request.sid
    if client_id in abort_flags:
        abort_flags[client_id] = True
        emit('response_aborted', {'message': '响应已中止'}, room=client_id)

@socketio.on('replay_audio')
def handle_replay_audio(data):
    client_id = request.sid
    text = data.get('text', '')
    
    if text.strip():
        def replay_tts():
            socketio.emit('tts_generating', {'message': '正在重新生成语音...'}, room=client_id)
            audio_data = tts_service.text_to_speech(text)
            if audio_data:
                socketio.emit('tts_playing', {'message': '正在播放语音...'}, room=client_id)
                audio_service.play_audio(audio_data)
                socketio.emit('tts_complete', {'message': '语音播放完成'}, room=client_id)
            else:
                socketio.emit('tts_error', {'message': '语音生成失败'}, room=client_id)
        
        threading.Thread(target=replay_tts).start()

@socketio.on('disconnect')
def handle_disconnect():
    client_id = request.sid
    print(f'客户端已断开连接: {client_id}')
    for dict_key in [audio_buffers, abort_flags, client_models]:
        if client_id in dict_key:
            del dict_key[client_id]

def generate_rag_response_and_emit(text, client_id, model_name="LongCat-Flash-Chat"):
    """生成RAG响应并通过WebSocket发送，同时生成语音"""
    try:
        print(f"开始生成响应，文本: {text}, 模型: {model_name}")
        
        socketio.emit('ai_response_start', {'message': '开始生成响应'}, room=client_id)
        
        # 获取完整响应
        full_response = answer_by_rag(text, model_name, RAG_CONFIG["similarity_threshold"])
        print(f"生成的响应: {full_response}")
        
        def generate_and_play_tts_with_text():
            try:
                socketio.emit('tts_generating', {'message': '正在生成语音...'}, room=client_id)
                
                # 生成TTS音频
                audio_data = tts_service.text_to_speech(full_response)
                
                if audio_data:
                    socketio.emit('tts_playing', {'message': '正在播放语音...'}, room=client_id)
                    
                    # 发送完整的AI响应文本
                    socketio.emit('ai_response_complete', {
                        'message': '回答完成',
                        'full_text': full_response
                    }, room=client_id)
                    
                    # 播放音频
                    audio_service.play_audio(audio_data)
                    
                    socketio.emit('tts_complete', {'message': '语音播放完成'}, room=client_id)
                else:
                    socketio.emit('tts_error', {'message': '语音生成失败'}, room=client_id)
                    # 即使TTS失败，也要发送文本响应
                    socketio.emit('ai_response_complete', {
                        'message': '回答完成',
                        'full_text': full_response
                    }, room=client_id)
                    
            except Exception as e:
                print(f"TTS处理过程中出错: {str(e)}")
                traceback.print_exc()
                socketio.emit('error', {'message': f'TTS处理失败: {str(e)}'}, room=client_id)
                # 即使出错也要发送文本响应
                socketio.emit('ai_response_complete', {
                    'message': '回答完成',
                    'full_text': full_response
                }, room=client_id)
        
        # 在新线程中处理TTS
        threading.Thread(target=generate_and_play_tts_with_text).start()
            
    except Exception as e:
        print(f'生成RAG响应时出错: {str(e)}')
        traceback.print_exc()
        socketio.emit('error', {'message': f'生成AI响应时出错: {str(e)}'}, room=client_id)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)