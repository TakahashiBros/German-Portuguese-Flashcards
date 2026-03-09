import requests
from deep_translator import GoogleTranslator
import database

def get_translation(german_word):
    translator = GoogleTranslator(source='de', target='pt')
    translation = translator.translate(german_word)
    return translation

def get_german_definition(german_word):
    url = "https://de.wiktionary.org/w/api.php"
    
    params = {
        "action": "query",
        "prop": "extracts",
        "titles": german_word,
        "format": "json",
        "explaintext": 1
    }
    
    headers = {
        'User-Agent': 'MyGermanFlashcardApp/1.0 (learning@example.com)'
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        pages = data.get("query", {}).get("pages", {})
        page = list(pages.values())[0] 
        
        if page.get("pageid", -1) == -1:
            return "Word not found. (Remember: German nouns must be capitalized!)"
            
        extract = page.get("extract", "")
        lines = extract.split('\n')
        found_bedeutung = False
        
        for line in lines:
            if "Bedeutung" in line:
                found_bedeutung = True
                continue
            
            if found_bedeutung and line.strip().startswith("[1]"):
                return line.strip().replace("[1]", "", 1).strip()
                
        return "Could not pinpoint the exact definition in the API text."
    else:
        return f"Error connecting to the API. Status code: {response.status_code}"

def add_words_mode():
    print("\n--- ADDING NEW WORDS ---")
    print("Type a German word, or 'q' to go back to the menu.")
    
    while True:
        word = input("Enter a word: ").strip()
        
        if word.lower() in ['q', 'quit']:
            break
            
        if not word:
            continue
            
        print(f"Fetching data for '{word}'...")
        translation = get_translation(word)
        definition = get_german_definition(word)
        
        # Our Gatekeeper
        if definition.startswith("Error") or definition.startswith("Word not found") or definition.startswith("Could not pinpoint"):
            print(f"❌ Failed to find '{word}'. Reason: {definition}")
        else:
            database.add_word(word, translation, definition)
            
        print("-" * 40)

def study_mode():
    print("\n" + "="*40)
    print("   STUDY MODE")
    print("="*40)
    
    # 1. Fetch the entire shuffled deck at once
    deck = database.get_all_words_shuffled()
    
    if not deck:
        print("Your database is empty! Add some words first.")
        return # This immediately exits the function and returns to the menu
        
    print(f"You have {len(deck)} words to study. Let's begin!\n")
    
    # 2. Deal the cards out one by one
    for word_data in deck:
        german, portuguese, definition = word_data
        
        print(f"Word: {german}")
        
        user_input = input("\nPress Enter to flip the card (or 'q' to quit)...")
        if user_input.lower() in ['q', 'quit']:
            break
            
        print(f"\nTranslation: {portuguese}")
        print(f"Definition:  {definition}")
        print("-" * 40)
        
        # Pause before the next card
        next_action = input("Press Enter for the next card (or 'q' to quit)...")
        if next_action.lower() in ['q', 'quit']:
            break
        print("\n")
        
    # 3. This prints only after the loop has naturally finished all the cards
    print("\n🎉 You have finished your entire deck! Returning to menu...")

def main():
    database.setup_database()
    
    # The Main Menu Loop
    while True:
        print("\n" + "="*40)
        print("   GERMAN LEARNING APP")
        print("="*40)
        print("1. Add new words")
        print("2. Study flashcards")
        print("3. Quit")
        
        choice = input("Choose an option (1, 2, or 3): ").strip()
        
        if choice == '1':
            add_words_mode()
        elif choice == '2':
            study_mode()
        elif choice == '3':
            print("Auf Wiedersehen! (Goodbye!)")
            break
        else:
            print("Invalid choice. Please type 1, 2, or 3.")

if __name__ == "__main__":
    main()