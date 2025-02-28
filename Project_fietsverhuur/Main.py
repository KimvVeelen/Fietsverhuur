import functies_fietsverhuur

quit = False

while quit == False:
    keuze_gebruiker = input("Wat wilt u doen?\n"
                            "1. Klant toevoegen\n"
                            "2. Klant wijzigen\n"
                            "3. Klant verwijderen\n"
                            "4. Klant zoeken\n"
                            "5. Fiets toevoegen\n"
                            "6. Contract opstellen\n"
                            "7. Contract tonen\n"
                            "8. Overzicht alle gegevens\n"
                            "9. Programma beeindigen\n"
                            "\n"
                            "Voer het cijfer in van uw keuze: ")

    if keuze_gebruiker.isdigit() != True and keuze_gebruiker not in range(1, 9):
        print("Maak een keuze uit één van de cijfers uit het menu!\n")

    elif keuze_gebruiker == "1":
        functies_fietsverhuur.vastleggen_klant()

    elif keuze_gebruiker == "2":
        functies_fietsverhuur.wijzigen_klant()

    elif keuze_gebruiker == "3":
        functies_fietsverhuur.verwijderen_klant()

    elif keuze_gebruiker == "4":
        functies_fietsverhuur.zoekfunctie("zoeken")

    elif keuze_gebruiker == "5":
        functies_fietsverhuur.toevoegen_fiets()

    elif keuze_gebruiker == "6":
        functies_fietsverhuur.vastleggen_contract()

    elif keuze_gebruiker == "7":
        functies_fietsverhuur.toon_contract()

    elif keuze_gebruiker == "8":
        functies_fietsverhuur.toon_alle_gegevens()

    elif keuze_gebruiker == "9":
        exit()