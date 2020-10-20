import numpy as np

import aktieskat.skat as skat

def test_aktiebeskatning():
    assert abs(skat.aktiebeskatning(50000, progressionsgrænse=55300) - 13500) < 10**-12
    assert abs(skat.aktiebeskatning(100000, progressionsgrænse=55300) - 33705) < 10**-12