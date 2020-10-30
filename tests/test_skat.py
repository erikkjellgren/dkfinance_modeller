import dkfinance_modeller.aktieskat.skat as skat


def test_aktiebeskatning():
    """Test aktiebeskatning"""
    assert abs(skat.aktiebeskatning(50000, progressionsgrænse=55300) - 13500) < 10 ** -12
    assert abs(skat.aktiebeskatning(100000, progressionsgrænse=55300) - 33705) < 10 ** -12


def test_aktiesparekontoskat():
    """Test beskatning af aktiesparekonto"""
    assert abs(skat.aktiesparekontobeskatning(50000) - 8500) < 10 ** -12


def test_pensionsbeskatning():
    """Test beskatning af pensionsopsparing"""
    assert abs(skat.pensionsbeskatning(50000) - 7650) < 10 ** -12


def test_nulskat():
    """Test beskatning med nul skat"""
    assert abs(skat.nulskat(50000) - 0) < 10 ** -12
