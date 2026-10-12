def welcome() -> None:
    print("Первая попытка запустить проект!")
    print()
    commands_help = (
        "***\n"
        "<command> exit - выйти из программы\n"
        "<command> help - справочная информация"
    )
    print(commands_help)

    while True:
        command = input("Введите команду: ").strip()
        if command == "exit":
            break
        elif command == "help":
            print(commands_help)