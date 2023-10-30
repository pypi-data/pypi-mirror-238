from typing import Dict, List, Set, Tuple, Union, Any

import pysailfish.internal.MT_EA.mt4_const as mc
from pysailfish.internal.DataCtrl.MT4DataCtrl.MT4DataCtrl import MT4DataCtrl

class common_functions(object):
    def __init__(self):
        self.__data_ctrl: MT4DataCtrl = None
        self.__fun_num_map: Dict[str, int] = dict()

    def init_component(self, data_ctrl: MT4DataCtrl, fun_num_map: Dict[str, int]):
        self.__data_ctrl = data_ctrl
        self.__fun_num_map = fun_num_map

    def get_datetime_from_mt(self, fun_name: str) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map[fun_name]))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_datetime_from_mt4()

    def get_int_from_mt(self, fun_name: str) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map[fun_name]))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_int_from_mt4()

    def get_float_from_mt(self, fun_name: str) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map[fun_name]))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def get_str_from_mt(self, fun_name: str) -> str:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map[fun_name]))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_string_from_mt4()

    def get_bool_from_mt(self, fun_name: str) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map[fun_name]))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()
