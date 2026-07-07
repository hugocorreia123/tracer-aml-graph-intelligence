"""Tracer — Phase 0: first look at HI-Small.

Prints schema, row counts, illicit rate, and a peek at the
laundering-pattern ground truth. Read-only; writes nothing.
"""

import pandas as pd

RAW = "data/raw"

# ---------- Transactions ----------
print("=" * 60)
print("TRANSACTIONS (HI-Small_Trans.csv)")
print("=" * 60)

trans = pd.read_csv(f"{RAW}/HI-Small_Trans.csv")
print(f"rows: {len(trans):,}")
print(f"columns: {list(trans.columns)}")
print()
print(trans.head(5).to_string())
print()
print("dtypes:")
print(trans.dtypes.to_string())
print()

label_col = "Is Laundering"
n_illicit = int(trans[label_col].sum())
print(f"illicit transactions: {n_illicit:,} / {len(trans):,} "
      f"({100 * n_illicit / len(trans):.4f}%)")
print()

# Unique accounts (sender/receiver account columns)
from_acct = trans.columns[2]  # bank-from, account-from, ...
to_acct = trans.columns[4]
n_accounts = pd.concat([trans[from_acct], trans[to_acct]]).nunique()
print(f"unique accounts referenced: {n_accounts:,}")
print(f"payment formats: {trans['Payment Format'].value_counts().to_dict()}")
print(f"currencies (receiving): "
      f"{trans['Receiving Currency'].nunique()} unique")
print(f"timestamp range: {trans['Timestamp'].min()}  →  "
      f"{trans['Timestamp'].max()}")
print()

# ---------- Accounts ----------
print("=" * 60)
print("ACCOUNTS (HI-Small_accounts.csv)")
print("=" * 60)
acct = pd.read_csv(f"{RAW}/HI-Small_accounts.csv")
print(f"rows: {len(acct):,}")
print(f"columns: {list(acct.columns)}")
print(acct.head(5).to_string())
print()

# ---------- Patterns (typology ground truth) ----------
print("=" * 60)
print("PATTERNS (HI-Small_Patterns.txt) — first 40 lines")
print("=" * 60)
with open(f"{RAW}/HI-Small_Patterns.txt") as f:
    for i, line in enumerate(f):
        if i >= 40:
            break
        print(line.rstrip())
