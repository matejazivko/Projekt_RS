from app.database import create_table_if_not_exists, dynamodb, users_table, houses_table
from app.routes.users import register_user, login
from app.models import UserRegister, UserLogin
from botocore.exceptions import ClientError
import io

def test_create_users_table():
    create_table_if_not_exists(
        "users",
        [{"AttributeName": "username", "KeyType": "HASH"}],
        [{"AttributeName": "username", "AttributeType": "S"}]
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

def run_tests():
    test_create_users_table()
    test_register_user()
    test_login_user()
    test_get_houses()

run_tests()