import testios

from testios import get_connected
from pages.ios_page import DemoPage


@testios.story('测试demo')
class TestIosDemo(testios.TestCase):

    def start(self):
        self.page = DemoPage(self.driver)

    @testios.title('进入设置页')
    def test_go_setting(self):
        self.page.adBtn.click_exists(timeout=5)
        self.page.myTab.click()
        self.page.settingBtn.click()
        self.page.about.assert_exists()


if __name__ == '__main__':
    testios.main(
        devices=get_connected(),
        pkg_name='com.qizhidao.company'
    )


