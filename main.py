import os
import json
import xml.etree.ElementTree as ET
import shutil
import time
import xml.dom.minidom


def convert_json_to_xml(json_file, output_folder, processed_folder):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)

        root = ET.Element("FLIGHT")

        for key, value in data['FLIGHT'].items():
            ET.SubElement(root, key).text = str(value)

        xml_str = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml()

        xml_file = os.path.join(output_folder, os.path.splitext(os.path.basename(json_file))[0] + '.xml')

        with open(xml_file, 'w') as xml_output:
            xml_output.write(xml_str)

        print(f"Plik: {json_file} przekonwertowany poprawne do formatu XML.")

        move_file(json_file, processed_folder)
        print(f"Plik: {json_file} przeniesiony poprawnie do folderu z przetworzonymi danymi")

    except Exception as e:
        print(f"Wystąpił błąd podczas konwertowania pliku {json_file}:", str(e))


def move_file(json_file, processed_folder):
    output_file = os.path.join(processed_folder, os.path.basename(json_file))
    shutil.move(json_file, output_file)


def monitor_folder(input_folder, output_folder, processed_folder):
    try:
        while True:
            for file in os.listdir(input_folder):
                if file.endswith(".json"):
                    json_file = os.path.join(input_folder, file)
                    convert_json_to_xml(json_file, output_folder, processed_folder)
            time.sleep(5)

    except KeyboardInterrupt:
        print("Program zatrzymany")


if __name__ == "__main__":
    input_folder = "input_folder"
    output_folder = "output_folder"
    processed_folder = "processed_folder"

    if not os.path.exists(input_folder):
        os.makedirs(input_folder)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if not os.path.exists(processed_folder):
        os.makedirs(processed_folder)

    monitor_folder(input_folder, output_folder, processed_folder)
