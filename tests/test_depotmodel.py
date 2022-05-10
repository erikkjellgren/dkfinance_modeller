import pytest

import dkfinance_modeller.aktieskat.depotmodel as depotmodel
import dkfinance_modeller.aktieskat.kurtage as kurtage
import dkfinance_modeller.aktieskat.skat as skat
import dkfinance_modeller.aktieskat.vaerdipapirer as værdipapirer
import dkfinance_modeller.aktieskat.valuta as valuta


def test_køb_værdipapirer():
    """Test køb af værdipapirer."""
    kapitalændring, kurtageudgift, antal_værdipapirer = depotmodel.køb_værdipapirer(
        1000, 100, kurtage.nulkurtage
    )
    assert abs(kapitalændring + 1000) < 10**-12
    assert kurtageudgift == 0
    assert antal_værdipapirer == 10

    def kurtage2(kapital: float, kurs: float = 0.0) -> float:  # pylint: disable=W0613
        return 0.001 * kapital

    kapitalændring, kurtageudgift, antal_værdipapirer = depotmodel.køb_værdipapirer(1000, 100, kurtage2)
    assert abs(kapitalændring + 900.9) < 10**-12
    assert kurtageudgift == 0.9
    assert antal_værdipapirer == 9

    def kurtage3(kapital: float, kurs: float = 0.0) -> float:  # pylint: disable=W0613
        return 0.0 * kapital + 101

    kapitalændring, kurtageudgift, antal_værdipapirer = depotmodel.køb_værdipapirer(1000, 100, kurtage3)
    assert abs(kapitalændring + 901) < 10**-12
    assert kurtageudgift == 101
    assert antal_værdipapirer == 8


def test_køb_værdipapirer_exceptions():
    """Test at exceptions virker som forventet i køb_værdipapirer()."""
    with pytest.raises(ValueError, match="kapital er negativ"):
        depotmodel.køb_værdipapirer(-1000, 100, kurtage.nulkurtage)
    with pytest.raises(ValueError, match="kurs er negativ"):
        depotmodel.køb_værdipapirer(1000, -100, kurtage.nulkurtage)


def test_DepotModel_simpel():
    """Test DepotModel simpelt tilfælde."""
    skatter = skat.Skat(beskatningstype="nul")
    etf = værdipapirer.ETF(kurs=1.0, åop=0.0, beskatningstype="lager")
    depot = depotmodel.DepotModel(
        kapital=1.0,
        kurtagefunktion=kurtage.nulkurtage,
        skatteklasse=skatter,
        minimumskøb=0,
        ETFer=[etf],
        ETF_fordeling=[1.0],
    )
    for i in range(0, 36):
        depot.afkast_månedlig([0.01 * (1 + 0.01) ** i], [0.0])
    assert abs(depot.total_salgsværdi() - (1 + 0.01) ** 36) < 10**-12
    assert depot.kapital == 0.0
    assert depot.ETFer[0].antal_værdipapirer == 1


def test_DepotModel_beskatning():
    """Test DepotModel med beskatning."""
    skatter = skat.Skat(beskatningstype="ask")
    etf = værdipapirer.ETF(kurs=1.0, åop=0.0, beskatningstype="lager")
    depot = depotmodel.DepotModel(
        kapital=10.0,
        kurtagefunktion=kurtage.nulkurtage,
        skatteklasse=skatter,
        minimumskøb=0,
        ETFer=[etf],
        ETF_fordeling=[1.0],
    )
    for i in range(0, 24):
        depot.afkast_månedlig([0.01 * (1 + 0.01) ** i], [0.0])
    assert abs(depot.total_salgsværdi() - 12.1201825995429) < 10**-12
    assert abs(depot.kapital - 0.692570762755705) < 10**-12
    assert depot.ETFer[0].antal_værdipapirer == 9


def test_DepotModel_geninvestering():
    """Test DepotModel med geninvestering."""
    skatter = skat.Skat(beskatningstype="nul")
    etf = værdipapirer.ETF(kurs=1.0, åop=0.0, beskatningstype="lager")
    depot = depotmodel.DepotModel(
        kapital=1.0,
        kurtagefunktion=kurtage.nulkurtage,
        skatteklasse=skatter,
        minimumskøb=0,
        ETFer=[etf],
        ETF_fordeling=[1.0],
    )
    for i in range(0, 24):
        depot.kapital += 1.0
        depot.afkast_månedlig([0.01 * (1 + 0.01) ** i], [0.0])
    assert abs(depot.total_salgsværdi() - 28.0706270191644) < 10**-12
    assert abs(depot.kapital - 0.136464751462226) < 10**-12
    assert depot.ETFer[0].antal_værdipapirer == 22


def test_DepotModel_udbytte():
    """Test DepotModel med udbytte."""
    skatter = skat.Skat(beskatningstype="nul")
    etf = værdipapirer.ETF(kurs=1.0, åop=0.0, beskatningstype="lager")
    depot = depotmodel.DepotModel(
        kapital=1.0,
        kurtagefunktion=kurtage.nulkurtage,
        skatteklasse=skatter,
        minimumskøb=0,
        ETFer=[etf],
        ETF_fordeling=[1.0],
    )
    for _ in range(0, 24):
        depot.afkast_månedlig([0.0], [0.05])
    assert abs(depot.total_salgsværdi() - 2.4) < 10**-12
    assert abs(depot.kapital - 0.4) < 10**-12
    assert depot.ETFer[0].antal_værdipapirer == 2


