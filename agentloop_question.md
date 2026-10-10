LLM 把 prompt 当成了"一份还没写完的对话记录"，自己接着往下把整段对话都写完了。
现在日志里的「反复检索、不停、续写对话」——全是 Agent 层的问题：prompt 结构、history 管理、循环终止条件。
日志里你看到几十轮 user: Observation: / assistant: Action: 反复出现，不是程序真的循环了，而是：

LLM 把 prompt 当成了"一份还没写完的对话记录"，自己接着往下把整段对话都写完了。

关键证据：user: 和 assistant: 这种角色前缀，只有你拼 prompt 时才会写进去，LLM 本不该输出它们。它输出了，说明它以为自己在"续写一份对话"——它把自己当成了剧本的续写者，而不是"这一轮的执行者"。

根因：你的 prompt 结尾是：

text
Question: {question}
History: {history}       ← history 以 "user: Observation:..." 结尾
LLM 看到 prompt 末尾是「user 说的话」，它的本能是「轮到 assistant 了，我来接着写」。于是它写完一个 Action，觉得"对话还没完"，又自己编了 Observation，又写下一个 Action……直到输出被截断。

这不是死循环，是一次生成里它自己演完了整场戏。

三、Codex 给的修法：只改 prompt 结构
Codex 明确说「先别动 _parse_output、别动 top_k、别加 history 上限——一次只改一处」。这个建议非常专业，理由是：

如果你同时改 5 个地方，跑通了，你不知道是哪一处起的作用；跑不通，你不知道是哪一处搞坏的。一次只改一个变量，才知道因果。这就是你 PROGRESS.md 里要的「有迭代痕迹」。

所以你现在只做一件事：改 prompt 模板结尾。

原来：

text
现在，请开始解决以下问题:
Question: {question}
History: {history}
改成：

text
以下是已完成的步骤，仅供你参考，不要重复输出:
{history}

现在轮到你。请只输出一段 Thought 和一行 Action，输出后立即停止。
不要输出 Observation，不要复述历史。
如果历史中的信息已经足以回答，直接输出 Finish[最终答案]。
Question: {question}
这个改法做了三件事：

改动	治哪个病
history 上加「只读、勿复述」标签	治 A（模型续写对话）
「只输出一条 Action 后停止」	治 A（模型一次生成几十轮）
「够了就 Finish」	治 C（模型不知道何时停，原地打转）
四、改完怎么看有没有生效
Codex 给了两个观察信号，非常具体：

第 2 步的模型输出里，只有一段 Thought + 一行 Action，不再往下续写。

终端里不再出现模型生成的 user: Observation:。

只要这两条满足，就说明主因（prompt 边界问题）修好了。 然后再看它能不能在 5 步内 Finish。

五、这次别改的 4 个（Codex 列了，我解释下为什么先别动）
先别动	为什么
_parse_output 只取第一个 Action	它是次要问题，prompt 修好后模型不会再输出一坨；先改它你就分不清功劳归谁
top_k 提到 3~5	这是效果调优，不是 bug；主因没修好之前调它没用
history 封顶（只留最近 3 轮）	这是性能优化，现在先保证逻辑对，再优化
thought 写进 history	这是改进，不是修 bug，留着后面做
Codex 的排序非常对：先修「模型会不会乱写」这个逻辑 bug，再修「token 太多」这个性能问题，最后修「检索不够准」这个效果问题。一次只动一处。

六、花销提醒（Codex 也提了，很重要）
这次会真调 DeepSeek，deepseek-chat 便宜档，一次完整运行几分到一两毛。改完再跑，别连着按。

这个意识很好——你已经进到「跑一次要花钱」的阶段了。生产环境的 Agent 更要控制调用次数（这本身就是面试话题：怎么控制 Agent 的成本）。

七、你现在处于哪一章
Codex 那句话很关键：

你撞上的这个问题就是第九章上下文工程本身——"怎么把历史塞进有限窗口"。不是多学一章，是你已经走到那一章的地界了。

翻译：你现在踩的坑，正是"上下文工程（Context Engineering）"要解决的问题。 这不是"超纲"，这是你自然走到了 Agent 开发的核心难点。

上下文工程要处理的事：

history 怎么拼、怎么截断（窗口有限）

prompt 怎么设计边界（模型不越权）

每轮塞什么、丢什么（token 成本）

怎么让模型知道「该停了」