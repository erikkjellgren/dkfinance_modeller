import dkfinance_modeller.aktieskat.kurtage as kurtage


def test_nulkurtage():
    """Test kurtage med nul kurtage."""
    assert abs(kurtage.nulkurtage(50000) - 0) < 10 ** -12


def test_saxo_kurtage():
    """Test kurtage for Saxo bank."""
    kurtagefunktion = kurtage.saxo_kurtage_bygger(valuta="Dkk")
    assert kurtagefunktion(100) == 14
    assert abs(kurtagefunktion(50000) - 50) < 10 ** -12
    kurtagefunktion = kurtage.saxo_kurtage_bygger(valuta="usd", valutakurs=6.29)
    assert abs(kurtagefunktion(100) - 19.37) < 10 ** -12
    assert abs(kurtagefunktion(50000) - 300) < 10 ** -12
    assert abs(kurtagefunktion(50000, kurs=5) - 1508) < 10 ** -12
    kurtagefunktion = kurtage.saxo_kurtage_bygger(valuta="usd", valutakurs=6.29, underkonto=True)
    assert abs(kurtagefunktion(100) - 18.87) < 10 ** -12
    assert abs(kurtagefunktion(50000) - 50) < 10 ** -12
    assert abs(kurtagefunktion(50000, kurs=5) - 1258) < 10 ** -12
    kurtagefunktion = kurtage.saxo_kurtage_bygger(valuta="euro", valutakurs=7.44)
    assert abs(kurtagefunktion(100) - 15.38) < 10 ** -12
    assert abs(kurtagefunktion(50000) - 300) < 10 ** -12
    kurtagefunktion = kurtage.saxo_kurtage_bygger(valuta="euro", valutakurs=7.44, underkonto=True)
    assert abs(kurtagefunktion(100) - 14.88) < 10 ** -12
    assert abs(kurtagefunktion(50000) - 50) < 10 ** -12


def test_nordnet_kurtage():
    """Test kurtage for Nordnet."""
    kurtagefunktion = kurtage.nordnet_kurtage_bygger(valuta="Dkk")
    assert kurtagefunktion(100) == 29
    assert abs(kurtagefunktion(50000) - 50) < 10 ** -12
    kurtagefunktion = kurtage.nordnet_kurtage_bygger(valuta="usd", valutakurs=6.29)
    assert abs(kurtagefunktion(100) - 82.02) < 10 ** -12
    assert abs(kurtagefunktion(75000) - 300) < 10 ** -12
    kurtagefunktion = kurtage.nordnet_kurtage_bygger(valuta="usd", valutakurs=6.29, valutakonto=True)
    assert abs(kurtagefunktion(100) - 81.77) < 10 ** -12
    assert abs(kurtagefunktion(75000) - 112.5) < 10 ** -12
    kurtagefunktion = kurtage.nordnet_kurtage_bygger(valuta="euro", valutakurs=7.44)
    assert abs(kurtagefunktion(100) - 89.53) < 10 ** -12
    assert abs(kurtagefunktion(75000) - 300) < 10 ** -12
    kurtagefunktion = kurtage.nordnet_kurtage_bygger(valuta="euro", valutakurs=7.44, valutakonto=True)
    assert abs(kurtagefunktion(100) - 89.28) < 10 ** -12
    assert abs(kurtagefunktion(75000) - 112.5) < 10 ** -12


def test_lunarinvest_kurtage():
    """Test kurtage for Lunar invest."""
    kurtagefunktion = kurtage.lunar_kurtage_bygger(valuta="Dkk")
    assert kurtagefunktion(40000) == 19
    assert abs(kurtagefunktion(50001) - 69.001) < 10 ** -12
    kurtagefunktion = kurtage.lunar_kurtage_bygger(valuta="usd")
    assert abs(kurtagefunktion(40000) - 219) < 10 ** -12
    assert abs(kurtagefunktion(50001) - 319.006) < 10 ** -12
