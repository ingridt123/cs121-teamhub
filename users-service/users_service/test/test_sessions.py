from users_service.sessions import Sessions


def test_sessions_double():

    # ensure two concurrent logins from same user have different tokens
    sessions = Sessions()
    session1 = sessions.add("athlete1", "dummy_token1")
    session2 = sessions.add("athlete1", "dummy_token2")
    assert session1.user_token != session2.user_token
