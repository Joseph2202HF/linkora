choice = input("1 = serveur / 2 = client : ")

if choice == "1":
    import core.server
elif choice == "2":
    import core.client
