import pytest

from tests.test_base import TestBase


class TestClass(TestBase):

    @pytest.mark.smoke
    def test_10005_(self):
        assert True is True

    @pytest.mark.smoke
    def test_10004_(self):
        assert True is False

    @pytest.mark.smoke
    def test_10006_(self):
        assert True is False

