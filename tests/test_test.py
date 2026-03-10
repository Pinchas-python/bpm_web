import pytest

from infra.browser import Browser
from logic.pages.login_page import LoginPage
from logic.pages.youtube_page import YTPage
from tests.test_base import TestBase
from infra.config.config_provider import configuration
from playwright.sync_api import sync_playwright


class TestClass(TestBase):
    @pytest.fixture(autouse=True, scope='class')
    def classscope(self):
        print('AAAAA')
        yield
        print('BBBBBB')

    @pytest.mark.tc14
    def test_10007_(self):
        browser = Browser()
        page: YTPage = browser.navigate("https://tiles-tiny.lupa.co.il/", YTPage)
        page.click_side_menu()
        print('past playwright')

    @pytest.mark.smoke
    def test_10008_(self):
        assert True is False

    @pytest.mark.smoke
    @pytest.mark.usefixtures("before_after_test")
    def test_upload_photo(self):
        browser = Browser()
        page: LoginPage = browser.navigate(configuration['url1'], LoginPage)
        page.choose_tiles()

        page: UploadPhotoPage = browser.create_page(UploadPhotoPage)

        print('past playwright')
        assert "התנתק" == ""

    @pytest.mark.smoke
    def test_10008_(self):
        assert True is False

