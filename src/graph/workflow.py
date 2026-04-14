from loguru import logger
from src.graph.state import AgentState
from src.models.llm_client import get_llm
from src.rag.retriever import do_search


# 读取 Prompt 模板
def read_prompt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def planner_node(state: AgentState, retriever) -> AgentState:
    """节点 1：规划者"""
    logger.info("🧠 [Planner] 开始思考并拆解任务...")
    llm = get_llm()
    prompt_template = read_prompt("prompts/planner_prompt.txt")

    prompt = prompt_template.format(question=state["question"])

    try:
        response = llm.invoke(prompt)
        state["plan"] = response.content
        logger.success(f"🧠 [Planner] 制定计划成功:\n{state['plan']}")
    except Exception as e:
        logger.error(f"🧠 [Planner] 规划失败: {e}")
        state["plan"] = "直接回答用户问题。"  # 🔥 面试加分项：降级兜底机制

    return state


def researcher_node(state: AgentState, retriever) -> AgentState:
    """节点 2：研究员（带工具调用）"""
    logger.info("🔍 [Researcher] 开始执行计划并检索知识库...")
    llm = get_llm()

    # 1. 调用 RAG 工具获取上下文
    state["context"] = do_search(retriever, state["question"])
    logger.info(f"🔍 [Researcher] 检索到上下文: {state['context'][:50]}...")

    # 2. 结合 Plan 和 Context 生成最终答案
    prompt_template = read_prompt("prompts/researcher_prompt.txt")
    prompt = prompt_template.format(
        plan=state["plan"],
        context=state["context"],
        question=state["question"]
    )

    try:
        response = llm.invoke(prompt)
        state["answer"] = response.content
        logger.success(f"🔍 [Researcher] 生成最终答案。")
    except Exception as e:
        logger.error(f"🔍 [Researcher] 生成答案失败: {e}")
        state["answer"] = "抱歉，系统在生成答案时发生错误，请稍后重试。"  # 🔥 兜底机制

    return state
