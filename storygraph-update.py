from dotenv import load_dotenv
import os
from storygraph_api import Book, User
import json


def main():
    load_dotenv()

    username = os.getenv("STORYGRAPH_USERNAME")
    session_cookie = os.getenv("_STORYGRAPH_SESSION")
    remember_token = os.getenv("REMEMBER_USER_TOKEN")

    if not all([username, session_cookie, remember_token]):
        print("🛑 Error: Missing one or more required environment variables.")
        print("Please ensure _STORYGRAPH_SESSION, REMEMBER_USER_TOKEN, and STORYGRAPH_USERNAME are in your .env file.")
    else:
        auth_cookies = {
            "_storygraph_session": session_cookie,
            "remember_user_token": remember_token
        }
    
        book_client = Book()
        user_client = User()
        print("✅ Setup complete.")

        print("\n--- 2. Testing User Client ---")

        currently_reading = user_client.currently_reading(username, auth_cookies)
        print(currently_reading)

        # user_id = None
        # try:
        #     print("\nFetching User ID for:", username)
        #     user_id_json = user_client.get_user_id(username)
        #     user_id_data = json.loads(user_id_json)
        #     if "user_id" in user_id_data:
        #         user_id = user_id_data["user_id"]
        #         print(f"✅ Success! User ID found: {user_id}")
        #     else:
        #         print(f"⚠️ Could not extract user_id from response: {user_id_json}")
        # except Exception as e:
        #     print(f"🛑 Error fetching user ID: {e}")


if __name__ == '__main__':
    main()
