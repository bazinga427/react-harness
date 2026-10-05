"""配置管理"""
import os
from pathlib import Path  # 【本次修改 4】用来算出 .env 文件的绝对路径
from typing import Optional, Dict, Any
from dotenv import load_dotenv  # 【本次修改 4】新加的导入：用来读取 .env 文件
from pydantic import BaseModel

# 【本次修改 4】把项目根目录下的 .env 文件读进环境变量。少了这一步，
# 下面 Config.from_env() 里用 os.getenv 读 LLM_API_KEY 这些变量时读到的全是空的。
# 这里先算出 .env 的完整路径再传给 load_dotenv()，原因是：
# 如果写成不带参数的 load_dotenv()，只要程序跑在调试器里（或者交互式环境里），
# 它就会退化成按当前工作目录去找 .env，工作目录一换就读不到了。
# __file__ 指的就是本文件 core/config.py，parent 是 core 目录，再 parent 就是项目根目录。
_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_ENV_FILE)


class Config(BaseModel):
    """HelloAgents配置类"""

    # LLM配置
    default_model: str = "gpt-3.5-turbo"
    default_provider: str = "openai"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    llm_api_key: Optional[str] = None
    llm_base_url: Optional[str] = None
    llm_model_id: Optional[str] = None
    serpapi_api_key: Optional[str] = None

    # 系统配置
    debug: bool = False
    log_level: str = "INFO"

    # 其他配置
    max_history_length: int = 100

    @classmethod
    def from_env(cls) -> "Config":
        """从环境变量创建配置"""
        return cls(
            debug=os.getenv("DEBUG", "false").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("MAX_TOKENS")) if os.getenv("MAX_TOKENS") else None,
            llm_api_key=os.getenv("LLM_API_KEY"),
            llm_base_url=os.getenv("LLM_BASE_URL"),
            llm_model_id=os.getenv("LLM_MODEL_ID"),
            serpapi_api_key=os.getenv("SERPAPI_API_KEY")
       )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self.dict()