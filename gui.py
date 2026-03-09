import customtkinter as ctk
import database
from main import get_translation, get_german_definition

ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")

class FlashcardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("German Flashcards")
        self.geometry("600x550")

        # 1. Create the Tabview Container
        self.tabs = ctk.CTkTabview(self, width=550, height=500)
        self.tabs.pack(padx=20, pady=20)

        # 2. Add the tabs (Now we have 3!)
        self.tabs.add("Add Words")
        self.tabs.add("Study")
        self.tabs.add("Manage")

        # 3. Build the UI inside each tab
        self.build_add_tab()
        self.build_study_tab()
        self.build_manage_tab()

    # ==========================================
    #               ADD WORDS TAB
    # ==========================================
    def build_add_tab(self):
        self.add_title = ctk.CTkLabel(self.tabs.tab("Add Words"), text="Add a New Word", font=("Helvetica", 24, "bold"))
        self.add_title.pack(pady=20)

        self.word_entry = ctk.CTkEntry(self.tabs.tab("Add Words"), placeholder_text="Enter German word...", width=300, height=40)
        self.word_entry.pack(pady=10)

        self.add_button = ctk.CTkButton(self.tabs.tab("Add Words"), text="Fetch & Save", command=self.add_word_action, height=40)
        self.add_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(self.tabs.tab("Add Words"), text="", text_color="gray", wraplength=400)
        self.status_label.pack(pady=20)

    def add_word_action(self):
        word = self.word_entry.get().strip()
        if not word:
            self.status_label.configure(text="Please enter a word!", text_color="red")
            return

        self.status_label.configure(text=f"Fetching data for '{word}'...", text_color="yellow")
        self.update()

        translation = get_translation(word)
        definition = get_german_definition(word)

        if definition.startswith("Error") or definition.startswith("Word not found") or definition.startswith("Could not pinpoint"):
            self.status_label.configure(text=f"Failed: {definition}", text_color="red")
        else:
            database.add_word(word, translation, definition)
            self.status_label.configure(text=f"Success! '{word}' added.", text_color="green")
            self.word_entry.delete(0, 'end')
            self.refresh_manage_dropdown() # Update the dropdown list automatically!

    # ==========================================
    #                 STUDY TAB
    # ==========================================
    def build_study_tab(self):
        self.deck = []
        self.current_card_index = 0

        self.study_title = ctk.CTkLabel(self.tabs.tab("Study"), text="Flashcards", font=("Helvetica", 24, "bold"))
        self.study_title.pack(pady=10)

        self.start_button = ctk.CTkButton(self.tabs.tab("Study"), text="Start / Shuffle Deck", command=self.start_study_session)
        self.start_button.pack(pady=10)

        self.card_frame = ctk.CTkFrame(self.tabs.tab("Study"), width=450, height=250)
        self.card_frame.pack(pady=20)
        self.card_frame.pack_propagate(False) 

        self.german_label = ctk.CTkLabel(self.card_frame, text="Click Start to begin!", font=("Helvetica", 28, "bold"))
        self.german_label.pack(pady=(20, 10))

        # --- THE FIX: Replaced CTkLabel with a scrollable CTkTextbox ---
        self.back_text = ctk.CTkTextbox(self.card_frame, font=("Helvetica", 16), width=400, height=130, 
                                        fg_color="transparent", text_color="white", wrap="word")
        self.back_text.pack(pady=10)
        self.back_text.insert("0.0", "")
        self.back_text.configure(state="disabled") # Make it read-only so you can't type in it
        # ---------------------------------------------------------------

        self.reveal_button = ctk.CTkButton(self.tabs.tab("Study"), text="Reveal Answer", command=self.reveal_card, state="disabled")
        self.reveal_button.pack(pady=5)

        self.next_button = ctk.CTkButton(self.tabs.tab("Study"), text="Next Card", command=self.next_card, state="disabled", fg_color="green", hover_color="darkgreen")
        self.next_button.pack(pady=5)

    def start_study_session(self):
        self.deck = database.get_all_words_shuffled()
        self.current_card_index = 0

        if not self.deck:
            self.german_label.configure(text="Database is empty!")
            return

        self.reveal_button.configure(state="normal")
        self.next_button.configure(state="disabled")
        self.show_current_card()

    def show_current_card(self):
        current_word_data = self.deck[self.current_card_index]
        german_word = current_word_data[0]

        self.german_label.configure(text=german_word)
        
        # Clear the textbox for the new card
        self.back_text.configure(state="normal")
        self.back_text.delete("0.0", "end")
        self.back_text.configure(state="disabled")
        
        self.reveal_button.configure(state="normal")
        self.next_button.configure(state="disabled")

    def reveal_card(self):
        current_word_data = self.deck[self.current_card_index]
        translation = current_word_data[1]
        definition = current_word_data[2]

        answer_text = f"Translation: {translation}\n\nDefinition: {definition}"
        
        # Insert the text into the textbox
        self.back_text.configure(state="normal")
        self.back_text.delete("0.0", "end")
        self.back_text.insert("0.0", answer_text)
        self.back_text.configure(state="disabled")

        self.reveal_button.configure(state="disabled")
        self.next_button.configure(state="normal")

    def next_card(self):
        self.current_card_index += 1

        if self.current_card_index >= len(self.deck):
            self.german_label.configure(text="Deck Finished! 🎉")
            
            # Clear the textbox
            self.back_text.configure(state="normal")
            self.back_text.delete("0.0", "end")
            self.back_text.configure(state="disabled")
            
            self.next_button.configure(state="disabled")
            self.reveal_button.configure(state="disabled")
        else:
            self.show_current_card()

    # ==========================================
    #                MANAGE TAB
    # ==========================================
    def build_manage_tab(self):
        self.manage_title = ctk.CTkLabel(self.tabs.tab("Manage"), text="Manage Database", font=("Helvetica", 24, "bold"))
        self.manage_title.pack(pady=20)

        # -- Delete Single Word Section --
        self.delete_label = ctk.CTkLabel(self.tabs.tab("Manage"), text="Remove a specific word:")
        self.delete_label.pack(pady=(10, 0))

        # A Dropdown menu to select words
        self.word_dropdown = ctk.CTkOptionMenu(self.tabs.tab("Manage"), values=["Loading..."])
        self.word_dropdown.pack(pady=10)

        self.delete_btn = ctk.CTkButton(self.tabs.tab("Manage"), text="Delete Selected Word", command=self.delete_selected_word)
        self.delete_btn.pack(pady=10)

        self.manage_status = ctk.CTkLabel(self.tabs.tab("Manage"), text="", text_color="green")
        self.manage_status.pack(pady=10)

        # -- Reset Entire Database Section --
        self.danger_label = ctk.CTkLabel(self.tabs.tab("Manage"), text="--- DANGER ZONE ---", text_color="red")
        self.danger_label.pack(pady=(40, 5))

        # Red button to indicate a destructive action
        self.reset_btn = ctk.CTkButton(self.tabs.tab("Manage"), text="Reset Entire Database", fg_color="red", hover_color="darkred", command=self.reset_entire_db)
        self.reset_btn.pack(pady=10)

        # Populate the dropdown when the app starts
        self.refresh_manage_dropdown()

    def refresh_manage_dropdown(self):
        words = database.get_all_words()
        if not words:
            words = ["Database is empty"]
            self.delete_btn.configure(state="disabled")
        else:
            self.delete_btn.configure(state="normal")
            
        self.word_dropdown.configure(values=words)
        self.word_dropdown.set(words[0]) # Set the default visible value

    def delete_selected_word(self):
        word_to_delete = self.word_dropdown.get()
        if word_to_delete and word_to_delete != "Database is empty":
            database.delete_word(word_to_delete)
            self.manage_status.configure(text=f"Deleted '{word_to_delete}'", text_color="green")
            self.refresh_manage_dropdown() # Refresh the list so the word disappears

    def reset_entire_db(self):
        database.reset_database()
        self.manage_status.configure(text="Database completely wiped!", text_color="red")
        self.refresh_manage_dropdown()

if __name__ == "__main__":
    database.setup_database()
    app = FlashcardApp()
    app.mainloop()