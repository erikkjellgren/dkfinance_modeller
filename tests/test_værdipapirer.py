import pytest

import dkfinance_modeller.aktieskat.værdipapirer as værdipapirer


def test_etf():
    """Test ETF klassen."""
    # Test at de simple funktioner virker
    etf = værdipapirer.ETF(kurs=10.0, åop=0.006)
    assert etf.kurs == 10.0
    assert etf.åop == 0.006
    assert etf.beskattet_kurs == 0.0
    assert etf.antal_værdipapirer == 0
    etf.updater_kurs(0.1)
    assert etf.kurs == 11.0
    # Test at ÅOP bliver modregnet korrekt.
    etf = værdipapirer.ETF(kurs=1.0, åop=0.006)
    etf.tilføj_enheder(1)
    for _ in range(0, 12):
        etf.modregn_åop()
    assert abs(etf.kurs - 0.994) < 10 ** -12
    # Test ved ulige antal måneder. // Tilføjet efter bug
    etf = værdipapirer.ETF(kurs=1.0, åop=0.006)
    etf.tilføj_enheder(1)
    for _ in range(0, 3):
        etf.modregn_åop()
    assert abs(etf.kurs - 0.998496613138553) < 10 ** -12
    # Test gennemsnitsmetoden virker via eksempler fra https://skat.dk/skat.aspx?oid=2244476, 25-10-2020
    etf = værdipapirer.ETF(kurs=300.0, åop=0.0)
    etf.tilføj_enheder(500)
    assert etf.total_værdi() == 150000
    etf.kurs = 200
    etf.tilføj_enheder(1000)
    etf.kurs = 150
    etf.tilføj_enheder(500)
    assert etf.beskattet_kurs == 212.5
    # Test lagerrealisering
    etf = værdipapirer.ETF(kurs=1.0, åop=0.0)
    etf.tilføj_enheder(1)
    etf.kurs = 2.0
    assert etf.lagerrealisering() == 1.0
    assert etf.beskattet_kurs == 2.0


def test_etf_exceptions():
    """Test exceptions i ETF klassen."""
    etf = værdipapirer.ETF(kurs=1.0, åop=0.0)
    with pytest.raises(Exception, match="Antal værdipapirer er negativ"):
        etf.antal_værdipapirer -= 1
