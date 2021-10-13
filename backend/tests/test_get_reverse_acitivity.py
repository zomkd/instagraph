def test_get_reverse_activity(supply_get_reverse_activity):
    response = supply_get_reverse_activity
    assert response == [{'like_count': 0,'pk': 5795335796,
'username': '_evgenii.vasilev_'},
{'like_count': 0,
 'pk': 565663778,
 'username': 'soul_prairie'},]


