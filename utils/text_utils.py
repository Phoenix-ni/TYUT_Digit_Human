# Description: 文本处理工具
# Author: TYUT创新学社
# Date: 2025-10-4 19：44
def create_rag_prompt(context, user_text):
    """创建RAG提示词"""
    system_prompt = (
        "你是TYUT创新学社的招新助手。\n"
        "请优先基于以下官方资料回答问题。\n"
        "回答时不要分点,请回答成一段话的形式,偏口语的形式。\n"
        "如果涉及到社团但是知识库没有的相关内容，请不要直接回答出资料没有相关部分，而是基于你自己的知识进行回答。\n"
        "回答的时候简洁一些，回答了问题的需求即可，不要添加多余的内容。\n"
        "请谨记，我们社团不限大一大二的年级约束，也不限专业约束，欢迎所有人加入。\n"
    )
    
    user_prompt = f"{context}\n\n用户问题：{user_text}"
    return system_prompt, user_prompt

def format_retrieved_context(retrieved_results):
    """格式化检索到的上下文"""
    return "\n\n".join([f"【相关资料】{r['chunk']}" for r in retrieved_results])