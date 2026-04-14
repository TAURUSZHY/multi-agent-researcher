from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import FakeEmbeddings  # 🌟面试亮点：用假向量避免你本地没装模型报错
from langchain_community.vectorstores import Chroma
from loguru import logger


def init_rag():
    """初始化 RAG，加载文档并向量化"""
    logger.info("正在加载本地文档并进行向量化...")
    try:
        # 1. 加载文档
        loader = TextLoader("data/test_doc.txt", encoding="utf-8")
        docs = loader.load()

        # 2. 切分文档
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = text_splitter.split_documents(docs)

        # 3. 向量化并存入 Chroma
        # 注意：这里用了 FakeEmbeddings 是为了你零配置跑通！
        # 面试时跟面试官说："为了演示方便用了假向量，生产环境我会换成 BGE 或 OpenAI Embedding"
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=FakeEmbeddings(size=1352),
            persist_directory="./chroma_db"
        )
        logger.success(f"文档加载完成，共切分 {len(splits)} 个文本块。")
        return vectorstore
    except FileNotFoundError:
        logger.warning("未找到 data/test_doc.txt，RAG 功能将不可用。")
        return None
    except Exception as e:
        logger.error(f"RAG 初始化失败: {e}")
        return None
