from meta_requests.utils.iterative import *


def test_power_set():
    input_iterable = ('1', '2', '3')
    expected_iterable = ((), ('1',), ('2',), ('3',), ('1', '2'), ('1', '3'), ('2', '3'), ('1', '2', '3'))
    output_iterable = power_set(input_iterable)
    assert tuple(output_iterable) == expected_iterable


def test_power_set_from_headers():
    input_headers = {"accept": None, "accept-encoding": "json"}
    expected_output = [
        {},
        {"accept": None},
        {"accept-encoding": "json"},
        {"accept": None, "accept-encoding": "json"}
    ]
    output_iterable = power_set(input_headers.items())
    assert [dict(output) for output in output_iterable] == expected_output
