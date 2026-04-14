import time
from loguru import logger
from src.rag.loader import init_rag
from src.rag.retriever import get_retriever
from src.graph.state import AgentState
from src.graph.workflow import planner_node, researcher_node

# 配置 loguru 打印到终端的格式
logger.remove()
logger.add(lambda msg: print(msg, end=""),
           format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")


def run_agent(question: str):
    """运行 Multi-Agent 工作流"""
    logger.info("=" * 50)
    logger.info(f"🎤 收到用户问题: {question}")
    logger.info("=" * 50)

    # 1. 初始化 RAG 
    vectorstore = init_rag()
    retriever = get_retriever(vectorstore)

    # 2. 初始化状态
    state = AgentState(
        question=question,
        plan="",
        context="",
        answer=""
    )

 
    start_time = time.time()

    # 执行节点 1
    state = planner_node(state, retriever)

    # 执行节点 2
    state = researcher_node(state, retriever)

    end_time = time.time()

    # 4. 输出结果
    logger.info("=" * 50)
    logger.info(f"📝 最终答案 (耗时 {end_time - start_time:.2f} 秒):")
    print("\n" + state["answer"] + "\n")
    logger.info("=" * 50)


if __name__ == "__main__":
    # 测试用例 1：能命中本地知识库的问题
    run_agent("技术部绩效A的年终奖什么时候发？发几个月？")

    # 测试用例 2：无法命中知识库，考验 Agent 兜底能力的问题
    # run_agent("Python的装饰器怎么写？")
