from signlanguage.interfaces.interfaces_model        import ITrace
import signlanguage.core.trainmodel_class            as tm
import signlanguage.core.executionmodel_class        as em
import signlanguage.interfaces.transfermodel_class   as ex
import signlanguage.models.statemodel_class          as st
import signlanguage.utils.utils_class                as ut
import time
import asyncio

class SignMovTrace(ITrace):
    def __init__(self, label= "", state_valuation=-1, evaluationStandard=True):
        self._matrix_states = None
        self._matrix_movement: [st.StateTrace] = []
        self._label = label
        self._state_valuation = state_valuation
        self._validate = False
        self._evaluationStandard = evaluationStandard

    @property
    def validate(self):
        return self._validate

    @property
    def label(self):
        return self._label
    
    @property
    def state_valuation(self):
        return self._state_valuation

    @property
    def matrix_movement(self):
        return self._matrix_movement

    @property
    def matrix_states(self):
        return self._matrix_states

    @matrix_states.setter
    def matrix_states(self, value):
        self._matrix_states = value

    
    def return_result(self, result=False, confidence=0, msg="", review=False):
        return {
            "hand_value": f"{self._label}",
            "evaluado": review,
            "rule_match": result,
            "message": msg,
            "confidence_results": confidence
        }
    
    async def exec_model_async(self, data=None, executionModelmovement : em.ExecutionModelMovement =None, executionModelclass: em.ExecutionModelClassifier=None, executionModelstate: em.ExecutionModelState = None, executionModelpool: em.ExecutionModelPool=None):
        try:
            if None in (data, executionModelmovement, executionModelclass, executionModelstate):
                return self.return_result(msg="Sin procesamiento de solicitud")
            
            if not isinstance(data, list):
                return self.return_result(msg="Sin procesamiento de solicitud")
            
            if len(data) < self._state_valuation:
                return self.return_result(msg="No se puede evaluar", review=False)
            
            #evaluations states
            matrix_states_evaluation = [[] for _ in data]
            rst_exec = []
            for idx, data_ in enumerate(data):
                tasks = []
                for movement_ in self._matrix_movement:
                    tasks.append(
                        movement_.exec_model_async(
                            data=data_, 
                            executionModelmovement=executionModelmovement, 
                            executionModelclass=executionModelclass, 
                            executionModelpool=executionModelpool
                        )
                    )
                rst_exec.append(asyncio.gather(*tasks))
            
            rst = await asyncio.gather(*rst_exec)
            for idx in range(len(data)):
                matrix_states_evaluation[idx].extend([result for result in rst[idx] if result['rule_match']])     
                
            ##evaluation_state
            combinations_evaluation = ut.utils().generate_combinations_evaluations(N=5, data=matrix_states_evaluation)

            if combinations_evaluation is None or len(combinations_evaluation)==0:
                return self.return_result(result=False, confidence=1.0, msg="Resultados sin evaluar, no cumple con los criterios", review=True)

            for idx, combination_ in enumerate(combinations_evaluation):
                resFinal = executionModelstate.evaluation(model_classification=self._matrix_states, data=combination_)
                
                if resFinal[0][0,0]:
                    return self.return_result(result=resFinal[0][0,0], confidence=resFinal[1][0, 0], msg="Resultado obtenido exitosamente", review=True)
                                
            return self.return_result(result=False, confidence=1.0, msg="Resultado obtenido exitosamente", review=True)

        except Exception as e:
            print("Error Ocurrido [Model Exec - Movement], Mensaje: {0}".format(str(e)))
            return self.return_result(msg="Error Ocurrido [Model Exec - Movement], Mensaje: {0}".format(str(e)))

    async def exec_model_async2(self, data=None, executionModelmovement : em.ExecutionModelMovement =None, executionModelclass: em.ExecutionModelClassifier=None, executionModelstate: em.ExecutionModelState = None, executionModelpool: em.ExecutionModelPool=None):
        try:
            if None in (data, executionModelmovement, executionModelclass, executionModelstate):
                return self.return_result(msg="Sin procesamiento de solicitud")
            
            if not isinstance(data, list):
                return self.return_result(msg="Sin procesamiento de solicitud")
            
            if len(data) < self._state_valuation:
                return self.return_result(msg="No se puede evaluar", review=False)
            
            #evaluations states
            matrix_states_evaluation = [[] for _ in data]
            rst_exec = []
            for idx, data_ in enumerate(data):
                tasks = []
                for movement_ in self._matrix_movement:
                    tasks.append(
                        movement_.exec_model_async2(
                            data=data_, 
                            executionModelmovement=executionModelmovement, 
                            executionModelclass=executionModelclass, 
                            executionModelpool=executionModelpool
                        )
                    )
                rst_exec.append(asyncio.gather(*tasks))
            
            rst = await asyncio.gather(*rst_exec)
            for idx in range(len(data)):
                matrix_states_evaluation[idx].extend([result for result in rst[idx] if result['rule_match']])     
                
            ##evaluation_state
            combinations_evaluation = ut.utils().generate_combinations_evaluations(N=5, data=matrix_states_evaluation)

            if combinations_evaluation is None or len(combinations_evaluation)==0:
                return self.return_result(result=False, confidence=0.0, msg="Resultados sin evaluar, no cumple con los criterios", review=True)

            for idx, combination_ in enumerate(combinations_evaluation):
                resFinal = executionModelstate.evaluation(model_classification=self._matrix_states, data=combination_)
                
                if resFinal[0][0,0]:
                    return self.return_result(result=resFinal[0][0,0], confidence=resFinal[1][0, 0], msg="Resultado obtenido exitosamente", review=True)
                                
            return self.return_result(result=False, confidence=0.0, msg="Resultado obtenido exitosamente", review=True)

        except Exception as e:
            print("Error Ocurrido [Model Exec - Movement], Mensaje: {0}".format(str(e)))
            return self.return_result(msg="Error Ocurrido [Model Exec - Movement], Mensaje: {0}".format(str(e)))

    def exec_model(self, data=None, executionModelmovement : em.ExecutionModelMovement =None, executionModelclass: em.ExecutionModelClassifier=None, executionModelstate: em.ExecutionModelState = None, executionModelpool: em.ExecutionModelPool=None):
        try:
            if None in (data, executionModelmovement, executionModelclass, executionModelstate):
                return self.return_result(msg="Sin procesamiento de solicitud")
            
            if not isinstance(data, list):
                return self.return_result(msg="Sin procesamiento de solicitud")
            
            if len(data) < self._state_valuation:
                return self.return_result(msg="No se puede evaluar", review=False)
            
            #evaluations states
            matrix_states_evaluation = [[] for _ in data]
            for idx, data_ in enumerate(data):
                for movement_ in self._matrix_movement:
                    res = movement_.exec_model(data=data_, executionModelmovement=executionModelmovement, executionModelclass=executionModelclass, executionModelpool=executionModelpool)
                    if res['rule_match']:
                        matrix_states_evaluation[idx].append(res)
                
            ##evaluation_state
            combinations_evaluation = ut.utils().generate_combinations_evaluations(N=5, data=matrix_states_evaluation)

            if combinations_evaluation is None or len(combinations_evaluation)==0:
                return self.return_result(result=False, confidence=0.0, msg="Resultados sin evaluar, no cumple con los criterios", review=True)

            if len(combinations_evaluation[0])>0:
                for idx, combination_ in enumerate(combinations_evaluation):
                    resFinal = executionModelstate.evaluation(model_classification=self._matrix_states, data=combination_)
                    
                    if resFinal[0][0,0]:
                       return self.return_result(result=resFinal[0][0,0], confidence=resFinal[1][0, 0], msg="Resultado obtenido exitosamente", review=True)
                                
            return self.return_result(result=False, confidence=0.0, msg="Resultado obtenido exitosamente", review=True)

        except Exception as e:
            print("Error Ocurrido [Model Exec - Movement], Mensaje: {0}".format(str(e)))
            return self.return_result(msg="Error Ocurrido [Model Exec - Movement], Mensaje: {0}".format(str(e)))

    def train_model2(self, data=None, configuration=None, trainModelmovement: tm.TrainModelMovement = None, trainModelpool: tm.TrainModelPool=None, trainModelclass: tm.TrainModelClassifier =None, trainModelstate: tm.TrainModelStates = None):
        try:
            if None in (data, configuration, trainModelclass, trainModelmovement, trainModelpool):
                raise ex.InvalidTrainModelException()

            if len(data) != len(configuration):
                raise ex.InvalidTrainModelException()

            qty_states = len(configuration)
            
            print(f"------------------------------------------------------------------------------------")
            print(f"Label: {self._label} - qty_states = {qty_states}")
            start_time = time.time()

            
            print(f" State movement training-------------------------------------")
            start_time_c = time.time()
            for idx, state_ in enumerate(configuration):
                sTraceTmp = st.StateTrace(label=state_['label'], state_value=idx)
                
                sTraceTmp.train_model(
                    trainModelmovement=trainModelmovement,
                    trainModelclass=trainModelclass,
                    trainModelpool=trainModelpool,
                    data=data[idx],
                    face_relation=state_['configuration']['face_relation'],
                    body_relation=state_['configuration']['body_relation'],
                    hand_relation=state_['configuration']['hand_relation'],
                    hand_diff_relation=state_['configuration']['hand_diff_relation']
                )

                if self._evaluationStandard:
                    if None in (sTraceTmp.body_evaluation):
                        self._matrix_movement = None
                        break
                else:
                    if None in (sTraceTmp.body_evaluation) or all(item is None for item in sTraceTmp.body_classification):
                        self._matrix_movement = None
                        break

                self._matrix_movement.append(sTraceTmp)
            
            end_time_c = time.time()
            print(f"Ejecucion finalizada en {(end_time_c - start_time_c):.2f} segundos.")
            
            if self._matrix_movement is None or all(item is None for item in self._matrix_movement):
                end_time = time.time()
                print(f"Label: {self._label}, Resultado: Insatisfactorio, Mensaje: El entrenamiento finalizó en {(end_time - start_time):.2f} segundos.")
                return None

            print(f" Classification model state movement training-------------------------------------")
            start_time_c = time.time()
            self._matrix_states = trainModelstate.Train_models(data=qty_states, lenght_valuation=self._state_valuation)
            end_time_c = time.time()
            print(f"Ejecucion finalizada en {(end_time_c - start_time_c):.2f} segundos.")

            print(f" Verification model movement training------------------------------------------------------")
            end_time = time.time()
            result_message = "Insatisfactorio" if self._matrix_states is None and not all(item.validate for item in self._matrix_movement) else "satisfactorio"
            print(f"Label: {self._label}, Resultado: {result_message}, Mensaje: El entrenamiento finalizó en {(end_time - start_time):.2f} segundos.")
            self._validate = all(item.validate for item in self._matrix_movement) and self._matrix_states is not None

        except Exception as e:
            self._matrix_states = None
            self._matrix_movement = None
            print(f"Label: {self._label}, Resultado: Insatisfactorio, Mensaje: {e}")
        finally:
            print(f"------------------------------------------------------------------------------------")
    
    def train_model(self, data=None, configuration=None, trainModelmovement: tm.TrainModelMovement = None, trainModelpool: tm.TrainModelPool=None, trainModelclass: tm.TrainModelClassifier =None, trainModelstate: tm.TrainModelStates = None):
        try:
            if None in (data, configuration, trainModelclass, trainModelmovement, trainModelpool):
                raise ex.InvalidTrainModelException()
            
            if len(data) != len(configuration):
                raise ex.InvalidTrainModelException()

            qty_states = len(configuration)
            
            print(f"------------------------------------------------------------------------------------")
            print(f"Label: {self._label} - qty_states = {qty_states}")
            
            if len(data)==0:
                print(f"Label: {self._label}, Resultado: Insatisfactorio, Mensaje: El entrenamiento finalizo en 0 segundos.")
                self._matrix_classification = None
                self._matrix_evaluation = None
                return None

            start_time = time.time()

            print(f" State movement training-------------------------------------")
            start_time_c = time.time()
            for idx, state_ in enumerate(configuration):
                sTraceTmp = st.StateTrace(label=state_['label'], state_value=idx)
                
                sTraceTmp.train_model(
                    trainModelmovement=trainModelmovement,
                    trainModelclass=trainModelclass,
                    trainModelpool=trainModelpool,
                    data=data[idx],
                    face_relation=state_['configuration']['face_relation'],
                    body_relation=state_['configuration']['body_relation'],
                    hand_relation=state_['configuration']['hand_relation'],
                    hand_diff_relation=state_['configuration']['hand_diff_relation']
                )

                if self._evaluationStandard:
                    if None in (sTraceTmp.body_evaluation):
                        self._matrix_movement = None
                        break
                else:
                    if None in (sTraceTmp.body_evaluation) or all(item is None for item in sTraceTmp.body_classification):
                        self._matrix_movement = None
                        break

                self._matrix_movement.append(sTraceTmp)
            
            end_time_c = time.time()
            print(f"Ejecucion finalizada en {(end_time_c - start_time_c):.2f} segundos.")
            
            if self._matrix_movement is None or all(item is None for item in self._matrix_movement):
                end_time = time.time()
                print(f"Label: {self._label}, Resultado: Insatisfactorio, Mensaje: El entrenamiento finalizó en {(end_time - start_time):.2f} segundos.")
                return None

            print(f" Classification model state movement training-------------------------------------")
            start_time_c = time.time()
            self._matrix_states = trainModelstate.Train_models(data=qty_states, lenght_valuation=self._state_valuation)
            end_time_c = time.time()
            print(f"Ejecucion finalizada en {(end_time_c - start_time_c):.2f} segundos.")

            print(f" Verification model movement training------------------------------------------------------")
            end_time = time.time()
            result_message = "Insatisfactorio" if self._matrix_states is None and not all(item.validate for item in self._matrix_movement) else "satisfactorio"
            print(f"Label: {self._label}, Resultado: {result_message}, Mensaje: El entrenamiento finalizó en {(end_time - start_time):.2f} segundos.")
            self._validate = all(item.validate for item in self._matrix_movement) and self._matrix_states is not None

        except Exception as e:
            self._matrix_states = None
            self._matrix_movement = None
            print(f"Label: {self._label}, Resultado: Insatisfactorio, Mensaje: {e}")
        finally:
            print(f"------------------------------------------------------------------------------------")
    
    