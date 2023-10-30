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

import pandas as pd
from config42 import ConfigManager
from sc_utilities import Singleton
from sc_utilities import calculate_column_index


class ManifestUtils(metaclass=Singleton):
    """
    花名册相关工具类
    """
    # 名单DataFrame
    _df: pd.DataFrame = None
    # 花名册姓名与所在部门对应关系DataFrame
    _dataframe: pd.DataFrame = None
    # 账户与所在部门对应关系DataFrame
    _account_df: pd.DataFrame = None
    _name_column_name: str = ""
    _branch_column_name: str = ""
    _account_column_name: str = ""
    _common_branch_name: str = ""
    _config = None

    @classmethod
    def calculate_column_index_from_config(cls, config: ConfigManager, key: str) -> int:
        initial_fund_amount_column_config = config.get(key)
        try:
            return calculate_column_index(initial_fund_amount_column_config)
        except ValueError as e:
            logging.getLogger(__name__).error("configuration {} is invalid".format(key), exc_info=e)
            raise e

    @classmethod
    def set_config(cls, config):
        cls._config = config

    @classmethod
    def get_data_frame(cls) -> pd.DataFrame:
        """
        花名册姓名与所在部门对应关系
        :return:
        """
        return cls._dataframe

    @classmethod
    def get_account_dataframe(cls) -> pd.DataFrame:
        return cls._account_df

    @classmethod
    def get_common_branch_name(cls) -> str:
        return cls._common_branch_name

    @classmethod
    def get_name_column_name(cls) -> str:
        """
        姓名列名
        :return: 姓名列名
        """
        return cls._name_column_name

    @classmethod
    def get_branch_column_name(cls) -> str:
        """
        所属机构列名
        :return: 所属机构列名
        """
        return cls._branch_column_name

    @classmethod
    def get_account_column_name(cls) -> str:
        """
        所属机构列名
        :return: 所属机构列名
        """
        return cls._account_column_name

    @classmethod
    def load_manifest(cls):
        """
        加载花名册
        :return:
        """
        config = cls._config
        src_file_path = config.get("manifest.source_file_path")
        sheet_name = config.get("manifest.sheet_name")
        common_manager_name = config.get("manifest.common_manager_name")
        cls._common_branch_name = config.get("manifest.common_branch_name")
        header_row = config.get("manifest.sheet_config.header_row")
        # 姓名列
        name_column = cls.calculate_column_index_from_config(config, "manifest.sheet_config.name_column")
        # 所属机构列
        branch_column = cls.calculate_column_index_from_config(config, "manifest.sheet_config.branch_column")
        # 所属机构列
        account_column = cls.calculate_column_index_from_config(config, "manifest.sheet_config.account_column")

        logging.getLogger(__name__).info("加载花名册：{}".format(src_file_path))
        df: pd.DataFrame = pd.read_excel(src_file_path, sheet_name=sheet_name, header=header_row)
        df = df.iloc[:, [name_column, branch_column, account_column]]
        cls._name_column_name = df.columns[0]
        cls._branch_column_name = df.columns[1]
        cls._account_column_name = df.columns[2]
        account_df = df.copy()
        criterion = account_df[cls._name_column_name].map(lambda x: x == common_manager_name)
        account_df = account_df.iloc[:, [account_column, branch_column]]
        account_df = account_df[criterion].copy()
        account_df = account_df.drop_duplicates()
        cls._account_df = account_df.copy()

        cls._dataframe = df.copy()
        name_branch_df = df[[cls._name_column_name, cls._branch_column_name]].copy()
        name_branch_df = name_branch_df.drop_duplicates()
        # 删除公共经理
        criterion = name_branch_df[cls._name_column_name].map(lambda x: x != common_manager_name)
        name_branch_df = name_branch_df[criterion].copy()
        cls._df = name_branch_df.copy()

    @classmethod
    def get_manifest_df(cls) -> pd.DataFrame:
        return cls._df
