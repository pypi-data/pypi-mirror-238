import pytest
from clustaar.schemas.models import Video, Message
from tests.utils import MAPPER


@pytest.fixture
def video():
    return Video(url="http://example.com/")


@pytest.fixture
def message(video):
    return Message(text="hello", attachments=[video])


@pytest.fixture
def data():
    return {
        "type": "message",
        "text": "hello",
        "attachments": [{"type": "video", "url": "http://example.com/"}],
    }


@pytest.fixture
def malicious_data():
    return {
        "type": "message",
        "text": "<script>void();</script>hello",
        "attachments": [{"type": "video", "url": "http://example.com/"}],
    }


class TestDump:
    def test_returns_a_dict(self, data, message):
        result = MAPPER.dump(message)
        assert result == data


class TestLoad:
    def test_returns_an_object(self, data):
        result = MAPPER.load(data, "incoming_message")
        assert isinstance(result, Message)
        assert result.text == "hello"
        assert isinstance(result.attachments[0], Video)


class TestLoadMalicious:
    def test_returns_an_object(self, malicious_data):
        result = MAPPER.load(malicious_data, "incoming_message")
        assert result.text == "&lt;script&gt;void();&lt;/script&gt;hello"


def a_data():
    return {
        "type": "message",
        "text": "<a>example</a> link",
        "attachments": [{"type": "video", "url": "http://example.com/"}],
    }


def a_data_target(target_value):
    return {
        "type": "message",
        "text": f'<a target="{target_value}">example</a> link',
        "attachments": [{"type": "video", "url": "http://example.com/"}],
    }


data_list = [(a_data(), a_data())]
data_list.extend([(a_data_target(t), a_data_target(t)) for t in ("_blank", "_top")])
data_list.extend([(a_data_target(t), a_data()) for t in ("_self", "_parent")])


class TestLoadATag:
    @pytest.fixture
    def a_data_fix(self):
        return a_data()

    @pytest.mark.parametrize("a_data,expected", data_list)
    def test_returns_an_object(self, a_data, expected):
        result = MAPPER.load(a_data, "incoming_message")
        assert result.text == expected["text"]
