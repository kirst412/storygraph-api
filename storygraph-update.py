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
        print("Setup complete.")

        print("\n--- 2. Retrieving currently reading list ---")

        currently_reading = user_client.currently_reading(username, auth_cookies)
        valid_date_entries = []        

        try:
            print("\nFetching all journal entries...")
            all_journal_entries = user_client.get_all_journal_entries(auth_cookies)
            all_journal_data = json.loads(all_journal_entries)
            if isinstance(all_journal_data, list):
                for entry in all_journal_data:
                    if entry['date'] != "No date":
                        valid_date_entries.append(entry)
            else:
                print(f"Error: All journal entries not returned as a list.")
        except Exception as e:
            print(f"Error fetching all journal entries: {e}")

        print(valid_date_entries)


if __name__ == '__main__':
    main()
