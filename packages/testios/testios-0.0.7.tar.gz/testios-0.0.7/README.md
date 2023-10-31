# 介绍

[Gitee](https://gitee.com/bluepang2021/testios_project)

IOS AppUI automation testing framework based on pytest.

> 基于pytest 的 IOS App UI自动化测试框架，支持图像识别和OCR识别。

## 特点

* 集成`facebook-wda`/`opencv`/`easyocr`
* APP图像识别：`图像识别定位`/`OCR识别定位`
* 集成`allure`, 支持HTML格式的测试报告
* 提供强大的`数据驱动`，支持json、yaml
* 提供丰富的断言
* 支持生成随机测试数据
* 支持设置用例依赖


## 三方依赖

* Allure：https://github.com/allure-framework/allure2
* WebDriverAgent：https://github.com/appium/WebDriverAgent
* weditor: https://github.com/alibaba/web-editor

## Install

```shell
> pip install -i https://pypi.tuna.tsinghua.edu.cn/simple testios
```

## 🤖 Quick Start

1、查看帮助：
```shell
Usage: testios [OPTIONS]

Options:
  --version               Show version.
  -p, --projectName TEXT  Create demo by project name
  --help                  Show this message and exit.

```

2、运行项目：

* ✔️ 在`pyCharm`中右键执行(需要把项目的单元测试框架改成unittests)

* ✔️ 通过命令行工具执行。

3、查看报告

运行`allure server report`浏览器会自动调起报告（需先安装配置allure）


## 🔬 Demo

[demo](/demo) 提供了丰富实例，帮你快速了解testios的用法。

* page类

```python
from testios import Page, Elem
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
```

* 用例类

```python
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
```

### 参数化

```python
import testios
from testios import logger


LIST_DATA = [
    {"name": "李雷", "age": "33"},
    {"name": "韩梅梅", "age": "30"}
]


class TestParameter(testios.TestCase):
    """
    参数化demo
    """

    @testios.data(LIST_DATA)
    def test_list(self, param):
        logger.info(param)

    @testios.file_data(file='../data/data.json')
    def test_json(self, param):
        logger.info(param)

    @testios.file_data(file='../data/data.yml', key='names')
    def test_yaml(self, param):
        print(param)


if __name__ == '__main__':
    testios.main()
```

### Run the test

```python
import testios

testios.main()  # 当前文件，pycharm中需要把默认的单元测试框架改成unittests
testios.main(path="./")  # 当前目录
testios.main(path="./test_dir/")  # 指定目录
testios.main(path="./test_dir/test_api.py")  # 指定特定文件
testios.main(path="./test_dir/test_api.py::TestCaseClass:test_case1") # 指定特定用例
```

### 感谢

感谢从以下项目中得到思路和帮助。

* [seldom](https://github.com/SeldomQA/seldom)
  
* [facebook-wda](https://github.com/openatx/facebook-wda)

* [opencv](https://github.com/opencv/opencv-python)

* [easyocr](https://github.com/JaidedAI/EasyOCR)

## 高级用法

### 随机测试数据

测试数据是测试用例的重要部分，有时不能把测试数据写死在测试用例中，比如注册新用户，一旦执行过用例那么测试数据就已经存在了，所以每次执行注册新用户的数据不能是一样的，这就需要随机生成一些测试数据。

testios 提供了随机获取测试数据的方法。

```python
import testios
from testios import testdata


class TestYou(testios.TestCase):
    
    def test_case(self):
        """a simple tests case """
        word = testdata.get_word()
        print(word)
        
if __name__ == '__main__':
    testios.main()
```

通过`get_word()` 随机获取一个单词，然后对这个单词进行搜索。

**更多的方法**

```python
from testios.testdata import *
# 随机一个名字
print("名字：", first_name())
print("名字(男)：", first_name(gender="male"))
print("名字(女)：", first_name(gender="female"))
print("名字(中文男)：", first_name(gender="male", language="zh"))
print("名字(中文女)：", first_name(gender="female", language="zh"))
# 随机一个姓
print("姓:", last_name())
print("姓(中文):", last_name(language="zh"))
# 随机一个姓名
print("姓名:", username())
print("姓名(中文):", username(language="zh"))
# 随机一个生日
print("生日:", get_birthday())
print("生日字符串:", get_birthday(as_str=True))
print("生日年龄范围:", get_birthday(start_age=20, stop_age=30))
# 日期
print("日期(当前):", get_date())
print("日期(昨天):", get_date(-1))
print("日期(明天):", get_date(1))
# 数字
print("数字(8位):", get_digits(8))
# 邮箱
print("邮箱:", get_email())
# 浮点数
print("浮点数:", get_float())
print("浮点数范围:", get_float(min_size=1.0, max_size=2.0))
# 随机时间
print("当前时间:", get_now_datetime())
print("当前时间(格式化字符串):", get_now_datetime(strftime=True))
print("未来时间:", get_future_datetime())
print("未来时间(格式化字符串):", get_future_datetime(strftime=True))
print("过去时间:", get_past_datetime())
print("过去时间(格式化字符串):", get_past_datetime(strftime=True))
# 随机数据
print("整型:", get_int())
print("整型32位:", get_int32())
print("整型64位:", get_int64())
print("MD5:", get_md5())
print("UUID:", get_uuid())
print("单词:", get_word())
print("单词组(3个):", get_words(3))
print("手机号:", get_phone())
print("手机号(移动):", get_phone(operator="mobile"))
print("手机号(联通):", get_phone(operator="unicom"))
print("手机号(电信):", get_phone(operator="telecom"))
```

* 运行结果

```shell
名字： Hayden
名字（男）： Brantley
名字（女）： Julia
名字（中文男）： 觅儿
名字（中文女）： 若星
姓: Lee
姓（中文）: 白
姓名: Genesis
姓名（中文）: 廉高义
生日: 2000-03-11
生日字符串: 1994-11-12
生日年龄范围: 1996-01-12
日期（当前）: 2022-09-17
日期（昨天）: 2022-09-16
日期（明天）: 2022-09-18
数字(8位): 48285099
邮箱: melanie@yahoo.com
浮点数: 1.5315717275531858e+308
浮点数范围: 1.6682402084146244
当前时间: 2022-09-17 23:33:22.736031
当前时间(格式化字符串): 2022-09-17 23:33:22
未来时间: 2054-05-02 11:33:47.736031
未来时间(格式化字符串): 2070-08-28 16:38:45
过去时间: 2004-09-03 12:56:23.737031
过去时间(格式化字符串): 2006-12-06 07:58:37
整型: 7831034423589443450
整型32位: 1119927937
整型64位: 3509365234787490389
MD5: d0f6c6abbfe1cfeea60ecfdd1ef2f4b9
UUID: 5fd50475-2723-4a36-a769-1d4c9784223a
单词: habitasse
单词组（3个）: уж pede. metus.
手机号: 13171039843
手机号(移动): 15165746029
手机号(联通): 16672812525
手机号(电信): 17345142737
```

### 用例的依赖

**depend**

`depend` 装饰器用来设置依赖的用例。

```python
import testios
from testios import depend


class TestDepend(testios.TestCase):
    
    @depend(name='test_001')
    def test_001(self):
        print("test_001")
        
    @depend("test_001", name='test_002')
    def test_002(self):
        print("test_002")
        
    @depend(["test_001", "test_002"])
    def test_003(self):
        print("test_003")
        
if __name__ == '__main__':
    testios.main()
```

* 被依赖的用例需要用name定义被依赖的名称，因为本装饰器是基于pytest.mark.dependency，它会出现识别不了被装饰的方法名的情况
  ，所以通过name强制指定最为准确
  ```@depend(name='test_001')```
* `test_002` 依赖于 `test_001` , `test_003`又依赖于`test_002`。当被依赖的用例，错误、失败、跳过，那么依赖的用例自动跳过。
* 如果依赖多个用例，传入一个list即可
```@depend(['test_001', 'test_002'])```
  
### 发送邮件

```shell script
pip install yagmail==0.15.293
```

```python
import testios
from testios.utils.mail import Mail


if __name__ == '__main__':
    testios.main()
    mail = Mail(host='xx.com', user='xx@xx.com', password='xxx')
    mail.send_report(title='Demo项目测试报告', report_url='https://www.baidu.com', to_list=['xx@xx.com'])
```

- title：邮件标题
- report_url: 测试报告的url
- to_list: 接收报告的用户列表


### 发送钉钉

```python
import testios
from testios.utils.dingtalk import DingTalk


if __name__ == '__main__':
    testios.main()
    dd = DingTalk(secret='xxx',
                  url='xxx')
    dd.send_report(msg_title='Demo测试消息', report_url='https://www.baidu.com')
```

- `secret`: 如果钉钉机器人安全设置了签名，则需要传入对应的密钥。
- `url`: 钉钉机器人的Webhook链接
- `msg_title`: 消息标题
- `report_url`: 测试报告url



