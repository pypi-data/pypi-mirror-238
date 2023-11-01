import allure  # pip install allure-pytest -i https://mirrors.aliyun.com/pypi/simple/


def report_screenshot(driver, out):
    """
        从result对象out获取调用结果的测试报告，返回一个report对象,

        report对象的属性
        包括when（setup, call, teardown三个值）、nodeid(测试用例的名字)、
        outcome(用例的执行结果，passed,failed)
    """

    report = out.get_result()  # 返回一个report对象

    # 仅仅获取用例call阶段的执行结果，不包含 setup/teardown
    if report.when == "call":
        # 获取用例call执行结果为失败的情况
        xfail = hasattr(report, "wasxfail")  # hasattr方法会：返回对象是否具有给定名称的属性

        # 如果测试用例被跳过且标记为预期失败，或者测试用例执行失败且不是预期失败
        if (report.skipped and xfail) or (report.failed and not xfail):
            # 添加allure报告截图
            with allure.step("添加失败截图......"):
                # 使用allure自带的添加附件的方法,三个参数分别为：源文件、文件名、文件类型
                allure.attach(driver.get_screenshot_as_png(),
                              "失败截图", allure.attachment_type.PNG)

        elif report.passed:
            # 如果测试用例执行通过，添加 allure 报告截图
            with allure.step("添加成功截图......"):
                # 使用 allure 自带的添加附件的方法,三个参数分别为：源文件、文件名、文件类型
                allure.attach(driver.get_screenshot_as_png(),
                              "成功截图", allure.attachment_type.PNG)
