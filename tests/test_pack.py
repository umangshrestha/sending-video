import pytest

from lib_pack import *


@pytest.mark.parametrize("data", [
    1,
    100,
    "apple",
    [1, 2, 3]
])
def test_fail_cases_struct(data):
    packed_data = cv_pack(data)
    output  = cv_unpack(packed_data)
    assert  output.data ==  data





