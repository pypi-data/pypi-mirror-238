from in_azure import funcs


# Define test functions using pytest
def test_addition():
    assert funcs.add_numbers(2, 3) == 5
    assert funcs.add_numbers(-1, 1) == 0
    assert funcs.add_numbers(0, 0) == 0
