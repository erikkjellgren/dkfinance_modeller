import os
import runpy


def test_sulån_simpel_model():
    """Test at koden i docs producere det rigtige."""
    runpy.run_path(
        os.path.join(os.path.dirname(__file__), "../docs/analyser/sulaan_inverstering/sulaan_inverstering.py")
    )
