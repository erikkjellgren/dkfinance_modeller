import pytest

import dkfinance_modeller.aktieskat.skat as skat


def test_aktiebeskatning():
    """Test aktiebeskatning."""
    skatter = skat.Skat("aktie")
    assert abs(skatter.beregn_skat(50000) - 13500) < 10 ** -12
    assert abs(skatter.beregn_skat(100000) - 33705) < 10 ** -12


def test_aktiesparekontoskat():
    """Test beskatning af aktiesparekonto."""
    skatter = skat.Skat("ask")
    assert abs(skatter.beregn_skat(50000) - 8500) < 10 ** -12


def test_pensionsbeskatning():
    """Test beskatning af pensionsopsparing."""
    skatter = skat.Skat("pension")
    assert abs(skatter.beregn_skat(50000) - 7650) < 10 ** -12


def test_nulskat():
    """Test beskatning med nul skat."""
    skatter = skat.Skat("nul")
    assert abs(skatter.beregn_skat(50000) - 0) < 10 ** -12


def test_skat_exceptions():
    """Test exceptions i skatteklassen."""
    with pytest.raises(ValueError, match="er ikke i"):
        skat.Skat("forkertskat")
