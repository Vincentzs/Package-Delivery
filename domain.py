"""Assignment 1 - Domain classes (Task 2)

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

This module contains the classes required to represent the entities
in the simulation: Parcel, Truck and Fleet.
"""
from typing import List, Dict
from distance_map import DistanceMap


class Parcel:
    # It must be consistent with the Fleet class docstring examples below.
    """ A parcel.

    === Private Attributes ===
    _id: ID of a parcel.
    _source: _source of a parcel.
    _destination: _destination of a parcel.
    _volume: the _volume of a parcel.

    === Representation Invariants ===
    - each parcel has a unique ID.
    - _volume is a positive integer.
    - No parcels have the depot as destination
    """
    _id: int
    _source: str
    _destination: str
    _volume: int

    def __init__(self, id_: int, volume: int, source: str, d: str) -> None:
        """Initialize this truck.

        Preconditions:
        - <_volume> is positive.
        - <_destination> can not be the same as _depot.
        """
        self._id = id_
        self._volume = volume
        self._source = source
        self._destination = d

    def __str__(self) -> str:
        """Return a string representing this parcel."""
        return f'Parcel# {self._id} with volume {self._volume} cc has ' \
               f'source {self._source} and destination {self._destination}.'

    def get_id(self) -> int:
        """Return the <_id> of this Parcel"""
        return self._id

    def get_source(self) -> str:
        """Return the <_source> of Parcel"""
        return self._source

    def get_destination(self) -> str:
        """Return the <_destination> of Parcel"""
        return self._destination

    def get_volume(self) -> int:
        """Return the <_volume> of Parcel"""
        return self._volume


class Truck:
    # It must be consistent with the Fleet class docstring examples below.
    """ A truck that stores parcel.

    === Private Attributes ===
    _id: ID of a truck.
    _capacity: _volume _capacity of a truck.
    # _load: current truck load of parcels (0 if no load)
    _depot: the _depot of the truck.
    _parcels: _parcels stored in this truck.
    _routes: _routes of a truck.

    === Representation Invariants ===
    - each truck has a unique ID.
    - _capacity is a positive integer.
    - All parcels have been shipped from their source city to the depot
    - No parcels have the depot as destination
    """
    _id: int
    _capacity: int
    # _load: int
    _depot: str
    _parcels: List[Parcel]
    _routes: List[str]

    def __init__(self, id_: int, capacity: int, depot: str) -> None:
        """Initialize this truck.

        Precondition: <_capacity> is positive."""
        self._id = id_
        # self._load = 0
        self._capacity = capacity
        self._depot = depot
        self._parcels = []
        self._routes = [depot]

    def __str__(self) -> str:
        """Return a string representing this Truck."""
        s = ''
        for p in self._parcels:
            s += '\n  ' + str(p)
        return f'Truck# {self._id} has capacity {self._capacity} and ' \
               f'{self._depot} as depot:' + s

    def get_id(self) -> int:
        """Return the <_id> of this Truck"""
        return self._id

    def get_capacity(self) -> int:
        """Return the <_capacity> of this Truck"""
        return self._capacity

    # def get_load(self) -> int:
    #     """Return the <_load> of this Truck"""
    #     return self._load

    def get_depot(self) -> str:
        """Return the <_depot> of this Truck"""
        return self._depot

    def get_parcels(self) -> List[Parcel]:
        """Return the <_parcels> of this Truck"""
        return self._parcels

    def get_routes(self) -> List[str]:
        """Return the <_routes> of this Truck"""
        return self._routes

    def total_volume(self) -> int:
        """Return the total _volume of _parcels in <self._parcels>"""
        v = 0
        for p in self._parcels:
            v += p.get_volume()
        return v

    def pack(self, p: Parcel) -> bool:
        """Pack <p> to <self._parcels>, update <self._routes> if possible.

        Precondition: No parcel with the same ID as <p> has already been
        added to this truck.

        - If <p> has the same ID as a parcel in <self._parcels> do not pack it.
        - If by packing <p> the total _volume of _parcels exceed the _capacity
        of this truck do not pack <p>.
        - If the last _destination of the _routes is the same as the
        _destination of <p>, pack the package but not update the _routes.

        Return True if packed successfully; return False otherwise.
        """
        # Piazza @1130: You may assume parcel IDs are unique (i.e. we won't try
        # to pack the same parcel onto your Truck twice in our tests).

        # for parcel in self._parcels:
        #     if p._id == parcel._id:
        #         return False

        if p.get_volume() + self.total_volume() > self._capacity:
            return False

        self._parcels.append(p)
        # self._load += p.get_volume()
        if self._routes[-1] != p.get_destination():
            # if the last location in _routes is not the same
            self._routes.append(p.get_destination())
        return True

    # def is_full(self) -> bool:
    #     """Return whether this truck is full"""
    #     return self._load == self._capacity

    def fullness(self) -> float:
        """Return the percentage fullness of the truck
        """
        load = 0
        for p in self._parcels:
            load += p.get_volume()
        return load / self._capacity * 100

    def is_empty(self) -> bool:
        """Return True if this truck is empty.
        Otherwise return False.
        """
        return len(self._parcels) == 0

    def route_distance(self, d_map: DistanceMap) -> int:
        """Return the total distance of the _routes of this truck.
        Including the distance between last location and the _depot.
        """

        d = 0
        loc = 0
        p_lst = self._routes
        while loc < len(p_lst) - 1:
            # distance between the last loc and curr loc
            d += d_map.distance(p_lst[loc], p_lst[loc + 1])
            loc += 1
        return d + d_map.distance(p_lst[-1], self._depot)