def test_DepotModel_valutakurtage():
    """Test DepotModel med valutakurtage."""
    skatter = skat.Skat(beskatningstype="nul")
    etf = værdipapirer.ETF(kurs=1.0, åop=0.0, beskatningstype="lager")
    depot = depotmodel.DepotModel(
        kapital=1.0,
        kurtagefunktion=kurtage.nulkurtage,
        skatteklasse=skatter,
        minimumskøb=0,
        ETFer=[etf],
        ETF_fordeling=[1.0],
        valutafunktion=valuta.saxo_underkonto_kurtage,
    )
    assert depot.kapital == 0.9985
    assert depot.ubeskattet == -0.0015
    assert abs(depot.total_salgsværdi() - 0.9985) < 10**-12


def test_DepotModel_negativt_afkast():
    """Test beskatning af negativt afkast."""
    skatter = skat.Skat(beskatningstype="ask")
    etf = værdipapirer.ETF(kurs=1.0, åop=0.0, beskatningstype="lager")
    depot = depotmodel.DepotModel(
        kapital=1.0,
        kurtagefunktion=kurtage.nulkurtage,
        skatteklasse=skatter,
        minimumskøb=0,
        ETFer=[etf],
        ETF_fordeling=[1.0],
    )
    depot.afkast_månedlig([-0.01], [0.0])
    depot.afkast_månedlig([0.01], [0.0])
    assert abs(depot.total_salgsværdi() - 1.0) < 10**-12
    assert depot.kapital == 0.0
    assert depot.ETFer[0].antal_værdipapirer == 1


def test_DepotModel_realisationsbeskatning():
    """Test realisationsbeskatning."""
    skatter = skat.Skat(beskatningstype="aktie")
    skatter.progressionsgrænse = 55300.0
    etf = værdipapirer.ETF(kurs=1.0, åop=0.0, beskatningstype="realisation")
    depot = depotmodel.DepotModel(
        kapital=100000.0,
        kurtagefunktion=kurtage.nulkurtage,
        skatteklasse=skatter,
        minimumskøb=0,
        ETFer=[etf],
        ETF_fordeling=[1.0],
    )
    for _ in range(0, 24):
        depot.afkast_månedlig([0.05], [0.0])
    assert abs(depot.total_salgsværdi() - 177895) < 10**-10
    assert depot.kapital < 10**-12
    assert depot.ETFer[0].antal_værdipapirer == 100000


def test_DepotModel_totalværdi_med_fradrag():
    """Test totalværdi af depot med fradrag."""
    skatter = skat.Skat(beskatningstype="aktie")
    etf = værdipapirer.ETF(kurs=1.0, åop=0.0, beskatningstype="lager")
    depot = depotmodel.DepotModel(
        kapital=100000.0,
        kurtagefunktion=kurtage.nulkurtage,
        skatteklasse=skatter,
        minimumskøb=0,
        ETFer=[etf],
        ETF_fordeling=[1.0],
    )
    depot.afkast_månedlig([-0.05], [0.0])
    assert abs(depot.total_salgsværdi(medregn_fradrag=True) - 96350) < 10**-10


def test_DepotModel_frigør_kapital():
    """Test frigørelse af kapital."""
    skatter = skat.Skat(beskatningstype="aktie")
    etf = værdipapirer.ETF(kurs=1.0, åop=0.0, beskatningstype="lager")
    depot = depotmodel.DepotModel(
        kapital=100000.0,
        kurtagefunktion=kurtage.nulkurtage,
        skatteklasse=skatter,
        minimumskøb=0,
        ETFer=[etf],
        ETF_fordeling=[1.0],
    )
    assert abs(depot.total_salgsværdi() - 100000) < 10**-10
    depot.frigør_kapital(10000)
    assert abs(depot.kapital - 10000) < 10**-10
    assert abs(depot.total_salgsværdi() - 100000) < 10**-10


def test_DepotModel_exceptions():
    """Test exceptions i DepotModel klassen."""
    with pytest.raises(ValueError, match="Kapital kan ikke være negativt"):
        skatter = skat.Skat(beskatningstype="nul")
        etf = værdipapirer.ETF(kurs=2.0, åop=0.0, beskatningstype="realisation")
        depot = depotmodel.DepotModel(
            kapital=1.0,
            kurtagefunktion=kurtage.nulkurtage,
            skatteklasse=skatter,
            minimumskøb=0,
            ETFer=[etf],
            ETF_fordeling=[1.0],
        )
        depot.kapital -= 2.0
    with pytest.raises(Exception, match="ETF er ikke stor nok til at betale skatten"):
        etfer = []
        fordeling = []
        afkast = []
        udbytte = []
        for _ in range(0, 200):
            etfer.append(værdipapirer.ETF(kurs=1.0, åop=0.0, beskatningstype="lager"))
            fordeling.append(1 / 200)
            afkast.append(10)
            udbytte.append(0)
        skatter = skat.Skat(beskatningstype="aktie")
        depot = depotmodel.DepotModel(
            kapital=1000.0,
            kurtagefunktion=kurtage.nulkurtage,
            skatteklasse=skatter,
            minimumskøb=0,
            ETFer=etfer,
            ETF_fordeling=fordeling,
        )
        for _ in range(0, 12):
            depot.afkast_månedlig(afkast, udbytte)
