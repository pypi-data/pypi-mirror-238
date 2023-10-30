from typing import List
from datetime import datetime

digits: int = 0
point: float = 0
last_error: int = 0
period: int = 0
symbol: str = ""
ask: float = 0
bars: int = 0
bid: float = 0

magic_num: int = 0

is_connected: bool = False
is_optimization: bool = False
is_testing: bool = False
is_trade_allowed: bool = False

close: List[float] = list()
high: List[float] = list()
low: List[float] = list()
open: List[float] = list()
time: List[datetime] = list()
volume: List[int] = list()
