import tkinter as tk
from tkinter import filedialog, messagebox
import json


class InstagramComparerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram Comparer")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Variabili per i file
        self.followers_file = None
        self.following_file = None

        # UI
        self.create_ui()

    def create_ui(self):
        # Dark mode colors
        bg_color = "#1e1e1e"
        fg_color = "#ffffff"
        primary_color = "#2196f3"  # Blu per i pulsanti e accenti

        self.root.configure(bg=bg_color)

        # Titolo
        title_label = tk.Label(
            self.root,
            text="Instagram Comparer",
            font=("Arial", 20, "bold"),
            bg=bg_color,
            fg=primary_color,
        )
        title_label.pack(pady=10)

        # Pulsanti per caricare i file
        followers_frame = tk.Frame(self.root, bg=bg_color)
        followers_frame.pack(pady=5)
        followers_btn = tk.Button(
            followers_frame,
            text="Importa Followers",
            command=self.load_followers_file,
            bg=primary_color,
            fg="white",
            font=("Arial", 12),
        )
        followers_btn.pack(side=tk.LEFT, padx=5)
        self.followers_label = tk.Label(
            followers_frame,
            text="Nessun file selezionato",
            font=("Arial", 12),
            bg=bg_color,
            fg=fg_color,
        )
        self.followers_label.pack(side=tk.LEFT)

        following_frame = tk.Frame(self.root, bg=bg_color)
        following_frame.pack(pady=5)
        following_btn = tk.Button(
            following_frame,
            text="Importa Following",
            command=self.load_following_file,
            bg=primary_color,
            fg="white",
            font=("Arial", 12),
        )
        following_btn.pack(side=tk.LEFT, padx=5)
        self.following_label = tk.Label(
            following_frame,
            text="Nessun file selezionato",
            font=("Arial", 12),
            bg=bg_color,
            fg=fg_color,
        )
        self.following_label.pack(side=tk.LEFT)

        # Pulsante per confrontare
        compare_btn = tk.Button(
            self.root,
            text="Confronta",
            command=self.compare_files,
            bg=primary_color,
            fg="white",
            font=("Arial", 14),
        )
        compare_btn.pack(pady=20)

        # Area di testo per i risultati
        self.result_text = tk.Text(
            self.root,
            wrap=tk.WORD,
            state=tk.DISABLED,
            height=20,
            width=90,
            bg="#2b2b2b",
            fg=fg_color,
            font=("Arial", 12),
            insertbackground=fg_color,  # Colore del cursore
        )
        self.result_text.pack(pady=10)

    def load_followers_file(self):
        self.followers_file = filedialog.askopenfilename(
            title="Seleziona il file Followers", filetypes=[("JSON Files", "*.json")]
        )
        if self.followers_file:
            self.followers_label.config(
                text=f"{self.followers_file.split('/')[-1]}"
            )
            messagebox.showinfo(
                "File Caricato", f"File Followers caricato:\n{self.followers_file}"
            )

    def load_following_file(self):
        self.following_file = filedialog.askopenfilename(
            title="Seleziona il file Following", filetypes=[("JSON Files", "*.json")]
        )
        if self.following_file:
            self.following_label.config(
                text=f"{self.following_file.split('/')[-1]}"
            )
            messagebox.showinfo(
                "File Caricato", f"File Following caricato:\n{self.following_file}"
            )

    def compare_files(self):
        if not self.followers_file or not self.following_file:
            messagebox.showerror(
                "Errore", "Devi importare entrambi i file prima di confrontarli!"
            )
            return

        try:
            # Carica i dati dai file JSON
            with open(self.followers_file, "r", encoding="utf-8") as f:
                followers_data = json.load(f)

            with open(self.following_file, "r", encoding="utf-8") as f:
                following_data = json.load(f)["relationships_following"]

            # Estrai i valori "value"
            followers = self.extract_values(followers_data)
            following = self.extract_values(following_data)

            # Trova i nomi presenti in "following" ma non in "followers"
            not_following_back = following - followers

            # Mostra i risultati
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)

            # Intestazione con il contatore
            count = len(not_following_back)
            self.result_text.insert(
                tk.END,
                f"\n\n\t\t\t\t UTENTI TROVATI: {count}\n",
                ("header",),
            )
            self.result_text.insert(
                tk.END,
                "\n\tQUESTI UTENTI SONO PRESENTI NELLA LISTA SEGUITI MA NON NELLA LISTA FOLLOWER:\n\n",
            )

            # Lista numerata
            for idx, user in enumerate(not_following_back, start=1):
                self.result_text.insert(tk.END, f" {idx} - {user}\n")

            self.result_text.tag_config("header", font=("Arial", 14, "bold"))
            self.result_text.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Errore", f"Si è verificato un errore:\n{e}")

    @staticmethod
    def extract_values(data, key="string_list_data"):
        values = set()
        for item in data:
            if key in item:
                for sub_item in item[key]:
                    values.add(sub_item["value"])
        return values


if __name__ == "__main__":
    root = tk.Tk()
    app = InstagramComparerApp(root)
    root.mainloop()
