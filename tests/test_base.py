import logging
import pytest
from infra.teardown.tear_down import tear_down_tasks
from infra.browser import Browser
from infra.teardown import tear_down


class TestBase():
    test_failed = True
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    browser = Browser()

    @pytest.fixture(scope="function")
    def before_after_test(self, request):
        test_name = request.node.originalname
        print('Starting test "' + test_name + '"')
        failed_before = request.session.testsfailed
        yield self.browser
        if request.session.testsfailed != failed_before:
            try:
                self.browser.stop_trace()
            except:
                pass
        self.tear_down_invoke()
        print('\r*****DONE*****')


    def tear_down_invoke(self):
        print('\r******TEARDOWN******')
        for tear_down in tear_down_tasks:
            try:
                invoke = getattr(tear_down, "invoke")
                invoke()
            except:
                pass
        tear_down_tasks.clear()
        print('\r*****DONE_TEARDOWN*****')
