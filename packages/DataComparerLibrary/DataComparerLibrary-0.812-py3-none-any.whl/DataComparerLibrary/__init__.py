#!/usr/bin/env python

from DataComparerLibrary.datacomparer import DataComparer
from DataComparerLibrary.datasorter import DataSorter


class DataComparerLibrary(DataComparer, DataSorter):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'



