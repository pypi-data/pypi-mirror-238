import itertools
import os
import json
import numpy as np


class utils:

    def evaluation_standard_m4(self, data=None):
        if all(element is None for element in data):
            return (False, 1.0)

        non_empty_data = [data_ for data_ in data if data_ is not None]
        if not non_empty_data:
            return (False, 1.0)

        confidence_result = sum(non_empty_data) / len(non_empty_data)

        return (confidence_result > 0.6, confidence_result)

    def evaluation_standard(self, data=None):
        if data is None or not any(data):
            return (False, 1.0)

        non_empty_data = [data_ for data_ in data if len(data_)>0]

        if not non_empty_data:
            return (False, 1.0)

        flat_data = np.concatenate(non_empty_data)

        total_sum = np.sum(flat_data)
        total_count = len(flat_data)

        confidence_result = total_sum / total_count

        return (confidence_result > 0.9, confidence_result)

    def evaluation_standard2(self, data=None):
        if data is None:
            return (False, 1.0)

        non_empty_data = [data_ for data_ in data if len(data_) > 0]

        if not non_empty_data:
            return (False, 1.0)

        confidence = [sum(data_)/len(data_) for data_ in non_empty_data]
        confidence_result = sum(confidence) / len(confidence)
        return (confidence_result>0.9, confidence_result)
    
    def evaluation_standard_body_m4(self, data=None):
        if all(element is None for element in data):
            return (False, 1.0)

        non_empty_data = [data_ for data_ in data if data_ is not None]
        if not non_empty_data:
            return (False, 1.0)

        confidence_result = sum(non_empty_data) / len(non_empty_data)

        return (confidence_result > 0.5, confidence_result)
    
    def evaluation_standard_body(self, data=None):
        if data is None or not any(data):
            return (False, 1.0)

        non_empty_data = [data_ for data_ in data if len(data_)>0]

        if not non_empty_data:
            return (False, 1.0)

        flat_data = np.concatenate(non_empty_data)

        total_sum = np.sum(flat_data)
        total_count = len(flat_data)

        confidence_result = total_sum / total_count

        return (confidence_result > 0.75, confidence_result)
    
    def evaluation_standard_body2(self, data=None):
        if data is None:
            return (False, 1.0)

        non_empty_data = [data_ for data_ in data if len(data_) > 0]

        if not non_empty_data:
            return (False, 1.0)

        confidence = [sum(data_)/len(data_) for data_ in non_empty_data]
        confidence_result = sum(confidence) / len(confidence)
        return (confidence_result>=0.75, confidence_result)


    def generate_combinations_evaluations(self, N=None, data=None):
        
        if N is None or data is None:
            return None

        filtered_data_started = [
            item['state_value']
            for item in data[0]
            if item.get('rule_match', False)
        ]

      
        filtered_data_finish = [
            item['state_value']
            for item in data[(len(data)-1)]
            if item.get('rule_match', False)
        ]
        
        if (not filtered_data_started or not filtered_data_finish) or (len(filtered_data_started)==0 or len(filtered_data_finish)==0):
            return None

        flattened_set = {
            item['state_value']
            for sublist in data
            for item in sublist
            if item.get('rule_match', False)
        }

        combinations = itertools.permutations(flattened_set, N)
        combinations = [list(perm) for perm in combinations if perm[0] in filtered_data_started]
        combinations = [list(perm) for perm in combinations if perm[(len(perm)-1)] in filtered_data_finish]
        return combinations
    

    def collect_simple_data(self, general=None, path=None):
        if general is None and path is None:
            return None
        
        label = general['label']
        data= []
        for num in range(general['countTraining']):
            try:
                path_ = f"{path}\\{label}\\{label}{num}.json"
                if os.path.exists(path_):
                    f = open(path_)
                    data.append(json.load(f))
                else:
                    path_ = path_.replace("\\", "|").replace("|", "/")
                    if os.path.exists(path_):
                        f = open(path_)
                        data.append(json.load(f))
            except Exception as e:
                print(f"Error Ocurrido, Mensaje: Entrenamiento Invalido, verifique la data de entrenamiento de la letra:[{label}]")
                return None
        return data
    
    def collect_movement_data(self, general=None, path=None):
        if general is None and path is None:
            return None
        
        data = []

        for idx, state_ in enumerate(general):
            label = state_['label']
            state = state_['state']
            dataTmp = []
            for num in range(state_['countTraining']):
                try:
                    path_ = f"{path}\\{label}\\{state}\\{label}{num}.json"
                    if os.path.exists(path_):
                        f = open(path_)
                        dataTmp.append(json.load(f))
                    else:
                        path_ = path_.replace("\\", "|").replace("|", "/")
                        if os.path.exists(path_):
                            f = open(path_)
                            data.append(json.load(f))
                except Exception as e:
                    print(f"Error Ocurrido, Mensaje: Entrenamiento Invalido, verifique la data de entrenamiento de la letra:[{label}] - state:[{state}]")
                    return None
                
            data.append(dataTmp)

        return data