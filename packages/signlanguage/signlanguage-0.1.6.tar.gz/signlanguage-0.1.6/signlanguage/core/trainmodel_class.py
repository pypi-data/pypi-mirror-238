from signlanguage.interfaces.interfaces_model   import Itrain
import signlanguage.core.core_class             as mk
import signlanguage.models.handmodel_classV2      as hm
import pandas                      as pd
import numpy                       as np
import math

HANDMODEL_LENGHT= 51

## train model
class TrainModelPool(Itrain):
    def transform_m4(self, data=None, face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False):
        data_model = [[] for _ in range(HANDMODEL_LENGHT)]
        for idx, val in enumerate(data):
            value_model = hm.HandModel().make_model(hand_Left=val['model_hand_Left'], hand_Right=val['model_hand_Right'], points_body=val['model_body'], face_relation=face_relation, body_relation=body_relation, hand_relation=hand_relation, hand_diff_relation=hand_diff_relation)
            
            for i, value in enumerate(value_model):
                if len(value) > 0:
                    if len(data_model[i]) != len(value):
                        data_model[i] = [[] for _ in range(len(value))]
                    
                    for j, val_pos in enumerate(value):
                        data_model[i][j].append(val_pos[0])
        return data_model

    def Train_models2(self, data=None, face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False):
        try:

            if data is None:
                return None
            
            #model4
            model_evaluation = []
            data_model = self.transform_m4(data=data,face_relation=face_relation,body_relation=body_relation,hand_relation=hand_relation, hand_diff_relation=hand_diff_relation)
            
            for i, dm in enumerate(data_model):
                if len(dm) > 0:
                    df = pd.DataFrame(dm, columns=[str(i) for i in range(len(dm[0]))]).transpose()
                    data_Train = df.to_numpy()
                    n_clusters = df.shape[1]
                    #init core pool
                    KmeanModel = mk.CorePool(n_clusters=n_clusters)
                    #train core pool
                    KmeanModel.fit(data_Train)
                    #add core pool, matrix values
                    model_evaluation.append(KmeanModel)
                else:
                    model_evaluation.append(None)
            
            
            """ #model3
            data_model = [[] for _ in range(HANDMODEL_LENGHT)]

            for idx, val in enumerate(data):
                value_model = hm.HandModel().make_model(hand_Left=val['model_hand_Left'], hand_Right=val['model_hand_Right'], points_body=val['model_body'], face_relation=face_relation, body_relation=body_relation, hand_relation=hand_relation, hand_diff_relation=hand_diff_relation)
                
                for i, value in enumerate(value_model):
                    if len(value) > 0:
                        if len(data_model[i]) != len(value):
                            data_model[i] = [[] for _ in range(len(value))]
                        
                        for j, val_pos in enumerate(value):
                            data_model[i][j].extend([val_pos])
                            
            for i, dm in enumerate(data_model):
                if len(dm) > 0:
                    KmeansModel = []
                    for i, dm_pos in enumerate(dm):
                        if len(dm_pos) <= 0:
                            break
                        #configure values
                        data_index = np.array(dm_pos).T
                        df_real = pd.DataFrame(data_index).transpose()
                        n_clusters = min(len(dm), round((len(data)/3))) #determinar la cantidad de clusters
                        #Retrieve data
                        data_Train = np.array(df_real.values.tolist())
                        #init core pool
                        KmeanModel = mk.CorePool(n_clusters=n_clusters)
                        #train core pool
                        KmeanModel.fit(data_Train)
                        #add core pool, matrix values
                        KmeansModel.append(KmeanModel)
                    model_evaluation.append(KmeansModel)
                else:
                    model_evaluation.append([])
            """
            
            return model_evaluation
        except Exception as e:
            print("Error Ocurrido [Train model], Mensaje: {0}".format(str(e)))
            return None

    def Train_models(self, data=None, face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False):
        try:

            if data is None:
                return None
            
            model_evaluation = []
            
            #model3
            data_model = [[] for _ in range(HANDMODEL_LENGHT)]

            for idx, val in enumerate(data):
                value_model = hm.HandModel().make_model(hand_Left=val['model_hand_Left'], hand_Right=val['model_hand_Right'], points_body=val['model_body'], face_relation=face_relation, body_relation=body_relation, hand_relation=hand_relation, hand_diff_relation=hand_diff_relation)
                
                for i, value in enumerate(value_model):
                    if len(value) > 0:
                        if len(data_model[i]) != len(value):
                            data_model[i] = [[] for _ in range(len(value))]
                        
                        for j, val_pos in enumerate(value):
                            data_model[i][j].extend([val_pos])
                            
            for i, dm in enumerate(data_model):
                if len(dm) > 0:
                    KmeansModel = []
                    for i, dm_pos in enumerate(dm):
                        if len(dm_pos) <= 0:
                            break
                        #configure values
                        data_index = np.array(dm_pos).T
                        df_real = pd.DataFrame(data_index).transpose()
                        n_clusters = min(len(dm), round((len(data)/3))) #determinar la cantidad de clusters
                        #Retrieve data
                        data_Train = np.array(df_real.values.tolist())
                        #init core pool
                        KmeanModel = mk.CorePool(n_clusters=n_clusters)
                        #train core pool
                        KmeanModel.fit(data_Train)
                        #add core pool, matrix values
                        KmeansModel.append(KmeanModel)
                    model_evaluation.append(KmeansModel)
                else:
                    model_evaluation.append([])
            
            return model_evaluation
        except Exception as e:
            print("Error Ocurrido [Train model], Mensaje: {0}".format(str(e)))
            return None

