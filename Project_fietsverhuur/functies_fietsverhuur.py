import sqlite3
import datetime

connectdb = sqlite3.connect("fietsverhuur.db")
cursor = connectdb.cursor()

def zoekfunctie(gebruik):
    zoeken = True
    while zoeken == True:
        opties = ["0. id", "1. voornaam", "2. achternaam", "3. adres"]
        print("Keuzemenu:")
        for x in opties:
            print(x)

        keuze_zoeken = input("Welke klantgegevens wilt u " + gebruik + " ? Maak uw keuze uit 0 t/m 3: ")

        if keuze_zoeken.isdigit() == True and int(keuze_zoeken) in range(0, 3):

            optie_zondernr = opties[int(keuze_zoeken)][3:].lower()
            gegevens = input("Geef de " + optie_zondernr + " op waar u op zoekt: ")

            cursor.execute(
                f"""SELECT * 
                FROM klant
                WHERE {optie_zondernr} = '{gegevens}';
                """
            )
            resultaten = cursor.fetchall()
            if resultaten:
                print("Ik heb de volgende gegevens voor u gevonden:")
                for row in resultaten:
                    print(row)

                if len(resultaten) > 1:
                    keuze_klantid = (input("Geef het id van de resultaten die u wilt gebruiken: "))
                    input("Druk op enter om door te gaan.")
                    return keuze_klantid

                else:
                    input("Druk op enter om door te gaan.")

                    return resultaten[0][0]

            else:
                print("Ik heb geen gegevens gevonden op de opgegeven zoekterm.")
                input("Druk op enter om door te gaan.")
                return None

        elif keuze_zoeken.isdigit() == True and int(keuze_zoeken) == 3:
            gegevens_adres = ["straat: ", "huisnummer: ", "postcode: ", "woonplaats: "]
            zoek_op_adres = []

            for gegevens in gegevens_adres:
                zoek_op_adres.append(input(gegevens))

            cursor.execute(
                f"""SELECT *
                FROM klant
                WHERE straat = '{zoek_op_adres[0]}' 
                AND huisnummer = '{zoek_op_adres[1]}' 
                AND postcode = '{zoek_op_adres[2]}' 
                AND woonplaats = '{zoek_op_adres[3]}';"""
            )

            resultaten_adres = cursor.fetchall()

            if resultaten_adres:
                print("Ik heb de volgende gegevens voor u gevonden:")
                for row in resultaten_adres:
                    print(row)
                input("Druk op enter om door te gaan.")
                return resultaten_adres[0][0]
            else:
                print("Ik heb geen gegevens gevonden op het opgegeven adres.")
                input("Druk op enter om door te gaan.")
                return None

        else:
            input("Geen geldige keuze. Druk op enter om terug te gaan naar het hoofdmenu.")
            return None

def vastleggen_klant():# -> return value: nieuwe_klant
    klantenlijst_vraag = ["voornaam: ", "tussenvoegsel: ", "achternaam: ", "straat: ", "huisnummer: ", "postcode: ", "woonplaats: "]
    klantenlijst_data = []

    for gegevens in klantenlijst_vraag:
        klantenlijst_data.append(input(gegevens))

    klantenlijst_vast = (klantenlijst_data)

    cursor.execute(
        """INSERT INTO klant (voornaam, tussenvoegsel, achternaam, straat, huisnummer, postcode, woonplaats)
        VALUES (?, ?, ?, ?, ?, ?, ?)""", klantenlijst_vast
    )

    connectdb.commit()

def wijzigen_klant(): # -> return value: klant
    id_klant = zoekfunctie("opzoeken en aanpassen")
    if id_klant != None:
        keuze_aanpassen = input("Wat wilt u aanpassen: ")
        nieuwe_data = input("Waar wilt u dit naar toe aanpassen: ")

        cursor.execute(
            f"""UPDATE klant
             SET {keuze_aanpassen} = '{nieuwe_data}'
            WHERE id = {int(id_klant)}"""
        )

        connectdb.commit()

        print("Ik heb de gegevens aangepast naar de volgende gegevens:")
        cursor.execute(
            f"""SELECT *
            FROM klant
            WHERE id = {int(id_klant)};"""
        )

        aanpassing = cursor.fetchall()

        print(aanpassing)
        input("Druk op enter om terug naar het menu te gaan.")

def verwijderen_klant(): # -> return value: list_klanten
    id_klant = zoekfunctie("opzoeken en verwijderen")
    if id_klant != None:
        keuze_maken = True
        while keuze_maken == True:
            antwoord = input("Weet u zeker dat u deze gegevens wilt verwijderen? ja/nee ")
            if antwoord == "ja":
                cursor.execute(
                    f"""DELETE FROM klant
                    WHERE id = {int(id_klant)};"""
                )
                connectdb.commit()

                keuze_maken = False
                input("De gegevens zijn verwijderd. Druk op enter om weer terug te gaan naar het hoofdmenu")
            else:
                keuze_maken = False
                input("Druk op enter om weer terug te gaan naar het hoofdmenu")

