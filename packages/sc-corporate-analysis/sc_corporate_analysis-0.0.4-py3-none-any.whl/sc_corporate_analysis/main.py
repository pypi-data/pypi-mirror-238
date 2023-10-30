# The MIT License (MIT)
#
# Copyright (c) 2022 Scott Lau
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
import os

import pandas as pd
from sc_utilities import Singleton
from sc_utilities import log_init

log_init()

from sc_config import ConfigUtils
from sc_corporate_analysis.utils.manifest_utils import ManifestUtils
from sc_corporate_analysis import PROJECT_NAME, __version__
from sc_corporate_analysis.summary.branch_summary_analyzer import BranchSummaryAnalyzer
from sc_corporate_analysis.analyzer.common_manager_deposit_analyzer import CommonManagerDepositAnalyzer
from sc_corporate_analysis.analyzer.manager_deposit_analyzer import ManagerDepositAnalyzer
import argparse


class Runner(metaclass=Singleton):

    def __init__(self):
        project_name = PROJECT_NAME
        ConfigUtils.clear(project_name)
        self._config = ConfigUtils.get_config(project_name)
        # 生成的目标Excel文件存放路径
        self._target_directory = self._config.get("corporate.target_directory")
        # 目标文件名称
        self._target_filename = self._config.get("corporate.target_filename")
        # 生成的Excel中按客户经理汇总的Sheet的名称
        self._target_manager_summary_sheet_name = self._config.get("corporate.target_manager_summary_sheet_name")
        # 生成的Excel中按账户汇总的Sheet的名称
        self._target_account_summary_sheet_name = self._config.get("corporate.target_account_summary_sheet_name")
        # 生成的Excel中按客户经理汇总的Sheet的名称
        self._target_branch_summary_sheet_name = self._config.get("corporate.target_branch_summary_sheet_name")

    def run(self, *, args):
        logging.getLogger(__name__).info("arguments {}".format(args))
        logging.getLogger(__name__).info("program {} version {}".format(PROJECT_NAME, __version__))
        logging.getLogger(__name__).debug("configurations {}".format(self._config.as_dict()))

        # 加载花名册相关配置
        result = self._load_manifest_stuff()
        if result != 0:
            return result

        target_filename_full_path = os.path.join(self._target_directory, self._target_filename)
        # 如果文件已经存在，则删除
        if os.path.exists(target_filename_full_path):
            logging.getLogger(__name__).info("删除输出文件：{} ".format(target_filename_full_path))
            try:
                os.remove(target_filename_full_path)
            except Exception as e:
                logging.getLogger(__name__).error("删除文件 {} 失败：{} ".format(target_filename_full_path, e))
                return 1
        logging.getLogger(__name__).info("输出文件：{} ".format(target_filename_full_path))

        with pd.ExcelWriter(target_filename_full_path) as excel_writer:
            summary_analyzer_list: list = list()
            target_column_list: list = list()
            # 分析客户经理汇总
            manager_summary_analyzer_list, manager_summary_result, column_list = \
                self._manager_summary_analysis(excel_writer)
            summary_analyzer_list.extend(manager_summary_analyzer_list)
            target_column_list.extend(column_list)
            # 分析公共经理汇总
            common_summary_analyzer_list, common_manager_summary_result, common_column_list = \
                self._common_manager_summary_analysis(excel_writer)
            summary_analyzer_list.extend(common_summary_analyzer_list)
            target_column_list.extend(common_column_list)
            # 分析机构汇总
            branch_summary_analyzer_list = self._branch_summary_analysis(
                excel_writer,
                manager_summary_result,
                common_manager_summary_result,
                target_column_list
            )
            # 输出原Excel数据
            self._write_original_excel_data(branch_summary_analyzer_list, summary_analyzer_list)
        logging.getLogger(__name__).info("结束数据分析...")
        return 0

    def _load_manifest_stuff(self):
        try:
            ManifestUtils.set_config(self._config)
            # 加载花名册
            ManifestUtils.load_manifest()
            return 0
        except Exception as error:
            logging.getLogger(__name__).error("加载花名册相关信息失败：{}".format(error))
            return 1

    def _manager_summary_analysis(self, excel_writer):
        manager_summary_analyzer_list = [
            # 客户经理存款统计分析
            ManagerDepositAnalyzer(config=self._config, excel_writer=excel_writer),
        ]
        # 按客户经理汇总结果
        manifest_data = ManifestUtils.get_manifest_df().copy()
        manager_summary_result = pd.DataFrame()
        previous_data = pd.DataFrame()
        # 输出列清单列表
        target_column_list = list()
        logging.getLogger(__name__).info("按客户经理分析...")
        for analyzer in manager_summary_analyzer_list:
            try:
                manager_summary_result = analyzer.analysis(
                    manifest_data=manifest_data,
                    previous_data=previous_data,
                )
                previous_data = manager_summary_result
                target_column_list.extend(analyzer.get_target_columns())
            except Exception as e:
                logging.getLogger(__name__).exception("分析 {} 时出错".format(analyzer.get_business_type()), exc_info=e)
        if not manager_summary_result.empty:
            # 没有业绩的显示0
            manager_summary_result.fillna(0, inplace=True)
            manager_summary_result.to_excel(excel_writer=excel_writer, index=False,
                                            sheet_name=self._target_manager_summary_sheet_name)
        return manager_summary_analyzer_list, manager_summary_result, target_column_list

    def _common_manager_summary_analysis(self, excel_writer):
        manager_summary_analyzer_list = [
            # 公共客户经理存款统计分析
            CommonManagerDepositAnalyzer(config=self._config, excel_writer=excel_writer),
        ]
        # 按客户经理汇总结果
        manifest_data = ManifestUtils.get_account_dataframe().copy()
        manager_summary_result = pd.DataFrame()
        previous_data = pd.DataFrame()
        # 输出列清单列表
        target_column_list = list()
        logging.getLogger(__name__).info("按公共客户经理分析...")
        for analyzer in manager_summary_analyzer_list:
            try:
                manager_summary_result = analyzer.analysis(
                    manifest_data=manifest_data,
                    previous_data=previous_data,
                )
                previous_data = manager_summary_result
                target_column_list.extend(analyzer.get_target_columns())
            except Exception as e:
                logging.getLogger(__name__).exception("分析 {} 时出错".format(analyzer.get_business_type()), exc_info=e)
        if not manager_summary_result.empty:
            # 没有业绩的显示0
            manager_summary_result.fillna(0, inplace=True)
            manager_summary_result.to_excel(excel_writer=excel_writer, index=False,
                                            sheet_name=self._target_account_summary_sheet_name)
        return manager_summary_analyzer_list, manager_summary_result, target_column_list

    def _branch_summary_analysis(
            self, excel_writer, manager_summary_result, account_summary_result, target_column_list
    ):
        branch_summary_analyzer_list = [
            # 机构汇总
            BranchSummaryAnalyzer(
                config=self._config,
                manager_summary=manager_summary_result,
                account_summary=account_summary_result,
                target_column_list=target_column_list,
                excel_writer=excel_writer,
            ),
        ]
        # 唯一的机构清单
        manifest_data = pd.DataFrame(
            data=set(ManifestUtils.get_manifest_df()[ManifestUtils.get_branch_column_name()]),
            columns=[ManifestUtils.get_branch_column_name()],
            dtype=str
        )
        branch_summary_result = pd.DataFrame()
        logging.getLogger(__name__).info("按机构汇总分析...")
        previous_data = pd.DataFrame()
        # 按机构汇总结果
        for analyzer in branch_summary_analyzer_list:
            try:
                branch_summary_result = analyzer.analysis(
                    manifest_data=manifest_data,
                    previous_data=previous_data,
                )
                previous_data = branch_summary_result
            except Exception as e:
                logging.getLogger(__name__).exception("分析 {} 时出错".format(analyzer.get_business_type()), exc_info=e)
        if not branch_summary_result.empty:
            # 没有业绩的显示0
            branch_summary_result.fillna(0, inplace=True)
            # 添加机构合计行
            branch_summary_result.set_index(ManifestUtils.get_branch_column_name(), inplace=True)
            branch_summary_result.loc["合计"] = branch_summary_result.apply(lambda x: x.sum())
            branch_summary_result.reset_index(inplace=True)
            # 输出到Excel
            branch_summary_result.to_excel(excel_writer=excel_writer, index=False,
                                           sheet_name=self._target_branch_summary_sheet_name)
        return branch_summary_analyzer_list

    def _write_original_excel_data(self, branch_summary_analyzer_list, manager_summary_analyzer_list):
        logging.getLogger(__name__).info("输出源数据到Excel...")
        # 输出源数据到Excel
        for analyzer in manager_summary_analyzer_list + branch_summary_analyzer_list:
            try:
                logging.getLogger(__name__).info(f"输出 {analyzer.get_business_type()}...")
                analyzer.write_origin_data()
            except Exception as e:
                logging.getLogger(__name__).exception(
                    "输出 {} 源数据到Excel时出错".format(analyzer.get_business_type()),
                    exc_info=e
                )


def main():
    try:
        parser = argparse.ArgumentParser(description='Python project')
        args = parser.parse_args()
        state = Runner().run(args=args)
    except Exception as e:
        logging.getLogger(__name__).exception('An error occurred.', exc_info=e)
        return 1
    else:
        return state
