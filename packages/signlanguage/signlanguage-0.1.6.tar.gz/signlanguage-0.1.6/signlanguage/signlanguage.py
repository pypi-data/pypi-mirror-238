import signlanguage.core.executionmodel_class      as em
import signlanguage.core.trainmodel_class          as tm
import signlanguage.models.signmodel_class         as sm
import signlanguage.models.movementmodel_class     as mm
import signlanguage.utils.utils_class              as utils
import signlanguage.interfaces.transfermodel_class as tf
import json
import time
import asyncio
import concurrent.futures

class signlanguage:
    def __init__(self, type_model=1):
        self.__sign_models = []
        self.__trainPool   = tm.TrainModelPool()
        self.__trainClass  = tm.TrainModelClassifier()
        self.__trainMov    = tm.TrainModelMovement()
        self.__trainState  = tm.TrainModelStates()
        self.__execPool    = em.ExecutionModelPool()
        self.__execClass   = em.ExecutionModelClassifier()
        self.__execMov     = em.ExecutionModelMovement()
        self.__execState   = em.ExecutionModelState()
        self.semaphore     = asyncio.Semaphore(10)
        self.model         = type_model

    @property
    def sign_models(self):
        return self.__sign_models

    @sign_models.setter
    def sign_models(self, value):
        self.__sign_models = value

    @property
    def trainPool(self):
        return self.__trainPool

    @trainPool.setter
    def trainPool(self, value):
        self.__trainPool = value

    @property
    def trainClass(self):
        return self.__trainClass

    @trainClass.setter
    def trainClass(self, value):
        self.__trainClass = value

    @property
    def trainMov(self):
        return self.__trainMov

    @trainMov.setter
    def trainMov(self, value):
        self.__trainMov = value

    @property
    def trainState(self):
        return self.__trainState

    @trainState.setter
    def trainState(self, value):
        self.__trainState = value

    @property
    def execPool(self):
        return self.__execPool

    @execPool.setter
    def execPool(self, value):
        self.__execPool = value

    @property
    def execClass(self):
        return self.__execClass

    @execClass.setter
    def execClass(self, value):
        self.__execClass = value

    @property
    def execMov(self):
        return self.__execMov

    @execMov.setter
    def execMov(self, value):
        self.__execMov = value

    @property
    def execState(self):
        return self.__execState

    @execState.setter
    def execState(self, value):
        self.__execState = value

    def get_SignModels(self, training_configuration=None):
        Train_Data = []
        try:
            
            if training_configuration is None:
                return None
            
            print(f" Collecting data configuration-------------------------------------")
            for signs in training_configuration: 
                if 'label' in signs and 'configuration' in signs and 'folderPath' in signs and 'countTraining' in signs and 'stateConfiguration' not in signs:
                    dataTmp = utils.utils().collect_simple_data(general=signs, path=signs['folderPath'])
                    if dataTmp is not None:
                        self.__sign_models.append(
                            sm.SignTrace(
                                label=signs['label'], 
                                face_relation=signs['configuration']['face_relation'], 
                                body_relation=signs['configuration']['body_relation'], 
                                hand_relation=signs['configuration']['hand_relation'], 
                                hand_diff_relation=signs['configuration']['hand_diff_relation']
                            )
                        )
                        Train_Data.append(dataTmp)
                    else:
                        self.__sign_models.append(None)
                        Train_Data.append(None)
                elif 'label' in signs and 'configuration' not in signs and 'configurationState' in signs and 'stateCountValidation' in signs:
                    dataTmp = utils.utils().collect_movement_data(general=signs['configurationState'], path=signs['folderPath'])
                    print(len(dataTmp)==len(signs['configurationState']))
                    if dataTmp is not None and len(dataTmp)==len(signs['configurationState']):
                        self.__sign_models.append(
                            mm.SignMovTrace(
                                label=signs['label'], 
                                state_valuation=signs['stateCountValidation']
                            )
                        )
                        Train_Data.append(dataTmp)
                    else:
                        self.__sign_models.append(None)
                        Train_Data.append(None)              
        except Exception as e:
            print("Error Ocurrido [getValues], Mensaje: {0}".format(str(e)))
            return None
        
        return Train_Data

    def Train(self, configuration_train=None, path_configuration=None):
        start_time = time.time()
        try:
            training_configuration = []
            
            if configuration_train is None and path_configuration is None:
                raise tf.InvalidModelException(msg="no data configuration provided")
            
            if configuration_train is not None and path_configuration is not None:
                raise tf.InvalidModelException(msg="configuration provided is not setted correctly")
            
            if path_configuration is not None:
                f = open(path_configuration)
                training_configuration = json.load(f)

            if configuration_train is not None:
                training_configuration = configuration_train
            
            if len(training_configuration)>0:
                print(f"------------------------------------------------------------------------------------")
                data_train = self.get_SignModels(training_configuration=training_configuration)
                print(f" verifying data configuration-------------------------------------")
                if data_train is not None and len(training_configuration) == len(data_train) == len(self.__sign_models):
                    print(f" Training data configuration-------------------------------------")
                    for idx, data_ in enumerate(data_train):
                        if self.__sign_models[idx] is not None:
                            configuration = training_configuration[idx]
                            sign_label = self.__sign_models[idx].label
                            if data_ is not None and self.__sign_models[idx] is not None:
                                if configuration['label'] == sign_label:
                                    if isinstance(self.__sign_models[idx], sm.SignTrace):
                                        self.__sign_models[idx].train_model(
                                            trainModelpool=self.__trainPool, 
                                            trainModelclass=self.__trainClass, 
                                            data=data_
                                        )
                                    elif isinstance(self.__sign_models[idx], mm.SignMovTrace):
                                        self.__sign_models[idx].train_model(
                                            data=data_, 
                                            configuration=configuration['configurationState'], 
                                            trainModelclass=self.__trainClass, 
                                            trainModelpool=self.__trainPool, 
                                            trainModelmovement=self.__trainMov, 
                                            trainModelstate=self.__trainState
                                        )
                    print(f" Sanitize data configuration-------------------------------------")
                    self.__sign_models = list(filter(None, self.__sign_models))

                else:
                    raise tf.InvalidModelException(msg="no data collected")
            else:
                raise tf.InvalidModelException(msg="no data configuration provided")
        except Exception as e:
            print(f"Error Ocurrido [Train], Mensaje: {e}")
            self.__sign_models = []
        finally:
            end_time = time.time()
            print(f" Training ended in {(end_time - start_time):.2f} seconds.")
            print(f"Implemented Model, qty recognized signs: {len([obj for obj in self.__sign_models if obj.validate])} - recognized signs: {[obj.label for obj in self.__sign_models if obj.validate]}")
            print(f"Required verification, qty signs: {len([obj for obj in self.__sign_models if obj.validate==False])} - signs: {[obj.label for obj in self.__sign_models if obj.validate==False]}")
            print(f"------------------------------------------------------------------------------------")

    def Train2(self, configuration_train=None, path_configuration=None):
        start_time = time.time()
        try:
            training_configuration = []
            
            if configuration_train is None and path_configuration is None:
                raise tf.InvalidModelException(msg="no data configuration provided")
            
            if configuration_train is not None and path_configuration is not None:
                raise tf.InvalidModelException(msg="configuration provided is not setted correctly")
            
            if path_configuration is not None:
                f = open(path_configuration)
                training_configuration = json.load(f)

            if configuration_train is not None:
                training_configuration = configuration_train
            
            if len(training_configuration)>0:
                print(f"------------------------------------------------------------------------------------")
                data_train = self.get_SignModels(training_configuration=training_configuration)
                print(f" verifying data configuration-------------------------------------")
                if data_train is not None and len(training_configuration) == len(data_train) == len(self.__sign_models):
                    print(f" Training data configuration-------------------------------------")
                    for idx, data_ in enumerate(data_train):
                        configuration = training_configuration[idx]
                        sign_label = self.__sign_models[idx].label
                        if data_ is not None and self.__sign_models[idx] is not None:
                            if configuration['label'] == sign_label:
                                if isinstance(self.__sign_models[idx], sm.SignTrace):
                                    self.__sign_models[idx].train_model2(
                                        trainModelpool=self.__trainPool, 
                                        trainModelclass=self.__trainClass, 
                                        data=data_
                                    )
                                elif isinstance(self.__sign_models[idx], mm.SignMovTrace):
                                    self.__sign_models[idx].train_model2(
                                        data=data_, 
                                        configuration=configuration['configurationState'], 
                                        trainModelclass=self.__trainClass, 
                                        trainModelpool=self.__trainPool, 
                                        trainModelmovement=self.__trainMov, 
                                        trainModelstate=self.__trainState
                                    )

                    print(f" Sanitize data configuration-------------------------------------")
                    self.__sign_models = list(filter(None, self.__sign_models))

                else:
                    raise tf.InvalidModelException(msg="no data collected")
            else:
                raise tf.InvalidModelException(msg="no data configuration provided")
        except Exception as e:
            print(f"Error Ocurrido [Train], Mensaje: {e}")
            self.__sign_models = []
        finally:
            end_time = time.time()
            print(f" Training ended in {(end_time - start_time):.2f} seconds.")
            print(f"Implemented Model, qty recognized signs: {len([obj for obj in self.__sign_models if obj.validate])} - recognized signs: {[obj.label for obj in self.__sign_models if obj.validate]}")
            print(f"Required verification, qty signs: {len([obj for obj in self.__sign_models if obj.validate==False])} - signs: {[obj.label for obj in self.__sign_models if obj.validate==False]}")
            print(f"------------------------------------------------------------------------------------")

    def Predict(self, data=None, idx=-1):
        try:
            if data is None:
                return self.model_object_result(value_result=[])
            
            results=[]
            for idx, signs_ in enumerate(self.__sign_models):
                if isinstance(signs_, sm.SignTrace) and not isinstance(data, list):
                    results.append(
                        signs_.exec_model(
                            data=data, 
                            executionModelclass=self.__execClass, 
                            executionModelpool=self.__execPool
                        )
                    )
                elif isinstance(signs_, mm.SignMovTrace) and isinstance(data, list):
                    results.append(
                        signs_.exec_model(
                            data=data[0], 
                            executionModelclass=self.__execClass, 
                            executionModelpool=self.__execPool, 
                            executionModelmovement=self.__execMov, 
                            executionModelstate=self.__execState
                        )
                    )

            return self.model_object_result(value_result=results, idx=idx)
        except Exception as e:
            print(f"Error Ocurrido [Predict], Mensaje: {e}")
            return self.model_object_result(value_result=[])
    
    async def Predict_async_prev(self, data=None, idx=-1):
        try:
            if data is None:
                return self.model_object_result(value_result=[])
            
            results=[]
            sign_exec = []
            
            if not isinstance(data, list):
                sign_exec = [signs_.exec_model_async(
                            data=data, 
                            executionModelclass=self.__execClass, 
                            executionModelpool=self.__execPool
                        ) for signs_ in self.__sign_models if isinstance(signs_, sm.SignTrace)]
            elif isinstance(data, list):
                sign_exec = [signs_.exec_model_async(
                            data=data, 
                            executionModelclass=self.__execClass, 
                            executionModelpool=self.__execPool, 
                            executionModelmovement=self.__execMov, 
                            executionModelstate=self.__execState
                        ) for signs_ in self.__sign_models if isinstance(signs_, mm.SignMovTrace)]

            resultados = await asyncio.gather(*sign_exec)
            results.extend(resultados)

            return self.model_object_result(value_result=results, idx=idx)

        except Exception as e:
            print(f"Error Ocurrido [Predict], Mensaje: {e}")
            return self.model_object_result(value_result=[])

    async def Predict_async(self, data=None, idx=-1):
        try:
            if data is None:
                return self.model_object_result(value_result=[])
            
            results=[]
            sign_exec = []
            
            if not isinstance(data, list):
                sign_exec = [signs_.exec_model_async(
                            data=data, 
                            executionModelclass=self.__execClass, 
                            executionModelpool=self.__execPool
                        ) for signs_ in self.__sign_models if isinstance(signs_, sm.SignTrace)]
            elif isinstance(data, list):
                sign_exec = [signs_.exec_model_async(
                            data=data, 
                            executionModelclass=self.__execClass, 
                            executionModelpool=self.__execPool, 
                            executionModelmovement=self.__execMov, 
                            executionModelstate=self.__execState
                        ) for signs_ in self.__sign_models if isinstance(signs_, mm.SignMovTrace)]

            resultados = await asyncio.gather(*sign_exec)
            results.extend(resultados)

            return self.model_object_result(value_result=results, idx=idx)

        except Exception as e:
            print(f"Error Ocurrido [Predict], Mensaje: {e}")
            return self.model_object_result(value_result=[])

    async def Predict_async2(self, data=None, idx=-1):
        try:
            if data is None:
                return self.model_object_result(value_result=[])
            
            results=[]
            sign_exec = []
            
            if not isinstance(data, list):
                sign_exec = [signs_.exec_model_async2(
                            data=data, 
                            executionModelclass=self.__execClass, 
                            executionModelpool=self.__execPool
                        ) for signs_ in self.__sign_models if isinstance(signs_, sm.SignTrace)]
            elif isinstance(data, list):
                sign_exec = [signs_.exec_model_async2(
                            data=data, 
                            executionModelclass=self.__execClass, 
                            executionModelpool=self.__execPool, 
                            executionModelmovement=self.__execMov, 
                            executionModelstate=self.__execState
                        ) for signs_ in self.__sign_models if isinstance(signs_, mm.SignMovTrace)]

            resultados = await asyncio.gather(*sign_exec)
            results.extend(resultados)

            return self.model_object_result(value_result=results, idx=idx)

        except Exception as e:
            print(f"Error Ocurrido [Predict], Mensaje: {e}")
            return self.model_object_result(value_result=[])

    async def Evaluate_async_prev(self, data=None):
        if data is None:
            return self.model_object_result(value_result=[])

        results_data = []
        if isinstance(data, list):
            rst_ejecucion = []
            rst_sended = []
            for idc, data_ in enumerate(data):
                rst_tmp = asyncio.create_task(self.Predict_async(data=data_, idx=idc))
                rst_tmp_value = await rst_tmp

                if rst_tmp_value['found']:
                    results_data.append(rst_tmp_value)
                    if len(rst_ejecucion) > 2:
                        rst_sended.append([rst_ejecucion, idc-1])
                    rst_ejecucion.clear()
                else:
                    rst_ejecucion.append(data_)

            if len(rst_ejecucion) > 2:
                rst_sended.append([rst_ejecucion, len(data)])

            tasks = [self.Predict_async(data=rst_exec_[0], idx=rst_exec_[1]) for rst_exec_ in rst_sended]
            results_data += await asyncio.gather(*tasks)
        else:
            results_data = [await asyncio.create_task(self.Predict_async(data=data))]

        return [results_ for results_ in results_data if results_['found']]
    
    async def Evaluate_async(self, data=None):
        if data is None:
            return self.model_object_result(value_result=[])

        results_data = []
        print("Evaluation--------------------------------------------")
        if isinstance(data, list):
            rst_ejecucion = []
            rst_sended = []
            rst_tmp = []

            tasks = [self.Predict_async(data=data_, idx=idx) for idx, data_ in enumerate(data)]
            rst_tmp = await asyncio.gather(*tasks)
            
            for idx, rst in enumerate(rst_tmp):
                
                if rst['found']:
                    results_data.append(rst)
                    if len(rst_ejecucion) > 2:
                        rst_sended.append([rst_ejecucion, idx-1])
                    rst_ejecucion.clear()
                else:
                    rst_ejecucion.append(data[idx])

            if len(rst_ejecucion) > 2:
                rst_sended.append([rst_ejecucion, len(data)])
                
            tasks = [self.Predict_async(data=rst_exec_[0], idx=rst_exec_[1]) for rst_exec_ in rst_sended]
            results_data += await asyncio.gather(*tasks)
            
        else:
            results_data = [await asyncio.create_task(self.Predict_async(data=data))]
        return [results_ for results_ in results_data if results_['found']]
    
    async def Evaluate_async2(self, data=None):
        if data is None:
            return self.model_object_result(value_result=[])

        results_data = []
        print("Evaluation--------------------------------------------")
        if isinstance(data, list):
            rst_ejecucion = []
            rst_sended = []
            rst_tmp = []

            tasks = [self.Predict_async2(data=data_, idx=idx) for idx, data_ in enumerate(data)]
            rst_tmp = await asyncio.gather(*tasks)
            
            for idx, rst in enumerate(rst_tmp):
                
                if rst['found']:
                    results_data.append(rst)
                    if len(rst_ejecucion) > 2:
                        rst_sended.append([rst_ejecucion, idx-1])
                    rst_ejecucion.clear()
                else:
                    rst_ejecucion.append(data[idx])

            if len(rst_ejecucion) > 2:
                rst_sended.append([rst_ejecucion, len(data)])
                
            tasks = [self.Predict_async2(data=rst_exec_[0], idx=rst_exec_[1]) for rst_exec_ in rst_sended]
            results_data += await asyncio.gather(*tasks)
            
        else:
            results_data = [await asyncio.create_task(self.Predict_async2(data=data))]
        print(f"--------------------------------------------{[results_['coincidences'][0]['hand_value'] for results_ in results_data if results_['found']]}")
        return [results_ for results_ in results_data if results_['found']]
    
    def Evaluate(self, data=None):
        if data is None:
            return self.model_object_result(value_result=[])

        rst_sended = []
        rst_ejecucion = []
        results_data = []
        
        if isinstance(data, list):
            for idc, data_ in enumerate(data):
                rst_tmp = self.Predict(data=data_, idx=idc)
                if rst_tmp['found']:
                    results_data.append(rst_tmp)
                    if len(rst_ejecucion) > 2:
                        rst_sended.append([rst_ejecucion, idc-1])
                    rst_ejecucion.clear()
                else: 
                    rst_ejecucion.append(data_)                    
                
            if len(rst_ejecucion) > 2:
                rst_sended.append([rst_ejecucion, len(data)])

            for idc, rst_exec_ in enumerate(rst_sended):
                results_data.append(self.Predict(data=rst_exec_[0], idx=rst_exec_[1]))
        else:
            results_data.append(self.Predict(data=data))

        return [results_  for results_ in results_data if results_['found']]

    def model_object_result(self,value_result=[], idx=-1):
        model_results = {
            'logs': [],
            'found': False,
            'coincidences': [],
            'results': [],
            'index_evaluation': idx
        }
        model_results["coincidences"] = list(filter(lambda a: a['rule_match'], value_result))
        model_results['found'] = len(model_results['coincidences'])>0
        model_results['logs'] = {
            "message": "recognition_model_execution_pass",
            "value": f"A total of {len(list(filter(lambda a: a['rule_match'], value_result)))} matching results were found",
        }
        model_results["results"] = value_result

        return model_results