import dkfinance_modeller.aktieskat.valuta as valuta


def test_nulvalutakurtage():
    """Test kurtage med nul kurtage"""
    assert abs(valuta.nulvalutakurtage(50000) - 0) < 10 ** -12


def test_saxo_valutakurtage():
    """Test kurtage med Saxo underkonto"""
    assert abs(valuta.saxo_underkonto_kurtage(50000) - 75) < 10 ** -12


def test_nordnet_valutakurtage():
    """Test kurtage med Nordnet valutakonto"""
    assert abs(valuta.nordnet_valutakonto_kurtage(50000) - 37.5) < 10 ** -12
