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
