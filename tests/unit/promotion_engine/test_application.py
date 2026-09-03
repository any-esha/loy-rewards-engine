from src.promotion_engine.application import apply_promotions


def test_room_stay_during_double_points_weekend_applies_multiplier_once():
    promotions = [
        {
            "id": "PROMO-1",
            "name": "Double Points Weekend",
            "type": "EARN_MULTIPLIER",
            "value": 2.0,
            "start": "2026-09-20",
            "end": "2026-09-22",
            "applies_to": ["ROOM"],
            "active": True,
        },
        {
            "id": "PROMO-2",
            "name": "Inactive duplicate",
            "type": "EARN_MULTIPLIER",
            "value": 3.0,
            "active": False,
        },
        {
            "id": "PROMO-9",
            "name": "Active duplicate",
            "type": "EARN_MULTIPLIER",
            "value": 3.0,
            "active": True,
        },
    ]

    assert apply_promotions(1250, promotions) == 2500
