import pytest

from users_service.app import app
from users_service.endpoints import sessions
from users_service.test.constants import *

# fixtures


@pytest.fixture
def client():
    with app.app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_sessions():
    sessions.reset()
    yield

# test client helper functions


def login(client, email=None, password=None):
    if not (email and password):
        return client.post("/users/login")
    return client.post("/users/login", json={
        "email": email,
        "password": password
    })


def logout(client, user_token):
    return client.post("/users/logout?user_token={}".format(user_token))


def check_token(client, user_token):
    return client.get("/users/check_token?user_token={}".format(user_token))


def get_current_user(client, user_token):
    return client.get("/users/users/current?user_token={}".format(user_token))


def get_team_members(client, team_id, user_token):
    return client.get("/users/teams/{}/members?user_token={}".format(
        team_id, user_token))

# test functions


def test_login_bad_request(client):

    # call login with no email and password
    rv = login(client)
    assert rv.status_code == 400


def test_login_wrong_credentials(client):

    # login with mismatched email and password
    rv = login(client, ATHLETE1_EMAIL, ATHLETE2_PASSWORD)
    assert rv.status_code == 401


def test_login_success(client):

    # login with correct email and password
    rv = login(client, ATHLETE1_EMAIL, ATHLETE1_PASSWORD)
    assert rv.status_code == 200


def test_login_success_double(client):

    # login twice
    rv1 = login(client, ATHLETE1_EMAIL, ATHLETE1_PASSWORD)
    rv2 = login(client, ATHLETE1_EMAIL, ATHLETE1_PASSWORD)
    assert rv1.status_code == 200
    assert rv2.status_code == 200

    # ensure different sessions are created
    assert rv1.get_json()["user_token"] != rv2.get_json()["user_token"]


def test_check_token_not_existing(client):

    # check token with invalid token
    rv = check_token(client, "XXXX-XXXX")
    assert rv.status_code == 401


def test_check_token_existing(client):

    # login
    rv1 = login(client, ATHLETE1_EMAIL, ATHLETE1_PASSWORD)
    assert rv1.status_code == 200
    user_token = rv1.get_json()["user_token"]

    # check token
    rv2 = check_token(client, user_token)
    assert rv2.status_code == 200


def test_logout(client):

    # get user token
    rv1 = login(client, ATHLETE1_EMAIL, ATHLETE1_PASSWORD)
    assert rv1.status_code == 200
    user_token = rv1.get_json()["user_token"]

    # check token
    rv2 = check_token(client, user_token)
    assert rv2.status_code == 200

    # logout
    rv3 = logout(client, user_token)
    assert rv3.status_code == 204

    # check token (and expect error)
    rv4 = check_token(client, user_token)
    assert rv4.status_code == 401


def test_get_current_user(client):

    # get user token
    rv1 = login(client, ATHLETE1_EMAIL, ATHLETE1_PASSWORD)
    assert rv1.status_code == 200
    user_token = rv1.get_json()["user_token"]

    # get current user
    rv2 = get_current_user(client, user_token)
    assert rv2.status_code == 200

    # logout
    rv3 = logout(client, user_token)
    assert rv3.status_code == 204

    # get current user (and expect error)
    rv4 = get_current_user(client, user_token)
    assert rv4.status_code == 401


def test_get_team_members_my_team(client):

    # get user token
    rv1 = login(client, ATHLETE1_EMAIL, ATHLETE1_PASSWORD)
    assert rv1.status_code == 200
    user_token = rv1.get_json()["user_token"]

    # get team id
    rv2 = get_current_user(client, user_token)
    assert rv2.status_code == 200
    team_id = rv2.get_json()["team"]["team_id"]

    # get team members
    rv3 = get_team_members(client, team_id, user_token)
    assert rv3.status_code == 200


def test_get_team_members_other_team(client):

    # get user token
    rv1 = login(client, ATHLETE1_EMAIL, ATHLETE1_PASSWORD)
    assert rv1.status_code == 200
    user_token = rv1.get_json()["user_token"]

    # get team members for some other team (and expect error)
    rv2 = get_team_members(client, TEAM2_ID, user_token)
    assert rv2.status_code == 401
