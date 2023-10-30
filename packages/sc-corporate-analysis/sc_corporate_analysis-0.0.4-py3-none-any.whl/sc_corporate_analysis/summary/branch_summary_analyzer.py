#  The MIT License (MIT)
#
#  Copyright (c) corporate.deposit.common. Scott Lau
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import logging

import numpy as np
import pandas as pd
from config42 import ConfigManager

from sc_corporate_analysis.analyzer.base_analyzer import BaseAnalyzer
from sc_corporate_analysis.utils.manifest_utils import ManifestUtils


class BranchSummaryAnalyzer(BaseAnalyzer):
    """
    按机构汇总分析BranchSummaryAnalyzer
    """

    def __init__(self, *, config: ConfigManager, manager_summary: pd.DataFrame, account_summary: pd.DataFrame,
                 target_column_list: list,
                 excel_writer: pd.ExcelWriter):
        super().__init__(config=config, excel_writer=excel_writer)
        self._manager_summary = manager_summary
        self._account_summary = account_summary
        self._key_enabled = "corporate.branch_summary.enabled"
        self._key_business_type = "corporate.branch_summary.business_type"
        self._target_column_list = list()
        self._target_column_list.extend(target_column_list)

    def _enabled(self):
        """始终启用机构汇总分析"""
        return True

    def _read_config(self, *, config: ConfigManager):
        # 经营、消费类汇总
        self._business_type_summary_dict = config.get("corporate.branch_summary.business_type_summary")

    def _read_src_file(self) -> pd.DataFrame:
        # 去掉第一列，即经理姓名列
        df: pd.DataFrame = self._manager_summary.copy()
        df = df.iloc[:, 1:]
        table = pd.pivot_table(
            df,
            index=[ManifestUtils.get_branch_column_name()],
            aggfunc=np.sum,
            fill_value=0,
        )
        # 去掉第一列，即账号列
        df2: pd.DataFrame = self._account_summary.copy()
        df2 = df2.iloc[:, 1:]
        table2 = pd.pivot_table(
            df2,
            index=[ManifestUtils.get_branch_column_name()],
            aggfunc=np.sum,
            fill_value=0,
        )
        result = table.merge(table2, how="outer", on=ManifestUtils.get_branch_column_name())
        result.fillna(0, inplace=True)
        return result

    def _pivot_table(self, *, data: pd.DataFrame) -> pd.DataFrame:
        # 没有统计列，则不处理
        if len(self._target_column_list) == 0:
            return data
        table = pd.pivot_table(
            data, values=self._target_column_list,
            index=[ManifestUtils.get_branch_column_name()],
            aggfunc=np.sum,
            fill_value=0,
        )
        if len(self._target_column_list) > 0:
            # 添加个经小计、个消小计
            real_key_list = list()
            if self._business_type_summary_dict is not None:
                for sum_key, column_list in self._business_type_summary_dict.items():
                    real_column_list = list()
                    for column in column_list:
                        if column in self._target_column_list:
                            real_column_list.append(column)
                    key = sum_key + "小计"
                    real_key_list.append(key)
                    if len(real_column_list) > 0:
                        table[key] = table[real_column_list].apply(lambda x: x.sum(), axis=1)
                    else:
                        table[key] = 0
                    self._target_column_list.append(key)
            # 调整列的顺序，合计排两个小计的前面
            table = table[self._target_column_list]
        return table

    def _after_pivot_table(self, *, data: pd.DataFrame) -> pd.DataFrame:
        return data.reset_index()

    def _merge_with_manifest(self, *, manifest_data: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
        if data.empty:
            return data
        logging.getLogger(__name__).info("与机构清单合并...")
        merge_result = manifest_data.merge(
            data,
            how="outer",
            on=[ManifestUtils.get_branch_column_name()],
        )
        merge_result.fillna(0, inplace=True)
        return merge_result

    def write_origin_data(self):
        # 机构汇总不输出明细数据，否则会将真正的汇总给覆盖掉
        pass
