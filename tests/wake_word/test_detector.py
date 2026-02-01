"""Tests for wake word detection domain logic."""

from hamcrest import assert_that, is_

from much_miller.wake_word.detector import contains_wake_word


class TestContainsWakeWord:
    """Tests for the contains_wake_word function."""

    def test_returns_true_for_hey_much(self) -> None:
        result = contains_wake_word("hey much what time is it")
        assert_that(result, is_(True))

    def test_returns_true_with_mixed_case(self) -> None:
        result = contains_wake_word("Hey Much what is the weather")
        assert_that(result, is_(True))

    def test_returns_true_with_upper_case(self) -> None:
        result = contains_wake_word("HEY MUCH tell me a joke")
        assert_that(result, is_(True))

    def test_returns_false_for_just_much(self) -> None:
        result = contains_wake_word("much what time is it")
        assert_that(result, is_(False))

    def test_returns_false_for_no_match(self) -> None:
        result = contains_wake_word("hello world")
        assert_that(result, is_(False))
