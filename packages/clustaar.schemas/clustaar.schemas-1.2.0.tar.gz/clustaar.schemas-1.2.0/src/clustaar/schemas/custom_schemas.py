from typing import Optional, Dict, List

from lupin import Mapper, Schema, bind
from lupin.errors import ValidationError, InvalidDocument


class MatchIntentConditionSchema(Schema):
    """We need a custom schema for the MatchIntentCondition because the JSON structure
    does not reflect the one in our models.
    """

    def load(self, cls, data, mapper, allow_partial=False, factory=bind):
        """Loads an instance of cls from dictionary

        Args:
            cls (class): class to instantiate
            data (dict): dictionary of data
            mapper (Mapper): mapper used to load data
            allow_partial (bool): allow partial schema, won't raise error if missing keys
            factory (callable): factory method used to instantiate objects
        Returns:
            object
        """
        return cls(intent_id=data["intent"]["id"])


class CustomerSatisfactionChoiceSchema(Schema):
    """We need a custom schema for the CustomerSatisfactionChoice because the JSON structure
    does not reflect the one in our models.
    """

    def load(self, cls, data, mapper, allow_partial=False, factory=bind):
        """Loads an instance of cls from dictionary

        Args:
            cls (class): class to instantiate
            data (dict): dictionary of data
            mapper (Mapper): mapper used to load data
            allow_partial (bool): allow partial schema, won't raise error if missing keys
            factory (callable): factory method used to instantiate objects
        Returns:
            object
        """
        matching_intent_data = data.get("matchingIntent")
        if matching_intent_data and matching_intent_data.get("id"):
            data["matching_intent_id"] = data["matchingIntent"]["id"]

        return super().load(cls, data, mapper, allow_partial, factory)


class SendChoicesListActionSchema(Schema):
    """Custom schema to add a particular validation not possible with basic lupin Schema.

    We have to raise an error in case of empty section title if there are more than two section.
    """

    def validate(
        self, data: dict, mapper: Mapper, allow_partial: bool = False, path: Optional[str] = None
    ) -> None:
        """Raise an error in case of empty section title if there are more than two section.

        Args:
            data: the json data repr
            mapper: the lupin mapper
            allow_partial: permit partial validation
            path: the path

        Raises:
            InvalidDocument

        """
        path: List[str] = path or []
        errors: List[ValidationError] = []

        super().validate(data, mapper, allow_partial, path)

        if len(data["sections"]) > 1:
            for index, section in enumerate(data["sections"]):
                if not section.get("title"):
                    error = ValidationError(
                        'Invalid value, got empty str "" instead of a valid title. If action contains only'
                        " one section empty title is permit",
                        path + ["sections", str(index), "title"],
                    )

                    errors.append(error)
            if errors:
                raise InvalidDocument(errors)
