from typing import Dict, List, Set, Tuple, Union, Any

import pysailfish.internal.MT_EA.mt4_const as mc
from pysailfish.internal.DataCtrl.MT4DataCtrl.MT4DataCtrl import MT4DataCtrl

class account_information(object):
    def __init__(self):
        self.__data_ctrl: MT4DataCtrl = None
        self.__fun_num_map: Dict[str, int] = dict()

    def init_component(self, data_ctrl: MT4DataCtrl, fun_num_map: Dict[str, int]):
        self.__data_ctrl = data_ctrl
        self.__fun_num_map = fun_num_map

    def account_info_double(self, property_id: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["AccountInfoDouble"]))
        self.__data_ctrl.add_data_to_msg(data=str(property_id))

        return self.__data_ctrl.receive_float_from_mt4()

    def account_info_integer(self, property_id: int) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["AccountInfoInteger"]))
        self.__data_ctrl.add_data_to_msg(data=str(property_id))

        return self.__data_ctrl.receive_int_from_mt4()

    def account_info_string(self, property_id: int) -> str:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["AccountInfoString"]))
        self.__data_ctrl.add_data_to_msg(data=str(property_id))

        return self.__data_ctrl.receive_string_from_mt4()

    def account_free_margin_check(self, symbol: str, cmd: int, volume: float) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["AccountFreeMarginCheck"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=int(cmd))
        self.__data_ctrl.add_data_to_msg(data=int(volume))

        return self.__data_ctrl.receive_float_from_mt4()
