import os
import json
import xml.etree.ElementTree as ET
import shutil
import time
import xml.dom.minidom


# Funkcja konwertująca plik JSON na format XML
def convert_json_to_xml(json_file, output_folder, processed_folder):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)

        # Sprawdzenie, czy klucz 'FLIGHT' istnieje w danych JSON
        if 'FLIGHT' not in data:
            raise ValueError("Brak klucza 'FLIGHT' w danych JSON")

        root = ET.Element("FLIGHT")

        for key, value in data['FLIGHT'].items():
            # Sprawdzenie, czy wartość nie jest pusta przed dodaniem do pliku XML
            if value != "":
                ET.SubElement(root, key).text = str(value)
            else:
                raise ValueError(f"Wartość dla klucza {key} jest pusta")

        xml_str = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml()

        xml_file = os.path.join(output_folder, os.path.splitext(os.path.basename(json_file))[0] + '.xml')

        with open(xml_file, 'w') as xml_output:
            xml_output.write(xml_str)

        print(f"Plik: {json_file} przekonwertowany poprawnie do formatu XML.")

        # Przeniesienie przetworzonego pliku do folderu przetworzonego
        move_file(json_file, processed_folder)
        print(f"Plik: {json_file} przeniesiony poprawnie do folderu z przetworzonymi danymi")

    except Exception as e:
        # Obsługa błędu w przypadku wystąpienia wyjątku
        print(f"Wystąpił błąd podczas konwertowania pliku {json_file}:", str(e))


# Funkcja przenosząca plik do innego folderu
def move_file(json_file, processed_folder):
    output_file = os.path.join(processed_folder, os.path.basename(json_file))
    # Przeniesienie pliku do folderu przetworzonego
    shutil.move(json_file, output_file)


# Funkcja monitorująca folder wejściowy i wykonująca konwersję
def monitor_folder(input_folder, output_folder, processed_folder):
    try:
        while True:
            # Iteracja przez pliki w folderze wejściowym
            for file in os.listdir(input_folder):
                if file.endswith(".json"):
                    json_file = os.path.join(input_folder, file)
                    # Wywołanie funkcji konwertującej plik JSON na XML
                    convert_json_to_xml(json_file, output_folder, processed_folder)
            # time sleep 3 celem ograniczenia intensywności wykorzystania zasobów procesora (można dostosować)
            time.sleep(3)

    except KeyboardInterrupt:
        # Obsługa przerwania programu przez użytkownika
        print("Program zatrzymany")


if __name__ == "__main__":
    input_folder = "input_folder"
    output_folder = "output_folder"
    processed_folder = "processed_folder"

    # Utworzenie folderów, jeśli nie istnieją
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)

    # Wywołanie funkcji monitorującej folder wejściowy
    monitor_folder(input_folder, output_folder, processed_folder)
