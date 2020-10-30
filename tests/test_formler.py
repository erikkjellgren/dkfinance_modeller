import dkfinance_modeller.simple_modeller.formler as formler


def test_årlig_til_n_rente():
    """Test årlig rente til månedlig rente."""
    assert abs(formler.årlig_til_n_rente(0.04, 12) - 0.00327373978219891) < 10 ** -12


def test_opsparing():
    """Test opsparing."""
    assert abs(formler.opsparing(0, 3194, 0.00327373978219891, 36) - 122221.45349595) < 10 ** -6


def test_afbetalling():
    """Test afbetalling."""
    assert abs(formler.afbetalling(122221.45349595, 0.000829538114346162, 132) - 977.111801040738) < 10 ** -6
