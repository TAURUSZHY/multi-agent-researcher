from langchain_community.vectorstores import Chroma
from loguru import logger

def get_retriever(vectorstore: Chroma):
    """获取检索器实例"""
    if not vectorstore:
        return None
    # 使用相似度检索，取 top 2
    return vectorstore.as_retriever(search_kwargs={"k": 2})

def do_search(retriever, query: str) -> str:
    """执行检索并返回拼接的字符串"""
    if not retriever:
        return "【系统提示：未加载知识库】"
    try:
        docs = retriever.invoke(query)
        context = "\n".join([doc.page_content for doc in docs])
        return context if context else "未检索到相关内容。"
    except Exception as e:
        logger.error(f"检索过程发生错误: {e}")
        return "【系统提示：检索工具调用失败】"
