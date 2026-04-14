import os
import yaml
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from loguru import logger

# 加载环境变量和配置
load_dotenv()
with open("config/config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

def get_llm():
    """获取统一配置的 LLM 实例"""
    try:
        llm = ChatOpenAI(
            model=config["llm"]["model_name"],
            temperature=config["llm"]["temperature"],
            max_tokens=config["llm"]["max_tokens"],
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )
        return llm
    except Exception as e:
        logger.error(f"LLM 初始化失败，请检查 API Key 和网络: {e}")
        raise
