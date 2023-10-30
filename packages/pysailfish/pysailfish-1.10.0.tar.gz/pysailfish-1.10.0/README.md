
## pysailfish

### Example EA --- simple client
```python
from pysailfish.internal.MT_EA.MT4_EA import MT4_EA

class MT4DemoEA(MT4_EA):
    def __init__(self):
        super().__init__()

    # override
    def _OnInit(self) -> int:
        self._logger.info(self._user_inputs)
        self._logger.info("Here")
        return 0

    # override
    def _OnDeinit(self, reason: int) -> None:
        self._logger.info(f"Here reason: {reason}")
        return None

    # override
    def _OnTick(self) -> None:
        self._logger.info("Here")
        return None

    # override
    def _OnTimer(self) -> None:
        return None

    # override
    def _OnTester(self) -> float:
        self._logger.info("Here")
        return 0.0

    # override
    def _OnChartEvent(self
                      , id: int
                      , lparam: int
                      , dparam: float
                      , sparam: str) -> None:
        self._logger.info(f"Here id: {id} lparam: {lparam} dparam: {dparam} sparam: {sparam}")
        return None

def main() -> None:
    ea = MT4DemoEA()
    ea.InitComponent(server_ip="127.0.0.1"
                     , server_port=23456
                     , ea_name="MT4DemoEA")
    ea.StartEA()

if __name__ == "__main__":
    main()
```

