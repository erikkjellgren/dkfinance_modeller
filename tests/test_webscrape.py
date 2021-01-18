import dkfinance_modeller.utility.webscrape as webscrape


def test_få_etf_info():
    """Test få info fra justetf.com/en/."""
    info = webscrape.få_etf_info(["IE00BYZK4669"], 1)[0]
    assert info["isin"] == "IE00BYZK4669"
    assert info["succes"]
    assert info["replication"] == "Physical (Optimized sampling)"
    assert info["åop"] == "0.40"
    assert info["indeks"] == "iSTOXX® FactSet Ageing Population index"
    assert info["navn"] == "iShares Ageing Population UCITS ETF"
    assert info["domicile"] == "Ireland"
    info = webscrape.få_etf_info(["IE00B5BMR087"], 1)[0]
    assert info["isin"] == "IE00B5BMR087"
    assert info["succes"]
    assert info["replication"] == "Physical (Full replication)"
    assert info["åop"] == "0.07"
    assert info["indeks"] == "S&P 500® index"
    assert info["navn"] == "iShares Core S&P 500 UCITS ETF (Acc)"
    assert info["domicile"] == "Ireland"
    info = webscrape.få_etf_info(["A"], 1)[0]
    assert info["isin"] == "A"
    assert not info["succes"]
