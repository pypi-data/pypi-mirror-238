#  The MIT License (MIT)
#
#  Copyright (c) 2022. Scott Lau
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


class CommonManagerDepositAnalyzer(BaseAnalyzer):
    """
    公共经理存款分析
    """

    def __init__(self, *, config: ConfigManager, excel_writer: pd.ExcelWriter):
        super().__init__(config=config, excel_writer=excel_writer)
        self._key_enabled = "corporate.deposit.common.enabled"
        self._key_business_type = "corporate.deposit.common.business_type"
        self._key_export_column_list = "corporate.deposit.common.sheet_config.export_column_list"

    def _read_config(self, *, config: ConfigManager):
        self._source_file_path = config.get("corporate.deposit.common.source_file_path")
        self._sheet_name = config.get("corporate.deposit.common.sheet_name")
        self._header_row = config.get("corporate.deposit.common.sheet_config.header_row")
        self._branch_filter = config.get("corporate.deposit.common.branch_filter")

        self._category_filters: list = list()
        category_filters = config.get("corporate.deposit.common.category_filters")
        if category_filters is not None and type(category_filters) == list:
            self._category_filters.extend(category_filters)
        # 姓名列索引
        self._name_column = self._calculate_column_index_from_config(
            config, "corporate.deposit.common.sheet_config.name_column"
        )
        # 账号列索引
        self._account_column = self._calculate_column_index_from_config(
            config, "corporate.deposit.common.sheet_config.account_column"
        )
        # 所属机构列索引
        self._account_branch_column = self._calculate_column_index_from_config(
            config, "corporate.deposit.common.sheet_config.account_branch_column"
        )
        # 科目列索引
        self._category_column = self._calculate_column_index_from_config(
            config, "corporate.deposit.common.sheet_config.category_column"
        )
        # 需要统计的列的索引与输出列名对
        key = "corporate.deposit.common.sheet_config.value_column_pairs"
        self._init_value_column_config(config, key)

    def _read_src_file(self) -> pd.DataFrame:
        logging.getLogger(__name__).info("读取源文件：{}".format(self._source_file_path))
        data = pd.read_excel(self._source_file_path, sheet_name=self._sheet_name, header=self._header_row, thousands=",")
        self._category_column_name = data.columns[self._category_column]
        self._name_column_name = data.columns[self._name_column]
        self._account_branch_column_name = data.columns[self._account_branch_column]
        self._account_column_name = data.columns[self._account_column]
        self._init_value_column_pairs(data)
        return data

    def _rename_target_columns(self, *, data: pd.DataFrame) -> pd.DataFrame:
        df = data.rename(columns=self._value_column_pairs)
        return df

    def _pre_pivot_table(self, *, data: pd.DataFrame) -> pd.DataFrame:
        # 过滤所属机构
        criterion = data[self._account_branch_column_name].map(lambda x: str(x).startswith(self._branch_filter))
        data = data[criterion].copy()
        # 过滤科目
        criterion = data[self._category_column_name].map(lambda x: x not in self._category_filters)
        data = data[criterion].copy()
        return data

    def _pivot_table(self, *, data: pd.DataFrame) -> pd.DataFrame:
        index_columns = [
            self._account_column_name,
        ]
        value_columns = self._get_value_columns()
        logging.getLogger(__name__).info("按{} 透视数据项：{}".format(
            index_columns,
            value_columns,
        ))
        if data.empty:
            return pd.DataFrame(columns=index_columns + value_columns)
        table = pd.pivot_table(data,
                               values=value_columns,
                               index=index_columns,
                               aggfunc=np.sum, fill_value=0)
        return table

    def _after_pivot_table(self, *, data: pd.DataFrame) -> pd.DataFrame:
        data.reset_index(inplace=True)
        return data

    def _merge_with_manifest(self, *, manifest_data: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
        logging.getLogger(__name__).info("与花名册合并...")
        merge_result = manifest_data.merge(
            data,
            how="outer",
            left_on=[ManifestUtils.get_account_column_name()],
            right_on=[self._account_column_name]
        )
        # 所属机构一列，如果值为空，则设置为分行公共
        branch_column_name = ManifestUtils.get_branch_column_name()
        merge_result.loc[
            merge_result[branch_column_name].isnull(),
            branch_column_name
        ] = ManifestUtils.get_common_branch_name()
        return merge_result

    def _add_target_columns(self) -> None:
        self._add_value_pair_target_columns()
