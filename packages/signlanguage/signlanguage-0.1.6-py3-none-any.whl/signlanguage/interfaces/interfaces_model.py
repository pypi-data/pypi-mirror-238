import abc

## interface models - Kmeans core
class IKmeans:
    @abc.abstractmethod
    def fit(self, data=[]) -> object:
        raise NotImplementedError
    
    @abc.abstractmethod
    def predict(self) -> object:
        raise NotImplementedError
    
    @abc.abstractmethod
    def predict_min(self) -> object:
        raise NotImplementedError
    
    @abc.abstractmethod
    def predict_cluster(self) -> object:
        raise NotImplementedError
    
## interface models - neural core
class INeural:
    @abc.abstractmethod
    def fit(self, data=[]) -> object:
        raise NotImplementedError
    
    @abc.abstractmethod
    def predict(self) -> object:
        raise NotImplementedError
    
    @abc.abstractmethod
    def compile(self) -> object:
        raise NotImplementedError

## interface models - general
class Imodel:
    @abc.abstractmethod
    def evaluation(self, model_evaluation=None, data=None, face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False) -> object:
        raise NotImplementedError
    

class Itrain:
    @abc.abstractmethod
    def Train_models(self, data=None) -> object:
        raise NotImplementedError

class ITrace:
    @abc.abstractmethod
    def exec_model(self, data=None) -> object:
        raise NotImplementedError
    
    @abc.abstractmethod
    def train_model(self, data=None) -> object:
        raise NotImplementedError