def toevoegen_fiets(): # -> return value: nieuwe_fiets
    fiets_vraag = ["Merk: ", "Aankoopdatum: "]
    type_vraag = ["Werf naam: ", "model: ", "Elektrisch True/False: ", "Dagprijs: "]
    fiets_data = []
    type_data = []

    for gegevens in fiets_vraag:
        fiets_data.append(input(gegevens))
    for type in type_vraag:
        type_data.append(input(type))
    fiets_data.append(type_data[0])

    fiets_vast = (fiets_data)
    type_vast = (type_data)

    cursor.execute(
        """INSERT INTO type (werf_naam, model, elektrisch, dagprijs)
        VALUES (?, ?, ?, ?)""", type_vast
    )

    cursor.execute(
        """INSERT INTO fiets (merk, aankoopdatum, type_werf_naam)
        VALUES (?, ?, ?)""", fiets_vast
    )

    connectdb.commit()

def vastleggen_contract(): # -> return value:contract
    id_klant = zoekfunctie("voor het contract gebruiken?")

    cursor.execute(
        """SELECT *
        FROM vestiging;"""
    )

    vestigingen = cursor.fetchall()
    lijst_vestiging_id = []

    print("Vestigingen: \n")
    for vestiging in vestigingen:
        print(vestiging)
        lijst_vestiging_id.append(str(vestiging[0]))
    print("\n")

    id_vestiging = input("Geef het id van de vestiging waar de fietsen gehuurd zijn: ")

    if id_vestiging in lijst_vestiging_id:

        contract_datum = input("Wat is de inleverdatum van de fietsen (dag-maand-jaar): ")

        try:
            contract_datum_check = datetime.datetime.strptime(contract_datum, "%d-%m-%Y")

            cursor.execute(
                f"""INSERT INTO contract (klant_id, vestiging_id, inleverdatum)
                VALUES ({id_klant}, {id_vestiging}, '{contract_datum}');"""
            )

            contract_id = cursor.lastrowid
            connectdb.commit()

            fietsen_vastleggen = True

            while fietsen_vastleggen == True:

                cursor.execute(
                    """SELECT *
                    FROM fiets
                    JOIN type
                    ON werf_naam = type_werf_naam"""
                    )

                fietsoverzicht = cursor.fetchall()

                lijst_fiets_id = []

                for fiets in fietsoverzicht:
                    print(fiets)
                    lijst_fiets_id.append(str(fiets[0]))

                fietsnummer = input("Welk fietsnummer is er gehuurd? ")

                if fietsnummer in lijst_fiets_id:

                    cursor.execute(
                        f"""INSERT INTO fiets_per_contract (fietsnummer, contract_id)
                        VALUES ({fietsnummer}, {contract_id});"""
                    )

                    connectdb.commit()

                    fiets_toevoegen = input("Wilt u nog meer fietsen toevoegen aan dit contract? ja/nee ")

                    if fiets_toevoegen == "ja":
                        fietsen_vastleggen = True
                    elif fiets_toevoegen == "nee":
                        print("Het contract is opgesteld.")
                        fietsen_vastleggen = False
                    else:
                        input("Geen geldige keuze, het contract wordt vastgelegd.")
                        fietsen_vastleggen = False
                else:
                    input("Geen geldige keuze, druk op enter om opnieuw te proberen.")
        except ValueError:
            input("Geen geldige keuze, druk op enter om terug te keren naar het hoofdmenu.")
    else:
        input("Geen geldige keuze, druk op enter om terug te keren naar het hoofdmenu.")

def toon_contract(): # -> return value: leeg
    id_klant = zoekfunctie("gebruiken om de contracten van op te zoeken?")
    if id_klant != None:
        cursor.execute(
            f"""SELECT contract.id, klant.voornaam, vestiging.naam, contract.inleverdatum
            FROM contract
            JOIN vestiging
            ON vestiging.id = contract.vestiging_id
            JOIN klant
            ON klant.id = contract.klant_id
            WHERE klant_id = {id_klant}"""
        )

        resultaten = cursor.fetchall()
        lijst_id = []

        print("Contracten:")
        for resultaat in resultaten:
            lijst_id.append(str(resultaat[0]))
            print(resultaat)

        contract_id = input("Geef aub het contract ID waar u een contract van wilt opstellen: ")

        if contract_id in lijst_id:
            cursor.execute(
                f"""SELECT *
                FROM klant
                WHERE id = {id_klant};
                """

            )

        # id, voornaam, tussenvoegsel, achternaam, straat, huisnummer, postcode, woonplaats

            klant_gegevens = cursor.fetchall()

            cursor.execute(
                f"""SELECT *
                FROM vestiging
                JOIN contract
                ON vestiging_id = vestiging.id
                WHERE contract.id = {contract_id};
                """
            )

        # id, naam, telnr, straat, huisnummer, postcode, plaats, contract_id, klant_id, inleverdatum

            contract_gegevens = cursor.fetchall()
            print(contract_gegevens)

            cursor.execute(
                f"""SELECT fiets.fietsnummer, fiets.merk, type.werf_naam, type.model, type.elektrisch, type.dagprijs 
                FROM contract
                JOIN fiets_per_contract
                ON contract.id = fiets_per_contract.contract_id
                JOIN fiets
                ON fiets.fietsnummer = fiets_per_contract.fietsnummer
                JOIN type
                ON fiets.type_werf_naam = type.werf_naam
                WHERE contract.id = {contract_id};
                """
            )

        # fietsnummer, merk, werf_naam, model, elektrisch, dagprijs

            fiets_gegevens = cursor.fetchall()

            print_contract(klant_gegevens, contract_gegevens, fiets_gegevens)
            input("Druk op enter om terug te keren naar het hoofdmenu.")
        else:
            input("Geen geldige keuze, druk op enter om terug te keren naar het hoofdmenu.")