## train model
class TrainModelClassifier(Itrain):
    def getOpposite(self, arrBucket=None):
        if arrBucket is None:
            return None

        arrBucketN = []
        OppFound = set()
        labels = []
        arrBucketOpp = []

        arr_first = [1 for _ in range(len(arrBucket[0]))]
        arrBucketN.append(arr_first)
        labels.append(1)
        OppFound.add(tuple(arr_first))

        for arr in arrBucket:
            if (sum(arr)/len(arr))>0.5:
                arr_Tuple = tuple(arr)
                if arr_Tuple not in OppFound:
                    arrBucketN.append(list(arr_Tuple))
                    OppFound.add(arr_Tuple)
                    labels.append(1)

        for arr in arrBucketN:
            arrOpp = [1 if bit == 0 else 0 for bit in arr]
            arrOpp_Tuple = tuple(arrOpp)

            if arrOpp_Tuple not in OppFound:
                arrBucketOpp.append(list(arrOpp_Tuple))
                OppFound.add(arrOpp_Tuple)
                labels.append(0)

        print(len(arrBucketN), len(arrBucketOpp), len(labels))

        return arrBucketN, arrBucketOpp, labels
    
    def Train_models(self, data=None):
        try:
            if data is None:
                return None
            # Generate opposite data
            data_model, data_model_opposite, labels = self.getOpposite(arrBucket=data)
            # Generate X,Y Values training
            
            if len(data_model[0])==0:
                return None
            
            if len(data_model) < (0.8*len(data)):
                return None

            X_Train = data_model + data_model_opposite
            Y_Train = labels
            # configure model
            Model_Classification = mk.CoreClass(neurals_count=len(X_Train), dim_values=len(data_model[0]), epochs=len(X_Train)*10)
            Model_Classification.compile()
            Model_Classification.fit(X=X_Train, Y=Y_Train)
            
            # return model
            return Model_Classification
        
        except Exception as e:
            print("Error Ocurrido [Train model], Mensaje: {0}".format(str(e)))
            return None

