from infra.page_base import PageBase


class YTPage(PageBase):

    side_menu = "id=guide-icon"

    def __init__(self, page):
        super().__init__(page)

    def click_side_menu(self):
        visible = self.wait_for_visible(self.side_menu)
        self.pw_page.click(selector=self.side_menu)
        self.pw_page.wait_for_timeout(200000)


