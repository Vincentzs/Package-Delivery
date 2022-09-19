from experiment import SchedulingExperiment
import pytest

config1 = {
    "depot_location": "Hangzhou",
    "parcel_file": "shit_parcels.txt",
    "truck_file": "shit_trucks.txt",
    "map_file": "shit_map.txt",
    "algorithm": "greedy",
    "parcel_priority": "volume",
    "parcel_order": "non-decreasing",
    "truck_order": "non-decreasing",
    "verbose": True
}

config2 = {
    "depot_location": "Hangzhou",
    "parcel_file": "shit_parcels.txt",
    "truck_file": "shit_trucks.txt",
    "map_file": "shit_map.txt",
    "algorithm": "greedy",
    "parcel_priority": "volume",
    "parcel_order": "non-increasing",
    "truck_order": "non-decreasing",
    "verbose": True
}

config3 = {
    "depot_location": "Hangzhou",
    "parcel_file": "shit_parcels.txt",
    "truck_file": "shit_trucks.txt",
    "map_file": "shit_map.txt",
    "algorithm": "greedy",
    "parcel_priority": "volume",
    "parcel_order": "non-decreasing",
    "truck_order": "non-increasing",
    "verbose": True
}

config4 = {
    "depot_location": "Hangzhou",
    "parcel_file": "shit_parcels.txt",
    "truck_file": "shit_trucks.txt",
    "map_file": "shit_map.txt",
    "algorithm": "greedy",
    "parcel_priority": "volume",
    "parcel_order": "non-increasing",
    "truck_order": "non-increasing",
    "verbose": True
}

config5 = {
    "depot_location": "Hangzhou",
    "parcel_file": "shit_parcels.txt",
    "truck_file": "shit_trucks.txt",
    "map_file": "shit_map.txt",
    "algorithm": "greedy",
    "parcel_priority": "destination",
    "parcel_order": "non-decreasing",
    "truck_order": "non-decreasing",
    "verbose": True
}

config6 = {
    "depot_location": "Hangzhou",
    "parcel_file": "shit_parcels.txt",
    "truck_file": "shit_trucks.txt",
    "map_file": "shit_map.txt",
    "algorithm": "greedy",
    "parcel_priority": "destination",
    "parcel_order": "non-increasing",
    "truck_order": "non-decreasing",
    "verbose": True
}

config7 = {
    "depot_location": "Hangzhou",
    "parcel_file": "shit_parcels.txt",
    "truck_file": "shit_trucks.txt",
    "map_file": "shit_map.txt",
    "algorithm": "greedy",
    "parcel_priority": "destination",
    "parcel_order": "non-decreasing",
    "truck_order": "non-increasing",
    "verbose": True
}

config8 = {
    "depot_location": "Hangzhou",
    "parcel_file": "shit_parcels.txt",
    "truck_file": "shit_trucks.txt",
    "map_file": "shit_map.txt",
    "algorithm": "greedy",
    "parcel_priority": "destination",
    "parcel_order": "non-increasing",
    "truck_order": "non-increasing",
    "verbose": True
}

configs = [config1, config2, config3, config4, config5, config6, config7, config8]

config_random = {
    "depot_location": "Hangzhou",
    "parcel_file": "shit_parcels.txt",
    "truck_file": "shit_trucks.txt",
    "map_file": "shit_map.txt",
    "algorithm": "random",
    "parcel_priority": "destination",
    "parcel_order": "non-increasing",
    "truck_order": "non-increasing",
    "verbose": True
}

def test_config1():
    exp = SchedulingExperiment(config1)
    assert exp.run(True) == {'avg_distance': pytest.approx(1568.888),
                             'avg_fullness': pytest.approx(91.79214969320313),
                             'fleet': 299,
                             'unscheduled': 0,
                             'unused_space': 2659,
                             'unused_trucks': 49}

def test_config2():
    exp = SchedulingExperiment(config2)
    assert exp.run(True) == {'avg_distance': pytest.approx(1575.3389830508474),
                             'avg_fullness': pytest.approx(99.33490092940006),
                             'fleet': 299,
                             'unscheduled': 0,
                             'unused_space': 183,
                             'unused_trucks': 63}

def test_config3():
    exp = SchedulingExperiment(config3)
    assert exp.run(True) == {'avg_distance': pytest.approx(487.3222222222222),
                             'avg_fullness': pytest.approx(91.14573312205387),
                             'fleet': 299,
                             'unscheduled': 0,
                             'unused_space': 2258,
                             'unused_trucks': 119}

def test_config4():
    exp = SchedulingExperiment(config4)
    assert exp.run(True) == {'avg_distance': pytest.approx(488.62048192771084),
                             'avg_fullness': pytest.approx(97.10630976555919),
                             'fleet': 299,
                             'unscheduled': 0,
                             'unused_space': 616,
                             'unused_trucks': 133}

def test_config5():
    exp = SchedulingExperiment(config5)
    assert exp.run(True) == {'avg_distance': pytest.approx(522.9789915966387),
                             'avg_fullness': pytest.approx(98.0538793823419),
                             'fleet': 299,
                             'unscheduled': 0,
                             'unused_space': 531,
                             'unused_trucks': 61}

def test_config6():
    exp = SchedulingExperiment(config6)
    assert exp.run(True) == {'avg_distance': pytest.approx(483.4978902953587),
                             'avg_fullness': pytest.approx(98.58169699871544),
                             'fleet': 299,
                             'unscheduled': 0,
                             'unused_space': 356,
                             'unused_trucks': 62}

def test_config7():
    exp = SchedulingExperiment(config7)
    assert exp.run(True) == {'avg_distance': pytest.approx(481.3757225433526),
                             'avg_fullness': pytest.approx(94.51969156468252),
                             'fleet': 299,
                             'unscheduled': 0,
                             'unused_space': 1446,
                             'unused_trucks': 126}

def test_config8():
    exp = SchedulingExperiment(config8)
    assert exp.run(True) == {'avg_distance': pytest.approx(501.6954022988506),
                             'avg_fullness': pytest.approx(94.18410528059779),
                             'fleet': 299,
                             'unscheduled': 0,
                             'unused_space': 1563,
                             'unused_trucks': 125}

if __name__ == '__main__':
    import pytest
    pytest.main(['experiment_playground.py'])

    # Uncomment the following to test random
    # exp = SchedulingExperiment(config_random)
    # print(exp.run(False))

    # Uncomment the following to see result from different config
    # for config in configs:
    #     exp = SchedulingExperiment(config)
    #     result = exp.run(False)
    #     import pprint
    #     pprint.pprint(result)




