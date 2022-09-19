"""Assignment 1 - Scheduling algorithms (Task 4)

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

This module contains the abstract Scheduler class, as well as the two
subclasses RandomScheduler and GreedyScheduler, which implement the two
scheduling algorithms described in the handout.
"""
from typing import List, Dict, Union, Callable
from random import shuffle
from container import PriorityQueue
from domain import Parcel, Truck


class Scheduler:
    """A scheduler, capable of deciding what _parcels go onto which trucks, and
    what _routes each truck will take.

    This is an abstract class.  Only child classes should be instantiated.
    """

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the given <_parcels> onto the given <trucks>, that is,
        decide which _parcels will go on which trucks, as well as the _routes
        each truck will take.

        Mutate the Truck objects in <trucks> so that they store information
        about which parcel objects they will deliver and what _routes they will
        take.  Do *not* mutate the list <_parcels>, or any of the parcel objects
        in that list.

        Return a list containing the _parcels that did not get scheduled onto
        any truck, due to lack of _capacity.

        If <verbose> is True, print step-by-step details regarding
        the scheduling algorithm as it runs.  This is *only* for debugging
        purposes for your benefit, so the content and format of this
        information is your choice; we will not test your code with <verbose>
        set to True.
        """
        raise NotImplementedError


# TO DO: Implement classes RandomScheduler and GreedyScheduler.
class RandomScheduler(Scheduler):
    """The random scheduler algorithm will go through the parcels in random
    order.
    """

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """ For each parcel, it will schedule it onto a randomly chosen truck
        (from among those trucks that have capacity to add that parcel).
        """
        p = 0  # index
        p_copy = parcels[:]
        t_copy = trucks[:]
        shuffle(t_copy)
        shuffle(p_copy)
        len_ = len(p_copy)
        i = 0  # i th parcel is going to be removed
        while p < len_:  # loop run len_ times
            packed = False
            for t in t_copy:
                #  always pack the i th parcel, if not possible, remove i+1 th
                if not packed and t.pack(p_copy[i]):
                    p_copy.pop(i)
                    packed = True
                    # break
            if not packed:
                i += 1
            # print(i)
            p += 1
        return p_copy


class GreedyScheduler(Scheduler):
    """ A Greedy Scheduler tries to be more strategic. Like the random
        algorithm, it processes parcels one at a time, picking a truck for each,
        but it tries to pick the "best" truck it can for each parcel. Our greedy
        algorithm is quite short-sighted: it makes each choice without looking
        ahead to possible consequences of the choice (that’s why we call it
        "greedy").

        === Private Attributes ===
        _parcel_order: the sorted order of parcels
        _truck_order: the sorted order of trucks
        """
    _parcel_order: Callable[[Parcel, Parcel], bool]
    _truck_order: Callable[[Truck, Truck], bool]

    def __init__(self, config: Dict[str, Union[bool, str]]) -> None:
        """Initialize this GreedyScheduler

        Precondition:
        - parcel_priority must only have 'volume' or 'destination'
        - parcel_order must be either 'non-decreasing' or 'non-increasing'
        - truck_order must be either 'non-decreasing' or 'non-increasing'
        """
        parcel_priority = config['parcel_priority']
        parcel_order = config['parcel_order']
        truck_order = config['truck_order']
        if parcel_priority == 'volume':
            if parcel_order == 'non-increasing':
                self._parcel_order = _larger
            elif parcel_order == 'non-decreasing':
                self._parcel_order = _smaller
        elif parcel_priority == 'destination':
            if parcel_order == 'non-increasing':
                self._parcel_order = _alphabet_larger
            elif parcel_order == 'non-decreasing':
                self._parcel_order = _alphabet_smaller

        if truck_order == 'non-increasing':
            self._truck_order = _available_larger
        elif truck_order == 'non-decreasing':
            self._truck_order = _available_smaller

    def _find(self, parcel: Parcel,
              trucks: List[Truck]) -> Union[None, Truck]:
        """Find the best truck for <parcel>. Do not add any parcels to any
        trucks.
        Return None if no trucks have enough capacity;
        return the truck found if truck is eligible."""
        truck_pq = PriorityQueue(self._truck_order)
        for t in trucks:
            truck_pq.add(t)
        # for t in truck_pq._queue:
        #     print(t.get_id(), t.get_capacity() - t.total_volume())
        # print('\n')
        new_truck_pq = PriorityQueue(self._truck_order)
        while not truck_pq.is_empty():
            truck = truck_pq.remove()  # truck with higher prio return first
            volume_after = truck.total_volume() + parcel.get_volume()
            if volume_after <= truck.get_capacity():
                new_truck_pq.add(truck)

        # truck_pq is now empty
        # new_truck_pq contains all trucks eligible (have enough capacity)
        first_truck, new_truck = None, None
        # no add new_truck = None, then code below have problem
        while not new_truck_pq.is_empty():
            if first_truck is None:
                first_truck = new_truck_pq.remove()
                new_truck = first_truck
            else:
                new_truck = new_truck_pq.remove()

            if new_truck.get_routes()[-1] == parcel.get_destination():
                # return truck when found
                return new_truck

        # if new_truck_pq is empty ==> no truck with same dest
        # ==> return first truck eligible # TO DO: ????
        if new_truck_pq.is_empty():
            return first_truck  # first truck is None or a Truck object

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the given <_parcels> onto the given <trucks> with a greedy
         schedule algorithm, that is, decide which _parcels will go on which
         trucks, as well as the _routes each truck will take.

        Mutate the Truck objects in <trucks> so that they store information
        about which parcel objects they will deliver and what _routes they will
        take.  Do *not* mutate the list <_parcels>, or any of the parcel objects
        in that list.

        Return a list containing the _parcels that did not get scheduled onto
        any truck, due to lack of _capacity.

        If <verbose> is True, print step-by-step details regarding
        the scheduling algorithm as it runs.  This is *only* for debugging
        purposes for your benefit, so the content and format of this
        information is your choice; we will not test your code with <verbose>
        set to True.
        """
        parcel_pq = PriorityQueue(self._parcel_order)
        parcels_not_packed = []
        for p in parcels:
            parcel_pq.add(p)
        # Now parcels and trucks are sorted
        while not parcel_pq.is_empty():
            parcel = parcel_pq.remove()
            # the helper will create a new truck_pq every time
            truck_found = self._find(parcel, trucks)
            if truck_found is None:
                parcels_not_packed.append(parcel)
            else:
                truck_found.pack(parcel)

        return parcels_not_packed


