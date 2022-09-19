import unittest
from distance_map import DistanceMap
from domain import Parcel, Truck, Fleet
from container import PriorityQueue
from scheduler import RandomScheduler, GreedyScheduler
from experiment import SchedulingExperiment
import random
import signal


class TestUtil(unittest.TestCase):
    def assertPublicAttrs(self, object_, allowed_attrs):
        attrs = list(object_.__dict__.keys())
        public_attrs = list(filter(lambda x: not x.startswith('_'), attrs))
        self.assertCountEqual(allowed_attrs, public_attrs,
                              'You should not add new public attrs beside')

    def assertPublicMethods(self, class_, allowed_methods):
        methods = list(class_.__dict__.keys())
        public_methods = list(filter(lambda x: not x.startswith('_'), methods))
        self.assertCountEqual(allowed_methods, public_methods,
                              'You should not add any new public methods')


class TimeOutException(Exception):
    pass


class TestTimeOut:
    def __init__(self, seconds, error_message=None):
        if error_message is None:
            error_message = 'test timed out after {}s.'.format(seconds)
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeOutException(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, exc_type, exc_val, exc_tb):
        signal.alarm(0)


class TestDistanceMap(TestUtil):
    def setUp(self) -> None:
        self.m = DistanceMap()

    def tearDown(self) -> None:
        self.m = DistanceMap()

    def test_public_attrs(self):
        self.assertPublicAttrs(self.m, [])

    def test_public_methods(self):
        self.assertPublicMethods(DistanceMap, ['distance', 'add_distance'])

    def test_add_distance(self):
        self.assertIsNone(self.m.add_distance('a', 'b', 10),
                          "Add distance should return None for this")

    def test_add_distance_2(self):
        self.assertIsNone(self.m.add_distance('a', 'b', 10, 12),
                          "You should take care of optional parameter")

    def test_distance(self):
        self.assertEqual(-1, self.m.distance('a', 'b'),
                         'You should return -1 for an empty distance map')

    def test_distance_2(self):
        self.m.add_distance('a', 'b', 10)
        self.assertEqual(10, self.m.distance('a', 'b'),
                         "You should return the distance between two places")
        self.assertEqual(10, self.m.distance('b', 'a'),
                         "You should return the distance between two places")

    def test_distance_3(self):
        self.m.add_distance('a', 'b', 10, 12)
        self.assertEqual(10, self.m.distance('a', 'b'),
                         "You should return 10 for distance from a to b")
        self.assertEqual(12, self.m.distance('b', 'a'),
                         "You should return 12 for distance from b to a")


class TestTask2(TestUtil):
    def setUp(self) -> None:
        self.parcel = Parcel(1, 10, '', 'b')
        self.parcel_2 = Parcel(2, 10, 'a', 'b')
        self.parcel_3 = Parcel(3, 5, 'a', 'b')
        self.parcel_4 = Parcel(4, 3, 'a', 'b')
        self.truck = Truck(1, 15, 'Toronto')
        self.truck2 = Truck(2, 5, 'Toronto')
        self.f = Fleet()
        self.m = DistanceMap()
        self.m.add_distance('Toronto', 'Kingston', 100)
        self.m.add_distance('Kingston', 'London', 50)
        self.m.add_distance('London', 'Toronto', 25)
        self.m.add_distance('Toronto', 'Ajax', 50, 100)

    def tearDown(self) -> None:
        self.parcel = Parcel(1, 10, 'a', 'b')
        self.parcel_2 = Parcel(2, 10, 'a', 'b')
        self.truck = Truck(1, 15, 'Toronto')
        self.truck2 = Truck(2, 5, 'Ajax')
        self.f = Fleet()
        self.m = DistanceMap()
        self.m.add_distance('Toronto', 'Kingston', 100)
        self.m.add_distance('Toronto', 'Ajax', 50, 100)


class TestTruck(TestTask2):
    def test_pack(self):
        self.assertTrue(self.truck.pack(self.parcel),
                        "There is enough volume for truck to pack a parcel "
                        "thus you should return True")
        self.assertFalse(self.truck2.pack(self.parcel),
                         "There is no enough volume for truck to pack a "
                         "parcel thus you should return False")

    def test_pack_2(self):
        self.assertTrue(self.truck.pack(self.parcel))
        self.assertFalse(self.truck.pack(self.parcel_2),
                         "There is no enough space to pack another parcel"
                         "thus you should return False")
        self.assertTrue(self.truck.pack(self.parcel_3),
                        "The remaining space can pack the last parcel")

    def test_fullness(self):
        self.assertEqual(0, self.truck.fullness())
        self.truck.pack(self.parcel)
        self.assertAlmostEqual((2 / 3) * 100, self.truck.fullness())
        self.truck.pack(self.parcel_3)
        self.assertEqual(100, self.truck.fullness())