### Example EA --- Moving Average EA
```python
from datetime import datetime

import pysailfish.internal.MT_EA.mt4_const as mc
from pysailfish.internal.MT_EA.MT4_EA import MT4_EA

class MA_EA(MT4_EA):
    def __init__(self):
        super().__init__()

    # override
    def _OnInit(self) -> int:
        self._logger.info(self._user_inputs)
        self._logger.info("Here")
        return 0

    # override
    def _OnDeinit(self, reason: int) -> None:
        self._logger.info(f"Here reason: {reason}")
        return None

    # override
    def _OnTick(self) -> None:
        vv = self.iADX(symbol=self._pv.symbol
                       , timeframe=mc.PERIOD_CURRENT
                       , period=self._user_inputs["MovingPeriod"]
                       , applied_price=mc.PRICE_CLOSE
                       , mode=mc.MODE_MAIN
                       , shift=0)
        # self._logger.info(f"Here {self._pv.symbol} {self._pv.time[0]}")
        # --- check for history and trading
        if self._pv.bars < 100 or self._pv.is_trade_allowed == False:
            return

        # --- calculate open orders by current symbol
        if self.__calculate_current_orders(self._pv.symbol) == 0:
            self.__check_for_open()
        else:
            self.__check_for_close()
        return None

    # override
    def _OnTimer(self) -> None:
        return None

    # override
    def _OnTester(self) -> float:
        self._logger.info("Here")
        return 0.0

    # override
    def _OnChartEvent(self
                      , id: int
                      , lparam: int
                      , dparam: float
                      , sparam: str) -> None:
        self._logger.info(f"Here id: {id} lparam: {lparam} dparam: {dparam} sparam: {sparam}")
        return None

    def __check_for_close(self) -> None:
        ma: float = 0
        #--- go trading only for first tiks of new bar
        if self._pv.volume[0] > 1:
            return None
        #--- get Moving Average
        ma = self.iMA(symbol=self._pv.symbol
                      , timeframe=mc.PERIOD_CURRENT
                      , ma_period=self._user_inputs["MovingPeriod"]
                      , ma_shift=self._user_inputs["MovingShift"]
                      , ma_method=mc.MODE_SMA
                      , applied_price=mc.PRICE_CLOSE
                      , shift=0)
        #---
        for i in range(self.OrdersTotal()):
            if self.OrderSelect(index=i, select=mc.SELECT_BY_POS, pool=mc.MODE_TRADES) == False:
                break
            if self.OrderMagicNumber() != self._pv.magic_num or self.OrderSymbol() != self._pv.symbol:
                continue
            #--- check order type
            if self.OrderType() == mc.OP_BUY:
                if self._pv.open[1] > ma and self._pv.close[1] < ma:
                    if not self.OrderClose(ticket=self.OrderTicket(), lots=self.OrderLots(), price=self._pv.bid, slippage=3, arrow_color=mc.clrWhite):
                        self._logger.error(f"OrderClose error {self.GetLastError()}")
                break
            if self.OrderType() == mc.OP_SELL:
                if self._pv.open[1] < ma and self._pv.close[1] > ma:
                    if not self.OrderClose(ticket=self.OrderTicket(), lots=self.OrderLots(), price=self._pv.ask, slippage=3, arrow_color=mc.clrWhite):
                        self._logger.error(f"OrderClose error {self.GetLastError()}");
                break

    def __lots_optimized(self) -> float:
        lot: float = float(self._user_inputs["Lots"])
        maximum_risk: float = float(self._user_inputs["MaximumRisk"])
        decrease_factor: float = float(self._user_inputs["DecreaseFactor"])
        orders: int = self.OrdersHistoryTotal() # history orders total
        losses: int = 0 # number of losses orders without a break
        #--- select lot size
        lot = self.NormalizeDouble(value=(self.AccountFreeMargin() * maximum_risk / 1000.0), digits=1);
        #--- calcuulate number of losses orders without a break
        if decrease_factor > 0:
            for i in reversed(range(orders)):
                if self.OrderSelect(index=i, select=mc.SELECT_BY_POS, pool=mc.MODE_HISTORY) == False:
                    self._logger.error("Error in history")
                    break
                if self.OrderSymbol() != self._pv.symbol or self.OrderType() > mc.OP_SELL:
                    continue
                #---
                if self.OrderProfit() > 0:
                    break
                if self.OrderProfit() < 0:
                    losses += 1
            if losses > 1:
                lot = self.NormalizeDouble(value=(lot - lot * losses / decrease_factor), digits=1)
        #--- return lot size
        if lot < 0.1:
            lot = 0.1
        return lot

    def __check_for_open(self) -> None:
        ma: float = 0
        res: int = 0
        #--- go trading only for first tiks of new bar
        if self._pv.volume[0] > 1:
            return None
        #--- get Moving Average
        ma = self.iMA(symbol=self._pv.symbol
                      , timeframe=mc.PERIOD_CURRENT
                      , ma_period=self._user_inputs["MovingPeriod"]
                      , ma_shift=self._user_inputs["MovingShift"]
                      , ma_method=mc.MODE_SMA
                      , applied_price=mc.PRICE_CLOSE
                      , shift=0)
        #--- sell conditions
        if self._pv.open[1] > ma and self._pv.close[1] < ma:
            res = self.OrderSend(symbol=self._pv.symbol
                                 , cmd=mc.OP_SELL
                                 , volume=self.__lots_optimized()
                                 , price=self._pv.bid
                                 , slippage=3
                                 , stoploss=0
                                 , takeprofit=0
                                 , comment=""
                                 , magic=self._pv.magic_num
                                 , expiration=datetime(1970, 1, 1, 0, 0, 0)
                                 , arrow_color=mc.clrRed)
            return None
        #--- buy conditions
        if self._pv.open[1] < ma and self._pv.close[1] > ma:
            res = self.OrderSend(symbol=self._pv.symbol
                                 , cmd=mc.OP_BUY
                                 , volume=self.__lots_optimized()
                                 , price=self._pv.ask
                                 , slippage=3
                                 , stoploss=0
                                 , takeprofit=0
                                 , comment=""
                                 , magic=self._pv.magic_num
                                 , expiration=datetime(1970, 1, 1, 0, 0, 0)
                                 , arrow_color=mc.clrBlue)
            return None

    def __calculate_current_orders(self, symbol: str) -> int:
        buys: int = 0
        sells: int = 0
        # ---
        for i in range(self.OrdersTotal()):
            if self._tf.order_select(index=i, select=mc.SELECT_BY_POS, pool=mc.MODE_TRADES) == False:
                break
            if self.OrderSymbol() == self._pv.symbol and self.OrderMagicNumber() == self._pv.magic_num:
                if self.OrderType() == mc.OP_BUY:
                    buys += 1
                if self.OrderType() == mc.OP_SELL:
                    sells += 1
        # --- return orders volume
        if buys > 0:
            return buys
        else:
            return -sells

def main() -> None:
    ea = MA_EA()
    ea.InitComponent(server_ip="127.0.0.1"
                     , server_port=23456
                     , ea_name="MA_EA")
    ea.StartEA()

if __name__ == "__main__":
    main()
```

### How to publish to pypi
```bash
# set up pypi token
$ poetry config pypi-token.pypi my-token

# build the project
$ poetry build

# publish the project
$ poetry publish

# DONE
```
