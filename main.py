while True:
    choice = input("1 = serveur / 2 = client : ").strip()
    if choice == "1":
        import core.server
        break
    elif choice == "2":
        import core.client
        break
    else:
        print("Choix invalide. Veuillez entrer 1 ou 2.")
