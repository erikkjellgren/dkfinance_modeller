

def aktiebeskatning(dkk: float, progressionsgrænse: float=55300) -> float:
    """Aktiebskatning.
    
    Args:
      dkk: Kapital til beskatning.
      progressionsgrænse: Grænse hvor skatten skifter fra 0.27% til 0.42%
      
    Returns:
      Skat
    """
    return min(progressionsgrænse, dkk)*0.27 + max(0, dkk-progressionsgrænse)*0.42
    
def aktiesparekontobeskatning(dkk: float):
    """Akstiesparekontobeskatning.
    
    Args:
      dkk: Kapital til beskatning.
      
    Returns:
      Skat
    """
    return dkk*0.17
    
def pensionsbeskatning(dkk: float):
    """Pensionsopsparingsbeskatning.
    
    Args:
      dkk: Kapital til beskatning.
      
    Returns:
      Skat
    """
    return dkk*0.153