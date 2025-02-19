from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SciKit:

    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def vectorize(self, input_data, output_data):
        """
        :param list input_data:
        :param list output_data:
        :return:
        """
        self.vectorizer.fit([value for data in input_data + output_data for value in data])

    def create_io_maps(self, input_data, output_data, input_datasets, output_datasets, alter_value_threshold):
        """
        :param list input_data:
        :param list output_data:
        :param list input_datasets:
        :param list output_datasets:
        :param number alter_value_threshold:
        :return:
        """
        io_map_exact = {}
        io_map_altered = {}
        output_properties = list(output_datasets[0].keys())
        input_properties = list(input_datasets[0].keys())

        for i in range(min(len(input_data), len(output_data))):
            for j, output_value in enumerate(output_data[i]):
                for k, input_value in enumerate(input_data[i]):
                    output_property = output_properties[j]
                    input_property = input_properties[k]
                    if input_value == output_value:
                        io_map_exact[output_property] = input_property
                        io_map_altered.pop(output_property, None)
                    else:
                        tfidf_matrix = self.vectorizer.fit_transform([input_value, output_value])
                        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                        if similarity > .0:
                            if similarity == 1.0:
                                io_map_exact[output_property] = input_property
                                if output_property in io_map_altered:
                                    del io_map_altered[output_property]
                            elif similarity > alter_value_threshold and output_property not in io_map_exact:
                                io_map_altered[output_property] = input_property

        return io_map_exact, io_map_altered
