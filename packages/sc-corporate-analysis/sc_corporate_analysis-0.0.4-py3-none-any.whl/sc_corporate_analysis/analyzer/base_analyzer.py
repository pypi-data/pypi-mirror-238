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

#  The MIT License (MIT)
#
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#
import logging

import pandas as pd
from config42 import ConfigManager
from sc_analyzer_base import BaseAnalyzer as SCBaseAnalyzer
from sc_utilities import calculate_column_index


class BaseAnalyzer(SCBaseAnalyzer):
    """
    分析基础类
    """

    def __init__(self, *, config: ConfigManager, excel_writer: pd.ExcelWriter):
        super().__init__(config=config, excel_writer=excel_writer)

    def write_detail_report(self, data: pd.DataFrame):
        # 不输出源报表的明细分析结果
        pass

    def _calculate_column_index_from_config(self, config: ConfigManager, key: str) -> int:
        initial_fund_amount_column_config = config.get(key)
        try:
            return calculate_column_index(initial_fund_amount_column_config)
        except ValueError as e:
            logging.getLogger(__name__).error("configuration {} is invalid".format(key), exc_info=e)
            raise e
