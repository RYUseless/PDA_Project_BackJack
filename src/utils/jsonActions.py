import os
import json


class Actions:
    def __init__(self):
        self.json_config_name = "config.json"
        self.assets_location = None

    @staticmethod
    def find_json_folder():
        """
        Najde složku 'assets' v projektu PDA_Project_BackJack.
        Pokud neexistuje, pokusí se ji vytvořit ve složce 'src'.
        """
        working_dir = os.getcwd()
        project_name = "PDA_Project_BackJack"
        assets_dir_name = "assets"

        # Najdi kořenový adresář projektu
        while os.path.basename(working_dir) != project_name:
            new_working_dir = os.path.abspath(os.path.join(working_dir, ".."))
            if new_working_dir == working_dir:  # Narazili jsme na kořenový adresář disku
                print(f"Nepodařilo se najít kořenový adresář projektu '{project_name}'.")
                return None
            working_dir = new_working_dir

        # Zkontroluj, zda existuje složka 'assets'
        location_assets = os.path.join(working_dir, assets_dir_name)
        if os.path.exists(location_assets):
            print(f"Složka '{assets_dir_name}' existuje na cestě: {location_assets}")
            return location_assets

        # searching for "assets" folder in "src" source folder
        location_src_assets = os.path.join(working_dir, "src", assets_dir_name)
        if os.path.exists(location_src_assets):
            print(f"Složka '{assets_dir_name}' existuje na cestě: {location_src_assets}")
            return location_src_assets

        # creating folder assets, if not found
        print(f"Složka '{assets_dir_name}' neexistuje. Zkusím ji vytvořit ve složce 'src'...")
        try:
            os.makedirs(location_src_assets, exist_ok=True)
            print(f"Složka '{assets_dir_name}' byla vytvořena na cestě: {location_src_assets}")
            return location_src_assets
        except OSError as e:
            print(f"Chyba při vytváření složky '{assets_dir_name}': {e}")
            return None

    def find_json_config(self):
        if self.assets_location is None:
            self.assets_location = self.find_json_folder()

        # if not successful with finding nor creating assets:
        if self.assets_location is None:
            print("Nelze najít ani vytvořit složku 'assets'. Pokračuji bez konfiguračního souboru.")
            return None

        full_path = os.path.join(self.assets_location, self.json_config_name)
        path_verify = os.path.exists(full_path)
        if not path_verify:
            print("No config file was found, generating default config now...")
            self.write_default_json(self.assets_location)

        return full_path

    def read_config(self, key, value):
        path = self.find_json_config()
        if path is None:
            print("Config file path is missing. Returning default value.")
            return None  # Nebo můžete vrátit výchozí hodnotu
        with open(path, "r") as file:
            jsonData = json.load(file)
        return jsonData[key][value]

    def write_default_json(self, path):
        dictionary = {
            'model_config': {
                "n_episodes": 100_000,
                "learning_rate": 0.01,
                "min_learning_rate": 0.001,
                "lr_decay": 0.95,
                "start_epsilon": 1.0,
                "epsilon_decay": 0.95,
                "final_epsilon": 0.1,
            },
            'number_of_models_trained': {
                "count": 10,
            },
        }
        json_object = json.dumps(dictionary, indent=4)
        try:
            with open(os.path.join(path, self.json_config_name), "w+", encoding='utf-8') as outfile:
                outfile.write(json_object)
        except Exception as e:
            print(f"Chyba při zápisu výchozího konfiguračního souboru: {e}")