def print_contract(klant_gegevens, contract_gegevens, fiets_gegevens):
    datum = datetime.date.today()
    datetime_vandaag = datetime.datetime.combine(datetime.datetime.today().date(), datetime.datetime.min.time())
    eind_datum = datetime.datetime.strptime(contract_gegevens[0][10], "%m-%d-%Y")
    dagen = (eind_datum - datetime_vandaag).days
    print("\n")
    print(f"{"Datum: "}"
          f"{datum}")
    print(f"{"Contractnr: "}"
          f"{contract_gegevens[0][7]}\n"
          f"{"":<50}{"Vestiging: "}"
          f"{contract_gegevens[0][1]}\n"
          f"{"":<50}{contract_gegevens[0][3]} {contract_gegevens[0][4]}\n"
          f"{"":<50}{contract_gegevens[0][5]} {contract_gegevens[0][6]}")
    print(f"{"Klant: ":<10}"
          f"{klant_gegevens[0][0]:<10}\n"
          f"{"Adres: ":<10}{klant_gegevens[0][4]} {klant_gegevens[0][5]:<10}\n"
          f"{"":<10}{klant_gegevens[0][6]} {klant_gegevens[0][7]:<10}")

    print("\n")

    print(f"{"Startdatum: ":<15}"
          f"{"":<10}{datum.strftime("%d-%m-%y")}\n"
          f"{"Inleverdatum: ":<15}"
          f"{"":<10}{contract_gegevens[0][10]}\n"
          f"{"Aantal dagen: ":<15}"
          f"{"":<10}{dagen}")

    print("\n")

    print("FIETSEN:")
    totaalprijs = 0
    print(f"{"Id:":<10}{"Type:":<10}{"Werfnaam:":<30}{"Model:":<10}{"Elektrisch:":<15}{"Prijs per dag:":<10}")
    for lijst in fiets_gegevens:
        totaalprijs += lijst[5]
        print(f"{lijst[0]:<10}{lijst[1]:<10}{lijst[2]:<30}{lijst[3]:<10}{lijst[4]:<15}{lijst[5]:<10}")
    print(f"{"Totaal: "} {totaalprijs}")
    print("\n")
    print(f"{"Aantal dagen: ":<15}"
          f"{"":<10}{dagen}\n"
          f"{"Prijs per dag: ":<15}"
          f"{"":<10}{totaalprijs}\n"
          f"{"Totaalbedrag: ":<15}"
          f"{"":<10}{dagen * totaalprijs}{" Euro"}")
    print("\n")


def toon_alle_gegevens(): # -> return value: geen
    cursor.execute(
        f"""SELECT *
        FROM klant;
        """
    )
    klant_gegevens = cursor.fetchall()

    cursor.execute(
        f"""SELECT *
            FROM vestiging;
            """
    )
    vestiging_gegevens = cursor.fetchall()

    cursor.execute(
        f"""SELECT *
            FROM contract;
            """
    )
    contract_gegevens = cursor.fetchall()

    cursor.execute(
        f"""SELECT *
            FROM fiets_per_contract;
            """
    )
    fiets_per_contract_gegevens = cursor.fetchall()

    cursor.execute(
        f"""SELECT *
            FROM fiets;
            """
    )
    fiets_gegevens = cursor.fetchall()

    cursor.execute(
        f"""SELECT *
            FROM type;
            """
    )
    type_gegevens = cursor.fetchall()

    lijst_gegevens = [klant_gegevens, vestiging_gegevens, contract_gegevens, fiets_per_contract_gegevens, fiets_gegevens, type_gegevens]
    lijst_gegevens_naam = ["Klant tabel: ", "Vestiging tabel: ", "Contract tabel: ", "Fiets per contract tabel: ", "Fiets tabel: ", "Type tabel: "]

    for x in range(len(lijst_gegevens)):
        print("\n")
        print(lijst_gegevens_naam[x])
        for b in lijst_gegevens[x]:
            print(b)
    print("\n")
    print("Bovenstaand vind u een overzicht van alle gegevens.")
    input("Druk op enter om terug te keren naar het hoofdmenu.")