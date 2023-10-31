"""
@Author: kang.yang
@Date: 2023/8/21 16:38
"""
import testios

from pages.ocr_page import OcrPage


class TestOcrDemo(testios.TestCase):
    """ocr识别demo"""

    def start(self):
        self.op = OcrPage(self.driver)

    def test_nanshan_wtt(self):
        self.op.searchBtn.click()
        self.op.searchInput.input("南山文体通")
        self.op.searchResult.click()
        self.op.schoolEntry.click()
        self.sleep(5)


if __name__ == '__main__':
    testios.main(
        devices=['00008101-000E646A3C29003A'],
        pkg_name='com.tencent.xin'
    )




