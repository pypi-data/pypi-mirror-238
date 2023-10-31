from signlanguage.interfaces.interfaces_model    import Imodel
import signlanguage.models.handmodel_classV2       as hm
import numpy                        as np
import pandas                       as pd
import asyncio
import time

HANDMODEL_LENGHT= 51
#HAND
HAND_RELATION_EVALUATION_VALUES = {0, 1, 2}
HAND_EVALUATION_VALUES = {3, 4, 5, 6, 7, 8}
#FACE
FACE_EVALUATION_VALUES = {39, 40, 41, 42, 43, 44}
FACE_DIFF_RELATION_EVALUATION_VALUES = {45, 46, 47, 48, 49, 50}
#BODY
BODY_RELATION_EVALUATION_VALUES = {12, 13, 14}
BODY_EVALUATION_VALUES = {15, 16, 17, 18, 19, 20}
BODY_DIFF_RELATION_EVALUATION_VALUES = {21, 22, 23, 24, 25, 26}
BODY_FACE_EVALUATION_VALUES = {27, 28, 29, 30, 31, 32}
BODY_FACE_DIFF_RELATION_EVALUATION_VALUES = {33, 34, 35, 36, 37, 38}

class ExecutionModelPool(Imodel):
    def transform_dataEvaluation_m4(self, data_model=None):
        if data_model is None:
            return [[] for _ in range(HANDMODEL_LENGHT)]
        
        data_evaluation = [[] for _ in range(HANDMODEL_LENGHT)]
        
        for i, value in enumerate(data_model):
            if len(value) > 0:
                if len(data_evaluation[i]) != len(value):
                    data_evaluation[i] = [[] for _ in range(len(value))]
                
                for j, val_pos in enumerate(value):
                    data_evaluation[i][j].append(val_pos[0])
        
        return data_evaluation
    
    def transform_dataEvaluation(self, data_model=None):
        if data_model is None:
            return None
        
        data_evaluation = [[] for _ in range(HANDMODEL_LENGHT)]

        for i in range(len(data_model)):
            value = data_model[i]
            if value:
                if len(data_evaluation[i]) != len(value):
                    data_evaluation[i] = value[:]
                else:
                    data_evaluation[i] = value[:]
        
        """
        data_evaluation = [[] for _ in range(54)]
        for i, value in enumerate(data_model):
            if len(value) > 0:
                if not len(data_evaluation[i]) == len(value):
                    data_evaluation[i] = [[] for _ in range(len(value))]

                for j, val_pos in enumerate(value):
                    data_evaluation[i][j].extend([val_pos])
        """
        
        return data_evaluation

    #model3
    async def evaluation_async(self, model_evaluation=None, data=None, face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False):
        try:
            if None in (model_evaluation, data):
                return None
            
            results = None
            ##evaluation_model
            if not (face_relation or body_relation):
                results = await self.hand_evaluation_async(model_evaluation=model_evaluation, data=data, face_relation=face_relation, body_relation=body_relation, hand_relation=hand_relation, hand_diff_relation=hand_diff_relation)      

            elif face_relation and not body_relation:
                results = await self.face_evaluation_async(model_evaluation=model_evaluation, data=data, face_relation=face_relation, body_relation=body_relation, hand_relation=hand_relation, hand_diff_relation=hand_diff_relation)         
            
            elif body_relation:
                results = await self.body_evaluation_async(model_evaluation=model_evaluation, data=data, face_relation=face_relation, body_relation=body_relation, hand_relation=hand_relation, hand_diff_relation=hand_diff_relation)
            ##results_recog
            return results
            
        except Exception as e:
            print("Error Ocurrido [Model Exec], Mensaje: {0}".format(str(e)))
            return None
        
    ## Evalua los puntos de interseccion de las manos especificas, para reconocer unicamente movimiento de mano
    async def hand_evaluation_async(self, model_evaluation=None, data=None, face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False):

        if None in (model_evaluation, data):
            return None
        
        defined_index = {i for i, model in enumerate(model_evaluation) if len(model) > 0}
        defined_intersection = list(defined_index.intersection(HAND_EVALUATION_VALUES))
        
        if len(defined_intersection) not in(3, 6):
            return None

        matrix_evaluation = [[] for _ in range(54)]
        
        #construct model data evaluation -- transform data evaluation
        data_model = hm.HandModel().make_model(
            hand_Left=data['model_hand_Left'],
            hand_Right=data['model_hand_Right'],
            points_body=data['model_body'],
            face_relation=face_relation,
            body_relation=body_relation,
            hand_relation=hand_relation,
            hand_diff_relation=hand_diff_relation
        )
        data_evaluation = self.transform_dataEvaluation(data_model=data_model)

        for idx in defined_intersection:
            evaluation_data  = data_evaluation[idx]
            evaluation_model = model_evaluation[idx]

            tasks = []
            for i, evaluation_pos in enumerate(evaluation_data):
                if len(evaluation_pos) == 0 and evaluation_model[i] is None:
                    return None
                
                #configure values
                data = np.array(evaluation_pos).T
                df_real = pd.DataFrame(data).transpose()

                #get core pool
                tasks.append(evaluation_model[i].predict_min_async(df_real))
            
            results = await asyncio.gather(*tasks)
            matrix_evaluation[idx].extend(results)

        if hand_relation:

            defined_intersection = list(defined_index.intersection(HAND_RELATION_EVALUATION_VALUES))

            if len(defined_intersection) != 3:
                return None
            
            for idx in defined_intersection:
                evaluation_data  = data_evaluation[idx]
                evaluation_model = model_evaluation[idx]

                tasks = []
                for i, evaluation_pos in enumerate(evaluation_data):
                    if len(evaluation_pos) <= 0 and evaluation_model[i] is None:
                        return None
                    
                    #configure values
                    data = np.array(evaluation_pos).T
                    df_real = pd.DataFrame(data).transpose()

                    #get core pool
                    tasks.append(evaluation_model[i].predict_min_async(df_real))

                results = await asyncio.gather(*tasks)
                matrix_evaluation[idx].extend(results)

        return matrix_evaluation
    
    ## Evalua los puntos de interseccion de la cara-mano especificos, para reconocer relaciones definidas
    async def face_evaluation_async(self, model_evaluation=None, data=None, face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False):
        
        if None in (model_evaluation, data) or not face_relation:
            return None
        
        # evaluate hand vals
        matrix_evaluation = await self.hand_evaluation_async(model_evaluation=model_evaluation, data=data, face_relation=face_relation, body_relation=body_relation, hand_relation=hand_relation)

        if matrix_evaluation is None or len(matrix_evaluation) != 54:
            return None

        #pre evaluation model, defined
        defined_index = {i for i, model in enumerate(model_evaluation) if len(model) > 0}
        defined_intersection = list(defined_index.intersection(FACE_EVALUATION_VALUES))

        if len(defined_intersection) not in(3, 6):
            return None

        #construct model data evaluation -- transform data evaluation
        data_model = hm.HandModel().make_model(
            hand_Left=data['model_hand_Left'],
            hand_Right=data['model_hand_Right'],
            points_body=data['model_body'],
            face_relation=face_relation,
            body_relation=body_relation,
            hand_relation=hand_relation,
            hand_diff_relation=hand_diff_relation
        )
        data_evaluation = self.transform_dataEvaluation(data_model=data_model)

        
        for idx in defined_intersection:
            evaluation_data  = data_evaluation[idx]
            evaluation_model = model_evaluation[idx]

            tasks = []
            for i, evaluation_pos in enumerate(evaluation_data):
                if len(evaluation_pos) <= 0 and evaluation_model[i] is None:
                    return None
                
                #configure values
                data = np.array(evaluation_pos).T
                df_real = pd.DataFrame(data).transpose()

                #get core pool
                tasks.append(evaluation_model[i].predict_min_async(df_real))
            results = await asyncio.gather(*tasks)
            matrix_evaluation[idx].extend(results)
        

        if hand_diff_relation:
            
            defined_intersection = list(defined_index.intersection(FACE_DIFF_RELATION_EVALUATION_VALUES))

            if len(defined_intersection) not in(3, 6):
                return None

            for idx in defined_intersection:
                evaluation_data  = data_evaluation[idx]
                evaluation_model = model_evaluation[idx]

                tasks = []
                for i, evaluation_pos in enumerate(evaluation_data):
                    if len(evaluation_pos) <= 0 and evaluation_model[i] is None:
                        return None
                    
                    #configure values
                    data = np.array(evaluation_pos).T
                    df_real = pd.DataFrame(data).transpose()

                    #get core pool
                    tasks.append(evaluation_model[i].predict_min_async(df_real))
                results = await asyncio.gather(*tasks)
                matrix_evaluation[idx].extend(results)


        return matrix_evaluation
      
    ## Evalua los puntos de interseccion del cuerpo en general
    async def body_evaluation_async(self, model_evaluation=None, data=None, face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False):
        if None in (model_evaluation, data) or not body_relation:
            return None
        
        matrix_evaluation = await self.hand_evaluation_async(model_evaluation=model_evaluation, data=data, face_relation=face_relation, body_relation=body_relation, hand_relation=hand_relation)

        if matrix_evaluation is None or len(matrix_evaluation) != 54:
            return None

        #pre evaluation model, defined
        defined_index = {i for i, model in enumerate(model_evaluation) if len(model) > 0}
        defined_intersection = list(defined_index.intersection(BODY_EVALUATION_VALUES))

        if len(defined_intersection) not in(3, 6):
            return None
        
        #transform data evaluation
        data_model = hm.HandModel().make_model(
            hand_Left=data['model_hand_Left'],
            hand_Right=data['model_hand_Right'],
            points_body=data['model_body'],
            face_relation=face_relation,
            body_relation=body_relation,
            hand_relation=hand_relation,
            hand_diff_relation=hand_diff_relation
        )
        data_evaluation = self.transform_dataEvaluation(data_model=data_model)

        
        for idx in defined_intersection:
            evaluation_data  = data_evaluation[idx]
            evaluation_model = model_evaluation[idx]

            tasks = []
            for i, evaluation_pos in enumerate(evaluation_data):
                if len(evaluation_pos) <= 0 and evaluation_model[i] is None:
                    return None
                
                #configure values
                data = np.array(evaluation_pos).T
                df_real = pd.DataFrame(data).transpose()

                #get core pool
                tasks.append(evaluation_model[i].predict_min_async(df_real))
            results = await asyncio.gather(*tasks)
            matrix_evaluation[idx].extend(results)

            
        if hand_relation:

            defined_intersection = list(defined_index.intersection(BODY_RELATION_EVALUATION_VALUES))

            if len(defined_intersection) != 3:
                return None
            
            for idx in defined_intersection:
                evaluation_data  = data_evaluation[idx]
                evaluation_model = model_evaluation[idx]

                tasks = []
                for i, evaluation_pos in enumerate(evaluation_data):
                    if len(evaluation_pos) <= 0 and evaluation_model[i] is None:
                        return None
                    
                    #configure values
                    data = np.array(evaluation_pos).T
                    df_real = pd.DataFrame(data).transpose()

                    #get core pool
                    tasks.append(evaluation_model[i].predict_min_async(df_real))
                results = await asyncio.gather(*tasks)
                matrix_evaluation[idx].extend(results)
            
        if hand_diff_relation:
            
            defined_intersection = list(defined_index.intersection(BODY_DIFF_RELATION_EVALUATION_VALUES))
            
            if len(defined_intersection) not in(3, 6):
                return None
            
            for idx in defined_intersection:
                evaluation_data  = data_evaluation[idx]
                evaluation_model = model_evaluation[idx]

                tasks = []
                for i, evaluation_pos in enumerate(evaluation_data):
                    if len(evaluation_pos) <= 0 and evaluation_model[i] is None:
                        return None
                    
                    #configure values
                    data = np.array(evaluation_pos).T
                    df_real = pd.DataFrame(data).transpose()

                    #get core pool
                    tasks.append(evaluation_model[i].predict_min_async(df_real))
                results = await asyncio.gather(*tasks)
                matrix_evaluation[idx].extend(results)

        if face_relation:
            
            defined_intersection = list(defined_index.intersection(BODY_FACE_EVALUATION_VALUES))

            if len(defined_intersection) not in(3, 6):
                return None
            
            for idx in defined_intersection:
                evaluation_data  = data_evaluation[idx]
                evaluation_model = model_evaluation[idx]

                tasks = []
                for i, evaluation_pos in enumerate(evaluation_data):
                    if len(evaluation_pos) <= 0 and evaluation_model[i] is None:
                        return None
                    
                    #configure values
                    data = np.array(evaluation_pos).T
                    df_real = pd.DataFrame(data).transpose()

                    #get core pool
                    tasks.append(evaluation_model[i].predict_min_async(df_real))
                results = await asyncio.gather(*tasks)
                matrix_evaluation[idx].extend(results)

            if hand_diff_relation:
                
                defined_intersection = list(defined_index.intersection(BODY_FACE_DIFF_RELATION_EVALUATION_VALUES))

                if len(defined_intersection) not in(3, 6):
                    return None
            
                for idx in defined_intersection:
                    evaluation_data  = data_evaluation[idx]
                    evaluation_model = model_evaluation[idx]

                    tasks = []
                    for i, evaluation_pos in enumerate(evaluation_data):
                        if len(evaluation_pos) <= 0 and evaluation_model[i] is None:
                            return None
                        
                        #configure values
                        data = np.array(evaluation_pos).T
                        df_real = pd.DataFrame(data).transpose()

                        #get core pool
                        tasks.append(evaluation_model[i].predict_min_async(df_real))
                    results = await asyncio.gather(*tasks)
                    matrix_evaluation[idx].extend(results)
        
        return matrix_evaluation
    

    # -------------------------------------------------------------------------------
    #model4
    async def evaluation_async2(self, model_evaluation=None, data=None, face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False):
        try:
            if None in (model_evaluation, data):
                return None
            
            results = None
            ##evaluation_model
            if not (face_relation or body_relation):
                results = await self.hand_evaluation_async2(model_evaluation=model_evaluation, data=data, face_relation=face_relation, body_relation=body_relation, hand_relation=hand_relation, hand_diff_relation=hand_diff_relation)      

            elif face_relation and not body_relation:
                results = await self.face_evaluation_async2(model_evaluation=model_evaluation, data=data, face_relation=face_relation, body_relation=body_relation, hand_relation=hand_relation, hand_diff_relation=hand_diff_relation)         
            
            elif body_relation:
                results = await self.body_evaluation_async2(model_evaluation=model_evaluation, data=data, face_relation=face_relation, body_relation=body_relation, hand_relation=hand_relation, hand_diff_relation=hand_diff_relation)
            ##results_recog
            return results
            
        except Exception as e:
            print("Error Ocurrido [Model Exec], Mensaje: {0}".format(str(e)))
            return None
    
    async def execute_operations_async(idx, evaluation_data, evaluation_model, matrix_evaluation):
        tasks = []
        for i, evaluation_pos in enumerate(evaluation_data):
            if len(evaluation_pos) <= 0 and evaluation_model[i] is None:
                return None
                
            # Configure values
            data = np.array(evaluation_pos).T
            df_real = pd.DataFrame(data).transpose()

            # Get core pool
            tasks.append(evaluation_model[i].predict_min_async(df_real))

        results = await asyncio.gather(*tasks)
        matrix_evaluation[idx].extend(results)
    ## Evalua los puntos de interseccion de las manos especificas, para reconocer unicamente movimiento de mano
    async def hand_evaluation_async2(self, model_evaluation=None, data=None, face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False):

        if None in (model_evaluation, data):
            return None
        
        defined_index = {i for i, model in enumerate(model_evaluation) if model is not None}
        defined_intersection = list(defined_index.intersection(HAND_EVALUATION_VALUES))
        
        if len(defined_intersection) not in(3, 6):
            return None

        matrix_evaluation = [None] * HANDMODEL_LENGHT
        
        #construct model data evaluation -- transform data evaluation
        data_model = hm.HandModel().make_model(
            hand_Left=data['model_hand_Left'],
            hand_Right=data['model_hand_Right'],
            points_body=data['model_body'],
            face_relation=face_relation,
            body_relation=body_relation,
            hand_relation=hand_relation,
            hand_diff_relation=hand_diff_relation
        )
        data_evaluation = self.transform_dataEvaluation_m4(data_model=data_model)

        """
        tasks = []
        for idx in defined_intersection:
            evaluation_data = data_evaluation[idx]
            evaluation_model = model_evaluation[idx]
            tasks.append(self.execute_operations_async(idx, evaluation_data, evaluation_model, matrix_evaluation))

        await asyncio.gather(*tasks)
        
        """
        tasks = []
        flag_writter = True
        for idx in defined_intersection:
            if len(data_evaluation[idx]) == 0 or (model_evaluation[idx] is None or data_evaluation[idx] is None):
                flag_writter = False
                break
            evaluation_data  = data_evaluation[idx]
            evaluation_model = model_evaluation[idx]

            df = pd.DataFrame(evaluation_data, columns=[str(i) for i in range(len(evaluation_data[0]))]).transpose()
            data_eval = df.to_numpy()
            tasks.append(evaluation_model.predict_min_async(data_eval))
        
        results = await asyncio.gather(*tasks)
        for i,idx in enumerate(defined_intersection):
            if len(results) < (i+1):
                break
            matrix_evaluation[idx] = results[i]
        
        if not flag_writter:
            return None

        if hand_relation:

            defined_intersection = list(defined_index.intersection(HAND_RELATION_EVALUATION_VALUES))

            if len(defined_intersection) != 3:
                return None
            
            tasks = []
            flag_writter = True
            for idx in defined_intersection:
                if len(data_evaluation[idx]) == 0 or (model_evaluation[idx] is None or data_evaluation[idx] is None):
                    flag_writter = False
                    break
                evaluation_data  = data_evaluation[idx]
                evaluation_model = model_evaluation[idx]

                df = pd.DataFrame(evaluation_data, columns=[str(i) for i in range(len(evaluation_data[0]))]).transpose()
                data_eval = df.to_numpy()
                tasks.append(evaluation_model.predict_min_async(data_eval))
            
            results = await asyncio.gather(*tasks)
            for i,idx in enumerate(defined_intersection):
                if len(results) < (i+1):
                    break
                matrix_evaluation[idx] = results[i]
            
            if not flag_writter:
                return None

        return matrix_evaluation
    
    ## Evalua los puntos de interseccion de la cara-mano especificos, para reconocer relaciones definidas
    async def face_evaluation_async2(self, model_evaluation=None, data=None, face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False):
        
        if None in (model_evaluation, data) or not face_relation:
            return None
        
        # evaluate hand vals
        matrix_evaluation = await self.hand_evaluation_async2(model_evaluation=model_evaluation, data=data, face_relation=face_relation, body_relation=body_relation, hand_relation=hand_relation)

        if matrix_evaluation is None:
            return None

        if all(element is None for element in matrix_evaluation) or len(matrix_evaluation) != HANDMODEL_LENGHT:
            return None

        #pre evaluation model, defined
        defined_index = {i for i, model in enumerate(model_evaluation) if model is not None}
        defined_intersection = list(defined_index.intersection(FACE_EVALUATION_VALUES))

        if len(defined_intersection) not in(3, 6):
            return None

        #construct model data evaluation -- transform data evaluation
        data_model = hm.HandModel().make_model(
            hand_Left=data['model_hand_Left'],
            hand_Right=data['model_hand_Right'],
            points_body=data['model_body'],
            face_relation=face_relation,
            body_relation=body_relation,
            hand_relation=hand_relation,
            hand_diff_relation=hand_diff_relation
        )
        data_evaluation = self.transform_dataEvaluation_m4(data_model=data_model)

        
        tasks = []
        flag_writter = True
        for idx in defined_intersection:
            if len(data_evaluation[idx]) == 0 or model_evaluation[idx] is None:
                flag_writter = False
                break
            evaluation_data  = data_evaluation[idx]
            evaluation_model = model_evaluation[idx]

            df = pd.DataFrame(evaluation_data, columns=[str(i) for i in range(len(evaluation_data[0]))]).transpose()
            data_eval = df.to_numpy()
            tasks.append(evaluation_model.predict_min_async(data_eval))
        
        results = await asyncio.gather(*tasks)
        for i,idx in enumerate(defined_intersection):
            if len(results) < (i+1):
                break
            matrix_evaluation[idx] = results[i]
        
        if not flag_writter:
            return None
        

        if hand_diff_relation:
            
            defined_intersection = list(defined_index.intersection(FACE_DIFF_RELATION_EVALUATION_VALUES))

            if len(defined_intersection) not in(3, 6):
                return None

            tasks = []
            flag_writter = True
            for idx in defined_intersection:
                if len(data_evaluation[idx]) == 0 or model_evaluation[idx] is None:
                    flag_writter = False
                    break
                evaluation_data  = data_evaluation[idx]
                evaluation_model = model_evaluation[idx]

                df = pd.DataFrame(evaluation_data, columns=[str(i) for i in range(len(evaluation_data[0]))]).transpose()
                data_eval = df.to_numpy()
                tasks.append(evaluation_model.predict_min_async(data_eval))
            
            results = await asyncio.gather(*tasks)
            for i,idx in enumerate(defined_intersection):
                if len(results) < (i+1):
                    break
                matrix_evaluation[idx] = results[i]
            
            if not flag_writter:
                return None


        return matrix_evaluation
      
    ## Evalua los puntos de interseccion del cuerpo en general
    async def body_evaluation_async2(self, model_evaluation=None, data=None, face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False):
        if None in (model_evaluation, data) or not body_relation:
            return None
        
        matrix_evaluation = await self.hand_evaluation_async2(model_evaluation=model_evaluation, data=data, face_relation=face_relation, body_relation=body_relation, hand_relation=hand_relation)
        
        if matrix_evaluation is None:
            return None

        if all(element is None for element in matrix_evaluation) or len(matrix_evaluation) != HANDMODEL_LENGHT:
            return None

        #pre evaluation model, defined
        defined_index = {i for i, model in enumerate(model_evaluation) if model is not None}
        defined_intersection = list(defined_index.intersection(BODY_EVALUATION_VALUES))

        if len(defined_intersection) not in(3, 6):
            return None
        
        #transform data evaluation
        data_model = hm.HandModel().make_model(
            hand_Left=data['model_hand_Left'],
            hand_Right=data['model_hand_Right'],
            points_body=data['model_body'],
            face_relation=face_relation,
            body_relation=body_relation,
            hand_relation=hand_relation,
            hand_diff_relation=hand_diff_relation
        )
        data_evaluation = self.transform_dataEvaluation_m4(data_model=data_model)

        
        tasks = []
        flag_writter = True
        for idx in defined_intersection:
            if len(data_evaluation[idx]) == 0 or model_evaluation[idx] is None:
                flag_writter = False
                break
            evaluation_data  = data_evaluation[idx]
            evaluation_model = model_evaluation[idx]

            df = pd.DataFrame(evaluation_data, columns=[str(i) for i in range(len(evaluation_data[0]))]).transpose()
            data_eval = df.to_numpy()
            tasks.append(evaluation_model.predict_min_async(data_eval))
        
        results = await asyncio.gather(*tasks)
        for i,idx in enumerate(defined_intersection):
            if len(results) < (i+1):
                break
            matrix_evaluation[idx] = results[i]
        
        if not flag_writter:
            return None

            
        if hand_relation:

            defined_intersection = list(defined_index.intersection(BODY_RELATION_EVALUATION_VALUES))

            if len(defined_intersection) != 3:
                return None
            
            tasks = []
            flag_writter = True
            for idx in defined_intersection:
                if len(data_evaluation[idx]) == 0 or model_evaluation[idx] is None:
                    flag_writter = False
                    break
                evaluation_data  = data_evaluation[idx]
                evaluation_model = model_evaluation[idx]

                df = pd.DataFrame(evaluation_data, columns=[str(i) for i in range(len(evaluation_data[0]))]).transpose()
                data_eval = df.to_numpy()
                tasks.append(evaluation_model.predict_min_async(data_eval))
            
            results = await asyncio.gather(*tasks)
            for i,idx in enumerate(defined_intersection):
                if len(results) < (i+1):
                    break
                matrix_evaluation[idx] = results[i]
            
            if not flag_writter:
                return None
            
        if hand_diff_relation:
            
            defined_intersection = list(defined_index.intersection(BODY_DIFF_RELATION_EVALUATION_VALUES))
            
            if len(defined_intersection) not in(3, 6):
                return None
            
            tasks = []
            flag_writter = True
            for idx in defined_intersection:
                if len(data_evaluation[idx]) == 0 or model_evaluation[idx] is None:
                    flag_writter = False
                    break
                evaluation_data  = data_evaluation[idx]
                evaluation_model = model_evaluation[idx]

                df = pd.DataFrame(evaluation_data, columns=[str(i) for i in range(len(evaluation_data[0]))]).transpose()
                data_eval = df.to_numpy()
                tasks.append(evaluation_model.predict_min_async(data_eval))
            
            results = await asyncio.gather(*tasks)
            for i,idx in enumerate(defined_intersection):
                if len(results) < (i+1):
                    break
                matrix_evaluation[idx] = results[i]
            
            if not flag_writter:
                return None

        if face_relation:
            
            defined_intersection = list(defined_index.intersection(BODY_FACE_EVALUATION_VALUES))

            if len(defined_intersection) not in(3, 6):
                return None
            
            tasks = []
            flag_writter = True
            for idx in defined_intersection:
                if len(data_evaluation[idx]) == 0 or model_evaluation[idx] is None:
                    flag_writter = False
                    break
                evaluation_data  = data_evaluation[idx]
                evaluation_model = model_evaluation[idx]

                df = pd.DataFrame(evaluation_data, columns=[str(i) for i in range(len(evaluation_data[0]))]).transpose()
                data_eval = df.to_numpy()
                tasks.append(evaluation_model.predict_min_async(data_eval))
            
            results = await asyncio.gather(*tasks)
            for i,idx in enumerate(defined_intersection):
                if len(results) < (i+1):
                    break
                matrix_evaluation[idx] = results[i]
            
            if not flag_writter:
                return None

            if hand_diff_relation:
                
                defined_intersection = list(defined_index.intersection(BODY_FACE_DIFF_RELATION_EVALUATION_VALUES))

                if len(defined_intersection) not in(3, 6):
                    return None
            
                tasks = []
                flag_writter = True
                for idx in defined_intersection:
                    if len(data_evaluation[idx]) == 0 or model_evaluation[idx] is None:
                        flag_writter = False
                        break
                    evaluation_data  = data_evaluation[idx]
                    evaluation_model = model_evaluation[idx]

                    df = pd.DataFrame(evaluation_data, columns=[str(i) for i in range(len(evaluation_data[0]))]).transpose()
                    data_eval = df.to_numpy()
                    tasks.append(evaluation_model.predict_min_async(data_eval))
                
                results = await asyncio.gather(*tasks)
                for i,idx in enumerate(defined_intersection):
                    if len(results) < (i+1):
                        break
                    matrix_evaluation[idx] = results[i]
                
                if not flag_writter:
                    return None
        
        return matrix_evaluation
    
    
    
