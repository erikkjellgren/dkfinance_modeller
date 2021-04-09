import os
import runpy


def test_investeringsforening_udbytte():
    """Test at koden i docs producere det rigtige."""
    runpy.run_path(
        f"{os.path.dirname(__file__)}/../docs/analyser/investeringsforening_udbytte/investeringsforening_udbytte.py"  # pylint: disable=C0301
    )
    os.remove("distributioner.svg")
    os.remove("fraktiler.svg")


def test_lager_vs_realisation():
    """Test at koden i docs producere det rigtige."""
    runpy.run_path(
        f"{os.path.dirname(__file__)}/../docs/analyser/lager_vs_realisation/lager_vs_realisation.py"  # pylint: disable=C0301
    )
    os.remove("fraktiler.svg")
    os.remove("real_lager_fraktiler.svg")


def test_skatteoptimering_limit():
    """Test at koden i docs producere det rigtige."""
    runpy.run_path(
        f"{os.path.dirname(__file__)}/../docs/analyser/skatteoptimering_limit/skatteoptimering_limit.py"  # pylint: disable=C0301
    )
    os.remove("oevregraense_skatteoptimering.svg")


def test_ask_aop_vs_realisation():
    """Test at koden i docs producere det rigtige."""
    runpy.run_path(
        f"{os.path.dirname(__file__)}/../docs/analyser/ask_aop_vs_realisation/ask_aop_vs_realisation.py"  # pylint: disable=C0301
    )
    os.remove("aop_vs_real.svg")
    os.remove("ask_vs_real.svg")
    os.remove("ask_vs_real_gennemsnit.svg")


def test_estimat_effektiv_cagr():
    """Test at koden i docs producere det rigtige."""
    runpy.run_path(
        f"{os.path.dirname(__file__)}/../docs/analyser/estimat_effektiv_cagr/estimat_effektiv_cagr.py"  # pylint: disable=C0301
    )
    os.remove("cagr7.svg")
    os.remove("cagr15.svg")


def test_sulaan_investering():
    """Test at koden i docs producere det rigtige."""
    runpy.run_path(
        f"{os.path.dirname(__file__)}/../docs/analyser/sulaan_investering/sulaan_investering.py"  # pylint: disable=C0301
    )
    os.remove("sulaan_profit.svg")


def test_huspriser():
    """Test at koden i docs producere det rigtige."""
    runpy.run_path(
        f"{os.path.dirname(__file__)}/../docs/analyser/huspriser/huspriser.py"  # pylint: disable=C0301
    )
    os.remove("indekser.svg")
    os.remove("geografiske_forskelle.svg")
    os.remove("huspris_rente_funktion.svg")