class TestFleet(TestTask2):
    def test_num_tracks(self):
        self.assertEqual(0, self.f.num_trucks())
        trucks = [self.truck, self.truck2]
        for i in range(len(trucks)):
            self.f.add_truck(trucks[i])
            self.assertEqual(i + 1, self.f.num_trucks())

    def test_num_nonempty_trucks(self):
        self.assertEqual(0, self.f.num_nonempty_trucks())
        trucks = [self.truck, self.truck2]
        for i in range(len(trucks)):
            self.f.add_truck(trucks[i])
            self.assertEqual(0, self.f.num_nonempty_trucks())

    def test_num_nonempty_trucks_2(self):
        parcels = [Parcel(100, 1, 'c', 'd'), Parcel(101, 2, 'e', 'f')]
        trucks = [self.truck, self.truck2, Truck(1000, 12, 'x')]
        for i in range(len(parcels)):
            trucks[i].pack(parcels[i])
            self.f.add_truck(trucks[i])
            self.assertEqual(i + 1, self.f.num_nonempty_trucks())
        self.f.add_truck(trucks[-1])
        self.assertEqual(2, self.f.num_nonempty_trucks())

    def test_parcel_allocations_empty(self):
        act = self.f.parcel_allocations()
        exp = {}
        self.assertDictEqual(exp, act,
                             "Since there is no trucks you should return empty "
                             "dictionary")
        self.f.add_truck(self.truck)
        act = self.f.parcel_allocations()
        self.assertDictEqual({1: []}, act,
                             "Since there is no parcel in the truck the truck "
                             "should only contains empty list")
        self.f.add_truck(self.truck2)
        act = self.f.parcel_allocations()
        self.assertDictEqual({1: [], 2: []}, act,
                             "Since there is no parcel in the truck the truck "
                             "should only contains empty list")

    def test_parcel_allocations_non_empty(self):
        self.f.add_truck(self.truck)
        self.truck.pack(self.parcel_3)
        self.assertDictEqual({1: [3]}, self.f.parcel_allocations(),
                             "You should return the parcels with correct order")
        self.f.add_truck(self.truck2)
        self.truck.pack(self.parcel_2)
        self.assertDictEqual({1: [3, 2], 2: []}, self.f.parcel_allocations(),
                             "You should return the parcels with correct order")

    def test_total_unused_space_full(self):
        self.assertEqual(0, self.f.total_unused_space(),
                         "Since there are no trucks you should return 0")
        self.f.add_truck(self.truck2)
        self.truck2.pack(self.parcel_3)
        self.assertEqual(0, self.f.total_unused_space(),
                         "Since the only truck is full you should return 0")

    def test_total_unused_space_2(self):
        self.f.add_truck(self.truck)
        self.assertEqual(0, self.f.total_unused_space(),
                         "Since the trucks is empty you should return 0")
        self.f.add_truck(self.truck2)
        self.assertEqual(0, self.f.total_unused_space(),
                         "Since both trucks are emtpy you still should return 0")
        self.truck.pack(self.parcel)
        self.assertEqual(5, self.f.total_unused_space(),
                         "One truck is filled thus you should should check the "
                         "unused space in the used truck")
        self.truck.pack(self.parcel_3)
        self.assertEqual(0, self.f.total_unused_space(),
                         "One truck is full thus you and other one is emtpy"
                         "thus that is 0")
        self.truck2.pack(self.parcel_4)
        self.assertEqual(2, self.f.total_unused_space(),
                         "The only non empty truck is filled with parcel of 3"
                         " there is only 2 left")

    def test_total_fullness(self):
        self.assertEqual(0, self.f._total_fullness(),
                         "No truck thus fullness is 0")
        self.f.add_truck(self.truck)
        self.assertEqual(0, self.f._total_fullness(),
                         "Empty truck thus fullness is 0")
        self.f.add_truck(self.truck2)
        self.assertEqual(0, self.f._total_fullness(),
                         "Empty trucks thus fullness is 0")

    def test_total_fullness_2(self):
        self.f.add_truck(self.truck)
        self.f.add_truck(self.truck2)
        self.truck.pack(self.parcel)
        self.assertAlmostEqual((2/3) * 100, self.f._total_fullness())
        self.truck2.pack(self.parcel_3)
        self.assertAlmostEqual((5/3) * 100, self.f._total_fullness())

    def test_average_fullness(self):
        self.f.add_truck(self.truck)
        self.f.add_truck(self.truck2)
        self.truck.pack(self.parcel)
        self.assertAlmostEqual((2 / 3) * 100, self.f.average_fullness())
        self.truck2.pack(self.parcel_3)
        self.assertAlmostEqual((5 / 6) * 100, self.f.average_fullness())

    def test_total_distance_travelled(self):
        """
        Toronto - Kingston 100
        Kingston - Toronto 100
        In total 20
        """
        self.f.add_truck(self.truck)
        parcel = Parcel(1, 10, 'Toronto', 'Kingston')
        self.truck.pack(parcel)
        self.assertEqual(200, self.f.total_distance_travelled(self.m))

    def test_total_distance_travelled_2(self):
        """
        Toronto - Kingston 100
        Kingston - London 50
        London - Toronto 25
        In total 175
        """
        self.f.add_truck(self.truck)
        self.f.add_truck(self.truck2)
        parcel = Parcel(1, 10, 'a', 'Kingston')
        parcel2 = Parcel(2, 5, 'x', 'London')
        self.truck.pack(parcel)
        self.truck.pack(parcel2)
        self.assertEqual(175, self.f.total_distance_travelled(self.m))

    def test_total_distance_travelled_3(self):
        """
        Truck 1:
        Toronto - Kingston 100
        Kingston - Toronto 100
        Truck 2:
        Toronto - Ajax 50
        Ajax - Toronto 100
        In total 350
        """
        self.f.add_truck(self.truck)
        self.f.add_truck(self.truck2)
        parcel = Parcel(1, 10, 'a', 'Kingston')
        parcel2 = Parcel(2, 5, 'x', 'Ajax')
        self.truck.pack(parcel)
        self.truck2.pack(parcel2)
        self.assertEqual(350, self.f.total_distance_travelled(self.m))

    def test_total_distance_travelled_4(self):
        self.f.add_truck(self.truck)
        self.f.add_truck(self.truck2)
        p1 = Parcel(1, 10, 'a', 'Ajax')
        p2 = Parcel(2, 3, 'a', 'Ajax')
        p3 = Parcel(3, 2, 'a', 'Ajax')
        self.truck.pack(p1)
        self.truck.pack(p2)
        self.truck.pack(p3)
        self.assertEqual(150, self.f.total_distance_travelled(self.m))

    def test_average_distance_travelled(self):
        self.f.add_truck(self.truck)
        self.f.add_truck(self.truck2)
        parcel = Parcel(1, 10, 'a', 'Kingston')
        parcel2 = Parcel(2, 5, 'x', 'London')
        self.truck.pack(parcel)
        self.truck.pack(parcel2)
        self.assertEqual(175, self.f.average_distance_travelled(self.m))

    def test_average_distance_travelled_2(self):
        self.f.add_truck(self.truck)
        self.f.add_truck(self.truck2)
        parcel = Parcel(1, 10, 'a', 'Kingston')
        parcel2 = Parcel(2, 5, 'x', 'Ajax')
        self.truck.pack(parcel)
        self.truck2.pack(parcel2)
        self.assertEqual(175, self.f.average_distance_travelled(self.m))


