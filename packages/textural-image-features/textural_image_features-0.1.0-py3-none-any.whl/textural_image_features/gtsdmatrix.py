import numpy as np
import sys


class GTSDMatrix:
    """
    Represents a helper class for extraction of some
    special properties from gray-tone spatial-dependence matrices
    """

    def __init__(self, gtsdm):
        if not isinstance(gtsdm, np.ndarray):
            raise TypeError(
                f"Provided object is of type {type(gtsdm)}! Expected {np.ndarray.__name__}"
            )
        if gtsdm.ndim != 2:
            raise ValueError(
                f"Provided matrix has {gtsdm.ndim} dimensions! Expected 2."
            )
        self._base_array = gtsdm
        # lazily evaluated
        self._P_X = None
        self._P_Y = None
        self._P_XY_SUM = None
        self._P_XY_DIFF = None
        self._HX = None
        self._HY = None

    # region Features

    @property
    def array(self):
        """
        NDarray buffer
        """
        return self._base_array

    @property
    def N_g(self):
        """
        Number of graytone levels
        """
        return self._base_array.shape[0]

    @property
    def P_X(self):
        if self._P_X is None:
            self._P_X = np.sum(self._base_array, axis=1)
        return self._P_X

    @property
    def P_Y(self):
        if self._P_Y is None:
            self._P_Y = np.sum(self._base_array, axis=0)
        return self._P_Y

    @property
    def P_XY_SUM(self):
        """
        Sum of elements whose indices (i, j)
        satisfy i + j = k
        """
        if self._P_XY_SUM is None:
            self._P_XY_SUM = np.array(
                [
                    np.fliplr(self._base_array).diagonal(self.N_g - 1 - k).sum()
                    for k in range(0, 2 * self.N_g - 1)
                ],
                dtype=np.float64,
            )
        return self._P_XY_SUM

    @property
    def P_XY_DIFF(self):
        """
        Sum of elements whose indices (i, j)
        satisfy |i - j| = k
        """
        if self._P_XY_DIFF is None:
            self._P_XY_DIFF = np.array(
                [
                    np.sum(self._base_array.diagonal(k) + self._base_array.diagonal(-k))
                    for k in range(0, self.N_g)
                ],
                dtype=np.float64,
            )
        return self._P_XY_DIFF

    @property
    def HX(self):
        if self._HX is None:
            self._HX = np.sum(
                self._base_array * np.log(self._base_array + sys.float_info.epsilon),
                axis=1,
            )
        return self._HX

    @property
    def HY(self):
        if self._HY is None:
            self._HY = np.sum(
                self._base_array * np.log(self._base_array + sys.float_info.epsilon),
                axis=0,
            )
        return self._HY

    # endregion

    # region Utility

    def __getitem__(self, index):
        return self._base_array[index]

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self._base_array)})"

    # endregion
