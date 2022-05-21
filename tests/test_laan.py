import dkfinance_modeller.laan.laanmodel as laanmodel


def test_SUlån():
    """Test SUlån."""
    sulån = laanmodel.SUlån(5 * 12, 16, 1)
    sulån.lån_per_måned = 3234
    idx = 0
    for afdrag, fradrag in sulån.propager_måned():
        if 0 <= idx < 60:
            assert afdrag == 3234.0
            assert fradrag == 0.0
        elif 60 <= idx < 76:
            assert afdrag == 0.0
            assert fradrag == 0.0
        else:
            assert abs(afdrag + 1301.8365902678604) < 10**-4
        idx += 1