class ExecutionModelMovement(Imodel):
    def transform_dataEvaluation(self, data_model=None):
        if data_model is None:
            return None
        
        data_evaluation = [[] for _ in range(6)]
        
        for i in range(len(data_model)):
            value = data_model[i]
            if value:
                if len(data_evaluation[i]) != len(value):
                    data_evaluation[i] = value[:]
                else:
                    data_evaluation[i] = value[:]
        
        """
        for i, value in enumerate(data_model):
            if len(value) > 0:
                if not len(data_evaluation[i]) == len(value):
                    data_evaluation[i] = [[] for _ in range(len(value))]
                
                for j, val_pos in enumerate(value):
                    data_evaluation[i][j].extend([val_pos])
        """
        
        return data_evaluation
    
    def evaluation(self, model_evaluation=None, data=None):
        try:
            if None in (model_evaluation, data):
                    return None
            
            matrix_evaluation = [[] for _ in range(6)]

            data_model = hm.HandModel().make_model_body(
                hand_Left=data['model_hand_Left'], 
                hand_Right=data['model_hand_Right'], 
                points_body=data['model_body']
            )
        
            #pre evaluation model, defined
            defined_index = [i for i, model in enumerate(model_evaluation) if len(model) > 0]
            #transform data evaluation
            data_evaluation = self.transform_dataEvaluation(data_model=data_model)
            defined_evaluation = [i for i, model in enumerate(data_evaluation) if len(model) > 0]

            if len(defined_index) != len(defined_evaluation):
                return None
            
            if defined_evaluation != defined_index:
                return None
                             
            for i in defined_index:
                if len(model_evaluation[i])>0:
                    evaluation_data  = data_evaluation[i]
                    evaluation_model = model_evaluation[i]

                    for j, evaluation_pos in enumerate(evaluation_data):
                        if len(evaluation_pos) <= 0 and evaluation_model[j] is None:
                            return None
                        
                        #configure values
                        data = np.array(evaluation_pos).T
                        df_real = pd.DataFrame(data).transpose()

                        #get core pool
                        result_value = evaluation_model[j].predict_min(df_real)
                        matrix_evaluation[i].append(result_value)
                else:
                    return None
                        
            return matrix_evaluation

        except Exception as e:
            print("Error Ocurrido [Model Exec Movement], Mensaje: {0}".format(str(e)))
            return None
    
    async def evaluation_async(self, model_evaluation=None, data=None):
        try:
            if None in (model_evaluation, data):
                    return None
            
            matrix_evaluation = [[] for _ in range(6)]

            data_model = hm.HandModel().make_model_body(
                hand_Left=data['model_hand_Left'], 
                hand_Right=data['model_hand_Right'], 
                points_body=data['model_body']
            )
            data_evaluation = self.transform_dataEvaluation(data_model=data_model)
        
            #pre evaluation model, defined
            defined_index = sorted([i for i, model in enumerate(model_evaluation) if len(model) > 0])
            defined_evaluation = sorted([i for i, model in enumerate(data_evaluation) if len(model) > 0])

            if len(defined_index) != len(defined_evaluation):
                return None
            
            if defined_evaluation != defined_index:
                return None
  
            for idx in defined_index:
                evaluation_data  = data_evaluation[idx]
                evaluation_model = model_evaluation[idx]

                tasks = []
                for i, evaluation_pos in enumerate(evaluation_data):
                    if len(evaluation_pos) <= 0 and evaluation_model[i] is None:
                        return None
                    
                    #configure values
                    data = np.array(evaluation_pos).T
                    df_real = pd.DataFrame(data).transpose()

                    #get core pool
                    tasks.append(evaluation_model[i].predict_min_async(df_real))
                results = await asyncio.gather(*tasks)
                matrix_evaluation[idx].extend(results)                
                
            return matrix_evaluation
        except Exception as e:
            print("Error Ocurrido [Model Exec Movement], Mensaje: {0}".format(str(e)))
            return None
        
