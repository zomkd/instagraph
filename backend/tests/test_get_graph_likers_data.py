def test_get_graph_likers_data(supply_get_graph_likers_data):
    response = supply_get_graph_likers_data
    assert response ==  [
                            [{'_color': 'blue',
                            'id': 4033918006,
                            'name': 'aikmartirosan'},
                        {'id': 5795335796,
                            'like_count': 2,
                            'name': '_evgenii.vasilev_\n'
                                    ' (Евгений Васильев)'},
                        {'id': 565663778,
                            'like_count': 2,
                            'name': 'soul_prairie\n'
                                    ' (🐺)'},
                        {'id': 3093705485,
                            'like_count': 1,
                            'name': 'm.a.t.v.e.__a.n.a.s.t.a.s\n'
                                    ' (♥☞ 𝓝𝐚𝓢𝕥Ⓔᑎᛕ𝕒 ✊👑)'}],
                        [{'_color': '#517d99',
                            '_svgAttrs': {'opacity': 1,
                                        'stroke-width': 2},
                            'like_count': 2,
                            'sid': 5795335796,
                            'tid': 4033918006},
                        {'_color': '#517d99',
                            '_svgAttrs': {'opacity': 1,
                                        'stroke-width': 2},
                            'like_count': 2,
                            'sid': 565663778,
                            'tid': 4033918006},
                        {'_color': '#517d99',
                            '_svgAttrs': {'opacity': 1,
                                        'stroke-width': 2},
                            'like_count': 1,
                            'sid': 3093705485,
                            'tid': 4033918006}],
                                ]


