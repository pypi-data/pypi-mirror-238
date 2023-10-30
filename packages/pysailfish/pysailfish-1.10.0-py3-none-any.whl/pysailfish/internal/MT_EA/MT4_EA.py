from typing import Dict, List, Set, Tuple, Union, Any
from datetime import datetime
import logging
import time
import decimal

from pysailfish.internal.DataCtrl.MT4DataCtrl.MT4DataCtrl import MT4DataCtrl
from pysailfish.internal.Network.TCPCast import TCPCast, TCPStatus
from pysailfish.internal.MT_EA.mt4_fun_num_map import mt4_fun_num_map
import pysailfish.internal.observability.log_helper as lh
import pysailfish.internal.MT_EA.predefined_variables as pv
import pysailfish.internal.MT_EA.trade_functions as tf
import pysailfish.internal.MT_EA.common_functions as cf
import pysailfish.internal.MT_EA.technical_indicators as ti
import pysailfish.internal.MT_EA.account_information as ai
import pysailfish.internal.MT_EA.market_info as mi
import pysailfish.internal.MT_EA.timeseries_and_indicators_access as taia
import pysailfish.internal.MT_EA.object_functions as of
import pysailfish.internal.MT_EA.chart_operations as co

class MT4_EA(object):
    def __init__(self):
        self._server_ip: str = ""
        self._server_port: int = 0
        self._ea_name: str = ""
        self._is_deinit: bool = False
        self._user_inputs: Dict[str, str] = dict() # key: variable name, value: variable
        self._logger: logging.Logger = None
        self._mt4_server: TCPCast = None

        self.__fun_map: Dict[str, Any] = self.__create_fun_map()
        self.__fun_num_map: Dict[str, int] = mt4_fun_num_map
        self.__data_ctrl: MT4DataCtrl = None

        self._pv = pv # predefined variables namespace
        self._tf = tf.trade_functions()
        self._cf = cf.common_functions()
        self._ti = ti.technical_indicators()
        self._ai = ai.account_information()
        self._mi = mi.market_info()
        self._taia = taia.timeseries_and_indicators_access()
        self._of = of.object_functions()
        self._co = co.chart_operations()

    def InitComponent(self
                      , server_ip: str
                      , server_port: int
                      , ea_name: str):
        self._server_ip = server_ip
        self._server_port = server_port
        self._ea_name = ea_name

        self._logger = lh.init_logger(logger_name=f"{ea_name}_logger", is_json_output=False)

        # tcp cast client
        tcp_cast: TCPCast = TCPCast()
        if tcp_cast.InitComponent(if_address=self._server_ip
                                    , if_port=self._server_port
                                    , is_client=True) == TCPStatus.ERROR:
            self._logger.error("Cannot create tcp client. Stop.")
            exit(1)

        if tcp_cast.Connect(to_address=self._server_ip
                              , to_port=self._server_port) == TCPStatus.ERROR:
            self._logger.error("Cannot connect to tcp server. Stop.")
            exit(1)

        # data control
        self.__data_ctrl: MT4DataCtrl = MT4DataCtrl()
        self.__data_ctrl.init_component(logger=self._logger
                                        , tcp_client=tcp_cast
                                        , mt4_msg_callback=self.mt4_msg_callback)

        # mt3 python interface funtions init
        self._tf.init_component(data_ctrl=self.__data_ctrl
                                , fun_num_map=self.__fun_num_map)
        self._cf.init_component(data_ctrl=self.__data_ctrl
                                , fun_num_map=self.__fun_num_map)
        self._ti.init_component(data_ctrl=self.__data_ctrl
                                , fun_num_map=self.__fun_num_map)
        self._ai.init_component(data_ctrl=self.__data_ctrl
                                , fun_num_map=self.__fun_num_map)
        self._mi.init_component(data_ctrl=self.__data_ctrl
                                , fun_num_map=self.__fun_num_map)
        self._taia.init_component(data_ctrl=self.__data_ctrl
                                  , fun_num_map=self.__fun_num_map)
        self._of.init_component(data_ctrl=self.__data_ctrl
                                , fun_num_map=self.__fun_num_map)
        self._co.init_component(data_ctrl=self.__data_ctrl
                                , fun_num_map=self.__fun_num_map)

    def StartEA(self) -> None:
        self.__data_ctrl.start_th()

        while True:
            time.sleep(1)
            if not self.__data_ctrl.is_connection_okay() or self.IsDeinited():
                self._logger.error(f"Connection lost. ip: {self._server_ip} port: {self._server_port}")
                self.__data_ctrl.stop_th()
                exit(1)

    def OnInit(self, parts: List[str]) -> int:
        self._pv.magic_num = int(parts[0])
        # init user inputs map
        self._user_inputs = dict()
        shift_pos = 1
        for i in range(int(parts[0 + shift_pos])):
            variable_name: str = parts[i*2+1 + shift_pos]
            variable_value: str = parts[i*2+2 + shift_pos]
            self._user_inputs[variable_name] = variable_value

        return self._OnInit()

    def OnDeinit(self, parts: List[str]) -> int:
        self._is_deinit = True
        self._OnDeinit(reason=int(parts[0]))

        # this value have no meaning for mt4 framework, this is a notification of the finish of this function
        return 0

    def OnTick(self, parts: List[str]) -> int:
        self.__UpdatePredefiniedVariables(parts=parts)
        self._OnTick()

        # this value have no meaning for mt4 framework, this is a notification of the finish of this function
        return 0

    def OnTimer(self, parts: List[str]) -> None:
        self._OnTimer()

    def OnTester(self, parts: List[str]) -> float:
        return self._OnTester()

    def OnChartEvent(self, parts: List[str]) -> int:
        self._OnChartEvent(id=int(parts[0])
                           , lparam=int(parts[1])
                           , dparam=float(parts[2])
                           , sparam=parts[3])

        # this value have no meaning for mt4 framework, this is a notification of the finish of this function
        return 0

    def IsDeinited(self) -> bool:
        return self._is_deinit

    def mt4_msg_callback(self, fun_name: str, parts: List[str]):
        # call back to python ea
        fun_ret: Any = self.__fun_map[fun_name](parts=parts)

        if fun_ret is not None:
            # call back to mt4 ea
            self.__data_ctrl.add_data_to_msg(str(self.__fun_num_map[fun_name]))
            self.__data_ctrl.add_data_to_msg(str(fun_ret))
            self.__data_ctrl.send_message()

    # override
    def _OnInit(self) -> int:
        raise NotImplementedError

    # override
    def _OnDeinit(self, reason: int) -> None:
        raise NotImplementedError

    # override
    def _OnTick(self) -> None:
        raise NotImplementedError

    # override
    def _OnTimer(self) -> None:
        raise NotImplementedError

    # override
    def _OnTester(self) -> float:
        raise NotImplementedError

    # override
    def _OnChartEvent(self
                     , id: int
                     , lparam: int
                     , dparam: float
                     , sparam: str) -> None:
        raise NotImplementedError

    # mt4 chart operations
    def ChartApplyTemplate(self, **kwargs) -> bool:
        return None

    def ChartSaveTemplate(self, **kwargs) -> bool:
        return None

    def ChartWindowFind_001(self, **kwargs) -> int:
        return None

    def ChartWindowFind_002(self, **kwargs) -> int:
        return None

    def ChartTimePriceToXY(self, **kwargs) -> bool:
        return None

    def ChartXYToTimePrice(self, **kwargs) -> bool:
        return None

    def ChartOpen(self, **kwargs) -> int:
        return None

    def ChartFirst(self) -> int:
        return None

    def ChartNext(self, **kwargs) -> int:
        return None

    def ChartClose(self, **kwargs) -> bool:
        return None

    def ChartSymbol(self, **kwargs) -> str:
        return None

    def ChartPeriod(self, **kwargs) -> int:
        return None

    def ChartRedraw(self, **kwargs) -> None:
        return None

    def ChartSetDouble(self, **kwargs) -> bool:
        return None

    def ChartSetInteger_001(self, **kwargs) -> bool:
        return None

    def ChartSetInteger_002(self, **kwargs) -> bool:
        return None

    def ChartSetString(self, **kwargs) -> bool:
        return None

    def ChartGetDouble_001(self, **kwargs) -> float:
        return None

    def ChartGetDouble_002(self, **kwargs) -> bool:
        return None

    def ChartGetInteger_001(self, **kwargs) -> int:
        return None

    def ChartGetInteger_002(self, **kwargs) -> bool:
        return None

    def ChartGetString_001(self, **kwargs) -> str:
        return None

    def ChartGetString_002(self, **kwargs) -> bool:
        return None

    def ChartNavigate(self, **kwargs) -> bool:
        return None

    def ChartID(self) -> int:
        return None

    def ChartIndicatorDelete(self, **kwargs) -> bool:
        return None

    def ChartIndicatorName(self, **kwargs) -> str:
        return None

    def ChartIndicatorsTotal(self, **kwargs) -> int:
        return None

    def ChartWindowOnDropped(self) -> int:
        return None

    def ChartPriceOnDropped(self) -> float:
        return None

    def ChartTimeOnDropped(self) -> datetime:
        return None

    def ChartXOnDropped(self) -> int:
        return None

    def ChartYOnDropped(self) -> int:
        return None

    def ChartSetSymbolPeriod(self, **kwargs) -> bool:
        return self._co.chart_set_symbol_period(**kwargs)

    def ChartScreenShot(self, **kwargs) -> bool:
        return None

    def Period(self) -> int:
        return None

    def Symbol(self) -> str:
        return None

    def WindowBarsPerChart(self) -> int:
        return None

    def WindowExpertName(self) -> str:
        return None

    def WindowFind(self, **kwargs) -> int:
        return None

    # mt4 interface functions
    def OrderClose(self, **kwargs) -> bool:
        return self._tf.order_close(**kwargs)

    def OrderCloseBy(self, **kwargs) -> bool:
        return self._tf.order_close_by(**kwargs)

    def OrderClosePrice(self) -> float:
        return self._cf.get_float_from_mt(fun_name="OrderClosePrice")

    def OrderCloseTime(self) -> datetime:
        return self._cf.get_datetime_from_mt(fun_name="OrderCloseTime")

    def OrderComment(self) -> str:
        return self._cf.get_str_from_mt(fun_name="OrderComment")

    def OrderCommission(self) -> float:
        return self._cf.get_float_from_mt(fun_name="OrderCommission")

    def OrderDelete(self, **kwargs) -> bool:
        return self._tf.order_delete(**kwargs)

    def OrderExpiration(self) -> datetime:
        return self._cf.get_datetime_from_mt(fun_name="OrderExpiration")

    def OrderLots(self) -> float:
        return self._cf.get_float_from_mt(fun_name="OrderLots")

    def OrderMagicNumber(self) -> int:
        return self._cf.get_int_from_mt(fun_name="OrderMagicNumber")

    def OrderModify(self, **kwargs) -> bool:
        return self._tf.order_modify(**kwargs)

    def OrderOpenPrice(self) -> float:
        return self._cf.get_float_from_mt(fun_name="OrderOpenPrice")

    def OrderOpenTime(self) -> datetime:
        return self._cf.get_datetime_from_mt(fun_name="OrderOpenTime")

    def OrderPrint(self) -> None:
        return self._tf.order_print()

    def OrderProfit(self) -> float:
        return self._cf.get_float_from_mt(fun_name="OrderProfit")

    def OrderSelect(self, **kwargs) -> bool:
        return self._tf.order_select(**kwargs)

    def OrderSend(self, **kwargs) -> int:
        return self._tf.order_send(**kwargs)

    def OrdersHistoryTotal(self) -> int:
        return self._cf.get_int_from_mt(fun_name="OrdersHistoryTotal")

    def OrderStopLoss(self) -> float:
        return self._cf.get_float_from_mt(fun_name="OrderStopLoss")

    def OrdersTotal(self) -> int:
        return self._cf.get_int_from_mt(fun_name="OrdersTotal")

    def OrderSwap(self) -> float:
        return self._cf.get_float_from_mt(fun_name="OrderSwap")

    def OrderSymbol(self) -> str:
        return self._cf.get_str_from_mt(fun_name="OrderSymbol")

    def OrderTakeProfit(self) -> float:
        return self._cf.get_float_from_mt(fun_name="OrderTakeProfit")

    def OrderTicket(self) -> int:
        return self._cf.get_int_from_mt(fun_name="OrderTicket")

    def OrderType(self) -> int:
        return self._cf.get_int_from_mt(fun_name="OrderType")

    # object functions
    # limit at 10 extra input pairs
    def ObjectCreate_001(self, **kwargs) -> bool:
        return self._of.object_create_001(**kwargs)

    def ObjectCreate_002(self, **kwargs) -> bool:
        return self._of.object_create_002(**kwargs)

    def ObjectName(self, **kwargs) -> str:
        return self._of.object_name(**kwargs)

    def ObjectDelete_001(self, **kwargs) -> bool:
        return self._of.object_delete_001(**kwargs)

    def ObjectDelete_002(self, **kwargs) -> bool:
        return self._of.object_delete_002(**kwargs)

    def ObjectsDeleteAll_001(self, **kwargs) -> int:
        return self._of.objects_delete_all_001(**kwargs)

    def ObjectsDeleteAll_002(self, **kwargs) -> int:
        return self._of.objects_delete_all_002(**kwargs)

    def ObjectsDeleteAll_003(self, **kwargs) -> int:
        return self._of.objects_delete_all_003(**kwargs)

    def ObjectFind_001(self, **kwargs) -> int:
        return self._of.object_find_001(**kwargs)

    def ObjectFind_002(self, **kwargs) -> int:
        return self._of.object_find_002(**kwargs)

    def ObjectGetTimeByValue(self, **kwargs) -> datetime:
        return self._of.object_get_time_by_value(**kwargs)

    def ObjectGetValueByTime(self, **kwargs) -> float:
        return self._of.object_get_value_by_time(**kwargs)

    def ObjectMove(self, **kwargs) -> bool:
        return self._of.object_move(**kwargs)

    def ObjectsTotal_001(self, **kwargs) -> int:
        return self._of.objects_total_001(**kwargs)

    def ObjectsTotal_002(self, **kwargs) -> int:
        return self._of.objects_total_002(**kwargs)

    def ObjectGetDouble(self, **kwargs) -> float:
        return self._of.object_get_double(**kwargs)

    def ObjectGetInteger(self, **kwargs) -> int:
        return self._of.object_get_integer(**kwargs)

    def ObjectGetString(self, **kwargs) -> str:
        return self._of.object_get_string(**kwargs)

    def ObjectSetDouble_001(self, **kwargs) -> bool:
        return self._of.object_set_double_001(**kwargs)

    def ObjectSetDouble_002(self, **kwargs) -> bool:
        return self._of.object_set_double_002(**kwargs)

    def ObjectSetInteger_001(self, **kwargs) -> bool:
        return self._of.object_set_integer_001(**kwargs)

    def ObjectSetInteger_002(self, **kwargs) -> bool:
        return self._of.object_set_integer_002(**kwargs)

    def ObjectSetString_001(self, **kwargs) -> bool:
        return self._of.object_set_string_001(**kwargs)

    def ObjectSetString_002(self, **kwargs) -> bool:
        return self._of.object_set_string_002(**kwargs)

    def TextSetFont(self, **kwargs) -> bool:
        return self._of.text_set_font(**kwargs)

    # def TextOut(self, **kwargs) -> bool:
    #     return self._of.text_out(**kwargs)

    def TextGetSize(self, **kwargs) -> Union[int, int]:
        return self._of.text_get_size(**kwargs)

    def ObjectDescription(self, **kwargs) -> str:
        return self._of.object_description(**kwargs)

    def ObjectGet(self, **kwargs) -> float:
        return self._of.object_get(**kwargs)

    def ObjectGetFiboDescription(self, **kwargs) -> str:
        return self._of.object_get_fibo_description(**kwargs)

    def ObjectGetShiftByValue(self, **kwargs) -> int:
        return self._of.object_get_shift_by_value(**kwargs)

    def ObjectGetValueByShift(self, **kwargs) -> float:
        return self._of.object_get_value_by_shift(**kwargs)

    def ObjectSet(self, **kwargs) -> bool:
        return self._of.object_set(**kwargs)

    def ObjectSetFiboDescription(self, **kwargs) -> bool:
        return self._of.object_set_fibo_description(**kwargs)

    def ObjectSetText(self, **kwargs) -> bool:
        return self._of.object_set_text(**kwargs)

    def ObjectType(self, **kwargs) -> int:
        return self._of.object_type(**kwargs)

    # mt4 technical indicator functions
    def iAC(self, **kwargs) -> float:
        return self._ti.i_ac(**kwargs)

    def iAD(self, **kwargs) -> float:
        return self._ti.i_ad(**kwargs)

    def iADX(self, **kwargs) -> float:
        return self._ti.i_adx(**kwargs)

    def iAlligator(self, **kwargs) -> float:
        return self._ti.i_alligator(**kwargs)

    def iAO(self, **kwargs) -> float:
        return self._ti.i_ao(**kwargs)

    def iATR(self, **kwargs) -> float:
        return self._ti.i_atr(**kwargs)

    def iBearsPower(self, **kwargs) -> float:
        return self._ti.i_bears_power(**kwargs)

    def iBands(self, **kwargs) -> float:
        return self._ti.i_bands(**kwargs)

    def iBandsOnArray(self, **kwargs) -> float:
        return self._ti.i_bands_on_array(**kwargs)

    def iBullsPower(self, **kwargs) -> float:
        return self._ti.i_bulls_power(**kwargs)

    def iCCI(self, **kwargs) -> float:
        return self._ti.i_cci(**kwargs)

    def iCCIOnArray(self, **kwargs) -> float:
        return self._ti.i_cci_on_array(**kwargs)

    # Only support string input for the custom inputs
    def iCustom(self, **kwargs) -> float:
        return self._ti.i_custom(**kwargs)

    def iDeMarker(self, **kwargs) -> float:
        return self._ti.i_de_marker(**kwargs)

    def iEnvelopes(self, **kwargs) -> float:
        return self._ti.i_envelopes(**kwargs)

    def iEnvelopesOnArray(self, **kwargs) -> float:
        return self._ti.i_envelopes_on_array(**kwargs)

    def iForce(self, **kwargs) -> float:
        return self._ti.i_force(**kwargs)

    def iFractals(self, **kwargs) -> float:
        return self._ti.i_fractals(**kwargs)

    def iGator(self, **kwargs) -> float:
        return self._ti.i_gator(**kwargs)

    def iIchimoku(self, **kwargs) -> float:
        return self._ti.i_ichimoku(**kwargs)

    def iBWMFI(self, **kwargs) -> float:
        return self._ti.i_bwmfi(**kwargs)

    def iMomentum(self, **kwargs) -> float:
        return self._ti.i_momentum(**kwargs)

    def iMomentumOnArray(self, **kwargs) -> float:
        return self._ti.i_momentum_on_array(**kwargs)

    def iMFI(self, **kwargs) -> float:
        return self._ti.i_mfi(**kwargs)

    def iMA(self, **kwargs) -> float:
        return self._ti.i_ma(**kwargs)

    def iMAOnArray(self, **kwargs) -> float:
        return self._ti.i_ma_on_array(**kwargs)

    def iOsMA(self, **kwargs) -> float:
        return self._ti.i_os_ma(**kwargs)

    def iMACD(self, **kwargs) -> float:
        return self._ti.i_macd(**kwargs)

    def iOBV(self, **kwargs) -> float:
        return self._ti.i_obv(**kwargs)

    def iSAR(self, **kwargs) -> float:
        return self._ti.i_sar(**kwargs)

    def iRSI(self, **kwargs) -> float:
        return self._ti.i_rsi(**kwargs)

    def iRSIOnArray(self, **kwargs) -> float:
        return self._ti.i_rsi_on_array(**kwargs)

    def iRVI(self, **kwargs) -> float:
        return self._ti.i_rvi(**kwargs)

    def iStdDev(self, **kwargs) -> float:
        return self._ti.i_std_dev(**kwargs)

    def iStdDevOnArray(self, **kwargs) -> float:
        return self._ti.i_std_dev_on_array(**kwargs)

    def iStochastic(self, **kwargs) -> float:
        return self._ti.i_stochastic(**kwargs)

    def iWPR(self, **kwargs) -> float:
        return self._ti.i_wpr(**kwargs)

    # mt4 checkup functions
    def GetLastError(self) -> int:
        return self._cf.get_int_from_mt(fun_name="GetLastError")

    # mt4 account information
    def AccountInfoDouble(self, **kwargs) -> float:
        return self._ai.account_info_double(**kwargs)

    def AccountInfoInteger(self, **kwargs) -> int:
        return self._ai.account_info_integer(**kwargs)

    def AccountInfoString(self, **kwargs) -> str:
        return self._ai.account_info_string(**kwargs)

    def AccountBalance(self) -> float:
        return self._cf.get_float_from_mt(fun_name="AccountBalance")

    def AccountCredit(self) -> float:
        return self._cf.get_float_from_mt(fun_name="AccountCredit")

    def AccountCompany(self) -> str:
        return self._cf.get_str_from_mt(fun_name="AccountCompany")

    def AccountCurrency(self) -> str:
        return self._cf.get_str_from_mt(fun_name="AccountCurrency")

    def AccountEquity(self) -> float:
        return self._cf.get_float_from_mt(fun_name="AccountEquity")

    def AccountFreeMargin(self) -> float:
        return self._cf.get_float_from_mt(fun_name="AccountFreeMargin")

    def AccountFreeMarginCheck(self, **kwargs) -> float:
        return self._ai.account_free_margin_check(**kwargs)

    def AccountFreeMarginMode(self) -> float:
        return self._cf.get_float_from_mt(fun_name="AccountFreeMarginMode")

    def AccountLeverage(self) -> int:
        return self._cf.get_int_from_mt(fun_name="AccountLeverage")

    def AccountMargin(self) -> float:
        return self._cf.get_float_from_mt(fun_name="AccountMargin")

    def AccountName(self) -> str:
        return self._cf.get_str_from_mt(fun_name="AccoauntName")

    def AccountNumber(self) -> int:
        return self._cf.get_int_from_mt(fun_name="AccountNumber")

    def AccountProfit(self) -> float:
        return self._cf.get_float_from_mt(fun_name="AccountProfit")

    def AccountServer(self) -> str:
        return self._cf.get_str_from_mt(fun_name="AccountServer")

    def AccountStopoutLevel(self) -> int:
        return self._cf.get_int_from_mt(fun_name="AccountStopoutLevel")

    def AccountStopoutMode(self) -> int:
        return self._cf.get_int_from_mt(fun_name="AccountStopoutMode")

    # market info
    def MarketInfo(self, **kwargs) -> float:
        return self._mi.market_info(**kwargs)

    def SymbolsTotal(self, **kwargs) -> int:
        return self._mi.symbols_total(**kwargs)

    def SymbolName(self, **kwargs) -> str:
        return self._mi.symbol_name(**kwargs)

    def SymbolSelect(self, **kwargs) -> bool:
        return self._mi.symbol_select(**kwargs)

    def SymbolInfoDouble(self, **kwargs) -> float:
        return self._mi.symbol_info_double(**kwargs)

    def SymbolInfoInteger(self, **kwargs) -> int:
        return self._mi.symbol_info_integer(**kwargs)

    def SymbolInfoString(self, **kwargs) -> str:
        return self._mi.symbol_info_string(**kwargs)

    def SymbolInfoTick(self, **kwargs) -> Union[datetime, float, float, float, int]:
        return self._mi.symbol_info_tick(**kwargs)

    def SymbolInfoSessionQuote(self, **kwargs) -> Union[datetime, datetime]:
        return self._mi.symbol_info_session_quote(**kwargs)

    def SymbolInfoSessionTrade(self, **kwargs) -> Union[datetime, datetime]:
        return self._mi.symbol_info_session_trade(**kwargs)

    # timeseries and indicators access
    def SeriesInfoInteger(self, **kwargs) -> int:
        return self._taia.series_info_integer(**kwargs)

    def RefreshRates(self, **kwargs) -> bool:
        return self._cf.get_bool_from_mt(fun_name="RefreshRates")

    def CopyRates_001(self, **kwargs) -> List[Union[datetime, float, float, float, float, int, int, int]]:
        return self._taia.copy_rates_001(**kwargs)

    def CopyRates_002(self, **kwargs) -> List[Union[datetime, float, float, float, float, int, int, int]]:
        return self._taia.copy_rates_002(**kwargs)

    def CopyRates_003(self, **kwargs) -> List[Union[datetime, float, float, float, float, int, int, int]]:
        return self._taia.copy_rates_003(**kwargs)

    def CopyTime_001(self, **kwargs) -> List[datetime]:
        return self._taia.copy_time_001(**kwargs)

    def CopyTime_002(self, **kwargs) -> List[datetime]:
        return self._taia.copy_time_002(**kwargs)

    def CopyTime_003(self, **kwargs) -> List[datetime]:
        return self._taia.copy_time_003(**kwargs)

    def CopyOpen_001(self, **kwargs) -> List[float]:
        return self._taia.copy_open_001(**kwargs)

    def CopyOpen_002(self, **kwargs) -> List[float]:
        return self._taia.copy_open_002(**kwargs)

    def CopyOpen_003(self, **kwargs) -> List[float]:
        return self._taia.copy_open_003(**kwargs)

    def CopyHigh_001(self, **kwargs) -> List[float]:
        return self._taia.copy_high_001(**kwargs)

    def CopyHigh_002(self, **kwargs) -> List[float]:
        return self._taia.copy_high_002(**kwargs)

    def CopyHigh_003(self, **kwargs) -> List[float]:
        return self._taia.copy_high_003(**kwargs)

    def CopyLow_001(self, **kwargs) -> List[float]:
        return self._taia.copy_low_001(**kwargs)

    def CopyLow_002(self, **kwargs) -> List[float]:
        return self._taia.copy_low_002(**kwargs)

    def CopyLow_003(self, **kwargs) -> List[float]:
        return self._taia.copy_low_003(**kwargs)

    def CopyClose_001(self, **kwargs) -> List[float]:
        return self._taia.copy_close_001(**kwargs)

    def CopyClose_002(self, **kwargs) -> List[float]:
        return self._taia.copy_close_002(**kwargs)

    def CopyClose_003(self, **kwargs) -> List[float]:
        return self._taia.copy_close_003(**kwargs)

    def CopyTickVolume_001(self, **kwargs) -> List[int]:
        return self._taia.copy_tick_volume_001(**kwargs)

    def CopyTickVolume_002(self, **kwargs) -> List[int]:
        return self._taia.copy_tick_volume_002(**kwargs)

    def CopyTickVolume_003(self, **kwargs) -> List[int]:
        return self._taia.copy_tick_volume_003(**kwargs)

    def Bars_001(self, **kwargs) -> int:
        return self._taia.bars_001(**kwargs)

    def Bars_002(self, **kwargs) -> int:
        return self._taia.bars_002(**kwargs)

    def iBars(self, **kwargs) -> int:
        return self._taia.ibars(**kwargs)

    def iBarShift(self, **kwargs) -> int:
        return self._taia.ibar_shift(**kwargs)

    def iClose(self, **kwargs) -> float:
        return self._taia.iclose(**kwargs)

    def iHigh(self, **kwargs) -> float:
        return self._taia.ihigh(**kwargs)

    def iHighest(self, **kwargs) -> float:
        return self._taia.ihighest(**kwargs)

    def iLow(self, **kwargs) -> float:
        return self._taia.ilow(**kwargs)

    def iLowest(self, **kwargs) -> float:
        return self._taia.ilowest(**kwargs)

    def iOpen(self, **kwargs) -> float:
        return self._taia.iopen(**kwargs)

    def iTime(self, **kwargs) -> datetime:
        return self._taia.itime(**kwargs)

    def iVolume(self, **kwargs) -> int:
        return self._taia.ivolume(**kwargs)

    # mt4 conversion functions
    def NormalizeDouble(self, value: float, digits: int):
        # https://stackoverflow.com/a/41383900/2358836
        factor = 1 / (10 ** digits)
        return (value // factor) * factor

    def __UpdatePredefiniedVariables(self, parts: List[str]) -> None:
        self._pv.digits = int(parts[0])
        self._pv.point = float(parts[1])
        self._pv.last_error = int(parts[2])
        self._pv.period = int(parts[3])
        self._pv.symbol = parts[4]
        self._pv.ask = float(parts[5])
        self._pv.bars = int(parts[6])
        self._pv.bid = float(parts[7])
        self._pv.is_connected = self.__GetBoolFromString(data=parts[8])
        self._pv.is_optimization = self.__GetBoolFromString(data=parts[9])
        self._pv.is_testing = self.__GetBoolFromString(data=parts[10])
        self._pv.is_trade_allowed = self.__GetBoolFromString(data=parts[11])

        end_pos: int = 12
        self._pv.close, end_pos = self.__GetFloatList(parts=parts, start_idx=end_pos)
        self._pv.high, end_pos = self.__GetFloatList(parts=parts, start_idx=end_pos)
        self._pv.low, end_pos = self.__GetFloatList(parts=parts, start_idx=end_pos)
        self._pv.open, end_pos = self.__GetFloatList(parts=parts, start_idx=end_pos)
        self._pv.time, end_pos = self.__GetTimeList(parts=parts, start_idx=end_pos)
        self._pv.volume, end_pos = self.__GetIntList(parts=parts, start_idx=end_pos)

    def __GetBoolFromString(self, data: str) -> bool:
        if data == "0":
            return False
        else:
            return True

    def __GetTimeList(self, parts: List[str], start_idx: int) -> Union[List[datetime], int]:
        result: List[datetime] = list()

        data_len: int = int(parts[start_idx])
        start_idx += 1
        end_pos: int = start_idx + data_len

        i: int = start_idx
        while i < end_pos:
            result.append(datetime.strptime(parts[i], "%Y.%m.%d %H:%M:%S"))
            i += 1

        return (result, end_pos)

    def __GetIntList(self, parts: List[str], start_idx: int) -> Union[List[int], int]:
        result: List[int] = list()

        data_len: int = int(parts[start_idx])
        start_idx += 1
        end_pos: int = start_idx + data_len

        i: int = start_idx
        while i < end_pos:
            result.append(int(parts[i]))
            i += 1

        return (result, end_pos)

    def __GetFloatList(self, parts: List[str], start_idx: int) -> Union[List[float], int]:
        result: List[float] = list()

        data_len: int = int(parts[start_idx])
        start_idx += 1
        end_pos: int = start_idx + data_len

        i: int = start_idx
        while i < end_pos:
            result.append(float(parts[i]))
            i += 1

        return (result, end_pos)

    def __create_fun_map(self) -> Dict[str, Any]:
        fun_map = dict()

        # basic callbacks
        fun_map["OnInit"] = self.OnInit
        fun_map["OnTick"] = self.OnTick
        fun_map["OnTester"] = self.OnTester
        fun_map["OnChartEvent"] = self.OnChartEvent
        fun_map["OnTimer"] = self.OnTimer
        fun_map["OnDeinit"] = self.OnDeinit

        return fun_map