class ExecutionModelClassifier(Imodel):
     def evaluation(self, model_classification=None, data=None):
        try:
            if None in (model_classification, data):
                return None
            
            if len(model_classification)!=len(data):
                return None
            
            results = []
            
            defined_index = [i for i, model in enumerate(model_classification) if model is not None]

            for index_ in defined_index:
               results.append(model_classification[index_].predict(np.array([data[index_]]))) 
            
            ##results_recog
            return [all(item[0] for item in results), results]
            
        except Exception as e:
            print("Error Ocurrido [Model Exec - class], Mensaje: {0}".format(str(e)))
            return None

class ExecutionModelState(Imodel):

    async def evaluation_async(self, model_classification=None, data=None):
        try:
            if None in (model_classification, data):
                return None          
            
            ##results_recog
            return model_classification.predict(np.array([data]))
            
        except Exception as e:
            print("Error Ocurrido [Model Exec - Movement State], Mensaje: {0}".format(str(e)))
            return None

    def evaluation(self, model_classification=None, data=None):
        try:
            if None in (model_classification, data):
                return None          
            
            ##results_recog
            return model_classification.predict(np.array([data]))
            
        except Exception as e:
            print("Error Ocurrido [Model Exec - Movement State], Mensaje: {0}".format(str(e)))
            return None