import os
import runpy


def test_sulån_simpel_model():
    """Test at koden i docs producere det rigtige."""
    runpy.run_path(f"{os.path.dirname(__file__)}/../docs/analyser/sulaan_investering/sulaan_investering.py")


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
