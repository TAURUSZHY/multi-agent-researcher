from typing import TypedDict, Optional

class AgentState(TypedDict):
    """定义多 Agent 之间传递的状态"""
    question: str       # 用户原始问题
    plan: str           # 规划器输出的计划
    context: str        # 研究员检索到的上下文
    answer: str         # 最终答案
