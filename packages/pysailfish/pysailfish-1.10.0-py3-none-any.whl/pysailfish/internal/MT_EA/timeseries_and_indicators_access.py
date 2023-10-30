from typing import Dict, List, Set, Tuple, Union, Any
from datetime import datetime

import pysailfish.internal.MT_EA.mt4_const as mc
from pysailfish.internal.DataCtrl.MT4DataCtrl.MT4DataCtrl import MT4DataCtrl

class timeseries_and_indicators_access(object):
    def __init__(self):
        self.__data_ctrl: MT4DataCtrl = None
        self.__fun_num_map: Dict[str, int] = dict()

    def init_component(self, data_ctrl: MT4DataCtrl, fun_num_map: Dict[str, int]):
        self.__data_ctrl = data_ctrl
        self.__fun_num_map = fun_num_map

    def series_info_integer(self, symbol_name: str, timeframe: int, prop_id: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["SeriesInfoInteger"]))
        self.__data_ctrl.add_data_to_msg(data=symbol_name)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(prop_id))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def copy_rates_001(self, symbol_name: str, timeframe: int, start_pos: int, count: int) -> List[Union[datetime, float, float, float, float, int, int, int]]:
        return self.__copy_001(symbol_name=symbol_name
                               , timeframe=timeframe
                               , start_pos=start_pos
                               , count=count
                               , fun_name="CopyRates_001"
                               , parse_fun=self.__copy_rates_common)

    def copy_rates_002(self, symbol_name: str, timeframe: int, start_time: datetime, count: int) -> List[Union[datetime, float, float, float, float, int, int, int]]:
        return self.__copy_002(symbol_name=symbol_name
                               , timeframe=timeframe
                               , start_time=start_time
                               , count=count
                               , fun_name="CopyRates_002"
                               , parse_fun=self.__copy_rates_common)

    def copy_rates_003(self, symbol_name: str, timeframe: int, start_time: datetime, end_time: datetime) -> List[Union[datetime, float, float, float, float, int, int, int]]:
        return self.__copy_003(symbol_name=symbol_name
                               , timeframe=timeframe
                               , start_time=start_time
                               , end_time=end_time
                               , fun_name="CopyRates_003"
                               , parse_fun=self.__copy_rates_common)

    def copy_time_001(self, symbol_name: str, timeframe: int, start_pos: int, count: int) -> List[datetime]:
        return self.__copy_001(symbol_name=symbol_name
                               , timeframe=timeframe
                               , start_pos=start_pos
                               , count=count
                               , fun_name="CopyTime_001"
                               , parse_fun=self.__copy_time_common)

    def copy_time_002(self, symbol_name: str, timeframe: int, start_time: datetime, count: int) -> List[datetime]:
        return self.__copy_002(symbol_name=symbol_name
                               , timeframe=timeframe
                               , start_time=start_time
                               , count=count
                               , fun_name="CopyTime_002"
                               , parse_fun=self.__copy_time_common)

    def copy_time_003(self, symbol_name: str, timeframe: int, start_time: datetime, end_time: datetime) -> List[datetime]:
        return self.__copy_003(symbol_name=symbol_name
                               , timeframe=timeframe
                               , start_time=start_time
                               , end_time=end_time
                               , fun_name="CopyTime_003"
                               , parse_fun=self.__copy_time_common)

    def copy_open_001(self, symbol_name: str, timeframe: int, start_pos: int, count: int) -> List[float]:
        return self.__copy_001(symbol_name=symbol_name
                               , timeframe=timeframe
                               , start_pos=start_pos
                               , count=count
                               , fun_name="CopyOpen_001"
                               , parse_fun=self.__copy_float_common)

    def copy_open_002(self, symbol_name: str, timeframe: int, start_time: datetime, count: int) -> List[float]:
        return self.__copy_002(symbol_name=symbol_name
                               , timeframe=timeframe
                               , start_time=start_time
                               , count=count
                               , fun_name="CopyOpen_002"
                               , parse_fun=self.__copy_float_common)

    def copy_open_003(self, symbol_name: str, timeframe: int, start_time: datetime, end_time: datetime) -> List[float]:
        return self.__copy_003(symbol_name=symbol_name
                               , timeframe=timeframe
                               , start_time=start_time
                               , end_time=end_time
                               , fun_name="CopyOpen_003"
                               , parse_fun=self.__copy_float_common)

    def copy_high_001(self, symbol_name: str, timeframe: int, start_pos: int, count: int) -> List[float]:
        return self.__copy_001(symbol_name=symbol_name
                               , timeframe=timeframe
                               , start_pos=start_pos
                               , count=count
                               , fun_name="CopyHigh_001"
                               , parse_fun=self.__copy_float_common)

    def copy_high_002(self, symbol_name: str, timeframe: int, start_time: datetime, count: int) -> List[float]:
        return self.__copy_002(symbol_name=symbol_name
                               , timeframe=timeframe
                               , start_time=start_time
                               , count=count
                               , fun_name="CopyHigh_002"
                               , parse_fun=self.__copy_float_common)

    def copy_high_003(self, symbol_name: str, timeframe: int, start_time: datetime, end_time: datetime) -> List[float]:
        return self.__copy_003(symbol_name=symbol_name
                               , timeframe=timeframe
                               , start_time=start_time
                               , end_time=end_time
                               , fun_name="CopyHigh_003"
                               , parse_fun=self.__copy_float_common)

    def copy_low_001(self, symbol_name: str, timeframe: int, start_pos: int, count: int) -> List[float]:
        return self.__copy_001(symbol_name=symbol_name
                               , timeframe=timeframe
                               , start_pos=start_pos
                               , count=count
                               , fun_name="CopyLow_001"
                               , parse_fun=self.__copy_float_common)

    def copy_low_002(self, symbol_name: str, timeframe: int, start_time: datetime, count: int) -> List[float]:
        return self.__copy_002(symbol_name=symbol_name
                               , timeframe=timeframe
                               , start_time=start_time
                               , count=count
                               , fun_name="CopyLow_002"
                               , parse_fun=self.__copy_float_common)

    def copy_low_003(self, symbol_name: str, timeframe: int, start_time: datetime, end_time: datetime) -> List[float]:
        return self.__copy_003(symbol_name=symbol_name
                               , timeframe=timeframe
                               , start_time=start_time
                               , end_time=end_time
                               , fun_name="CopyLow_003"
                               , parse_fun=self.__copy_float_common)

    def copy_close_001(self, symbol_name: str, timeframe: int, start_pos: int, count: int) -> List[float]:
        return self.__copy_001(symbol_name=symbol_name
                               , timeframe=timeframe
                               , start_pos=start_pos
                               , count=count
                               , fun_name="CopyClose_001"
                               , parse_fun=self.__copy_float_common)

    def copy_close_002(self, symbol_name: str, timeframe: int, start_time: datetime, count: int) -> List[float]:
        return self.__copy_002(symbol_name=symbol_name
                               , timeframe=timeframe
                               , start_time=start_time
                               , count=count
                               , fun_name="CopyClose_002"
                               , parse_fun=self.__copy_float_common)

    def copy_close_003(self, symbol_name: str, timeframe: int, start_time: datetime, end_time: datetime) -> List[float]:
        return self.__copy_003(symbol_name=symbol_name
                               , timeframe=timeframe
                               , start_time=start_time
                               , end_time=end_time
                               , fun_name="CopyClose_003"
                               , parse_fun=self.__copy_float_common)

    def copy_tick_volume_001(self, symbol_name: str, timeframe: int, start_pos: int, count: int) -> List[int]:
        return self.__copy_001(symbol_name=symbol_name
                               , timeframe=timeframe
                               , start_pos=start_pos
                               , count=count
                               , fun_name="CopyTickVolume_001"
                               , parse_fun=self.__copy_int_common)

    def copy_tick_volume_002(self, symbol_name: str, timeframe: int, start_time: datetime, count: int) -> List[int]:
        return self.__copy_002(symbol_name=symbol_name
                               , timeframe=timeframe
                               , start_time=start_time
                               , count=count
                               , fun_name="CopyTickVolume_002"
                               , parse_fun=self.__copy_int_common)

    def copy_tick_volume_003(self, symbol_name: str, timeframe: int, start_time: datetime, end_time: datetime) -> List[int]:
        return self.__copy_003(symbol_name=symbol_name
                               , timeframe=timeframe
                               , start_time=start_time
                               , end_time=end_time
                               , fun_name="CopyTickVolume_003"
                               , parse_fun=self.__copy_int_common)

    def __copy_001(self, symbol_name: str, timeframe: int, start_pos: int, count: int, fun_name: str, parse_fun: Any) -> List[Any]:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map[fun_name]))
        self.__data_ctrl.add_data_to_msg(data=symbol_name)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(start_pos))
        self.__data_ctrl.add_data_to_msg(data=str(count))
        self.__data_ctrl.send_message()

        return parse_fun(str_ret=self.__data_ctrl.receive_string_from_mt4())

    def __copy_002(self, symbol_name: str, timeframe: int, start_time: datetime, count: int, fun_name: str, parse_fun: Any) -> List[Any]:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map[fun_name]))
        self.__data_ctrl.add_data_to_msg(data=symbol_name)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=start_time.strftime("%Y.%m.%d %H:%M:%S"))
        self.__data_ctrl.add_data_to_msg(data=str(count))
        self.__data_ctrl.send_message()

        return parse_fun(str_ret=self.__data_ctrl.receive_string_from_mt4())

    def __copy_003(self, symbol_name: str, timeframe: int, start_time: datetime, end_time: datetime, fun_name: str, parse_fun: Any) -> List[Any]:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map[fun_name]))
        self.__data_ctrl.add_data_to_msg(data=symbol_name)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=start_time.strftime("%Y.%m.%d %H:%M:%S"))
        self.__data_ctrl.add_data_to_msg(data=end_time.strftime("%Y.%m.%d %H:%M:%S"))
        self.__data_ctrl.send_message()

        return parse_fun(str_ret=self.__data_ctrl.receive_string_from_mt4())

    def __copy_time_common(self, str_ret: str) -> List[datetime]:
        if str_ret == "-1":
            return list()
        parts = str_ret.split("~")
        arr_size = int(parts[0])
        if arr_size+1 != len(parts):
            return list()

        datetime_array: List[datetime] = list()
        for ele in parts[1:]:
            datetime_array.append(datetime.strptime(ele, "%Y.%m.%d %H:%M:%S"))

        return datetime_array

    def __copy_float_common(self, str_ret: str) -> List[float]:
        if str_ret == "-1":
            return list()
        parts = str_ret.split("~")
        arr_size = int(parts[0])
        if arr_size+1 != len(parts):
            return list()

        float_array: List[float] = list()
        for ele in parts[1:]:
            float_array.append(float(ele))

        return float_array

    def __copy_int_common(self, str_ret: str) -> List[int]:
        if str_ret == "-1":
            return list()
        parts = str_ret.split("~")
        arr_size = int(parts[0])
        if arr_size+1 != len(parts):
            return list()

        int_array: List[float] = list()
        for ele in parts[1:]:
            int_array.append(int(ele))

        return int_array

    def __copy_rates_common(self, str_ret: str) -> List[Union[datetime, float, float, float, float, int, int, int]]:
        if str_ret == "-1":
            return list()
        parts = str_ret.split("~")
        arr_size = int(parts[0])
        if (arr_size*8)+1 != len(parts):
            return list()

        rates_array: List[Union[datetime, float, float, float, float, int, int, int]] = list()
        for idx in range(1, len(parts), 8):
            rates_array.append((datetime.strptime(parts[idx], "%Y.%m.%d %H:%M:%S")
                                , float(parts[idx+1])
                                , float(parts[idx+2])
                                , float(parts[idx+3])
                                , float(parts[idx+4])
                                , int(parts[idx+5])
                                , int(parts[idx+6])
                                , int(parts[idx+7])))

        return rates_array

    def bars_001(self, symbol_name: str, timeframe: int) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["Bars_001"]))
        self.__data_ctrl.add_data_to_msg(data=symbol_name)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_int_from_mt4()

    def bars_002(self, symbol_name: str, timeframe: int, start_time: datetime, stop_time: datetime) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["Bars_002"]))
        self.__data_ctrl.add_data_to_msg(data=symbol_name)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=start_time.strftime("%Y.%m.%d %H:%M:%S"))
        self.__data_ctrl.add_data_to_msg(data=stop_time.strftime("%Y.%m.%d %H:%M:%S"))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_int_from_mt4()

    def ibars(self, symbol: str, timeframe: int) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iBars"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_int_from_mt4()

    def ibar_shift(self, symbol: str, timeframe: int, time: datetime, exact: bool) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iBarShift"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=time.strftime("%Y.%m.%d %H:%M:%S"))
        self.__data_ctrl.add_data_to_msg(data=str(exact))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_int_from_mt4()

    def iclose(self, symbol: str, timeframe: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iClose"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def ihigh(self, symbol: str, timeframe: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iHigh"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def ihighest(self, symbol: str, timeframe: int, type: int, count: int, start: int) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iHighest"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(type))
        self.__data_ctrl.add_data_to_msg(data=str(count))
        self.__data_ctrl.add_data_to_msg(data=str(start))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_int_from_mt4()

    def ilow(self, symbol: str, timeframe: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iLow"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def ilowest(self, symbol: str, timeframe: int, type: int, count: int, start: int) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iLowest"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(type))
        self.__data_ctrl.add_data_to_msg(data=str(count))
        self.__data_ctrl.add_data_to_msg(data=str(start))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_int_from_mt4()

    def iopen(self, symbol: str, timeframe: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iOpen"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def itime(self, symbol: str, timeframe: int, shift: int) -> datetime:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iTime"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_datetime_from_mt4()

    def ivolume(self, symbol: str, timeframe: int, shift: int) -> int:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iVolume"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_int_from_mt4()
