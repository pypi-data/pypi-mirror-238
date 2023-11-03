from database import firebase


def main():
    print("Benvenuto! Inserisci il tuo nome utente per incrementare il contatore delle visite.")
    username = input("Nome Utente: ")
    firebase.initialize_firebase()
    if firebase.increment_counter(username):
        print(f"Contatore delle visite per {username} è stato incrementato con successo {firebase.get_counter(username)}")

    else:
        print(f"Errore durante l'incremento del contatore per {username}.")


if __name__ == "__main__":
    main()