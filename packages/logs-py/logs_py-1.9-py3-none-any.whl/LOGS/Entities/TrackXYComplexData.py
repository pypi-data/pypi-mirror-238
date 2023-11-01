from typing import Optional

from LOGS.Entities.DatatrackNumericArray import DatatrackNumericArray
from LOGS.Entities.TrackData import TrackData


class TrackXYComplexData(TrackData):
    _x: Optional[DatatrackNumericArray] = None
    _re: Optional[DatatrackNumericArray] = None
    _im: Optional[DatatrackNumericArray] = None

    def fetchFull(self):
        if self.x:
            self.x.fetchFull()
        if self.re:
            self.re.fetchFull()
        if self.im:
            self.im.fetchFull()

    @property
    def x(self) -> Optional[DatatrackNumericArray]:
        return self._x

    @x.setter
    def x(self, value):
        self._x = self.checkAndConvertNullable(value, DatatrackNumericArray, "x")

    @property
    def re(self) -> Optional[DatatrackNumericArray]:
        return self._re

    @re.setter
    def re(self, value):
        self._re = self.checkAndConvertNullable(value, DatatrackNumericArray, "re")

    @property
    def im(self) -> Optional[DatatrackNumericArray]:
        return self._im

    @im.setter
    def im(self, value):
        self._im = self.checkAndConvertNullable(value, DatatrackNumericArray, "im")
