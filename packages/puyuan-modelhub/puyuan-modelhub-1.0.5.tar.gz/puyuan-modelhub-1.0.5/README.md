# Description
ModelhubClient: A Python client for the Modelhub API

# Installation

```shell
pip install puyuan_modelhub --user
```


# Usage 

## ModelhubClient

```python
from modelhub import ModelhubClient

client = ModelhubClient(
    host="https://xxxx.com/api/",
    user_name="xxxx",
    user_password="xxxx",
    model="xxx", # Optional
)
```

```python
response = client.chat(
    query,
    model="xxx", # Optional(use model in client construction)
    history=history,
    parameters=dict(
        key1=value1,
        key2=value2
    )
)
```

Response format:

```yaml
generated_text: response_text from model
history: generated history
details: generation details. Include tokens used, request duration, ...
```

History can be only used with ChatGLM3 now.

BaseMessage is the unit of history.

```python
# import some pre-defined message types
from modelhub.common.types import SystemMessage, AIMessage, UserMessage
# construct history of your own
history = [
    SystemMessage(content="xxx", other_value="xxxx"),
    UserMessage(content="xxx", other="xxxx"),
]
```
## VLMClient

```python
from modelhub import VLMClient
client = VLMClient(...)
client.chat(prompt=..., image_path=..., parameters=...)
```

Initialize a ModelhubClient
```python
from modelhub import ModelhubClient

client = ModelhubClient(
    host="http://*****:*****/", user_name="****", user_password="*****"
)
```

Get supported Models

```python
client.supported_models
```

Get model supported params

```python
client.get_supported_params("Minimax")
```

Chat with model

```python
client.chat("Hello?", model="m3e")
```

Get model embeddings

```python
client.get_embeddings(["你好", "Hello"], model="m3e")
```

# Examples

## Use ChatCLM3 for tools calling

```python
from modelhub import ModelhubClient, VLMClient
from modelhub.common.types import SystemMessage

client = ModelhubClient(
    host="https://xxxxx/api/",
    user_name="xxxxx",
    user_password="xxxxx",
)
tools = [
    {
        "name": "track",
        "description": "追踪指定股票的实时价格",
        "parameters": {
            "type": "object",
            "properties": {"symbol": {"description": "需要追踪的股票代码"}},
            "required": ["symbol"],
        },
    },
    {
        "name": "text-to-speech",
        "description": "将文本转换为语音",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"description": "需要转换成语音的文本"},
                "voice": {"description": "要使用的语音类型（男声、女声等）"},
                "speed": {"description": "语音的速度（快、中等、慢等）"},
            },
            "required": ["text"],
        },
    },
]

# construct system history
history = [
    SystemMessage(
        content="Answer the following questions as best as you can. You have access to the following tools:",
        tools=tools,
    )
]
query = "帮我查询股票10111的价格"

# call ChatGLM3
response = client.chat(query, model="ChatGLM3", history=history)
history = response["history"]
print(response["generated_text"])
```
```shell
Output:
{"name": "track", "parameters": {"symbol": "10111"}}
```

```python
# generate a fake result for track function call

result = {"price": 1232}

res = client.chat(
    json.dumps(result),
    parameters=dict(role="observation"), # Tell ChatGLM3 this is a function call result
    model="ChatGLM3",
    history=history,
)
print(res["generated_text"])
```

```shell
Output:
根据API调用结果，我得知当前股票的价格为1232。请问您需要我为您做什么？
```
# Contact
