from typing import Dict, List, Set, Tuple, Union, Any
from datetime import datetime

import pysailfish.internal.MT_EA.mt4_const as mc
from pysailfish.internal.DataCtrl.MT4DataCtrl.MT4DataCtrl import MT4DataCtrl

# https://docs.mql4.com/objects/objectname
class object_functions(object):
    def __init__(self):
        self.__data_ctrl: MT4DataCtrl = None
        self.__fun_num_map: Dict[str, int] = dict()

    def init_component(self, data_ctrl: MT4DataCtrl, fun_num_map: Dict[str, int]):
        self.__data_ctrl = data_ctrl
        self.__fun_num_map = fun_num_map

    # chart_id: int, object_name: str, object_type: int, sub_window: int, time1: datetime, price1: float ... timeN: datetime, priceN: float
    def object_create_001(self, **kwargs) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectCreate_001"]))
        for k, v in kwargs.items():
            if isinstance(v, datetime):
                self.__data_ctrl.add_data_to_msg(data=v.strftime("%Y.%m.%d %H:%M:%S"))
            else:
                self.__data_ctrl.add_data_to_msg(data=v)
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()

    def object_create_002(self
                          , object_name: str
                          , object_type: int
                          , sub_window: int
                          , time1: datetime
                          , price1: float
                          , time2: datetime = datetime(1970, 1, 1, 0, 0, 0)
                          , price2: float = 0
                          , time3: datetime = datetime(1970, 1, 1, 0, 0, 0)
                          , price3: float = 0) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectCreate_002"]))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.add_data_to_msg(data=object_type)
        self.__data_ctrl.add_data_to_msg(data=str(sub_window))
        self.__data_ctrl.add_data_to_msg(data=time1.strftime("%Y.%m.%d %H:%M:%S"))
        self.__data_ctrl.add_data_to_msg(data=str(price1))
        self.__data_ctrl.add_data_to_msg(data=time2.strftime("%Y.%m.%d %H:%M:%S"))
        self.__data_ctrl.add_data_to_msg(data=str(price2))
        self.__data_ctrl.add_data_to_msg(data=time3.strftime("%Y.%m.%d %H:%M:%S"))
        self.__data_ctrl.add_data_to_msg(data=str(price3))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()

    def object_name(self, object_index: int) -> str:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectName"]))
        self.__data_ctrl.add_data_to_msg(data=str(object_index))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_string_from_mt4()

    def object_delete_001(self, chart_id: int, object_name: str) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectDelete_001"]))
        self.__data_ctrl.add_data_to_msg(data=str(chart_id))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()

    def object_delete_002(self, object_name: str) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectDelete_002"]))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()

    def objects_delete_all_001(self, chart_id: int, sub_window: int = -1, object_type: int = -1) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectsDeleteAll_001"]))
        self.__data_ctrl.add_data_to_msg(data=str(chart_id))
        self.__data_ctrl.add_data_to_msg(data=str(sub_window))
        self.__data_ctrl.add_data_to_msg(data=str(object_type))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_int_from_mt4()

    def objects_delete_all_002(self, sub_window: int = -1, object_type: int = -1) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectsDeleteAll_002"]))
        self.__data_ctrl.add_data_to_msg(data=str(sub_window))
        self.__data_ctrl.add_data_to_msg(data=str(object_type))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_int_from_mt4()

    def objects_delete_all_003(self, chart_id: int, prefix: str, sub_window: int = -1, object_type: int = -1) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectsDeleteAll_003"]))
        self.__data_ctrl.add_data_to_msg(data=str(chart_id))
        self.__data_ctrl.add_data_to_msg(data=prefix)
        self.__data_ctrl.add_data_to_msg(data=str(sub_window))
        self.__data_ctrl.add_data_to_msg(data=str(object_type))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_int_from_mt4()

    def object_find_001(self, chart_id: int, object_name: str) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectFind_001"]))
        self.__data_ctrl.add_data_to_msg(data=str(chart_id))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_int_from_mt4()

    def object_find_002(self, object_name: str) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectFind_002"]))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_int_from_mt4()

    def object_get_time_by_value(self, chart_id: int, object_name: str, value: float, line_id: int = 0) -> datetime:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectGetTimeByValue"]))
        self.__data_ctrl.add_data_to_msg(data=str(chart_id))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.add_data_to_msg(data=str(value))
        self.__data_ctrl.add_data_to_msg(data=str(line_id))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_datetime_from_mt4()

    def object_get_value_by_time(self, chart_id: int, object_name: str, time: datetime, line_id: int = 0) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectGetValueByTime"]))
        self.__data_ctrl.add_data_to_msg(data=str(chart_id))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.add_data_to_msg(data=time.strftime("%Y.%m.%d %H:%M:%S"))
        self.__data_ctrl.add_data_to_msg(data=str(line_id))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def object_move(self, object_name: str, point_index: int, time: datetime, price: float) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectMove"]))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.add_data_to_msg(data=str(point_index))
        self.__data_ctrl.add_data_to_msg(data=time.strftime("%Y.%m.%d %H:%M:%S"))
        self.__data_ctrl.add_data_to_msg(data=str(price))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()

    def objects_total_001(self, chart_id: int, sub_window: int = -1, type: int = -1) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectsTotal_001"]))
        self.__data_ctrl.add_data_to_msg(data=str(chart_id))
        self.__data_ctrl.add_data_to_msg(data=str(sub_windows))
        self.__data_ctrl.add_data_to_msg(data=str(type))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_int_from_mt4()

    def objects_total_002(self, type: int = -1) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectsTotal_002"]))
        self.__data_ctrl.add_data_to_msg(data=str(type))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_int_from_mt4()

    def object_get_double(self, chart_id: int, object_name: str, prop_id: int, prop_modifier: int = 0) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectGetDouble"]))
        self.__data_ctrl.add_data_to_msg(data=str(chart_id))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.add_data_to_msg(data=str(prop_id))
        self.__data_ctrl.add_data_to_msg(data=str(prop_modifier))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def object_get_integer(self, chart_id: int, object_name: str, prop_id: int, prop_modifier: int = 0) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectGetInteger"]))
        self.__data_ctrl.add_data_to_msg(data=str(chart_id))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.add_data_to_msg(data=str(prop_id))
        self.__data_ctrl.add_data_to_msg(data=str(prop_modifier))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_int_from_mt4()

    def object_get_string(self, chart_id: int, object_name: str, prop_id: int, prop_modifier: int = 0) -> str:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectGetString"]))
        self.__data_ctrl.add_data_to_msg(data=str(chart_id))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.add_data_to_msg(data=str(prop_id))
        self.__data_ctrl.add_data_to_msg(data=str(prop_modifier))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_string_from_mt4()

    def object_set_double_001(self, chart_id: int, object_name: str, prop_id: int, prop_value: float) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectSetDouble_001"]))
        self.__data_ctrl.add_data_to_msg(data=str(chart_id))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.add_data_to_msg(data=str(prop_id))
        self.__data_ctrl.add_data_to_msg(data=str(prop_value))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()

    def object_set_double_002(self, chart_id: int, object_name: str, prop_id: int, prop_modifier: int, prop_value: float) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectSetDouble_002"]))
        self.__data_ctrl.add_data_to_msg(data=str(chart_id))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.add_data_to_msg(data=str(prop_id))
        self.__data_ctrl.add_data_to_msg(data=str(prop_modifier))
        self.__data_ctrl.add_data_to_msg(data=str(prop_value))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()

    def object_set_integer_001(self, chart_id: int, object_name: str, prop_id: int, prop_value: float) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectSetInteger_001"]))
        self.__data_ctrl.add_data_to_msg(data=str(chart_id))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.add_data_to_msg(data=str(prop_id))
        self.__data_ctrl.add_data_to_msg(data=str(prop_value))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()

    def object_set_integer_002(self, chart_id: int, object_name: str, prop_id: int, prop_modifier: int, prop_value: float) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectSetInteger_002"]))
        self.__data_ctrl.add_data_to_msg(data=str(chart_id))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.add_data_to_msg(data=str(prop_id))
        self.__data_ctrl.add_data_to_msg(data=str(prop_modifier))
        self.__data_ctrl.add_data_to_msg(data=str(prop_value))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()

    def object_set_string_001(self, chart_id: int, object_name: str, prop_id: int, prop_value: float) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectSetString_001"]))
        self.__data_ctrl.add_data_to_msg(data=str(chart_id))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.add_data_to_msg(data=str(prop_id))
        self.__data_ctrl.add_data_to_msg(data=str(prop_value))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()

    def object_set_string_002(self, chart_id: int, object_name: str, prop_id: int, prop_modifier: int, prop_value: float) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectSetString_002"]))
        self.__data_ctrl.add_data_to_msg(data=str(chart_id))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.add_data_to_msg(data=str(prop_id))
        self.__data_ctrl.add_data_to_msg(data=str(prop_modifier))
        self.__data_ctrl.add_data_to_msg(data=str(prop_value))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()

    def text_set_font(self, name: str, size: int, flags: int = 0, orientation: int = 0) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["TextSetFont"]))
        self.__data_ctrl.add_data_to_msg(data=name)
        self.__data_ctrl.add_data_to_msg(data=str(size))
        self.__data_ctrl.add_data_to_msg(data=str(flags))
        self.__data_ctrl.add_data_to_msg(data=str(orientation))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()

    # def text_out(self, text: str, x: int, y: int, anchor: int, ) -> bool:
    #     self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["TextSetFont"]))
    #     self.__data_ctrl.add_data_to_msg(data=name)
    #     self.__data_ctrl.add_data_to_msg(data=str(size))
    #     self.__data_ctrl.add_data_to_msg(data=str(flags))
    #     self.__data_ctrl.add_data_to_msg(data=str(orientation))
    #     self.__data_ctrl.send_message()

    #     return self.__data_ctrl.receive_bool_from_mt4()

    def text_get_size(self, text: str) -> Union[int, int]:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["TextGetSize"]))
        self.__data_ctrl.add_data_to_msg(data=text)
        self.__data_ctrl.send_message()

        str_ret: str = self.__data_ctrl.receive_string_from_mt4()
        parts = str_ret.split("-")

        return (int(parts[0]), int(parts[1])) # width, height

    def object_description(self, object_name: str) -> str:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectDescription"]))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_string_from_mt4()

    def object_get(self, object_name: str, index: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectGet"]))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.add_data_to_msg(data=str(index))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def object_get_fibo_description(self, object_name: str, index: int) -> str:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectGetFiboDescription"]))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.add_data_to_msg(data=str(index))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_string_from_mt4()

    def object_get_shift_by_value(self, object_name: str, value: float) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectGetShiftByValue"]))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.add_data_to_msg(data=str(value))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_int_from_mt4()

    def object_get_value_by_shift(self, object_name: str, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectGetValueByShift"]))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def object_set(self, object_name: str, index: int, vlaue: float) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectSet"]))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.add_data_to_msg(data=str(index))
        self.__data_ctrl.add_data_to_msg(data=str(value))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()

    def object_set_fibo_description(self, object_name: str, index: int, text: str) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectSetFiboDescription"]))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.add_data_to_msg(data=str(index))
        self.__data_ctrl.add_data_to_msg(data=text)
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()

    def object_set_text(self, object_name: str, text: str, font_size: int = 0, font_name: str = "", text_color: str = mc.clrBlack) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectSetText"]))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.add_data_to_msg(data=text)
        self.__data_ctrl.add_data_to_msg(data=str(font_size))
        self.__data_ctrl.add_data_to_msg(data=font_name)
        self.__data_ctrl.add_data_to_msg(data=text_color)
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()

    def object_type(self, object_name: str) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["ObjectType"]))
        self.__data_ctrl.add_data_to_msg(data=object_name)
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_int_from_mt4()
