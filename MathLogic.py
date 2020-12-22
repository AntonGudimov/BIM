import numpy as np


class MathLogic:

    @staticmethod
    def calculate_mean_and_var_vector_values(vector_list: list, vector_len):
        vector = list()
        mean_vector = list()
        var_vector = list()
        for i in range(vector_len):
            vector.append([])
            for j in range(i, len(vector_list), vector_len):
                vector[i].append(vector_list[j][0])
            mean_vector.append(np.mean(vector[i]))
            var_vector.append(np.var(vector[i]))
        return mean_vector, var_vector

    @staticmethod
    def calculate_mean_value(var_list: dict):
        output = dict()
        for key, val in var_list.items():
            output[key] = np.mean(val)
        return output
