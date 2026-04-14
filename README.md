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
