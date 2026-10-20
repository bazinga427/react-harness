# Hello-Agents

一个用于学习 Agent 核心原理的 Python 项目。项目手写了 ReAct 循环、工具注册与调用、BM25 知识库检索、工作记忆以及上下文压缩，没有依赖 LangChain 等 Agent 编排框架。

## 主要功能

- 使用 ReAct 模式完成“思考 → 调用工具 → 观察结果 → 输出答案”的流程
- 可插拔的工具注册机制，目前包含计算器、知识库检索和记忆查询
- 基于 `jieba + BM25` 的中文文档切分与关键词检索
- 简单的工作记忆，用于保存和查询用户信息
- 通过滑动窗口、摘要压缩和重复调用检测控制上下文长度
- 支持任意兼容 OpenAI 接口的大模型服务

## 快速开始

环境要求：Python 3.9 及以上。

```bash
pip install openai pydantic python-dotenv google-search-results jieba rank-bm25
```

在项目根目录创建 `.env` 文件：

```env
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://your-api-endpoint/v1
LLM_MODEL_ID=your_model_id

# 可选：启用网页搜索工具时需要
SERPAPI_API_KEY=your_serpapi_key
```

启动示例：

```bash
python main.py
```

示例会读取 `text.txt` 作为知识库，构建 ReAct Agent，并回答一个与法律条文相关的问题。你可以在 `main.py` 中修改问题、注册其他工具，或调整最大执行步数。

## 项目结构

```text
.
├── agents/          # Agent 基类与 ReAct Agent
├── core/            # 配置、消息模型与 LLM 客户端
├── memory/          # 工作记忆
├── rag/             # 文档切分与 BM25 检索
├── tools/           # 工具定义、注册表及具体工具
├── main.py          # 运行示例
└── text.txt         # 示例知识库
```

## 说明

这是一个偏学习与实践性质的原型项目，主要用于理解 Agent Loop、Tool Calling、Memory 和 RAG 的基本实现。后续可以继续接入 FastAPI、向量检索、更多工具或更完整的评测流程。
