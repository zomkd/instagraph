def test_get_post_likers(supply_get_post_likers):
    response = supply_get_post_likers
    assert response == [{'full_name': 'Евгений Васильев',
            'is_following': False,
            'is_private': True,
            'like_count': 2,
            'pk': 5795335796,
            'username': '_evgenii.vasilev_'},
           {'full_name': '🐺',
            'is_following': False,
            'is_private': True,
            'like_count': 2,
            'pk': 565663778,
            'username': 'soul_prairie'},
           {'full_name': '♥☞ 𝓝𝐚𝓢𝕥Ⓔᑎᛕ𝕒 ✊👑',
            'is_following': False,
            'is_private': True,
            'like_count': 1,
            'pk': 3093705485,
            'username': 'm.a.t.v.e.__a.n.a.s.t.a.s'},
           ]