## train model
class TrainModelMovement(Itrain):
    def Train_models(self, data=None):
        try:

            if data is None:
                return None
            
            
            model_evaluation = []
            data_model = [[] for _ in range(6)]
           
            for val in data:
                value_model = hm.HandModel().make_model_body(hand_Left=val['model_hand_Left'], hand_Right=val['model_hand_Right'], points_body=val['model_body'])
                for i, value in enumerate(value_model):
                    if len(value) > 0:
                        if not len(data_model[i]) == len(value):
                            data_model[i] = [[] for _ in range(len(value))]
                        for j, val_pos in enumerate(value):
                            data_model[i][j].extend([val_pos])

            for i, dm in enumerate(data_model):
                if len(dm) > 0:
                    KmeansModel = []
                    for i, dm_pos in enumerate(dm):
                        
                        if len(dm_pos) <= 0:
                            break
                        #configure values
                        data_index = np.array(dm_pos).T
                        df_real = pd.DataFrame(data_index).transpose()
                        n_clusters = min(len(dm), round((len(data)/3))) #determinar la cantidad de clusters
                        #Retrieve data
                        data_Train = np.array(df_real.values.tolist())
                        #init core pool
                        KmeanModel = mk.CorePool(n_clusters=n_clusters)
                        #train core pool
                        KmeanModel.fit(data_Train)
                        #add core pool, matrix values
                        KmeansModel.append(KmeanModel)
                    model_evaluation.append(KmeansModel)
                else:
                    model_evaluation.append([])

            return model_evaluation
        except Exception as e:
            print("Error Ocurrido [Train model Movement], Mensaje: {0}".format(str(e)))
            return None
        

## train model
class TrainModelStates(Itrain):
    # Generar secuencias que cumplen con las restricciones
    def sequence_generator(self, lenght_valuation=None, lenght_states=None):
        
        if None in (lenght_states, lenght_valuation):
            return None

        secuencia = [-1 for _ in range(lenght_valuation)]
        secuencia[0] = np.random.randint(0, lenght_states)  # Estado inicial
        
        for i in range(lenght_valuation - 1):
            if i == 0:
                continue
            nuevo_estado = np.random.randint(1, lenght_states)  # Estados repetibles
            secuencia[i] = nuevo_estado
        
        secuencia[lenght_valuation-1] = np.random.choice([0, lenght_states])  # Estado final

        return secuencia

    # Generar secuencias que no cumplen con las restricciones
    def no_sequence_generator(self, lenght_valuation=None, lenght_states=None):
        
        if None in (lenght_states, lenght_valuation):
            return None
        
        secuencia = [-1 for _ in range(lenght_valuation)] 
        secuencia[0] = np.random.randint(0, lenght_states)  # Estado inicial 
        
        for i in range(lenght_valuation - 1):
            if i == 0:
                continue
            nuevo_estado = np.random.randint(1, lenght_states)  # Estados repetibles
            secuencia[i] = nuevo_estado
        
        secuencia[lenght_valuation-1] = np.random.randint(1, (lenght_states-1))  # Estado final en medio
        
        return secuencia
    

    def Train_models(self, data=None, lenght_valuation=None):
        try:
            if None in (data, lenght_valuation):
                return None
        
            # Generate sequence data
            num_datos     = math.comb(data, lenght_valuation)
            data_model    = [self.sequence_generator(lenght_valuation=lenght_valuation,lenght_states=data)  for _ in range(num_datos)]
            data_no_model = [self.no_sequence_generator(lenght_valuation=lenght_valuation,lenght_states=data)  for _ in range(num_datos)]
            labels        = np.array([1] * num_datos + [0] * num_datos)
            data_operations = {
                data < 20: 3000,
                20 <= data < 40: 2500,
            }
            num_datos = data_operations.get(True, 2000)
            # define X,Y Values training 
            if None in (data_model, data_no_model):
                return None
            
            X_Train = data_model + data_no_model
            Y_Train = labels

            # Conversion values
            indx = np.arange(len(X_Train))
            np.random.shuffle(indx)
            X_Train = [X_Train[i] for i in indx]
            Y_Train = Y_Train[indx]

            
            Y_Train = np.array(Y_Train)
            X_Train = np.array(X_Train)

            # configure model
            Model_State = mk.CoreClass(neurals_count=len(X_Train), dim_values=len(X_Train[0]), epochs=num_datos)
            Model_State.compile()
            Model_State.fit(X=X_Train, Y=Y_Train)
            #Model_State = mk.CoreState(states_qty=data)
            #Model_State.fit(X=X_Train, Y=Y_Train)
            
            # return model
            return Model_State
        
        except Exception as e:
            print("Error Ocurrido [Train model - States], Mensaje: {0}".format(str(e)))
            return None