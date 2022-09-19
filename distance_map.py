"""Assignment 1 - Distance map (Task 1)

CSC148, Winter 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Maryam Majedi, and Jaisie Sin.

===== Module Description =====

This module contains the class DistanceMap, which is used to store
and look up distances between cities. This class does not read distances
from the map file. (All reading from files is done in module experiment.)
Instead, it provides public methods that can be called to store and look up
distances.
"""
from typing import Dict


class DistanceMap:
    """ A distance map.

       === Private Attributes ===
       _distance_map: a dictionary with name of start location as key,
       sub-dictionary as values. Each key for the sub-dictionary is name of
       end location, the distance from start location to end
       location as value.

       === Representation Invariants ===
       - We do not need to get the distance between 2 same locations (?
       """
    _distance_map: Dict[str, Dict[str, int]]

    def __init__(self) -> None:
        """Initialize a distance map"""
        self._distance_map = {}

    def add_distance(self, loc1: str, loc2: str, d1: int, d2: int = -1) -> None:
        """Add distance between <loc1> and <loc2> to self._distance_map.
        Return None."""
        dict_ = self._distance_map
        if loc1 not in dict_:
            dict_[loc1] = {}
            # dict_[loc1][loc1] = 0
        if loc2 not in dict_:
            dict_[loc2] = {}
            # dict_[loc2][loc2] = 0
        if d2 == -1:
            dict_[loc1][loc2] = d1
            dict_[loc2][loc1] = d1
        else:
            dict_[loc1][loc2] = d1
            dict_[loc2][loc1] = d2

    def distance(self, loc1: str, loc2: str) -> int:
        """Return the distance from <loc1> to <loc2>.
        Return -1 if distance not stored."""
        d_map = self._distance_map
        if loc1 in d_map and loc2 in d_map[loc1]:
            return self._distance_map[loc1][loc2]
        return -1


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest

    doctest.testmod()
