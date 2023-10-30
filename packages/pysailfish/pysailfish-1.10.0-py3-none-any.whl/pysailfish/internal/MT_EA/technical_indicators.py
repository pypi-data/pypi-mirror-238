from typing import Dict, List, Set, Tuple, Union, Any

import pysailfish.internal.MT_EA.mt4_const as mc
from pysailfish.internal.DataCtrl.MT4DataCtrl.MT4DataCtrl import MT4DataCtrl

# https://docs.mql4.com/indicators
class technical_indicators(object):
    def __init__(self):
        self.__data_ctrl: MT4DataCtrl = None
        self.__fun_num_map: Dict[str, int] = dict()

    def init_component(self, data_ctrl: MT4DataCtrl, fun_num_map: Dict[str, int]):
        self.__data_ctrl = data_ctrl
        self.__fun_num_map = fun_num_map

    def i_ac(self, symbol: str, timeframe: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iAC"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_ad(self, symbol: str, timeframe: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iAD"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_adx(self, symbol: str, timeframe: int, period: int, applied_price: int, mode: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iADX"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(period))
        self.__data_ctrl.add_data_to_msg(data=str(applied_price))
        self.__data_ctrl.add_data_to_msg(data=str(mode))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_alligator(self
                    , symbol: str
                    , timeframe: int
                    , jaw_period: int
                    , jaw_shift: int
                    , teeth_period: int
                    , teeth_shift: int
                    , lips_period: int
                    , lips_shift: int
                    , ma_method: int
                    , applied_price: int
                    , mode: int
                    , shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iAlligator"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(jaw_period))
        self.__data_ctrl.add_data_to_msg(data=str(jaw_shift))
        self.__data_ctrl.add_data_to_msg(data=str(teeth_period))
        self.__data_ctrl.add_data_to_msg(data=str(teeth_shift))
        self.__data_ctrl.add_data_to_msg(data=str(lips_period))
        self.__data_ctrl.add_data_to_msg(data=str(lips_shift))
        self.__data_ctrl.add_data_to_msg(data=str(ma_method))
        self.__data_ctrl.add_data_to_msg(data=str(applied_price))
        self.__data_ctrl.add_data_to_msg(data=str(mode))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_ao(self, symbol: str, timeframe: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iAO"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_atr(self, symbol: str, timeframe: int, period: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iATR"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(period))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_bears_power(self, symbol: str, timeframe: int, period: int, applied_price: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iBearsPower"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(period))
        self.__data_ctrl.add_data_to_msg(data=str(applied_price))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_bands(self, symbol: str, timeframe: int, period: int, deviation: float, bands_shift: int, applied_price: int, mode: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iBands"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(period))
        self.__data_ctrl.add_data_to_msg(data=str(deviation))
        self.__data_ctrl.add_data_to_msg(data=str(bands_shift))
        self.__data_ctrl.add_data_to_msg(data=str(applied_price))
        self.__data_ctrl.add_data_to_msg(data=str(mode))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_bands_on_array(self, array: List[float], total: int, period: int, deviation: float, bands_shift: int, applied_price: int, mode: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iBandsOnArray"]))
        self.__data_ctrl.add_data_to_msg(data=str(len(array)))
        self.__data_ctrl.add_data_to_msg(data=",".join([str(ele) for ele in array]))
        self.__data_ctrl.add_data_to_msg(data=str(total))
        self.__data_ctrl.add_data_to_msg(data=str(period))
        self.__data_ctrl.add_data_to_msg(data=str(deviation))
        self.__data_ctrl.add_data_to_msg(data=str(bands_shift))
        self.__data_ctrl.add_data_to_msg(data=str(applied_price))
        self.__data_ctrl.add_data_to_msg(data=str(mode))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_bulls_power(self, symbol: str, timeframe: int, period: int, applied_price: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iBullsPower"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(period))
        self.__data_ctrl.add_data_to_msg(data=str(applied_price))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_cci(self, symbol: str, timeframe: int, period: int, applied_price: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iCCI"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(period))
        self.__data_ctrl.add_data_to_msg(data=str(applied_price))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_cci_on_array(self, array: List[float], total: int, period: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iCCIOnArray"]))
        self.__data_ctrl.add_data_to_msg(data=str(len(array)))
        self.__data_ctrl.add_data_to_msg(data=",".join([str(ele) for ele in array]))
        self.__data_ctrl.add_data_to_msg(data=str(total))
        self.__data_ctrl.add_data_to_msg(data=str(period))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_custom(self, **kwargs) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iCustom"]))
        for k, v in kwargs.items():
            self.__data_ctrl.add_data_to_msg(data=v)
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_de_marker(self, symbol: str, timeframe: int, period: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iDeMarker"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(period))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_envelopes(self
                    , symbol: str
                    , timeframe: int
                    , ma_period: int
                    , ma_method: int
                    , ma_shift: int
                    , applied_price: int
                    , deviation: float
                    , mode: int
                    , shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iEnvelopes"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(ma_period))
        self.__data_ctrl.add_data_to_msg(data=str(ma_method))
        self.__data_ctrl.add_data_to_msg(data=str(ma_shift))
        self.__data_ctrl.add_data_to_msg(data=str(applied_price))
        self.__data_ctrl.add_data_to_msg(data=str(deviation))
        self.__data_ctrl.add_data_to_msg(data=str(mode))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_envelopes_on_array(self
                             , array: List[float]
                             , total: int
                             , ma_period: int
                             , ma_method: int
                             , ma_shift: int
                             , deviation: float
                             , mode: int
                             , shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iEnvelopesOnArray"]))
        self.__data_ctrl.add_data_to_msg(data=str(len(array)))
        self.__data_ctrl.add_data_to_msg(data=",".join([str(ele) for ele in array]))
        self.__data_ctrl.add_data_to_msg(data=str(total))
        self.__data_ctrl.add_data_to_msg(data=str(ma_period))
        self.__data_ctrl.add_data_to_msg(data=str(ma_method))
        self.__data_ctrl.add_data_to_msg(data=str(ma_shift))
        self.__data_ctrl.add_data_to_msg(data=str(deviation))
        self.__data_ctrl.add_data_to_msg(data=str(mode))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_force(self, symbol: str, timeframe: int, period: int, ma_method: int, applied_price: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iForce"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(period))
        self.__data_ctrl.add_data_to_msg(data=str(ma_method))
        self.__data_ctrl.add_data_to_msg(data=str(applied_price))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_fratals(self, symbol: str, timeframe: int, mode: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iFratals"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(mode))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_gator(self
                , symbol: str
                , timeframe: int
                , jaw_period: int
                , jaw_shift: int
                , teeth_period: int
                , teeth_shift: int
                , lips_period: int
                , lips_shift: int
                , ma_method: int
                , applied_price: int
                , mode: int
                , shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iGator"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(jaw_period))
        self.__data_ctrl.add_data_to_msg(data=str(jaw_shift))
        self.__data_ctrl.add_data_to_msg(data=str(teeth_period))
        self.__data_ctrl.add_data_to_msg(data=str(teeth_shift))
        self.__data_ctrl.add_data_to_msg(data=str(lips_period))
        self.__data_ctrl.add_data_to_msg(data=str(lips_shift))
        self.__data_ctrl.add_data_to_msg(data=str(ma_method))
        self.__data_ctrl.add_data_to_msg(data=str(applied_pr))
        self.__data_ctrl.add_data_to_msg(data=str(mode))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_ichimoku(self, symbol: str, timeframe: int, tenkan_sen: int, kijun_sen: int, senkou_span_b: int, mode: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iIchimoku"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(tenkan_sen))
        self.__data_ctrl.add_data_to_msg(data=str(kijun_sen))
        self.__data_ctrl.add_data_to_msg(data=str(senkou_span_b))
        self.__data_ctrl.add_data_to_msg(data=str(mode))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_bwmfi(self, symbol: str, timeframe: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iBWMFI"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_momentum(self, symbol: str, timeframe: int, period: int, applied_price: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iMomentum"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(period))
        self.__data_ctrl.add_data_to_msg(data=str(applied_price))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_momentum_on_array(self, array: List[float], total: int, period: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iMomentumOnArray"]))
        self.__data_ctrl.add_data_to_msg(data=str(len(array)))
        self.__data_ctrl.add_data_to_msg(data=",".join([str(ele) for ele in array]))
        self.__data_ctrl.add_data_to_msg(data=str(total))
        self.__data_ctrl.add_data_to_msg(data=str(period))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_mfi(self, symbol: str, timeframe: int, period: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iMFI"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(period))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_ma(self, symbol: str, timeframe: int, ma_period: int, ma_shift: int, ma_method: int, applied_price: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iMA"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(ma_period))
        self.__data_ctrl.add_data_to_msg(data=str(ma_shift))
        self.__data_ctrl.add_data_to_msg(data=str(ma_method))
        self.__data_ctrl.add_data_to_msg(data=str(applied_price))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_ma_on_array(self, array: List[float], total: int, ma_period: int, ma_shift: int, ma_method: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iMAOnArray"]))
        self.__data_ctrl.add_data_to_msg(data=str(len(array)))
        self.__data_ctrl.add_data_to_msg(data=",".join([str(ele) for ele in array]))
        self.__data_ctrl.add_data_to_msg(data=str(total))
        self.__data_ctrl.add_data_to_msg(data=str(ma_period))
        self.__data_ctrl.add_data_to_msg(data=str(ma_shift))
        self.__data_ctrl.add_data_to_msg(data=str(ma_method))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_os_ma(self, symbol: str, timeframe: int, fast_ema_period: int, slow_ema_period: int, signal_period: int, applied_price: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iOsMA"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(fast_ema_period))
        self.__data_ctrl.add_data_to_msg(data=str(slow_ema_shift))
        self.__data_ctrl.add_data_to_msg(data=str(signal_period))
        self.__data_ctrl.add_data_to_msg(data=str(applied_price))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_macd(self, symbol: str, timeframe: int, fast_ema_period: int, slow_ema_period: int, signal_period: int, applied_price: int, mode: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iMACD"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(fast_ema_period))
        self.__data_ctrl.add_data_to_msg(data=str(slow_ema_shift))
        self.__data_ctrl.add_data_to_msg(data=str(signal_period))
        self.__data_ctrl.add_data_to_msg(data=str(applied_price))
        self.__data_ctrl.add_data_to_msg(data=str(mode))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_obv(self, symbol: str, timeframe: int, applied_price: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iOBV"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(applied_price))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_sar(self, symbol: str, timeframe: int, step: float, maximum: float, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iSAR"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(step))
        self.__data_ctrl.add_data_to_msg(data=str(maximum))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_rsi(self, symbol: str, timeframe: int, period: int, applied_price: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iRSI"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(period))
        self.__data_ctrl.add_data_to_msg(data=str(applied_price))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_rsi_on_array(self, array: List[float], total: int, period: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iRSIOnArray"]))
        self.__data_ctrl.add_data_to_msg(data=str(len(array)))
        self.__data_ctrl.add_data_to_msg(data=",".join([str(ele) for ele in array]))
        self.__data_ctrl.add_data_to_msg(data=str(total))
        self.__data_ctrl.add_data_to_msg(data=str(period))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_rvi(self, symbol: str, timeframe: int, period: int, mode: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iRVI"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(period))
        self.__data_ctrl.add_data_to_msg(data=str(mode))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_std_dev(self, symbol: str, timeframe: int, ma_period: int, ma_shift: int, ma_method: int, applied_price: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iStdDev"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(ma_period))
        self.__data_ctrl.add_data_to_msg(data=str(ma_shift))
        self.__data_ctrl.add_data_to_msg(data=str(ma_method))
        self.__data_ctrl.add_data_to_msg(data=str(applied_price))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_std_dev_on_array(self, array: List[float], total: int, ma_period: int, ma_shift: int, ma_method: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iStdDevOnArray"]))
        self.__data_ctrl.add_data_to_msg(data=str(len(array)))
        self.__data_ctrl.add_data_to_msg(data=",".join([str(ele) for ele in array]))
        self.__data_ctrl.add_data_to_msg(data=str(total))
        self.__data_ctrl.add_data_to_msg(data=str(ma_period))
        self.__data_ctrl.add_data_to_msg(data=str(ma_shift))
        self.__data_ctrl.add_data_to_msg(data=str(ma_method))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_stochastic(self, symbol: str, timeframe: int, Kperiod: int, Dperiod: int, slowing, int, method: int, price_field: int, mode: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iStochastic"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(Kperiod))
        self.__data_ctrl.add_data_to_msg(data=str(Dperiod))
        self.__data_ctrl.add_data_to_msg(data=str(slowing))
        self.__data_ctrl.add_data_to_msg(data=str(method))
        self.__data_ctrl.add_data_to_msg(data=str(price_field))
        self.__data_ctrl.add_data_to_msg(data=str(mode))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()

    def i_wpr(self, symbol: str, timeframe: int, period: int, shift: int) -> float:
        self.__data_ctrl.add_data_to_msg(data=str(self.__fun_num_map["iWPR"]))
        self.__data_ctrl.add_data_to_msg(data=symbol)
        self.__data_ctrl.add_data_to_msg(data=str(timeframe))
        self.__data_ctrl.add_data_to_msg(data=str(period))
        self.__data_ctrl.add_data_to_msg(data=str(shift))
        self.__data_ctrl.send_message()

        return self.__data_ctrl.receive_float_from_mt4()
