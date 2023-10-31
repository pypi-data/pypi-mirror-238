import testios


if __name__ == '__main__':
    # 执行多个用例文件，主程序入口
    testios.main(
        case_path='tests/test_ios.py',
        devices=['00008101-000E646A3C29003A'],
        pkg_name='com.qizhidao.company'
    )



