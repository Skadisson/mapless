import json


class File:

    def __init__(self, source_file_path, demo_file_path, target_file_path):
        """
        :param string source_file_path:
        :param string demo_file_path:
        :param string target_file_path:
        """
        self.source_file_path = source_file_path
        self.demo_file_path = demo_file_path
        self.target_file_path = target_file_path

    def get_paired_source_and_demo_values(self, source_id_property, demo_id_property):
        """
        :param string source_id_property:
        :param string demo_id_property:
        :return: tuple A tuple of two lists containing source and demo values.
        """
        source = self.read_json_file(self.source_file_path)
        demo = self.read_json_file(self.demo_file_path)
        source_data = [list(source_ds.values()) for source_ds in source for demo_ds in demo if source_ds[source_id_property] == demo_ds[demo_id_property]]
        demo_data = [list(demo_ds.values()) for source_ds in source for demo_ds in demo if source_ds[source_id_property] == demo_ds[demo_id_property]]
        source_data = self.stringify_values(source_data)
        demo_data = self.stringify_values(demo_data)
        return source_data, demo_data, source, demo

    @staticmethod
    def read_json_file(file_path):
        """
        :param string file_path:
        :return: list A list of dictionaries deriving from a JSON file.
        """
        with open(file_path, 'r', encoding='utf-8') as source_file:
            source = json.load(source_file)
            if len(source) <= 0:
                print(f"{file_path} is empty or unreadable")
                exit()
        return source

    def store_output(self, output):
        with open(self.target_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(output, output_file)

    @staticmethod
    def stringify_values(values):
        """
        :param values:
        :return:
        """
        stringified = []
        for words in values:
            stringify = []
            for word in words:
                string_word = str(word)
                if string_word != '':
                    stringify.append(string_word)
            stringified.append(stringify)
        return stringified
