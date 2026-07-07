import statistics
from collections import defaultdict

def summarize_transactions(transactions):
    amounts = []
    by_category = defaultdict(float)
    for t in transactions:
        amt = t.amount if t.type == "income" else -t.amount
        amounts.append(amt)
        by_category[t.category] += amt

    if not amounts:
        stats = {"count": 0, "mean": 0, "median": 0, "min": 0, "max": 0, "std": 0}
    else:
        stats = {
            "count": len(amounts),
            "mean": statistics.mean(amounts),
            "median": statistics.median(amounts),
            "min": min(amounts),
            "max": max(amounts),
            "std": statistics.pstdev(amounts) if len(amounts) > 0 else 0
        }
    return {"stats": stats, "by_category": dict(by_category)}
