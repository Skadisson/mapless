from bin import File, SciKit, Template


def main():
    """TBI: args"""
    source_file_path = 'tmp/source.json'
    demo_file_path = 'tmp/demo.json'
    target_file_path = 'tmp/output.json'
    source_identifier = 'ean'
    demo_identifier = 'Artikelnummer'
    similarity_threshold = 0.3

    file_processor = File.File(source_file_path, demo_file_path, target_file_path)
    source_values, demo_values, source, demo = file_processor.get_paired_source_and_demo_values(source_identifier, demo_identifier)
    scikit_processor = SciKit.SciKit()
    scikit_processor.vectorize(source_values, demo_values)
    io_map_exact, io_map_altered = scikit_processor.create_io_maps(source_values, demo_values, source, demo, similarity_threshold)
    template_processor = Template.Template()
    alter_value_templates = template_processor.build_alter_value_templates(source, demo, io_map_altered, source_identifier, demo_identifier)
    output = template_processor.generate_output(source, io_map_exact, io_map_altered, alter_value_templates)
    file_processor.store_output(output)


if __name__ == "__main__":
    main()