class TestPriorityQueue(TestUtil):
    def setUp(self) -> None:
        self.num_gt = lambda x, y: x > y
        self.list_len = lambda x, y: len(x) > len(y)
        self.error_msg = lambda x, y, z: "Input Sequence:{}, Expected Sequence: {} Output Sequence:{}".format(str(x), str(y), str(z))

        def remove_pq(pq):
            acc = []
            while not pq.is_empty():
                acc.append(pq.remove())
            return acc
        self.remove_pq = remove_pq

    def test_no_public_attrs(self):
        self.assertPublicAttrs(PriorityQueue(lambda x, y: True), [])

    def test_no_public_methods(self):
        self.assertPublicMethods(PriorityQueue, ['add', 'remove', 'is_empty'])

    def test_add_empty(self):
        pq = PriorityQueue(self.num_gt)
        pq.add(1)
        act = self.remove_pq(pq)
        self.assertEqual([1], act, self.error_msg([1], [1], act))

    def test_add_higher_priority(self):
        pq = PriorityQueue(self.num_gt)
        pq.add(1)
        pq.add(2)
        act = self.remove_pq(pq)
        self.assertEqual([2, 1], act, self.error_msg([1, 2], [2, 1], act))

    def test_add_with_middle(self):
        pq = PriorityQueue(self.num_gt)
        seq = [1, 3, 2]
        for i in seq:
            pq.add(i)
        act = self.remove_pq(pq)
        exp = sorted(seq, reverse=True)
        self.assertEqual(exp, act, self.error_msg(seq, exp, act))

    def test_add_with_middle_2(self):
        pq = PriorityQueue(self.num_gt)
        seq = [1, 4, 2, 0, 3, 5]
        for i in seq:
            pq.add(i)
        act = self.remove_pq(pq)
        exp = sorted(seq, reverse=True)
        self.assertEqual(exp, act, self.error_msg(seq, exp, act))

    def test_add_with_reverse_priority(self):
        pq = PriorityQueue(self.num_gt)
        seq = [i for i in range(10, 0, -1)]
        for i in seq:
            pq.add(i)
        act = self.remove_pq(pq)
        exp = sorted(seq, reverse=True)
        self.assertEqual(exp, act, self.error_msg(seq, exp, act))

    def test_add_tie(self):
        pq = PriorityQueue(self.list_len)
        seq = [[1], [2], [3]]
        for i in seq:
            pq.add(i)
        act = self.remove_pq(pq)
        exp = seq[::]
        self.assertEqual(exp, act, self.error_msg(seq, exp, act))

    def test_add_with_tie(self):
        pq = PriorityQueue(self.list_len)
        seq = [[1], [1, 2], [2], [2, 3]]
        for i in seq:
            pq.add(i)
        act = self.remove_pq(pq)
        exp = [[1, 2], [2, 3], [1], [2]]
        self.assertEqual(exp, act, self.error_msg(seq, exp, act))

    def test_add_random_order(self):
        for _ in range(100):
            pq = PriorityQueue(self.num_gt)
            seq = random.sample(range(1, 100), 10)
            random.shuffle(seq)
            for i in seq:
                pq.add(i)
            act = self.remove_pq(pq)
            exp = sorted(seq, reverse=True)
            self.assertEqual(exp, act, self.error_msg(seq, exp, act))


