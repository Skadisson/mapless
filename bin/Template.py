import re


class Template:

    def __init__(self):
        """TBI"""

    def build_alter_value_templates(self, source, demo, io_map_altered, source_identifier, demo_identifier):
        alter_value_templates = {}

        for source_ds in source:
            for demo_ds in demo:
                if source_ds[source_identifier] == demo_ds[demo_identifier]:
                    for altered_output_property in io_map_altered:
                        altered_input_property = io_map_altered[altered_output_property]
                        altered_input_value = source_ds[altered_input_property]
                        altered_output_value = demo_ds[altered_output_property]
                        target_numeric_positions, target_numbers = self.positions_of_numeric_characters(altered_output_value)

                        template = altered_output_value
                        i = 0
                        input_numbers = self.numbers_from_string(altered_input_value)
                        for input_number in input_numbers:
                            if input_number in target_numbers:
                                template = template.replace(str(input_number), "{" + str(i) + "}")
                            i += 1
                        alter_value_templates[altered_output_property] = template

        return alter_value_templates

    @staticmethod
    def count_format_variables(template_string):
        return len(re.findall(r'\{[^{}]*\}', template_string))

    def generate_output(self, source, io_map_exact, io_map_altered, alter_value_templates):
        output = []

        for source_ds in source:
            output_ds = {}

            for exact_output_property in io_map_exact:
                output_ds[exact_output_property] = source_ds[io_map_exact[exact_output_property]]

            for altered_output_property in io_map_altered:
                input_value = source_ds[io_map_altered[altered_output_property]]
                input_numbers = self.numbers_from_string(input_value)
                output_variable_count = self.count_format_variables(alter_value_templates[altered_output_property])
                input_variable_count = len(input_numbers)
                if input_variable_count >= output_variable_count:
                    try:
                        output_ds[altered_output_property] = alter_value_templates[altered_output_property].format(*input_numbers)
                    except Exception as e:
                        output_ds[altered_output_property] = ""

            output.append(output_ds)

        return output

    @staticmethod
    def numbers_from_string(string_value):
        return [int(number) for number in re.findall(r'\d+', string_value)]

    @staticmethod
    def positions_of_numeric_characters(string_value):
        target_numbers = [int(number) for number in re.findall(r'\d+', string_value)]
        target_positions = []

        for i, number in enumerate(target_numbers):
            start_position = string_value.find(str(number))
            if start_position != -1:
                target_positions.extend(range(start_position, start_position + len(str(number))))

        target_positions = sorted(set(target_positions))
        return target_positions, target_numbers
