import sys
import numpy as np
from textural_image_features.gtsdmatrix import GTSDMatrix
from functools import cached_property, lru_cache


class FeaturesExtractor:
    """
    Extracts textural features of an image when provided with its
    GTSDM (gray-tone spatial-dependence matrix).
    Information about  implemented features:
    http://haralick.org/journals/TexturalFeatures.pdf
    """

    def __init__(self, gtsdm: GTSDMatrix):
        if not isinstance(gtsdm, GTSDMatrix):
            raise TypeError(
                f"Provided object is of type {type(gtsdm)}! Expected {GTSDMatrix.__name__}"
            )
        self._gtsdm = gtsdm

    @classmethod
    def from_array(cls, array):
        return cls(GTSDMatrix(array))

    # region Primary Features

    @cached_property
    def gtsdm(self):
        return self._gtsdm

    @cached_property
    def angular_second_moment(self):
        return np.sum(self._gtsdm._base_array**2)

    @cached_property
    def contrast(self):
        arr_of_ns = np.arange(0, self._gtsdm.N_g)
        return np.sum((arr_of_ns**2) * self._gtsdm.P_XY_DIFF[arr_of_ns])

    @lru_cache(maxsize=256)
    def correlation(self, x, y):
        indices = np.arange(self._gtsdm.N_g)
        return (np.sum(indices.reshape(-1, 1) * indices * self._gtsdm.array)) - np.mean(
            self._gtsdm[x]
        ) * np.mean(self._gtsdm[:, y]) / (
            np.std(self._gtsdm[x]) * np.std(self._gtsdm[:, y])
        )

    @cached_property
    def sum_of_squares(self):
        indices = np.arange(self._gtsdm.N_g)
        return np.sum(
            np.reshape((indices - np.mean(self._gtsdm.N_g)) ** 2, (self._gtsdm.N_g, 1))
            * self._gtsdm.N_g
        )

    @cached_property
    def inverse_difference_moment(self):
        indices = np.arange(self._gtsdm.N_g)
        return np.sum(
            1 / (1 + (indices.reshape(-1, 1) - indices) ** 2) * self._gtsdm.array
        )

    @cached_property
    def sum_average(self):
        indices = np.arange(1, 2 * self._gtsdm.N_g - 1, dtype=np.intp)
        return np.sum(indices * self._gtsdm.P_XY_SUM[indices])

    @cached_property
    def sum_entropy(self):
        p_xy_sum_slice = self._gtsdm.P_XY_SUM[1:]
        return -np.sum(p_xy_sum_slice * np.log(p_xy_sum_slice + sys.float_info.epsilon))

    @cached_property
    def sum_variance(self):
        indices = np.arange(1, 2 * self._gtsdm.N_g - 1, dtype=np.intp)
        p_xy_sum_slice = self._gtsdm.P_XY_SUM[1:]
        return np.sum(p_xy_sum_slice * (indices - self.sum_entropy) ** 2)

    @cached_property
    def entropy(self):
        return -np.sum(
            self._gtsdm.array * np.log(self._gtsdm.array + sys.float_info.epsilon)
        )

    @cached_property
    def difference_entropy(self):
        return -np.sum(self._gtsdm.P_XY_DIFF * np.log(self._gtsdm.P_XY_DIFF))

    @cached_property
    def difference_variance(self):
        return np.sum(
            (np.arange(self._gtsdm.N_g) - self.difference_entropy) ** 2
            * self._gtsdm.P_XY_DIFF
        )

    @lru_cache(256)
    def information_measures_of_correlation(self, x, y):
        f12 = (self.HXY - self.HXY1) / np.max([self._gtsdm.HX[x], self._gtsdm.HY[y]])
        f13 = np.sqrt(1 - np.exp((-2.0) * (self.HXY2 - self.HXY)))
        return f12, f13

    @cached_property
    def maximal_correlation_coeff(self):
        Q = (
            (self._gtsdm.array / np.sum(self._gtsdm.array, axis=0))
            @ self._gtsdm.array.T
            / np.sum(self._gtsdm.array, axis=1).reshape(-1, 1)
        )
        eigenvalues = np.unique(np.linalg.eigvals(Q))
        return np.sqrt(eigenvalues[-2])

    # endregion !Primary Features

    # region Secondary Features

    @property
    def HXY(self):
        return self.entropy

    @cached_property
    def HXY1(self):
        p_xy_prod = self._gtsdm.P_X.reshape(-1, 1) * self._gtsdm.P_Y
        return -np.sum(self._gtsdm.array * np.log(p_xy_prod + sys.float_info.epsilon))

    @cached_property
    def HXY2(self):
        p_xy_prod = self._gtsdm.P_X.reshape(-1, 1) * self._gtsdm.P_Y
        return -np.sum(p_xy_prod * np.log(p_xy_prod + sys.float_info.epsilon))

    # endregion
