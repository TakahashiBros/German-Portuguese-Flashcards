# 🇩🇪 German-Portuguese Flashcard Builder

A custom desktop application built in Python to help me learn German.

As a native Portuguese speaker, I needed a way to study vocabulary. I started reading books in German, but that wasn´t enough. So I designed an app that automatically fetches the Portuguese translation via Google Translate and scrapes the official German definition directly from the German Wiktionary API. 

## ✨ Features

* **Automated Data Fetching:** Type a German word, and the app instantly retrieves its Portuguese translation and German definition.
* **Modern GUI:** Built with `customtkinter` for a sleek, dark-mode desktop experience.
* **Smart Study Mode:** Shuffles your database into a randomized deck for testing, featuring a clickable UI to reveal answers.
* **Local Database:** Uses SQLite to store all vocabulary locally on your machine, requiring no complex server setup.
* **Database Management:** Built-in tools to delete specific words or reset the entire deck.

## 🛠️ Tech Stack

* **Language:** Python 3
* **GUI Framework:** `customtkinter`
* **Database:** `sqlite3`
* **APIs & Libraries:** `requests` (Wiktionary API), `deep-translator` (Google Translate)

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/TakahashiBros/German-Portuguese-Flashcards.git](https://github.com/TakahashiBros/German-Portuguese-Flashcards.git)
   cd German-Portuguese-Flashcards
   ```

2. **Create and activate a virtual environment:**
Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```
macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install the required dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python gui.py
```

## 💡 How It Works

The app uses the official Wikimedia API (https://de.wiktionary.org/w/api.php) to fetch raw JSON data for German words. It parses the plain text extract to isolate the primary definition, handling edge cases (like English words existing in the German dictionary) to ensure only valid German nouns, verbs, and adjectives are saved to the local SQLite database.
