def test_get_user_info(supply_get_user_info):
    response = supply_get_user_info
    assert response[0]['username'] == 'aikmartirosan'