class TestRandomScheduler(TestUtil):
    def setUp(self) -> None:
        self.scheduler = RandomScheduler()

    def test_no_public_attrs(self):
        self.assertPublicAttrs(RandomScheduler(), [])

    def test_no_public_methods(self):
        self.assertPublicMethods(RandomScheduler, ['schedule'])

    def test_unavailable_truck(self):
        parcels = [Parcel(i, 10, 'a', 'b') for i in range(1, 10)]
        trucks = [Truck(1, 1, 'Toronto')]
        act = self.scheduler.schedule(parcels, trucks)
        self.assertCountEqual(parcels, act)
    
    def test_available_trucks(self):
        parcels = [Parcel(i, i, 'a', 'b') for i in range(1, 5)]
        trucks = [Truck(1, 10, 'Toronto'), Truck(2, 10, 'Toronto')]
        act = self.scheduler.schedule(parcels, trucks)
        self.assertEqual([], act)

    def test_unavailable_parcels(self):
        parcels = [Parcel(i, i, 'a', 'b') for i in range(1, 5)]
        trucks = [Truck(1, 6, 'Toronto')]
        act = self.scheduler.schedule(parcels, trucks)
        self.assertTrue(1 <= len(act) <= 2)


class TestGreedyScheduler(TestUtil):
    def setUp(self) -> None:
        self.config = {'algorithm': 'greedy',
                       'parcel_priority': 'volume',
                       'parcel_order': 'non-decreasing',
                       'truck_order': 'non-decreasing'}

    def tearDown(self) -> None:
        self.config = {'algorithm': 'greedy',
                       'parcel_priority': 'volume',
                       'parcel_order': 'non-decreasing',
                       'truck_order': 'non-decreasing'}

    def assertTruck(self, trucks, exp):
        for i in range(len(trucks)):
            truck = trucks[i]
            self.assertAlmostEqual(truck.fullness(), exp[i])

    def test_parcel_volume_non_dec_truck_non_dec_1(self):
        """
        Parcel
        1, 1, '', 1
        2, 2, '', 2
        3, 3, '', 3
        4, 4, '', 4
        Truck
        1, 1, ''
        2, 2, ''
        3, 3, ''
        4, 4, ''
        Arrange
        Parcel 1 -> Truck 1
        Parcel 2 -> Truck 2
        Parcel 3 -> Truck 3
        Parcel 4 -> Truck 4
        """
        parcels = [Parcel(i, i, '', str(i)) for i in range(1, 5)]
        trucks = [Truck(i, i, '') for i in range(1, 5)]
        scheduler = GreedyScheduler(self.config)
        act = scheduler.schedule(parcels, trucks)
        self.assertTrue(act == [])
        self.assertTruck(trucks, [100 for _ in range(4)])

    def test_parcel_volume_non_dec_truck_non_dec_2(self):
        """
        Be careful in this case every parcel goes to the same destination
        Parcel
        1, 1, '', b
        2, 2, '', b
        3, 3, '', b
        4, 4, '', b
        Truck
        1, 1, ''
        2, 2, ''
        3, 3, ''
        4, 4, ''
        Arrange
        Parcel 1 -> Truck 1
        Parcel 2 -> Truck 2
        Parcel 3 -> Truck 3
        Parcel 4 -> Truck 4
        """
        parcels = [Parcel(i, i, '', 'b') for i in range(1, 5)]
        trucks = [Truck(i, i, '') for i in range(1, 5)]
        scheduler = GreedyScheduler(self.config)
        act = scheduler.schedule(parcels, trucks)
        self.assertTrue(act == [])
        self.assertTruck(trucks, [100 for _ in range(4)])

    def test_parcel_volume_non_dec_truck_non_inc_1(self):
        """
        Parcel
        1, 1, '', 1
        2, 2, '', 2
        3, 3, '', 3
        4, 4, '', 4
        Truck
        1, 1, ''
        2, 2, ''
        3, 3, ''
        4, 4, ''
        """
        parcels = [Parcel(i, i, '', str(i)) for i in range(1, 5)]
        trucks = [Truck(i, i, 'a') for i in range(1, 5)]
        self.config.update({'truck_order': 'non-increasing'})
        scheduler = GreedyScheduler(self.config)
        act = scheduler.schedule(parcels, trucks)
        self.assertTrue(len(act) == 1)
        self.assertTrue(act == [parcels[-1]])
        self.assertTruck(trucks, [0, 0, (2 / 3) * 100, 100])

    def test_parcel_volume_non_dec_truck_non_inc_2(self):
        """
        Be careful this case every parcel goes to the same destination
        Parcel
        1, 1, '', b
        2, 2, '', b
        3, 3, '', b
        4, 4, '', b
        Truck
        1, 1, ''
        2, 2, ''
        3, 3, ''
        4, 4, ''
        Arrange
        Parcel 1 -> Truck 4
        Parcel 2 -> Truck 4
        Parcel 3 -> Truck 3
        Parcel 4 -> No available truck
        """
        parcels = [Parcel(i, i, '', 'b') for i in range(1, 5)]
        trucks = [Truck(i, i, 'a') for i in range(1, 5)]
        self.config.update({'truck_order': 'non-increasing'})
        scheduler = GreedyScheduler(self.config)
        act = scheduler.schedule(parcels, trucks)
        self.assertTrue(len(act) == 1)
        self.assertTrue(act == [parcels[-1]])
        self.assertTruck(trucks, [0, 0, 100, 75])

    def test_parcel_volume_non_inc_truck_non_dec_1(self):
        """
        Parcel
        1, 1, '', 1
        2, 2, '', 2
        3, 3, '', 3
        4, 4, '', 4
        Truck
        1, 1, ''
        2, 2, ''
        3, 3, ''
        4, 4, ''
        Arrange
        Parcel 1 -> Truck 1
        Parcel 2 -> Truck 2
        Parcel 3 -> Truck 3
        Parcel 4 -> Truck 4
        """
        parcels = [Parcel(i, i, '', str(i)) for i in range(1, 5)]
        trucks = [Truck(i, i, '') for i in range(1, 5)]
        self.config.update({'parcel_order': 'non-increasing'})
        scheduler = GreedyScheduler(self.config)
        act = scheduler.schedule(parcels, trucks)
        self.assertTrue(len(act) == 0)
        self.assertTruck(trucks, [100] * 4)

    def test_parcel_volume_non_inc_truck_non_dec_2(self):
        """
        Be careful in this case every parcel goes to the same destination
        Parcel
        1, 1, '', b
        2, 2, '', b
        3, 3, '', b
        4, 4, '', b
        Truck
        1, 1, ''
        2, 2, ''
        3, 3, ''
        4, 4, ''
        Arrange
        Parcel 1 -> Truck 1
        Parcel 2 -> Truck 2
        Parcel 3 -> Truck 3
        Parcel 4 -> Truck 4
        """
        parcels = [Parcel(i, i, '', 'b') for i in range(1, 5)]
        trucks = [Truck(i, i, '') for i in range(1, 5)]
        self.config.update({'parcel_order': 'non-increasing'})
        scheduler = GreedyScheduler(self.config)
        act = scheduler.schedule(parcels, trucks)
        self.assertTrue(len(act) == 0)
        self.assertTruck(trucks, [100] * 4)

    def test_parcel_volume_non_inc_truck_non_inc_1(self):
        """
        Parcel
        1, 1, '', 1
        2, 2, '', 2
        3, 3, '', 3
        4, 4, '', 4
        Truck
        1, 1, ''
        2, 2, ''
        3, 3, ''
        4, 4, ''
        Arrange
        Parcel 1 -> Truck 1
        Parcel 2 -> Truck 2
        Parcel 3 -> Truck 3
        Parcel 4 -> Truck 4
        """
        parcels = [Parcel(i, i, '', str(i)) for i in range(1, 5)]
        trucks = [Truck(i, i, '') for i in range(1, 5)]
        self.config.update({'parcel_order': 'non-increasing'})
        self.config.update({'truck_order': 'non-decreasing'})
        scheduler = GreedyScheduler(self.config)
        act = scheduler.schedule(parcels, trucks)
        self.assertTrue(len(act) == 0)
        self.assertTruck(trucks, [100] * 4)

    def test_parcel_volume_non_inc_truck_non_inc_2(self):
        """
        Be careful in this case every parcel goes to the same destination
        Parcel
        1, 1, '', b
        2, 2, '', b
        3, 3, '', b
        4, 4, '', b
        Truck
        1, 1, ''
        2, 2, ''
        3, 3, ''
        4, 4, ''
        Arrange
        Parcel 1 -> Truck 1
        Parcel 2 -> Truck 2
        Parcel 3 -> Truck 3
        Parcel 4 -> Truck 4
        """
        parcels = [Parcel(i, i, '', 'b') for i in range(1, 5)]
        trucks = [Truck(i, i, '') for i in range(1, 5)]
        self.config.update({'parcel_order': 'non-increasing'})
        self.config.update({'truck_order': 'non-decreasing'})
        scheduler = GreedyScheduler(self.config)
        act = scheduler.schedule(parcels, trucks)
        self.assertTrue(len(act) == 0)
        self.assertTruck(trucks, [100] * 4)

    def test_parcel_dest_non_dec_truck_non_dec_1(self):
        """
        Parcel
        1, 1, '', 4
        2, 2, '', 3
        3, 3, '', 2
        4, 4, '', 1
        Truck
        1, 1, ''
        2, 2, ''
        3, 3, ''
        4, 4, ''
        Arrange
        Parcel 1 -> Truck 1
        Parcel 2 -> Truck 2
        Parcel 3 -> Truck 3
        Parcel 4 -> Truck 4
        """
        parcels = [Parcel(i, i, '', str(5 - i)) for i in range(1, 5)]
        trucks = [Truck(i, i, '') for i in range(1, 5)]
        self.config.update({'parcel_priority': 'destination'})
        scheduler = GreedyScheduler(self.config)
        act = scheduler.schedule(parcels, trucks)
        self.assertTrue(act == [])
        self.assertTruck(trucks, [100] * 4)

    def test_parcel_dest_non_dec_truck_non_dec_2(self):
        """
        Be careful in this case every parcel goes to the same destination
        Parcel
        1, 1, '', b
        2, 2, '', b
        3, 3, '', b
        4, 4, '', b
        Truck
        1, 1, ''
        2, 2, ''
        3, 3, ''
        4, 4, ''
        Arrange
        Parcel 1 -> Truck 1
        Parcel 2 -> Truck 2
        Parcel 3 -> Truck 3
        Parcel 4 -> Truck 4
        """
        parcels = [Parcel(i, i, '', 'b') for i in range(1, 5)]
        trucks = [Truck(i, i, '') for i in range(1, 5)]
        self.config.update({'parcel_priority': 'destination'})
        scheduler = GreedyScheduler(self.config)
        act = scheduler.schedule(parcels, trucks)
        self.assertTrue(act == [])
        self.assertTruck(trucks, [100] * 4)

    def test_parcel_dest_non_dec_truck_non_inc_1(self):
        """
        Parcel
        1, 1, '', 4
        2, 2, '', 3
        3, 3, '', 2
        4, 4, '', 1
        Truck
        1, 1, ''
        2, 2, ''
        3, 3, ''
        4, 4, ''
        Arrange
        Parcel 1 -> Truck 1
        Parcel 2 -> Truck 2
        Parcel 3 -> Truck 3
        Parcel 4 -> Truck 4
        """
        parcels = [Parcel(i, i, '', str(5 - i)) for i in range(1, 5)]
        trucks = [Truck(i, i, '') for i in range(1, 5)]
        self.config.update({'parcel_priority': 'destination',
                            'truck_order': 'non-increasing'})
        scheduler = GreedyScheduler(self.config)
        act = scheduler.schedule(parcels, trucks)
        self.assertTrue(len(act) == 0)
        self.assertTruck(trucks, [100] * 4)

    def test_parcel_dest_non_dec_truck_non_inc_2(self):
        """
        Be careful in this case every parcel goes to the same destination
        Parcel
        1, 1, '', b
        2, 2, '', b
        3, 3, '', b
        4, 4, '', b
        Truck
        1, 1, ''
        2, 2, ''
        3, 3, ''
        4, 4, ''
        Arrange
        Parcel 1 -> Truck 4
        Parcel 2 -> Truck 4
        Parcel 3 -> Truck 3
        Parcel 4 -> No available truck
        """
        parcels = [Parcel(i, i, '', 'b') for i in range(1, 5)]
        trucks = [Truck(i, i, '') for i in range(1, 5)]
        self.config.update({'parcel_priority': 'destination',
                            'truck_order': 'non-increasing'})
        scheduler = GreedyScheduler(self.config)
        act = scheduler.schedule(parcels, trucks)
        self.assertTrue(len(act) == 1)
        self.assertTrue(act == [parcels[-1]])
        self.assertTruck(trucks, [0, 0, 100, 75])

    def test_parcel_dest_non_inc_truck_non_dec_1(self):
        """
        Parcel
        1, 1, '', 4
        2, 2, '', 3
        3, 3, '', 2
        4, 4, '', 1
        Truck
        1, 1, ''
        2, 2, ''
        3, 3, ''
        4, 4, ''
        Arrange
        Parcel 1 -> Truck 1
        Parcel 2 -> Truck 2
        Parcel 3 -> Truck 3
        Parcel 4 -> Truck 4
        """
        parcels = [Parcel(i, i, '', str(5 - i)) for i in range(1, 5)]
        trucks = [Truck(i, i, '') for i in range(1, 5)]
        self.config.update({'parcel_priority': 'destination',
                            'parcel_order': 'non-increasing',
                            'truck_order': 'non-decreasing'})
        scheduler = GreedyScheduler(self.config)
        act = scheduler.schedule(parcels, trucks)
        self.assertTrue(len(act) == 0)
        self.assertTruck(trucks, [100] * 4)

    def test_parcel_dest_non_inc_truck_non_dec_2(self):
        """
        Be careful in this case every parcel goes to the same destination
        Parcel
        1, 1, '', b
        2, 2, '', b
        3, 3, '', b
        4, 4, '', b
        Truck
        1, 1, ''
        2, 2, ''
        3, 3, ''
        4, 4, ''
        Arrange
        Parcel 1 -> Truck 1
        Parcel 2 -> Truck 2
        Parcel 3 -> Truck 3
        Parcel 4 -> Truck 4
        """
        parcels = [Parcel(i, i, '', 'b') for i in range(1, 5)]
        trucks = [Truck(i, i, '') for i in range(1, 5)]
        self.config.update({'parcel_priority': 'destination',
                            'parcel_order': 'non-increasing',
                            'truck_order': 'non-decreasing'})
        scheduler = GreedyScheduler(self.config)
        act = scheduler.schedule(parcels, trucks)
        self.assertTrue(len(act) == 0)
        self.assertTruck(trucks, [100] * 4)

    def test_parcel_desc_non_inc_truck_non_inc_1(self):
        """
        Parcel
        1, 1, '', 4
        2, 2, '', 3
        3, 3, '', 2
        4, 4, '', 1
        Truck
        1, 1, ''
        2, 2, ''
        3, 3, ''
        4, 4, ''
        Arrange
        Parcel 1 -> Truck 4
        Parcel 2 -> Truck 2
        Parcel 3 -> Truck 3
        Parcel 4 -> Truck 4
        """
        parcels = [Parcel(i, i, '', str(5 - i)) for i in range(1, 5)]
        trucks = [Truck(i, i, '') for i in range(1, 5)]
        self.config.update({'parcel_priority': 'destination',
                            'parcel_order': 'non-increasing',
                            'truck_order': 'non-increasing'})
        scheduler = GreedyScheduler(self.config)
        act = scheduler.schedule(parcels, trucks)
        self.assertTrue(len(act) == 1)
        self.assertEqual(parcels[-1], act[0])
        self.assertTruck(trucks, [0, 0, (2/3) * 100, 100])

    def test_parcel_desc_non_inc_truck_non_inc_2(self):
        """
        Be careful in this case every parcel goes to the same destination
        Parcel
        1, 1, '', b
        2, 2, '', b
        3, 3, '', b
        4, 4, '', b
        Truck
        1, 1, ''
        2, 2, ''
        3, 3, ''
        4, 4, ''
        Arrange
        Parcel 1 -> Truck 4
        Parcel 2 -> Truck 4
        Parcel 3 -> Truck 3
        Parcel 4 -> No available truck
        """
        parcels = [Parcel(i, i, '', 'b') for i in range(1, 5)]
        trucks = [Truck(i, i, '') for i in range(1, 5)]
        self.config.update({'parcel_priority': 'destination',
                            'parcel_order': 'non-increasing',
                            'truck_order': 'non-increasing'})
        scheduler = GreedyScheduler(self.config)
        act = scheduler.schedule(parcels, trucks)
        self.assertTrue(len(act) == 1)
        self.assertTrue(act[0] == parcels[-1])
        self.assertTruck(trucks, [0, 0, 100, 75])

    def test_schedule_tie(self):
        """
        Parcel
        1 3 '' a
        2 2 '' b
        Truck
        1, 2 ''
        2, 5 ''
        Parcel 1 -> Truck 2
        Parcel 2 -> Truck 1
        """
        parcels = [Parcel(1, 3, '', 'a'), Parcel(2, 2, '', 'b')]
        trucks = [Truck(1, 2, ''), Truck(2, 5, '')]
        self.config.update({'parcel_priority': 'destination',
                            'parcel_order': 'non-increasing',
                            'truck_order': 'non-decreasing'})
        scheduler = GreedyScheduler(self.config)
        act = scheduler.schedule(parcels, trucks)
        self.assertTrue(act == [])
        self.assertTruck(trucks, [100, 60])

    def test_non_minimal_solution(self):
        """
        Parcel
        1 1 '' 'a'
        2 2 '' 'b'
        3 3 '' 'c'
        4 4 '' 'd'
        Truck
        1 2 ''
        2 3 ''
        3 4 ''
        4 5 ''
        """
        parcels = [Parcel(1, 1, '', 'a'), Parcel(2, 2, '', 'b'),
                   Parcel(3, 3, '', 'c'), Parcel(4, 4, '', 'd')]
        trucks = [Truck(1, 2, ''), Truck(2, 3, ''),
                  Truck(3, 4, ''), Truck(4, 5, '')]
        self.config.update({'parcel_priority': 'volume',
                            'parcel_order': 'non-decreasing',
                            'truck_order': 'non-decreasing'})
        scheduler = GreedyScheduler(self.config)
        act = scheduler.schedule(parcels, trucks)
        self.assertTrue(len(act) == 0)
        self.assertTruck(trucks, [50, (2 / 3) * 100, 75, 80])

    def test_non_minimal_solution_2(self):
        """
        Parcel
        1 1 '' 'a'
        2 2 '' 'b'
        3 3 '' 'c'
        4 4 '' 'd'
        Truck
        1 2 ''
        2 3 ''
        3 4 ''
        4 6 ''
        Arrange
        Parcel 1 -> Truck 4
        Parcel 2 -> Truck 4
        Parcel 3 -> Truck 3
        Parcel 4 -> No Truck
        """
        parcels = [Parcel(1, 1, '', 'a'), Parcel(2, 2, '', 'b'),
                   Parcel(3, 3, '', 'c'), Parcel(4, 4, '', 'd')]
        trucks = [Truck(1, 2, ''), Truck(2, 3, ''),
                  Truck(3, 4, ''), Truck(4, 6, '')]
        self.config.update({'parcel_priority': 'volume',
                            'parcel_order': 'non-decreasing',
                            'truck_order': 'non-increasing'})
        scheduler = GreedyScheduler(self.config)
        act = scheduler.schedule(parcels, trucks)
        self.assertTrue(len(act) == 1)
        self.assertEqual(act[0], parcels[-1])
        self.assertTruck(trucks, [0, 0, 75, 50])

    def test_pick_destination_order(self):
        """
        Parcel
        1 4 '' 'b'
        2 2 '' 'b'
        3 2 '' 'c'
        4 1 '' 'c'
        Truck
        3 7 ''
        1 3 ''
        2 3 ''
        Arrange
        Parcel 1 -> Truck 3
        Parcel 2 -> Truck 3 because of same destination
        Parcel 3 -> Truck 1
        Parcel 4 -> Truck 1
        """
        parcels = [Parcel(1, 4, '', 'b'), Parcel(2, 2, '', 'b'),
                   Parcel(3, 2, '', 'c'), Parcel(4, 1, '', 'c')]
        trucks = [Truck(1, 3, ''), Truck(2, 3, ''), Truck(3, 7, '')]
        self.config.update({'parcel_priority': 'destination',
                            'parcel_order': 'non-decreasing',
                            'truck_order': 'non-increasing'})
        scheduler = GreedyScheduler(self.config)
        act = scheduler.schedule(parcels, trucks)
        self.assertTrue(len(act) == 0)
        self.assertTruck(trucks, [100, 0, (6 / 7) * 100])


