graph TD
    User[用户输入复杂问题] --> Planner[Agent 1: 规划器 Planner]
    Planner -->|拆解任务| Researcher[Agent 2: 研究员 Researcher]
    
    subgraph 工具层
        Researcher -.->|调用| Search[(Tavily 联网搜索)]
        Researcher -.->|调用| VectorDB[(Chroma 向量库 RAG)]
    end
    
    Researcher -->|汇总信息| Reviewer[Agent 3: 审查员 Reviewer]
    Reviewer -->|通过| FinalAnswer[生成最终回复]
    Reviewer -.->|信息不足| Planner
    
    classDef agent fill:#f9f,stroke:#333,stroke-width:2px;
    classDef tool fill:#bbf,stroke:#333,stroke-width:1px;
    class Planner,Researcher,Reviewer agent;
    class Search,VectorDB tool;
# Multi-Agent RAG System

基于LangGraph的多智能体RAG系统，实现Planner+Researcher协作架构。

## 技术栈
- Python
- LangGraph
- ChromaDB
- DeepSeek API
- RAG（检索增强生成）

## 功能特点
- 多智能体协作
- 本地文档检索
- 结构化问题解答

## 快速开始
1. 安装依赖：`pip install -r requirements.txt`
2. 配置环境变量：复制.env.example为.env
3. 运行：`python main.py`