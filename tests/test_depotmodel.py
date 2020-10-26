import aktieskat.depotmodel as depotmodel
import aktieskat.kurtage as kurtage
import aktieskat.skat as skat
import aktieskat.værdipapirer as værdipapirer


def test_køb_værdipapirer():
    """Test køb af værdipapirer."""
    kapitalændring, kurtageudgift, antal_værdipapirer = depotmodel.køb_værdipapirer(
        1000, 100, kurtage.nulkurtage
    )
    assert abs(kapitalændring + 1000) < 10 ** -12
    assert kurtageudgift == 0
    assert antal_værdipapirer == 10

    def kurtage2(kapital: float, kurs: float = 0.0) -> float:  # pylint: disable=W0613
        return 0.001 * kapital

    kapitalændring, kurtageudgift, antal_værdipapirer = depotmodel.køb_værdipapirer(1000, 100, kurtage2)
    assert abs(kapitalændring + 900.9) < 10 ** -12
    assert kurtageudgift == 0.9
    assert antal_værdipapirer == 9

    def kurtage3(kapital: float, kurs: float = 0.0) -> float:  # pylint: disable=W0613
        return 0.0 * kapital + 101

    kapitalændring, kurtageudgift, antal_værdipapirer = depotmodel.køb_værdipapirer(1000, 100, kurtage3)
    assert abs(kapitalændring + 901) < 10 ** -12
    assert kurtageudgift == 101
    assert antal_værdipapirer == 8


def test_lagerbeskatning_simpel():
    """Test lagerbeskatning simpelt tilfælde."""
    etf = værdipapirer.ETF(kurs=1.0, åop=0.0)
    depot = depotmodel.Lagerbeskatning(
        kapital=1.0,
        kurtagefunktion=kurtage.nulkurtage,
        skattefunktion=skat.nulskat,
        minimumskøb=0,
        ETFer=[etf],
        ETF_fordeling=[1.0],
    )
    for _ in range(0, 36):
        depot.afkast_månedlig([0.01], [0.0])
    assert abs(depot.total_salgsværdi() - (1 + 0.01) ** 36) < 10 ** -12
    assert depot.kapital == 0.0
    assert depot.ETFer[0].antal_værdipapirer == 1


def test_lagerbeskatning_beskatning():
    """Test lagerbeskatning simpelt tilfælde."""
    etf = værdipapirer.ETF(kurs=1.0, åop=0.0)
    depot = depotmodel.Lagerbeskatning(
        kapital=10.0,
        kurtagefunktion=kurtage.nulkurtage,
        skattefunktion=skat.aktiesparekontobeskatning,
        minimumskøb=0,
        ETFer=[etf],
        ETF_fordeling=[1.0],
    )
    for _ in range(0, 24):
        depot.afkast_månedlig([0.01], [0.0])
    assert abs(depot.total_salgsværdi() - 12.1201825995429) < 10 ** -12
    assert abs(depot.kapital - 0.692570762755705) < 10 ** -12
    assert depot.ETFer[0].antal_værdipapirer == 9
