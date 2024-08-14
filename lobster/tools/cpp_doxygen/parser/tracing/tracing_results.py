# Copyright (C) 2020, Bayerische Motoren Werke Aktiengesellschaft (BMW AG)


class TracingUnitResult:
    def __init__(self, correct_references, missing_references, incorrect_references):
        self.failure_desc = "incorrect or missing references"
        self.failures = len(missing_references) + len(incorrect_references)

        self.correct_references = len(correct_references)
        self.missing_references = len(missing_references)
        self.incorrect_references = len(incorrect_references)

        self.correct = correct_references
        self.missing = missing_references
        self.incorrect = incorrect_references

    def __str__(self):
        representation = ""
        representation += f"Correct references: {self.correct_references}\n"
        representation += f"Missing references: {self.missing_references}\n"
        representation += f"Incorrect references: {self.incorrect_references}\n"
        return representation

    @staticmethod
    def create_empty():
        return TracingUnitResult([], [], [])


class TracingComponentResult:
    def __init__(self, available_requirement_tags, missing_requirement_tags):
        self.failure_desc = "missing requirement tags"
        self.failures = len(missing_requirement_tags)

        self.available_requirement_tags = len(available_requirement_tags)
        self.missing_requirement_tags = len(missing_requirement_tags)

        self.available = available_requirement_tags
        self.missing = missing_requirement_tags

    def __str__(self):
        representation = ""
        representation += f"Available requirement tags: {self.available_requirement_tags}\n"
        representation += f"Missing requirement tags: {self.missing_requirement_tags}\n"
        return representation

    @staticmethod
    def create_empty():
        return TracingComponentResult([], [])
