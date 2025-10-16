import numpy as np
from scipy.sparse import hstack
import pandas as pd # Import pandas as it was not imported in the last code block

def extract_keyword_features(code):
    features = {}
    # Example keywords related to different vulnerabilities
    keywords = {
        "reentrancy": ["call.value", "send", "transfer", "delegatecall"],
        "access_control": ["onlyowner", "require", "assert", "revert", "modifier"],
        "arithmetic": ["add", "sub", "mul", "div", "overflow", "underflow"],
        "time_manipulation": ["block.timestamp", "now"],
        "denial_of_service": ["while", "for", "gas"],
        "bad_randomness": ["block.number", "block.timestamp", "now", "blockhash"],
        "unchecked_low_level_calls": ["call", "delegatecall", "staticcall"]
    }
    for label, kw_list in keywords.items():
        for kw in kw_list:
            features[f"{label}_{kw}"] = int(kw in code)
    return pd.Series(features)
