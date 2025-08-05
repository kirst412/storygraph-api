from dotenv import load_dotenv
import os
from storygraph_api import Book, User
import json
from notion_client import Client
from datetime import datetime


def entry_exists(client, database_id, book_title, author, date, progress_percent):
    """
    Check if the journal entry already exists in the notion database
    """
    query = client.databases.query(
        database_id=database_id,
        filter={
            "and": [
                {"property": "Book Title", "title": {"equals": book_title}},
                {"property": "Author", "rich_text": {"equals": author}},
                {"property": "Date", "date": {"equals": date}},
                {"property": "Progress", "number": {"equals": round(progress_percent, 2)}}
            ]
        }
    )
    results = query['results']

    return results[0] if results else None


def create_entry(client, database_id, book_title, author, date, progress_percent):
    """
    Create a new entry for a reading session in the notion database.
    """
    properties = {
        "Book Title": {"title": [{"text": {"content": book_title}}]},
        "Author": {"rich_text": [{"text": {"content": author}}]},
        "Date": {"date": {"start": date}},
        "Progress": {"number": round(progress_percent, 2)},
    }

    page = {
        "parent": {"database_id": database_id},
        "properties": properties,
    }
    
    client.pages.create(**page)

def format_date(date_str):
    date_obj = datetime.strptime(date_str, "%d %B %Y")
    return datetime.strftime(date_obj, "%Y-%m-%d")

def main():
    load_dotenv()

    username = os.getenv("STORYGRAPH_USERNAME")
    session_cookie = os.getenv("_STORYGRAPH_SESSION")
    remember_token = os.getenv("REMEMBER_USER_TOKEN")

    if not all([username, session_cookie, remember_token]):
        print("Error: Missing one or more required environment variables.")
        print("Please ensure _STORYGRAPH_SESSION, REMEMBER_USER_TOKEN, and STORYGRAPH_USERNAME are in your .env file.")
    else:
        auth_cookies = {
            "_storygraph_session": session_cookie,
            "remember_user_token": remember_token
        }
        notion_token = os.getenv("NOTION_TOKEN")
        database_id = os.getenv("NOTION_STORYGRAPH_DB_ID")
        client = Client(auth=notion_token)
    
        book_client = Book()
        user_client = User()
        print("Setup complete.")

        print("\n--- 2. Retrieving currently reading list ---")

        currently_reading = user_client.currently_reading(username, auth_cookies)
        print(currently_reading)
        valid_date_entries = []        

        try:
            print("\nFetching all journal entries...")
            all_journal_entries = user_client.get_all_journal_entries(auth_cookies)
            print(all_journal_entries)
            all_journal_data = json.loads(all_journal_entries)
            if isinstance(all_journal_data, list):
                for entry in all_journal_data:
                    if entry['date'] != "No date":
                        valid_date_entries.append(entry)
            else:
                print(f"Error: All journal entries not returned as a list.")
        except Exception as e:
            print(f"Error fetching all journal entries: {e}")

        print(len(valid_date_entries))
        
        for entry in valid_date_entries:
            book_title = entry['book_title']
            book_id = entry['book_id']
            date = entry['date']
            clean_date = format_date(date)
            progress_percent = entry['progress_percent']
            if progress_percent is None:
                progress_percent = 0
            book_info = eval(book_client.book_info(book_id))
            author = ", ".join(book_info['authors']) # type: ignore
            existing_entry = entry_exists(client, database_id, book_title, author, clean_date, progress_percent)
            if not existing_entry:
                print(f"creating new entry for {book_title}")
                create_entry(client, database_id, book_title, author, clean_date, progress_percent)
            else:
                print("entry already exists")


if __name__ == '__main__':
    main()
