
class MainHelper:
    def __init__(self):
        self.__player_percentage = []
        self.__dealer_percentage = []
        self.__draw_percentage = []

    @staticmethod
    def get_user_input():
        attempts = 0  # Počet pokusů o správný vstup

        while attempts < 3:
            user_input = input("Turn on test loop of 10 training? [y/n]").strip().lower()

            if user_input == 'y':
                return True  # Vstup je 'Y' nebo 'y', vrátí True
            elif user_input == 'n':
                return False  # Vstup je 'N' nebo 'n', vrátí False
            else:
                attempts += 1  # Zvýšíme počet pokusů
                print(f"Neplatný vstup. Pokus {attempts} z 3.")  # Oznámení o neplatném vstupu

        print("Příliš mnoho neplatných pokusů, vizualizace bude vypnuta.")
        return False  # Po třech neplatných pokusech, vrátí False

    def get_run_percentage(self, player_percentage, delaer_percentage, draw_percentage):
        self.__player_percentage.append(player_percentage)
        self.__dealer_percentage.append(delaer_percentage)
        self.__draw_percentage.append(draw_percentage)

    def get_avarage(self):
        print("\n\nVýsledky po 10 runech:")
        # for some random reason my round did not work so i added 2f funny thing, but still kept round for round thingys
        print(
            f"Průměrná procentuální výhra hráče je: {round(sum(self.__player_percentage) / len(self.__player_percentage), 2):.2f}%")

        print(
            f"Průměrná procentuální výhra dealera je: {round(sum(self.__dealer_percentage) / len(self.__dealer_percentage), 2):.2f}%")

        print(f"Průměrná procentuální remíza je: {round(sum(self.__draw_percentage) / len(self.__draw_percentage), 2):.2f}%")

    @staticmethod
    def get_user_input2():
        attempts2 = 0  # Počet pokusů o správný vstup

        while attempts2 < 3:
            print("\n")
            user_input = input("Chcete uložit natrénovaný model? [y/n]").strip().lower()

            if user_input == 'y':
                return True  # Vstup je 'Y' nebo 'y', vrátí True
            elif user_input == 'n':
                return False  # Vstup je 'N' nebo 'n', vrátí False
            else:
                attempts2 += 1  # Zvýšíme počet pokusů
                print(f"Neplatný vstup. Pokus {attempts2} z 3.")  # Oznámení o neplatném vstupu

        print("Příliš mnoho neplatných pokusů. Model nebude uložen.")
        return False  # Po třech neplatných pokusech, vrátí False