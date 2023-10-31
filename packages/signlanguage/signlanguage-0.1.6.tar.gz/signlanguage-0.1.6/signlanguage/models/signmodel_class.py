from signlanguage.interfaces.interfaces_model       import ITrace
import signlanguage.core.trainmodel_class           as tm
import signlanguage.core.executionmodel_class       as em
import signlanguage.interfaces.transfermodel_class  as ex
import signlanguage.utils.utils_class               as utils
import numpy                           as np
import time
import asyncio

#principal class execution
class SignTrace(ITrace):
    def __init__(self, label= "", face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False, evaluationStandard=True):
        self._matrix_evaluation = []
        self._matrix_classification = []
        self._validate = False
        self._label = label
        self._hand_relation = hand_relation
        self._face_relation = face_relation
        self._hand_diff_relation = hand_diff_relation
        self._body_relation = body_relation
        self._evaluationStandard = evaluationStandard

    @property
    def label(self):
        return self._label
    
    @property
    def validate(self):
        return self._validate

    @property
    def matrix_classification(self):
        return self._matrix_classification

    @property
    def matrix_evaluation(self):
        return self._matrix_evaluation

    @matrix_evaluation.setter
    def matrix_evaluation(self, value):
        self._matrix_evaluation = value

    def return_result(self, result=False, confidence=0, msg="", review=False):
        return {
            "hand_value": self._label,
            "evaluado": review,
            "rule_match": result,
            "message": msg,
            "confidence_results": confidence
        }
    
    async def exec_model_async2(self, data=None, executionModelpool : em.ExecutionModelPool =None, executionModelclass: em.ExecutionModelClassifier=None):
        try:
            if None in (data, executionModelpool, executionModelclass):
                return self.return_result(msg="Sin procesamiento de solicitud", confidence=1.0)
                
            res = await executionModelpool.evaluation_async2(
                model_evaluation=self._matrix_evaluation, 
                data=data, face_relation=self._face_relation, 
                body_relation=self._body_relation, 
                hand_relation=self._hand_relation, 
                hand_diff_relation=self._hand_diff_relation
            )
            if res is None:
                return self.return_result(result=False, confidence=0.0, msg="Resultado obtenido exitosamente - no cumple con los criterios", review=True)
           
            if all(element is None for element in res):
                return self.return_result(msg="Resultados sin evaluar", confidence=0.0)

            if self._evaluationStandard:
                result, confidence = utils.utils().evaluation_standard_m4(data=res)
                return self.return_result(result=result, confidence=confidence, msg="Resultado obtenido exitosamente", review=True)         

            return self.return_result(result=False, confidence=0.0, msg="Resultado obtenido exitosamente - method not allowed -> [classificationEvaluation]", review=True)
        except Exception as e:
            print("Error Ocurrido [Model Exec - SignTrace], Mensaje: {0}".format(str(e)))
            return self.return_result(msg="Error Ocurrido [Model Exec - SignTrace], Mensaje: {0}".format(str(e)), review=True)

    async def exec_model_async(self, data=None, executionModelpool : em.ExecutionModelPool =None, executionModelclass: em.ExecutionModelClassifier=None):
        try:
            if None in (data, executionModelpool, executionModelclass):
                return self.return_result(msg="Sin procesamiento de solicitud", confidence=0.0)
                
            res = await executionModelpool.evaluation_async(
                model_evaluation=self._matrix_evaluation, 
                data=data, face_relation=self._face_relation, 
                body_relation=self._body_relation, 
                hand_relation=self._hand_relation, 
                hand_diff_relation=self._hand_diff_relation
            )
            if res is None:
                return self.return_result(result=False, confidence=0.0, msg="Resultado obtenido exitosamente - no cumple con los criterios", review=True)
           
            if all(element is None for element in res):
                return self.return_result(msg="Resultados sin evaluar", confidence=0.0)

            if self._evaluationStandard:
                result, confidence = utils.utils().evaluation_standard(data=res)
                return self.return_result(result=result, confidence=confidence, msg="Resultado obtenido exitosamente", review=True)         

            return self.return_result(result=False, confidence=0.0, msg="Resultado obtenido exitosamente - method not allowed -> [classificationEvaluation]", review=True)
        except Exception as e:
            print("Error Ocurrido [Model Exec - SignTrace], Mensaje: {0}".format(str(e)))
            return self.return_result(msg="Error Ocurrido [Model Exec - SignTrace], Mensaje: {0}".format(str(e)), review=True)

    def exec_model(self, data=None, executionModelpool : em.ExecutionModelPool =None, executionModelclass: em.ExecutionModelClassifier=None):
        try:
            if None in (data, executionModelpool, executionModelclass):
                return self.return_result(msg="Sin procesamiento de solicitud", confidence=1.0)
            
            res = asyncio.run(
                executionModelpool.evaluation(
                    model_evaluation=self._matrix_evaluation, 
                    data=data, face_relation=self._face_relation, 
                    body_relation=self._body_relation, 
                    hand_relation=self._hand_relation, 
                    hand_diff_relation=self._hand_diff_relation
                )
            )

            if res is None:
                return self.return_result(msg="Resultados sin evaluar", confidence=0.0)

            if self._evaluationStandard:
                result, confidence = utils.utils().evaluation_standard(data=res)
                return self.return_result(result=result, confidence=confidence, msg="Resultado obtenido exitosamente", review=True)  
            
            return self.return_result(result=False, confidence=0.0, msg="Resultado obtenido exitosamente - method not allowed -> [classificationEvaluation]", review=True)
            for idx, in_ in enumerate(self._matrix_classification):
                if in_ is not None and (res[idx] is None or len(res[idx])==0):
                    return self.return_result(msg="Resultados sin evaluar, no cumple con los criterios", confidence=1.0)

            validation_lenght1 = [1 for obj_ in res if len(obj_)>0]
            validation_lenght2 = [1 for obj_ in self._matrix_classification if obj_ is not None]

            if len(validation_lenght1) != len(validation_lenght2):
                return self.return_result(msg="Resultados sin evaluar, no cumple con los criterios de clasificacion", confidence=1.0)

            # evaluation - deprecated at moment
            resFinal = executionModelclass.evaluation(model_classification=self._matrix_classification, data=res)
            if resFinal is None:
                return self.return_result(result=False, confidence=1.0, msg="Resultado obtenido exitosamente", review=True)
            confidence = sum([item[0][0, 0] for item in resFinal[1] if isinstance(item[0], np.ndarray) and item[0].size > 0 and item[0][0, 0] > 0.9])/len(resFinal[1])
            return self.return_result(result=resFinal[0], confidence=confidence, msg="Resultado obtenido exitosamente", review=True)          
    
        except Exception as e:
            print("Error Ocurrido [Model Exec - SignTrace], Mensaje: {0}".format(str(e)))
            return self.return_result(msg="Error Ocurrido [Model Exec - SignTrace], Mensaje: {0}".format(str(e)), review=True)

    def train_model2(self, trainModelpool: tm.TrainModelPool=None, trainModelclass: tm.TrainModelClassifier =None, data=None):
        try:
            if None in (trainModelclass, trainModelpool, data):
                raise ex.InvalidTrainModelException()
            
            print(f"------------------------------------------------------------------------------------")
            print(f"Label: {self._label}-  qty_data = {len(data)} -  face_relation={self._face_relation}, body_relation={self._body_relation}, hand_relation={self._hand_relation}, hand_diff_relation={self._hand_diff_relation}")
            start_time = time.time()

            print(f" Clustering model training----------------------------------------------------------")
            #group model
            start_time_g = time.time()
            self._matrix_evaluation = trainModelpool.Train_models2(data=data, face_relation=self._face_relation, body_relation=self._body_relation, hand_relation=self._hand_relation, hand_diff_relation=self._hand_diff_relation)
            end_time_g = time.time()
            print(f"Ejecucion finalizada en {(end_time_g - start_time_g):.2f} segundos.")
            
            if self._matrix_evaluation is None:
                raise ex.InvalidTrainModelException(group_model=True, msg=f"it was not possible to create the evaluation model for the letter, label: {self._label}")
            
            # evaluation - deprecated at moment
            if not self._evaluationStandard:
                print(f" Classification model training------------------------------------------------------")
                start_time_c = time.time()

                end_time_c = time.time()
                print(f"Ejecucion finalizada en {(end_time_c - start_time_c):.2f} segundos.") 
            
                print(f" Verification model training------------------------------------------------------")
                result_message = "Insatisfactorio" if None in (self._matrix_evaluation) or all(item is None for item in self._matrix_classification) or len([1 for obj in index_matrix if self._matrix_classification[obj] is None]) else "Satisfactorio"
                end_time = time.time()
                print(f"Label: {self._label}, Resultado: {result_message}, Mensaje: El entrenamiento finalizo en {(end_time - start_time):.2f} segundos.")
                self._validate = not (None in (self._matrix_evaluation) or all(item is None for item in self._matrix_classification) or len([1 for obj in index_matrix if self._matrix_classification[obj] is None]))

            else:
                print(f" Verification model training------------------------------------------------------")
                result_message = "Insatisfactorio" if all(element is None for element in self._matrix_evaluation) else "Satisfactorio"
                end_time = time.time()
                print(f"Label: {self._label}, Resultado: {result_message}, Mensaje: El entrenamiento finalizo en {(end_time - start_time):.2f} segundos.")
                self._validate = not all(element is None for element in self._matrix_evaluation)

        except Exception as e:
            self._matrix_classification = None
            self._matrix_evaluation = None
            print(f"Label: {self._label}, Resultado: Insatisfactorio, Mensaje: {e}")
        finally:
            print(f"------------------------------------------------------------------------------------")

    def train_model(self, trainModelpool: tm.TrainModelPool=None, trainModelclass: tm.TrainModelClassifier =None, data=None):
        try:
            if None in (trainModelclass, trainModelpool, data):
                raise ex.InvalidTrainModelException()
            
            print(f"------------------------------------------------------------------------------------")
            print(f"Label: {self._label}-  qty_data = {len(data)} -  face_relation={self._face_relation}, body_relation={self._body_relation}, hand_relation={self._hand_relation}, hand_diff_relation={self._hand_diff_relation}")
            
            
            if len(data)==0:
                print(f"Label: {self._label}, Resultado: Insatisfactorio, Mensaje: El entrenamiento finalizo en 0 segundos.")
                self._matrix_classification = None
                self._matrix_evaluation = None
                return None
            
            start_time = time.time()

            print(f" Clustering model training----------------------------------------------------------")
            #group model
            start_time_g = time.time()
            self._matrix_evaluation = trainModelpool.Train_models(data=data, face_relation=self._face_relation, body_relation=self._body_relation, hand_relation=self._hand_relation, hand_diff_relation=self._hand_diff_relation)
            end_time_g = time.time()
            print(f"Ejecucion finalizada en {(end_time_g - start_time_g):.2f} segundos.")
            
            matrix_classification = [[] for _ in range(54)]
            if self._matrix_evaluation is None:
                raise ex.InvalidTrainModelException(group_model=True, msg=f"it was not possible to create the evaluation model for the letter, label: {self._label}")
            
            # evaluation - deprecated at moment
            if not self._evaluationStandard:
                print(f" Classification model training------------------------------------------------------")
                start_time_c = time.time()

                #class model
                for j, dataTmp in enumerate(data):

                    reslt = em.ExecutionModelPool().evaluation(model_evaluation=self._matrix_evaluation, data=dataTmp, face_relation=self._face_relation, body_relation=self._body_relation, hand_relation=self._hand_relation, hand_diff_relation=self._hand_diff_relation)
                    if reslt is not None:
                        for idx, rst in enumerate(reslt):
                            print(f"{idx} -- {rst}")
                            if len(rst) == len(self._matrix_evaluation[idx]) and len(rst)>0:
                                matrix_classification[idx].append(rst)

                class_relation_validation = True
                for idx, value in enumerate([ a_ for a_ in matrix_classification if len(a_)>0]):
                    if len(value)<90:
                        class_relation_validation = False
                        break

                list_length = [ len(a_) for a_ in matrix_classification if len(a_)>0]
                validation_length = all(length == list_length[0] for length in list_length)

                index_matrix = []
                if class_relation_validation and validation_length:
                    for k, class_data in enumerate(matrix_classification):
                        if len(class_data)>0:
                            core_class = trainModelclass.Train_models(data=class_data)
                            if core_class is None:
                                index_matrix.append(k)
                            self._matrix_classification.append(core_class)
                        else:
                            self._matrix_classification.append(None)

                end_time_c = time.time()
                print(f"Ejecucion finalizada en {(end_time_c - start_time_c):.2f} segundos.") 
            
                print(f" Verification model training------------------------------------------------------")
                result_message = "Insatisfactorio" if None in (self._matrix_evaluation) or all(item is None for item in self._matrix_classification) or len([1 for obj in index_matrix if self._matrix_classification[obj] is None]) else "Satisfactorio"
                end_time = time.time()
                print(f"Label: {self._label}, Resultado: {result_message}, Mensaje: El entrenamiento finalizo en {(end_time - start_time):.2f} segundos.")
                self._validate = not (None in (self._matrix_evaluation) or all(item is None for item in self._matrix_classification) or len([1 for obj in index_matrix if self._matrix_classification[obj] is None]))

            else:
                print(f" Verification model training------------------------------------------------------")
                result_message = "Insatisfactorio" if all(element is None for element in self._matrix_evaluation) else "Satisfactorio"
                end_time = time.time()
                print(f"Label: {self._label}, Resultado: {result_message}, Mensaje: El entrenamiento finalizo en {(end_time - start_time):.2f} segundos.")
                self._validate = not all(element is None for element in self._matrix_evaluation)

        except Exception as e:
            self._matrix_classification = None
            self._matrix_evaluation = None
            print(f"Label: {self._label}, Resultado: Insatisfactorio, Mensaje: {e}")
        finally:
            print(f"------------------------------------------------------------------------------------")


