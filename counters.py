"""
Auto-increment helper.

MongoDB documents normally use random ObjectIds, not sequential integers.
To keep our API contract identical to the SQL version (account_id: 1, 2, 3...),
we simulate auto-increment using a small "counters" collection that tracks
the last-used ID per entity type.
"""
from pymongo.database import Database


def get_next_sequence(db: Database, sequence_name: str) -> int:
    """
    Atomically increments and returns the next ID for the given sequence
    (e.g. "user_id", "account_id", "txn_id").
    """
    result = db["counters"].find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True,
    )
    return result["seq"]
