from typing import Dict, List, Set, Tuple, Union, Any
from datetime import datetime

import pysailfish.internal.MT_EA.mt4_const as mc
from pysailfish.internal.DataCtrl.MT4DataCtrl.MT4DataCtrl import MT4DataCtrl

# https://docs.mql4.com/objects/objectname
class chart_operations(object):
    def __init__(self):
        self.__data_ctrl: MT4DataCtrl = None
        self.__fun_num_map: Dict[str, int] = dict()

    def init_component(self, data_ctrl: MT4DataCtrl, fun_num_map: Dict[str, int]):
        self.__data_ctrl = data_ctrl
        self.__fun_num_map = fun_num_map

    def chart_apply_template(self, **kwargs) -> bool:
        return None

    def chart_save_template(self, **kwargs) -> bool:
        return None

    def chart_window_find_001(self, **kwargs) -> int:
        return None

    def chart_window_find_002(self, **kwargs) -> int:
        return None

    def chart_time_price_to_xy(self, **kwargs) -> bool:
        return None

    def chart_xy_to_time_price(self, **kwargs) -> bool:
        return None

    def chart_open(self, **kwargs) -> int:
        return None

    def chart_first(self) -> int:
        return None

    def chart_next(self, **kwargs) -> int:
        return None

    def chart_close(self, **kwargs) -> bool:
        return None

    def chart_symbol(self, **kwargs) -> str:
        return None

    def chart_period(self, **kwargs) -> int:
        return None

    def chart_redraw(self, **kwargs) -> None:
        return None

    def chart_set_double(self, **kwargs) -> bool:
        return None

    def chart_set_integer_001(self, **kwargs) -> bool:
        return None

    def chart_set_integer_002(self, **kwargs) -> bool:
        return None

    def chart_set_string(self, **kwargs) -> bool:
        return None

    def chart_get_double_001(self, **kwargs) -> float:
        return None

    def chart_get_double_002(self, **kwargs) -> bool:
        return None

    def chart_get_integer_001(self, **kwargs) -> int:
        return None

    def chart_get_integer_002(self, **kwargs) -> bool:
        return None

    def chart_get_string_001(self, **kwargs) -> str:
        return None

    def chart_get_string_002(self, **kwargs) -> bool:
        return None

    def chart_navigate(self, **kwargs) -> bool:
        return None

    def chart_id(self) -> int:
        return None

    def chart_indicator_delete(self, **kwargs) -> bool:
        return None

    def chart_indicator_name(self, **kwargs) -> str:
        return None

    def chart_indicators_total(self, **kwargs) -> int:
        return None

    def chart_window_on_dropped(self) -> int:
        return None

    def chart_price_on_dropped(self) -> float:
        return None

    def chart_time_on_dropped(self) -> datetime:
        return None

    def chart_x_on_dropped(self) -> int:
        return None

    def chart_y_on_dropped(self) -> int:
        return None

    def chart_set_symbol_period(self, chart_id: int, symbol: str, period: int) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ChartSetSymbolPeriod"]))
        self.__data_ctrl.add_data_to_msg(data=str(chart_id))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(period))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()

    def chart_screen_shot(self, **kwargs) -> bool:
        return None

    def period(self) -> int:
        return None

    def symbol(self) -> str:
        return None

    def window_bars_per_chart(self) -> int:
        return None

    def window_expert_name(self) -> str:
        return None

    def window_find(self, **kwargs) -> int:
        return None
