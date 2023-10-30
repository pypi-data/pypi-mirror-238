from typing import Dict, List, Set, Tuple, Union, Any
from datetime import datetime

import pysailfish.internal.MT_EA.mt4_const as mc
from pysailfish.internal.DataCtrl.MT4DataCtrl.MT4DataCtrl import MT4DataCtrl

class market_info(object):
    def __init__(self):
        self.__data_ctrl: MT4DataCtrl = None
        self.__fun_num_map: Dict[str, int] = dict()

    def init_component(self, data_ctrl: MT4DataCtrl, fun_num_map: Dict[str, int]):
        self.__data_ctrl = data_ctrl
        self.__fun_num_map = fun_num_map

    def market_info(self, symbol: str, type: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["MarketInfo"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(type))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def symbols_total(self, selected: bool) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["SymbolsTotal"]))
        self.__data_ctrl.add_data_to_msg(data=str(selected))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_int_from_mt4()

    def symbol_name(self, pos: int, selected: bool) -> str:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["SymbolName"]))
        self.__data_ctrl.add_data_to_msg(data=str(pos))
        self.__data_ctrl.add_data_to_msg(data=str(selected))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_string_from_mt4()

    def symbol_select(self, name: str, select: bool) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["SymbolSelect"]))
        self.__data_ctrl.add_data_to_msg(data=name)
        self.__data_ctrl.add_data_to_msg(data=str(select))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()

    def symbol_info_double(self, name: str, prop_id: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["SymbolInfoDouble"]))
        self.__data_ctrl.add_data_to_msg(data=name)
        self.__data_ctrl.add_data_to_msg(data=str(prop_id))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def symbol_info_integer(self, name: str, prop_id: int) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["SymbolInfoInteger"]))
        self.__data_ctrl.add_data_to_msg(data=name)
        self.__data_ctrl.add_data_to_msg(data=str(prop_id))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_int_from_mt4()

    def symbol_info_string(self, name: str, prop_id: int) -> str:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["SymbolInfoString"]))
        self.__data_ctrl.add_data_to_msg(data=name)
        self.__data_ctrl.add_data_to_msg(data=str(prop_id))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_string_from_mt4()

    def symbol_info_tick(self, symbol: str) -> Union[datetime, float, float, float, int]:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["SymbolInfoTick"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.send_message()

        str_ret: str = self.__data_ctrl.receive_string_from_mt4()

        parts = str_ret.split(",")

        return (datetime.strptime(parts[0], "%Y.%m.%d %H:%M:%S")
                , float(parts[1])
                , float(parts[2])
                , float(parts[3])
                , int(parts[4]))

    def symbol_info_session_quote(self, name: str, day_of_week: int, session_index: int) -> Union[datetime, datetime]:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["SymbolInfoSessionQuote"]))
        self.__data_ctrl.add_data_to_msg(data=name)
        self.__data_ctrl.add_data_to_msg(data=str(day_of_week))
        self.__data_ctrl.add_data_to_msg(data=str(session_index))
        self.__data_ctrl.send_message()

        str_ret: str = self.__data_ctrl.receive_string_from_mt4()

        parts = str_ret.split(",")

        return (datetime.strptime(parts[0], "%Y.%m.%d %H:%M:%S")
                , datetime.strptime(parts[1], "%Y.%m.%d %H:%M:%S"))

    def symbol_info_session_trade(self, name: str, day_of_week: int, session_index: int) -> Union[datetime, datetime]:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["SymbolInfoSessionTrade"]))
        self.__data_ctrl.add_data_to_msg(data=name)
        self.__data_ctrl.add_data_to_msg(data=str(day_of_week))
        self.__data_ctrl.add_data_to_msg(data=str(session_index))
        self.__data_ctrl.send_message()

        str_ret: str = self.__data_ctrl.receive_string_from_mt4()

        parts = str_ret.split(",")

        return (datetime.strptime(parts[0], "%Y.%m.%d %H:%M:%S")
                , datetime.strptime(parts[1], "%Y.%m.%d %H:%M:%S"))