def _smaller(p1: Parcel, p2: Parcel) -> bool:
    """Return true is <p1> has smaller volume than <p2>.
    """
    return p1.get_volume() < p2.get_volume()


def _larger(p1: Parcel, p2: Parcel) -> bool:
    """Return true is <p1> has larger volume than <p2>.
    """
    return p1.get_volume() > p2.get_volume()


def _alphabet_smaller(p1: Parcel, p2: Parcel) -> bool:
    """Return true is <p1> is alphabetically smaller than <p2>.
    """
    return p1.get_destination() < p2.get_destination()


def _alphabet_larger(p1: Parcel, p2: Parcel) -> bool:
    """Return true is <p1> is alphabetically larger than <p2>.
    """
    return p1.get_destination() > p2.get_destination()


# Maybe add a method in Truck ? # TO DO
def _available_smaller(t1: Truck, t2: Truck) -> bool:
    """Return true is <t1> has less available space than <t2>.
    """
    available1 = t1.get_capacity() - t1.total_volume()
    available2 = t2.get_capacity() - t2.total_volume()
    return available1 < available2


def _available_larger(t1: Truck, t2: Truck) -> bool:
    """Return true is <t1> has more available space than <t2>.
    """
    available1 = t1.get_capacity() - t1.total_volume()
    available2 = t2.get_capacity() - t2.total_volume()
    return available1 > available2


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['compare_algorithms'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'random', 'container', 'domain'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })

    # t_ = [
    #     Truck(0, 10, 'Toronto'),
    #     Truck(1, 1, 'Beijing'),
    #     Truck(2, 1, 'Shanghai')
    # ]
    #
    # p_ = [
    #     Parcel(10, 5, 'Toronto', 'PS5'),
    #     Parcel(11, 5, 'Toronto', 'XBOX'),
    #     Parcel(12, 2, 'Beijing', 'SWITCH'),
    #     Parcel(13, 1, 'Beijing', 'iPhone'),
    #     Parcel(14, 1, 'Shanghai', 'Vivo'),
    #     Parcel(15, 1, 'Shanghai', 'Xiaomi')
    # ]
    #
    # d = RandomScheduler()
    # result = d.schedule(p_, t_, verbose=True)
    # print(result)

    # ttt2 = Truck(2, 100, 'Toronto')
    # ttt3 = Truck(3, 50, 'Toronto')
    # ttt4 = Truck(4, 50, 'Toronto')
    # ttt1 = Truck(1, 100, 'Toronto')
    # tt = [ttt2, ttt3, ttt4, ttt1]
    #
    # pp = [
    #     Parcel(7, 38, 'Toronto', 's0'),
    #     Parcel(6, 29, 'Toronto', 's1'),
    #     Parcel(5, 25, 'Beijing', 's1'),
    #     Parcel(8, 40, 'Beijing', 's2'),
    # ]
    # g = GreedyScheduler({
    #     "depot_location": "Toronto",
    #     "parcel_file": "data/parcel-data-small.txt",
    #     "truck_file": "data/truck-data-small.txt",
    #     "map_file": "data/map-data.txt",
    #     "algorithm": "greedy",
    #     "parcel_priority": "destination",
    #     "parcel_order": "non-increasing",
    #     "truck_order": "non-increasing",
    # })
    # print(g.schedule(pp, tt))
