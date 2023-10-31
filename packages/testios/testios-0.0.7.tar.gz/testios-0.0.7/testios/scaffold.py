import os.path

case_content_ios = """import testios

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
"""

page_content = """from testios import Page, Elem
'''
定位方式：优先选择label
name: 根据name属性进行定位
label: 根据label属性进行定位
value: 根据value属性进行定位
text: 根据文本属性进行定位，集合和label、value等文本属性的内容
className: 根据className属性进行定位
xpath: 根据xpath进行定位
index: 获取到定位到的第index个元素
'''


class DemoPage(Page):
    # 首页
    adBtn = Elem(label='close white big', desc='广告关闭按钮')
    myTab = Elem(label='我的', desc='我的tab')
    # 我的页
    settingBtn = Elem(label='settings navi', desc='设置按钮')
    # 设置页
    about = Elem(text="关于企知道", desc='关于企知道文本')
"""

run_content = """import testios


if __name__ == '__main__':
    # 执行多个用例文件，主程序入口
    testios.main(
        case_path='tests/test_ios.py',
        devices=['00008101-000E646A3C29003A'],
        pkg_name='com.qizhidao.company'
    )
"""


def create_scaffold(projectName):
    """create scaffold with specified project name."""

    def create_folder(path):
        os.makedirs(path)
        msg = f"created folder: {path}"
        print(msg)

    def create_file(path, file_content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_content)
        msg = f"created file: {path}"
        print(msg)

    # 新增测试数据目录
    root_path = projectName
    create_folder(root_path)
    create_folder(os.path.join(root_path, "pages"))
    create_folder(os.path.join(root_path, "tests"))
    create_folder(os.path.join(root_path, "report"))
    create_folder(os.path.join(root_path, "data"))
    create_folder(os.path.join(root_path, "screenshot"))
    create_file(
        os.path.join(root_path, "pages", "ios_page.py"),
        page_content,
    )
    create_file(
        os.path.join(root_path, "tests", "test_ios.py"),
        case_content_ios,
    )
    create_file(
        os.path.join(root_path, "run.py"),
        run_content,
    )


