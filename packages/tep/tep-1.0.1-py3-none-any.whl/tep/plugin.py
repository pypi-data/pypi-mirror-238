#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  dongfanger
@Date    :  8/14/2020 9:16 AM
@Desc    :  插件
"""
import inspect
import os

import time
import shutil

import allure_commons
from allure_commons.logger import AllureFileLogger
from allure_pytest.listener import AllureListener
from allure_pytest.plugin import cleanup_factory

from tep.config import Config, fixture_paths

# allure源文件临时目录，那一堆json文件，生成HTML报告会删除
allure_source_path = ".allure.source.temp"


def _tep_reports(config):
    """
    --tep-reports命令行参数不能和allure命令行参数同时使用，否则可能出错
    """
    if config.getoption("--tep-reports") and not config.getoption("allure_report_dir"):
        return True
    return False


def _is_master(config):
    """
    pytest-xdist分布式执行时，判断是主节点master还是子节点
    主节点没有workerinput属性
    """
    return not hasattr(config, 'workerinput')


class Plugin:
    reports_path = os.path.join(Config.project_root_dir, "reports")

    @staticmethod
    def pytest_addoption(parser):
        """
        allure测试报告 命令行参数
        """
        parser.addoption(
            "--tep-reports",
            action="store_const",
            const=True,
            help="Create tep allure HTML reports."
        )

    @staticmethod
    def pytest_configure(config):
        """
        这段代码源自：https://github.com/allure-framework/allure-python/blob/master/allure-pytest/src/plugin.py
        目的是生成allure源文件，用于生成HTML报告
        """
        if _tep_reports(config):
            if os.path.exists(allure_source_path):
                shutil.rmtree(allure_source_path)
            test_listener = AllureListener(config)
            config.pluginmanager.register(test_listener)
            allure_commons.plugin_manager.register(test_listener)
            config.add_cleanup(cleanup_factory(test_listener))

            clean = config.option.clean_alluredir
            file_logger = AllureFileLogger(allure_source_path, clean)  # allure_source
            allure_commons.plugin_manager.register(file_logger)
            config.add_cleanup(cleanup_factory(file_logger))

    @staticmethod
    def pytest_sessionfinish(session):
        """
        测试运行结束后生成allure报告
        """
        reports_path = os.path.join(Config.project_root_dir, "reports")
        if _tep_reports(session.config):
            if _is_master(session.config):  # 只在master节点才生成报告
                # 最近一份报告的历史数据，填充allure趋势图
                if os.path.exists(reports_path):
                    his_reports = os.listdir(reports_path)
                    if his_reports:
                        latest_report_history = os.path.join(reports_path, his_reports[-1], "history")
                        shutil.copytree(latest_report_history, os.path.join(allure_source_path, "history"))

                current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
                html_report_name = os.path.join(reports_path, "report-" + current_time)
                os.system(f"allure generate {allure_source_path} -o {html_report_name}  --clean")
                shutil.rmtree(allure_source_path)


def tep_plugins():
    caller = inspect.stack()[1]
    Config.project_root_dir = os.path.dirname(caller.filename)
    plugins = fixture_paths()  # +[其他插件]
    return plugins
