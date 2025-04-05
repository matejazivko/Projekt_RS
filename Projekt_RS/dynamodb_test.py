from app.database import create_table_if_not_exists, dynamodb, users_table, houses_table
from app.routes.users import register_user, login
from app.routes.comments import add_comment, get_comments, update_comment, delete_comment
from app.models import UserRegister, UserLogin, Comment
from botocore.exceptions import ClientError
import io

def test_create_users_table():
    create_table_if_not_exists(
        "users",
        [{"AttributeName": "username", "KeyType": "HASH"}],
        [{"AttributeName": "username", "AttributeType": "S"}]
    )

def test_create_comments_table():
    create_table_if_not_exists(
        "comments",
        [{"AttributeName": "house_name", "KeyType": "HASH"}, {"AttributeName": "username", "KeyType": "RANGE"}],
        [{"AttributeName": "house_name", "AttributeType": "S"}, {"AttributeName": "username", "AttributeType": "S"}]
    )

def test_register_user():
    user = UserRegister(username="TestUser", email="testuser@example.com", password="test123")
    try:
        response = register_user(user)
        print(f"Korisnik registriran: {response}")
    except Exception as e:
        print(f"Greška pri registraciji korisnika: {e}")

def test_login_user():
    user = UserLogin(username="TestUser", password="test123")
    try:
        response = login(user)
        print(f"Prijava uspješna: {response}")
    except Exception as e:
        print(f"Greška prilikom prijave korisnika: {e}")

def test_get_houses():
    try:
        response = houses_table.scan()
        print("Kuće:", response.get("Items", []))
    except ClientError as e:
        print(f"Greška prilikom dohvaćanja kuća: {e}")

def test_add_comment():
    comment = Comment(username="TestUser", house_id="ID kuće", content="komentar")
    try:
        response = add_comment(comment)
        print(f"Komentar uspješno dodan: {response}")
    except Exception as e:
        print (f"Greška prilikom dodavanja komentara: {e}")

def test_get_comments():
    house_name = "Naziv kuće"
    try:
        response = get_comments(house_name)
        print(f"Komentari za kuću {house_name}: {response}")
    except Exception as e:
        print (f"Greška prilikom dohvaćanja: {e}")

def test_update_comment():
    house_name = "Naziv kuće"
    username = "TestUser"
    new_content = "komentar"
    try:
        response = update_comment(house_name, new_content, username)
        print(f"Komentar je uspješno ažuriran: {response}")
    except Exception as e:
        print(f"Greška prilikom ažuriranja komentara: {e}")

def test_delete_comment():
    house_name = "Naziv kuće"
    username = "TestUser"
    try:
        response = delete_comment(house_name, username)
        print(f"Komentar je uspješno obrisan: {response}")
    except Exception as e:
        print (f"Greška prilikom brisanja komentara: {e}")

def run_tests():
    test_create_users_table()
    test_create_comments_table()
    test_register_user()
    test_login_user()
    test_get_houses()
    test_add_comment()
    test_get_comments()
    test_update_comment()
    test_delete_comment()

run_tests()