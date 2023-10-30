from typing import Dict, List, Set, Tuple, Union, Any
from datetime import datetime

import pysailfish.internal.MT_EA.mt4_const as mc
from pysailfish.internal.DataCtrl.MT4DataCtrl.MT4DataCtrl import MT4DataCtrl

class trade_functions(object):
    def __init__(self):
        self.__data_ctrl: MT4DataCtrl = None
        self.__fun_num_map: Dict[str, int] = dict()

    def init_component(self, data_ctrl: MT4DataCtrl, fun_num_map: Dict[str, int]):
        self.__data_ctrl = data_ctrl
        self.__fun_num_map = fun_num_map

    def order_close(self, ticket: int, lots: float, price: float, slippage: int, arrow_color: str) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["OrderClose"]))
        self.__data_ctrl.add_data_to_msg(data=str(ticket))
        self.__data_ctrl.add_data_to_msg(data=str(lots))
        self.__data_ctrl.add_data_to_msg(data=str(price))
        self.__data_ctrl.add_data_to_msg(data=str(slippage))
        self.__data_ctrl.add_data_to_msg(data=arrow_color)
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()

    def order_close_by(self, ticket: int, opposite: int, arrow_color: str) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["OrderCloseBy"]))
        self.__data_ctrl.add_data_to_msg(data=str(ticket))
        self.__data_ctrl.add_data_to_msg(data=str(opposite))
        self.__data_ctrl.add_data_to_msg(data=arrow_color)
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()

    def order_delete(self, ticket: int, arrow_color: str) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["OrderDelete"]))
        self.__data_ctrl.add_data_to_msg(data=str(ticket))
        self.__data_ctrl.add_data_to_msg(data=arrow_color)
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()

    def order_modify(self, ticket: int, price: float, stoploss: float, takeprofit: float, expiration: datetime, arrow_color: str) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["OrderModify"]))
        self.__data_ctrl.add_data_to_msg(data=str(ticket))
        self.__data_ctrl.add_data_to_msg(data=str(price))
        self.__data_ctrl.add_data_to_msg(data=str(stoploss))
        self.__data_ctrl.add_data_to_msg(data=str(takeprofit))
        self.__data_ctrl.add_data_to_msg(data=expiration.strftime("%Y.%m.%d %H:%M:%S"))
        self.__data_ctrl.add_data_to_msg(data=arrow_color)
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()

    def order_print(self) -> None:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["OrderPrint"]))

    def order_select(self, index: int, select: int, pool: int = mc.MODE_TRADES) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["OrderSelect"]))
        self.__data_ctrl.add_data_to_msg(data=str(index))
        self.__data_ctrl.add_data_to_msg(data=str(select))
        self.__data_ctrl.add_data_to_msg(data=str(pool))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()

    def order_send(self
                   , symbol: str
                   , cmd: int
                   , volume: float
                   , price: float
                   , slippage: int
                   , stoploss: float
                   , takeprofit: float
                   , comment: str = ""
                   , magic: int = 0
                   , expiration: datetime = datetime(1970, 1, 1, 0, 0, 0)
                   , arrow_color: str = mc.clrNONE):
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["OrderSend"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(cmd))
        self.__data_ctrl.add_data_to_msg(data=str(volume))
        self.__data_ctrl.add_data_to_msg(data=str(price))
        self.__data_ctrl.add_data_to_msg(data=str(slippage))
        self.__data_ctrl.add_data_to_msg(data=str(stoploss))
        self.__data_ctrl.add_data_to_msg(data=str(takeprofit))
        self.__data_ctrl.add_data_to_msg(data=comment)
        self.__data_ctrl.add_data_to_msg(data=str(magic))
        self.__data_ctrl.add_data_to_msg(data=expiration.strftime("%Y.%m.%d %H:%M:%S"))
        self.__data_ctrl.add_data_to_msg(data=arrow_color)
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_int_from_mt4()

    def order_close(self
                    , ticket: int
                    , lots: float
                    , price: float
                    , slippage: int
                    , arrow_color: str) -> bool:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["OrderClose"]))
        self.__data_ctrl.add_data_to_msg(data=str(ticket))
        self.__data_ctrl.add_data_to_msg(data=str(lots))
        self.__data_ctrl.add_data_to_msg(data=str(price))
        self.__data_ctrl.add_data_to_msg(data=str(slippage))
        self.__data_ctrl.add_data_to_msg(data=arrow_color)
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_bool_from_mt4()