class TestExperiment(TestUtil):
    def setUp(self) -> None:

        def assertStat(exp, act):
            for k in exp:
                self.assertAlmostEqual(exp[k], act[k])
        self.config = {
         'depot_location': 'Toronto',
         'parcel_file': './test_data/parcel-1.txt',
         'truck_file': './test_data/truck-1.txt',
         'map_file': './test_data/distance.txt',
         'algorithm': 'greedy',
         'parcel_priority': 'volume',
         'parcel_order': 'non-decreasing',
         'truck_order': 'non-decreasing',
         'verbose': 'false'
     }
        self.assertStat = assertStat

    def test_experiment_1(self):
        experiment = SchedulingExperiment(self.config)
        act = experiment.run()
        exp = {'fleet': 4,
               'unused_trucks': 0,
               'unused_space': 0,
               'avg_distance': 437.5,
               'avg_fullness': 100,
               'unscheduled': 0}
        self.assertStat(exp, act)

    def test_experiment_2(self):
        self.config.update({'truck_order': 'non-increasing'})
        experiment = SchedulingExperiment(self.config)
        act = experiment.run()
        exp = {'fleet': 4,
               'unused_trucks': 2,
               'unused_space': 1,
               'avg_distance': 675,
               'avg_fullness': (5 / 6) * 100,
               'unscheduled': 1}
        self.assertStat(exp, act)

    def test_experiment_3(self):
        self.config.update({'parcel_file': './test_data/parcel-2.txt',
                            'truck_file': './test_data/truck-2.txt',
                            'parcel_priority': 'destination',
                            'parcel_order': 'non-decreasing',
                            'truck_order': 'non-increasing'})
        experiment = SchedulingExperiment(self.config)
        act = experiment.run()
        exp = {'fleet': 3,
               'unused_trucks': 1,
               'unused_space': 1,
               'avg_distance': 275,
               'avg_fullness': (13 / 14) * 100,
               'unscheduled': 0
               }
        self.assertStat(exp, act)

    def test_experiment_4(self):
        self.config.update({'parcel_file': './test_data/parcel-1.txt',
                            'truck_file': './test_data/truck-3.txt',
                            'parcel_priority': 'volume',
                            'parcel_order': 'non-decreasing',
                            'truck_order': 'non-increasing'})
        experiment = SchedulingExperiment(self.config)
        act = experiment.run()
        exp = {'fleet': 4,
               'unused_trucks': 2,
               'unused_space': 4,
               'avg_distance': 650,
               'avg_fullness': (5/8) * 100,
               'unscheduled': 1
               }
        self.assertStat(exp, act)

    def test_experiment_5(self):
        self.config.update({'parcel_file': './test_data/parcel-1.txt',
                            'truck_file': './test_data/truck-4.txt',
                            'parcel_priority': 'volume',
                            'parcel_order': 'non-decreasing',
                            'truck_order': 'non-decreasing'})
        experiment = SchedulingExperiment(self.config)
        act = experiment.run()
        exp = {'fleet': 4,
               'unused_trucks': 0,
               'unused_space': 4,
               'avg_distance': 437.5,
               'avg_fullness': (163 / 240) * 100,
               'unscheduled': 0
               }
        self.assertStat(exp, act)


if __name__ == '__main__':
    unittest.main(verbosity=2)
