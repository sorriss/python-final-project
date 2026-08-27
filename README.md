# python-final-project

## Description

A console-based personal assistant bot: helps you store contacts (address
book) and notes. Contacts support phone numbers, email, address, and
birthday (with reminders for upcoming birthdays); notes support text and
tags for quick searching. All data is automatically saved to disk
(`~/.personal_assistant/addressbook.pkl`) on exit and reloaded on the next
run.

Run it with:

```bash
python main.py
```

The bot works as a dialog: type a command and its arguments separated by
spaces, and it replies. If a command is misspelled, the bot suggests a
similar one.

## Commands

| Command | Description | Example |
|---|---|---|
| `hello` | Greet the bot | `hello` |
| `add <name> <phone>` | Add a contact or a phone to an existing contact | `add John 1234567890` |
| `change <name> <old_phone> <new_phone>` | Replace a contact's phone number | `change John 1234567890 0987654321` |
| `edit-phone <name> <old_phone> <new_phone>` | Same as `change` | `edit-phone John 1234567890 0987654321` |
| `remove-phone <name> <phone>` | Remove a phone number from a contact | `remove-phone John 1234567890` |
| `phone <name>` | Show a contact's phone numbers | `phone John` |
| `all` | Show all contacts | `all` |
| `delete <name>` | Delete a contact | `delete John` |
| `add-address <name> <address>` | Add an address to a contact | `add-address John 221B Baker Street` |
| `add-email <name> <email>` | Add an email to a contact | `add-email John john@example.com` |
| `add-birthday <name> <DD.MM.YYYY>` | Add a birthday to a contact | `add-birthday John 15.05.1990` |
| `show-birthday <name>` | Show a contact's birthday | `show-birthday John` |
| `birthdays [days]` | Show birthdays coming up in the next `days` days (default 7) | `birthdays 14` |
| `search <query>` | Search contacts by name, phone, email, or address | `search John` |
| `add-note <text>` | Add a note | `add-note Buy milk` |
| `find-note <id\|text>` | Find a note by id or text | `find-note milk` |
| `edit-note <id> <new_text>` | Edit a note's text | `edit-note 1 Buy bread` |
| `delete-note <id>` | Delete a note | `delete-note 1` |
| `all-notes` | Show all notes | `all-notes` |
| `add-tag <note_id> <tag>` | Add a tag to a note | `add-tag 1 shopping` |
| `find-by-tag <tag> [tag...]` | Find notes by one or more tags | `find-by-tag shopping urgent` |
| `close` / `exit` | Save data and quit | `exit` |
