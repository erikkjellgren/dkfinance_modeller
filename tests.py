import aktieskat.kurtage as kurtage
import aktieskat.skat as skat
import aktieskat.skattemodel as skattemodel


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


def test_nulkurtage():
    """Test kurtage med nul kurtage"""
    assert abs(kurtage.nulkurtage(50000) - 0) < 10 ** -12


def test_køb_værdipapirer():
    """Test køb af værdipapirer"""
    kapitalændring, kurtageudgift, værdipapirer = skattemodel.køb_værdipapirer(1000, 100, kurtage.nulkurtage)
    assert abs(kapitalændring + 1000) < 10 ** -12
    assert kurtageudgift == 0
    assert værdipapirer == [100] * 10

    def kurtage2(kapital, kurs=0.0):  # pylint: disable=W0613
        return 0.001 * kapital

    kapitalændring, kurtageudgift, værdipapirer = skattemodel.køb_værdipapirer(1000, 100, kurtage2)
    assert abs(kapitalændring + 900.9) < 10 ** -12
    assert kurtageudgift == 0.9
    assert værdipapirer == [100] * 9

    def kurtage3(kapital, kurs=0.0):  # pylint: disable=W0613
        return 0.0 * kapital + 101

    kapitalændring, kurtageudgift, værdipapirer = skattemodel.køb_værdipapirer(1000, 100, kurtage3)
    assert abs(kapitalændring + 901) < 10 ** -12
    assert kurtageudgift == 101
    assert værdipapirer == [100] * 8


def test_saxo_kurtage():
    """Test kurtage for Saxo bank"""
    kurtagefunktion = kurtage.saxo_kurtage_bygger(valuta="Dkk")
    assert kurtagefunktion(100) == 14
    assert abs(kurtagefunktion(50000) - 50) < 10 ** -12
    kurtagefunktion = kurtage.saxo_kurtage_bygger(valuta="usd", valutakurs=6.29)
    assert abs(kurtagefunktion(100) - 19.37) < 10 ** -12
    assert abs(kurtagefunktion(50000) - 300) < 10 ** -12
    assert abs(kurtagefunktion(50000, kurs=5) - 1508) < 10 ** -12
    kurtagefunktion = kurtage.saxo_kurtage_bygger(valuta="usd", valutakurs=6.29, underkonto=True)
    assert abs(kurtagefunktion(100) - 19.02) < 10 ** -12
    assert abs(kurtagefunktion(50000) - 125) < 10 ** -12
    assert abs(kurtagefunktion(50000, kurs=5) - 1333) < 10 ** -12
    kurtagefunktion = kurtage.saxo_kurtage_bygger(valuta="euro", valutakurs=7.44)
    assert abs(kurtagefunktion(100) - 15.38) < 10 ** -12
    assert abs(kurtagefunktion(50000) - 300) < 10 ** -12
    kurtagefunktion = kurtage.saxo_kurtage_bygger(valuta="euro", valutakurs=7.44, underkonto=True)
    assert abs(kurtagefunktion(100) - 15.03) < 10 ** -12
    assert abs(kurtagefunktion(50000) - 125) < 10 ** -12


def test_nordnet_kurtage():
    """Test kurtage for Saxo bank"""
    kurtagefunktion = kurtage.nordnet_kurtage_bygger(valuta="Dkk")
    assert kurtagefunktion(100) == 29
    assert abs(kurtagefunktion(50000) - 50) < 10 ** -12
    kurtagefunktion = kurtage.nordnet_kurtage_bygger(valuta="usd", valutakurs=6.29)
    assert abs(kurtagefunktion(100) - 82.02) < 10 ** -12
    assert abs(kurtagefunktion(75000) - 300) < 10 ** -12
    kurtagefunktion = kurtage.nordnet_kurtage_bygger(valuta="usd", valutakurs=6.29, valutakonto=True)
    assert abs(kurtagefunktion(100) - 81.845) < 10 ** -12
    assert abs(kurtagefunktion(75000) - 168.75) < 10 ** -12
    kurtagefunktion = kurtage.nordnet_kurtage_bygger(valuta="euro", valutakurs=7.44)
    assert abs(kurtagefunktion(100) - 89.53) < 10 ** -12
    assert abs(kurtagefunktion(75000) - 300) < 10 ** -12
    kurtagefunktion = kurtage.nordnet_kurtage_bygger(valuta="euro", valutakurs=7.44, valutakonto=True)
    assert abs(kurtagefunktion(100) - 89.355) < 10 ** -12
    assert abs(kurtagefunktion(75000) - 168.75) < 10 ** -12


def test_lunarinvest_kurtage():
    """Test kurtage for Saxo bank"""
    kurtagefunktion = kurtage.lunar_kurtage_bygger(valuta="Dkk")
    assert kurtagefunktion(40000) == 19
    assert abs(kurtagefunktion(50001) - 69.001) < 10 ** -12
    kurtagefunktion = kurtage.lunar_kurtage_bygger(valuta="usd")
    assert abs(kurtagefunktion(40000) - 219) < 10 ** -12
    assert abs(kurtagefunktion(50001) - 319.006) < 10 ** -12
