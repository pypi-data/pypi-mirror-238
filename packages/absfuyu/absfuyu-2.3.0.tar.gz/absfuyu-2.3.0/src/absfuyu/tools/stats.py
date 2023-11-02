# -*- coding: utf-8 -*-
"""
Absfuyu: Stats
---
List's stats

Version: 2.0.0
Date updated: 05/06/2023 (dd/mm/yyyy)
"""


# Module level
###########################################################################
__all__ = [
    "ListStats"
]


# Library
###########################################################################
import math
from typing import List, Union

from absfuyu.collections.data_extension import ListKai
from absfuyu.logger import logger


# Class
###########################################################################
class ListStats(List[Union[int, float]]):
    """Stats"""
    def mean(self) -> float:
        """Mean/Average"""
        s = sum(self)
        return s/len(self)

    def median(self) -> Union[int, float]:
        """Median - Middle value"""
        lst = sorted(self)
        LENGTH = len(lst)
        if LENGTH % 2 != 0:
            return lst[math.floor(LENGTH / 2)]
        else:
            num1 = lst[math.floor(LENGTH / 2) - 1]
            num2 = lst[math.floor(LENGTH / 2)]
            med = (num1 + num2) / 2
            return med

    def mode(self) -> List[Union[int, float]]:
        """Mode:
        
        The Mode value is the value that appears the most number of times
        """
        lst = self
        frequency = ListKai(lst).freq()
        
        max_val = max(frequency.values())
        keys = []
        
        for k, v in frequency.items():
            if v == max_val:
                keys.append(k)
        
        return keys

    def var(self) -> float:
        """Variance"""
        lst = self
        MEAN = self.mean()
        v = [(x-MEAN)**2 for x in lst]
        out = sum(v)/len(v)
        return out

    def std(self) -> float:
        """Standard deviation"""
        sd = math.sqrt(self.var())
        return sd

    def percentile(self, percent: int = 50) -> Union[int, float]:
        """Percentile"""
        lst = self
        idx = math.floor(len(lst) / 100 * percent)
        if idx == len(lst):
            idx -= 1
        return sorted(lst)[idx]

    def summary(self):
        """Quick summary of data"""
        lst = self
        output = {
            "Observations": len(lst),
            "Mean": self.mean(),
            "Median": self.median(),
            "Mode": self.mode(),
            "Standard deviation": self.std(),
            "Variance": self.var(),
            "Max": max(lst),
            "Min": min(lst),
            "Percentiles": {
                "1st Quartile": self.percentile(25),
                "2nd Quartile": self.percentile(50),
                "3rd Quartile": self.percentile(75),
            }
        }
        return output


# Run
###########################################################################
if __name__ == "__main__":
    logger.setLevel(10)
    from rich import print
    test = ListStats([1,8,9,2,3,4,4])
    print(test.summary())