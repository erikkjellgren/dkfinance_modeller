import os
import runpy


def test_sulån_simpel_model():
    """Test at koden i docs producere det rigtige."""
    runpy.run_path(f"{os.path.dirname(__file__)}/../docs/analyser/sulaan_inverstering/sulaan_inverstering.py")


def test_inversteringsforening_udbytte():
    """Test at koden i docs producere det rigtige."""
    runpy.run_path(
        f"{os.path.dirname(__file__)}/../docs/analyser/inversteringsforening_udbytte/inversteringsforening_udbytte.py"  # pylint: disable=C0301
    )
    os.remove(f"distributioner.svg")
    os.remove(f"fraktiler.svg")
