# Weather Agent Core

LLM Agent アプリケーションの **Core 化アーキテクチャ** を実証するデモプロジェクトです。

## 解決する課題

LLM Agent アプリの開発では、以下のような課題がよく発生します：

1. コードの二重管理
2. 環境差異による移植コスト
3. 同期コストの増大

## 解決アプローチ

**Hexagonal Architecture（ポートとアダプタ）** の考え方を採用し、Agent のコアロジックを共有ライブラリとして切り出します。

```
┌──────────────────────────────────────┐
│            Core ライブラリ             │
│                                      │
│  LangChain / Prompt / MLflow tracing │
│                                      │
│  Port (Protocol):                    │
│    - WeatherDBService                │
│    - OtherService                    │
└──────────────────────────────────────┘
        ▲                    ▲
        │                    │
   A アダプタ                B アダプタ
   (Spark, DBFS)         (PostgreSQL, Redis)
```

### 設計原則

| 分類               | 方針                         | 理由                                        |
| ------------------ | ---------------------------- | ------------------------------------------- |
| Agent ロジック     | Core に集約                  | 複数チームで同一のAgentコードを使用するため |
| 外部データサービス | Protocol で抽象化            | 各チームの実装が異なるため                  |
| LLM クライアント   | Core に集約（Config レベル） | Bedrock を統一的に管理するため              |
| MLflow 観測性      | Core に集約（Config レベル） | 記録内容・粒度を統一するため                |

## プロジェクト構成

```
core/
├── ports.py              # Protocol インターフェース定義（WeatherDBService）
├── runtime.py            # LLMConfig / ObservabilityConfig / AgentRuntime
├── llm.py                # LLM ファクトリ（ChatBedrock）
├── agent.py              # WeatherAgent コアロジック
├── prompts/
│   └── weather.yaml      # プロンプトテンプレート
└── tests/
    └── contract_test_weather_db.py  # 契約テスト基底クラス
```

## インストール

```bash
pip install "git+https://github.com/Nial4/llm-interface.git@v0.1.0"
```

## 使い方

### 1. アダプタを実装する

`WeatherDBService` Protocol を満たすクラスを作成します：

```python
from core.ports import WeatherDBService, WeatherInfo

class MyWeatherDB:
    def get_user_location(self, user_id: str) -> str:
        # 自チームの DB から取得
        ...

    def get_today_weather(self, location: str) -> WeatherInfo:
        # 自チームの DB から取得
        ...
```

### 2. Agent を起動する

```python
from core import AgentRuntime, LLMConfig, ObservabilityConfig, WeatherAgent

runtime = AgentRuntime(
    weather_db=MyWeatherDB(),
    llm_config=LLMConfig(
        model_id="anthropic.claude-3-haiku-20240307-v1:0",
        region_name="ap-northeast-1",
        credentials_profile_name="your-aws-profile",
    ),
    observability=ObservabilityConfig(enabled=False),
)

agent = WeatherAgent(runtime)
response = agent.invoke(user_id="user-1", user_input="今日の天気はどうですか？")
```

### 3. 契約テストでアダプタを検証する

Core が提供する契約テスト基底クラスを継承し、自チームのアダプタが正しく動作することを保証します：

```python
import pytest
from core.tests.contract_test_weather_db import WeatherDBServiceContractTest

class TestMyWeatherDB(WeatherDBServiceContractTest):
    @pytest.fixture()
    def weather_db(self):
        return MyWeatherDB()

    @pytest.fixture()
    def known_user_id(self):
        return "user-1"

    @pytest.fixture()
    def known_location(self):
        return "Tokyo"
```

```bash
pytest test_my_adapter.py -v
```

## 技術スタック

- Python 3.11+
- LangChain Core / LangChain AWS v1.x
- Amazon Bedrock (Claude)
- MLflow (観測性)