class Fleet:
    """ A fleet of trucks for making deliveries.

    ===== Public Attributes =====
    trucks:
      List of all Truck objects in this fleet.
    """
    trucks: List[Truck]

    def __init__(self) -> None:
        """Create a Fleet with no trucks.

        >>> f = Fleet()
        >>> f.num_trucks()
        0
        """
        self.trucks = []

    def add_truck(self, truck: Truck) -> None:
        """Add <truck> to this fleet.

        Precondition: No truck with the same ID as <truck> has already been
        added to this Fleet.

        >>> f = Fleet()
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> f.add_truck(t)
        >>> f.num_trucks()
        1
        """
        self.trucks.append(truck)

    # We will not test the format of the string that you return -- it is up
    # to you.
    def __str__(self) -> str:
        """Produce a string representation of this fleet
        """
        s = ''
        for truck in self.trucks:
            s += str(truck) + '\n'
        return s

    def num_trucks(self) -> int:
        """Return the number of trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> f.num_trucks()
        1
        """
        return len(self.trucks)

    def num_nonempty_trucks(self) -> int:
        """Return the number of non-empty trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> p2 = Parcel(2, 4, 'Toronto', 'Montreal')
        >>> t1.pack(p2)
        True
        >>> t1.fullness()
        90.0
        >>> t2 = Truck(5912, 20, 'Toronto')
        >>> f.add_truck(t2)
        >>> p3 = Parcel(3, 2, 'New York', 'Windsor')
        >>> t2.pack(p3)
        True
        >>> t2.fullness()
        10.0
        >>> t3 = Truck(1111, 50, 'Toronto')
        >>> f.add_truck(t3)
        >>> f.num_nonempty_trucks()
        2
        """
        n = 0
        for t in self.trucks:
            if not t.is_empty():
                n += 1
        return n

    def parcel_allocations(self) -> Dict[int, List[int]]:
        """Return a dictionary in which each key is the ID of a truck in this
        fleet and its value is a list of the IDs of the _parcels packed onto it,
        in the order in which they were packed.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(27, 5, 'Toronto', 'Hamilton')
        >>> p2 = Parcel(12, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t1.pack(p2)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p3 = Parcel(28, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p3)
        True
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.parcel_allocations() == {1423: [27, 12], 1333: [28]}
        True
        """
        dic = {}
        for t in self.trucks:
            lst = []
            for p in t.get_parcels():
                lst.append(p.get_id())
            dic[t.get_id()] = lst
        return dic

    def total_unused_space(self) -> int:
        """Return the total unused space, summed over all non-empty trucks in
        the fleet.
        If there are no non-empty trucks in the fleet, return 0.

        >>> f = Fleet()
        >>> f.total_unused_space()
        0
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.total_unused_space()
        995
        """
        space = 0
        for truck in self.trucks:
            if not truck.is_empty():
                space += truck.get_capacity() - truck.total_volume()
        return space

    def _total_fullness(self) -> float:
        """Return the sum of truck.fullness() for each non-empty truck in the
        fleet. If there are no non-empty trucks, return 0.

        >>> f = Fleet()
        >>> f._total_fullness() == 0.0
        True
        >>> t = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t)
        >>> f._total_fullness() == 0.0
        True
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f._total_fullness()
        50.0
        """
        per = 0.0
        for truck in self.trucks:
            if not truck.is_empty():
                per += truck.fullness()
        return per

    def average_fullness(self) -> float:
        """Return the average percent fullness of all non-empty trucks in the
        fleet.

        Precondition: At least one truck is non-empty.

        >>> f = Fleet()
        >>> t = Truck(1423, 10, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.average_fullness()
        50.0
        """
        return self._total_fullness() / self.num_nonempty_trucks()

    def total_distance_travelled(self, d_map: DistanceMap) -> int:
        """Return the total distance travelled by the trucks in this fleet,
        according to the distances in <d_map>.

        Precondition: <d_map> contains all distances required to compute the
                      average distance travelled.
        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.total_distance_travelled(m)
        36
        """
        d = 0
        for truck in self.trucks:
            if not truck.is_empty():
                d += truck.route_distance(d_map)
        return d

    def average_distance_travelled(self, d_map: DistanceMap) -> float:
        """Return the average distance travelled by the trucks in this fleet,
        according to the distances in <d_map>.

        Include in the average only trucks that have actually travelled some
        non-zero distance.

        Preconditions:
        - <d_map> contains all distances required to compute the average
          distance travelled.
        - At least one truck has travelled a non-zero distance.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.average_distance_travelled(m)
        18.0
        """
        # include only trucks traveled non_zero distance =>
        # have _parcels => non_empty
        return self.total_distance_travelled(d_map) / self.num_nonempty_trucks()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'distance_map'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest

    doctest.testmod()
