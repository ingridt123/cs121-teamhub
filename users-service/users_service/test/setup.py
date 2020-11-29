from users_service import firebase
from users_service.test.constants import *


def setup_tests():

    # connect database client
    db = firebase.connect_db()

    # create users
    athlete1_auth = firebase.create_user_with_email_and_password(
        email=ATHLETE1_EMAIL,
        password=ATHLETE1_PASSWORD)
    athlete2_auth = firebase.create_user_with_email_and_password(
        email=ATHLETE2_EMAIL,
        password=ATHLETE2_PASSWORD)
    coach1_auth = firebase.create_user_with_email_and_password(
        email=COACH1_EMAIL,
        password=COACH1_PASSWORD)

    # make references
    users_ref = db.collection("users")
    school_ref = db.collection("schools").document(SCHOOL_ID)
    team1_ref = school_ref.collection("teams").document(TEAM1_ID)
    team2_ref = school_ref.collection("teams").document(TEAM2_ID)

    # add school to database
    school_data = {"name": SCHOOL_NAME, "school_id": SCHOOL_ID}
    school = school_ref.push(school_data)

    # add teams to database
    team1_data = {"name": TEAM1_NAME, "team_id": TEAM1_ID}
    team1 = team1_ref.push(team1_data)

    team2_data = {"name": TEAM2_NAME, "team_id": TEAM2_ID}
    team2 = team2_ref.push(team2_data)

    # add users to teams
    athlete1_uid = athlete1_auth["localId"]
    athlete2_uid = athlete2_auth["localId"]
    coach1_uid = coach1_auth["localId"]
    athlete1_data = {
        "user_id": athlete1_uid,
        "name": ATHLETE1_NAME,
        "role": ATHLETE1_ROLE,
        "school": school_data,
        "team": team1_data
    }
    athlete2_data = {
        "user_id": athlete2_uid,
        "name": ATHLETE2_NAME,
        "role": ATHLETE2_ROLE,
        "school": school_data,
        "team": team2_data
    }
    coach1_data = {
        "user_id": coach1_uid,
        "name": COACH1_NAME,
        "role": COACH1_ROLE,
        "school": school_data,
        "team": team2_data
    }
    team1_ref.collection("members").document(athlete1_uid).push(athlete1_data)
    team2_ref.collection("members").document(athlete2_uid).push(athlete2_data)
    team2_ref.collection("members").document(coach1_uid).push(coach1_data)

    # add users to database
    users_ref.document(athlete1_uid).push(athlete1_data)
    users_ref.document(athlete2_uid).push(athlete2_data)
    users_ref.document(coach1_uid).push(coach1_data)
