import pytest
from langchain_core.messages import (
    AIMessage,
    AIMessageChunk,
    ChatMessage,
    FunctionMessage,
    HumanMessage,
    HumanMessageChunk,
    SystemMessage,
)
from langchain_core.pydantic_v1 import SecretStr

from langchain.chat_models.hunyuan import (
    _convert_delta_to_message_chunk,
    _convert_dict_to_message,
    _convert_message_to_dict,
    _signature,
)


def test__convert_message_to_dict_human() -> None:
    message = HumanMessage(content="foo")
    result = _convert_message_to_dict(message)
    expected_output = {"role": "user", "content": "foo"}
    assert result == expected_output


def test__convert_message_to_dict_ai() -> None:
    message = AIMessage(content="foo")
    result = _convert_message_to_dict(message)
    expected_output = {"role": "assistant", "content": "foo"}
    assert result == expected_output


def test__convert_message_to_dict_system() -> None:
    message = SystemMessage(content="foo")
    with pytest.raises(TypeError) as e:
        _convert_message_to_dict(message)
    assert "Got unknown type" in str(e)


def test__convert_message_to_dict_function() -> None:
    message = FunctionMessage(name="foo", content="bar")
    with pytest.raises(TypeError) as e:
        _convert_message_to_dict(message)
    assert "Got unknown type" in str(e)


def test__convert_dict_to_message_human() -> None:
    message_dict = {"role": "user", "content": "foo"}
    result = _convert_dict_to_message(message_dict)
    expected_output = HumanMessage(content="foo")
    assert result == expected_output


def test__convert_dict_to_message_ai() -> None:
    message_dict = {"role": "assistant", "content": "foo"}
    result = _convert_dict_to_message(message_dict)
    expected_output = AIMessage(content="foo")
    assert result == expected_output


def test__convert_dict_to_message_other_role() -> None:
    message_dict = {"role": "system", "content": "foo"}
    result = _convert_dict_to_message(message_dict)
    expected_output = ChatMessage(role="system", content="foo")
    assert result == expected_output


def test__convert_delta_to_message_assistant() -> None:
    delta = {"role": "assistant", "content": "foo"}
    result = _convert_delta_to_message_chunk(delta, AIMessageChunk)
    expected_output = AIMessageChunk(content="foo")
    assert result == expected_output


def test__convert_delta_to_message_human() -> None:
    delta = {"role": "user", "content": "foo"}
    result = _convert_delta_to_message_chunk(delta, HumanMessageChunk)
    expected_output = HumanMessageChunk(content="foo")
    assert result == expected_output


def test__signature() -> None:
    secret_key = SecretStr("YOUR_SECRET_KEY")
    url = "https://hunyuan.cloud.tencent.com/hyllm/v1/chat/completions"

    result = _signature(
        secret_key=secret_key,
        url=url,
        payload={
            "app_id": "YOUR_APP_ID",
            "secret_id": "YOUR_SECRET_ID",
            "query_id": "test_query_id_cb5d8156-0ce2-45af-86b4-d02f5c26a142",
            "messages": [
                {
                    "role": "user",
                    "content": "You are a helpful assistant that translates English"
                    " to French.Translate this sentence from English to"
                    " French. I love programming.",
                }
            ],
            "temperature": 0.0,
            "top_p": 0.8,
            "stream": 1,
            "timestamp": 1697738378,
            "expired": 1697824778,
        },
    )

    # The signature was generated by the demo provided by Huanyuan.
    # https://hunyuan-sdk-1256237915.cos.ap-guangzhou.myqcloud.com/python.zip
    expected_output = "MXBvqNCXyxJWfEyBwk1pYBVnxzo="
    assert result == expected_output
