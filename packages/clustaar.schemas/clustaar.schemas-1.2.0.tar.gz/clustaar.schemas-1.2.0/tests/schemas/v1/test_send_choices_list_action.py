from clustaar.schemas.v1 import SEND_CHOICES_LIST_ACTION
from clustaar.schemas.models import StepTarget, GoToAction, Section, Choice, SendChoicesListAction
from lupin.errors import InvalidDocument

import pytest


@pytest.fixture
def go_to_action():
    target = StepTarget(step_id="a1" * 12, name="a step")

    return GoToAction(target=target)


@pytest.fixture
def section():
    return Section(title="A", choices=[Choice(title="Amelin", image_url="https://image.com")])


@pytest.fixture
def action(section, go_to_action):
    return SendChoicesListAction(
        message="hello", placeholder="toto", sections=[section], action=go_to_action
    )


@pytest.fixture
def data(section):
    return {
        "type": "send_choices_list_action",
        "message": "hello",
        "placeholder": "toto",
        "sections": [
            {
                "type": "section",
                "title": "A",
                "choices": [
                    {
                        "type": "choice",
                        "imageUrl": "https://image.com",
                        "title": "Amelin",
                        "sessionValues": None,
                    }
                ],
            }
        ],
        "action": {
            "type": "go_to_action",
            "target": {"type": "step", "name": "a step", "id": "a1" * 12},
            "sessionValues": None,
        },
    }


@pytest.fixture
def malicious_data():
    return {
        "type": "send_choices_list_action",
        "message": "<script>void();</script>hello",
        "placeholder": "toto",
        "sections": [
            {
                "type": "section",
                "title": "<script>void();</script>A",
                "choices": [
                    {
                        "type": "choice",
                        "title": "<script>void();</script>Amelin",
                        "imageUrl": "<script>void();</script>image",
                    }
                ],
            }
        ],
    }


class TestDump:
    def test_returns_a_dict(self, action, data, mapper):
        result = SEND_CHOICES_LIST_ACTION.dump(action, mapper)

        assert result == data


class TestValidate:
    def test_validate_simple_action(self, data, mapper):
        mapper.validate(data, SEND_CHOICES_LIST_ACTION)

        new_section = data["sections"][0].copy()
        data["sections"].append(new_section)

        mapper.validate(data, SEND_CHOICES_LIST_ACTION)

    def test_raise_if_multiple_sections_and_empty_title(self, data, mapper):
        new_section_with_empty_title = data["sections"][0].copy()
        new_section_with_empty_title["title"] = ""

        data["sections"].append(new_section_with_empty_title)

        with pytest.raises(InvalidDocument) as e:
            mapper.validate(data, SEND_CHOICES_LIST_ACTION)

        assert e.value.errors[0].path == ["sections", "1", "title"]
        assert (
            e.value.errors[0].args[0]
            == 'Invalid value, got empty str "" instead of a valid title. If action contains only one section empty title is permit'
        )


class TestLoad:
    def test_returns_an_action(self, data, mapper):
        action = mapper.load(data, SEND_CHOICES_LIST_ACTION)
        assert isinstance(action, SendChoicesListAction)
        assert action.message == "hello"
        assert action.placeholder == "toto"
        section = action.sections[0]
        assert section.title == "A"
        choice = section.choices[0]
        assert choice.title == "Amelin"
        assert choice.image_url == "https://image.com"

    def test_returns_an_action_malicious(self, malicious_data, mapper):
        action = mapper.load(malicious_data, SEND_CHOICES_LIST_ACTION)
        assert isinstance(action, SendChoicesListAction)
        assert action.message == "&lt;script&gt;void();&lt;/script&gt;hello"
        assert action.placeholder == "toto"
        section = action.sections[0]
        assert section.title == "&lt;script&gt;void();&lt;/script&gt;A"
        choice = section.choices[0]
        assert choice.title == "&lt;script&gt;void();&lt;/script&gt;Amelin"
        assert choice.image_url == "&lt;script&gt;void();&lt;/script&gt;image"
