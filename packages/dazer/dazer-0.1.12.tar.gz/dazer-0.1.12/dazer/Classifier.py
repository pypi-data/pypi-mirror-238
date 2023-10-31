from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from pathlib import Path
import joblib
import os
# from sklearn.inspection import permutation_importance
import pandas as pd



class Classifier:
    
    def __init__(self, X_train, y_train, X_test, y_test):
       
        self.label_encodings = {}
        
        # encode categorical columns
        categorical_columns = X_train.columns[~X_test.columns.isin(X_test._get_numeric_data().columns)]
        for col in categorical_columns:
            self.label_encodings[col] = {x: i for i, x in enumerate(X_test[col].unique())}
            X_test[col] = X_test[col].map(self.label_encodings[col])
            X_train[col] = X_train[col].map(self.label_encodings[col])
            
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        
        
    def train_test_random_forest(self,  param_grid={}, cv=10, n_jobs=-1, model_path='', verbose=1, scoring='f1', random_state=101):
        # random forest
        
        if param_grid == {}:
            param_grid = {
                        'bootstrap': [True],
                        'max_depth': [1, 2, 5, 10, 50, None],
                        'class_weight': ['balanced'],
                        'min_samples_split': [2, 4, 8],
                        'min_samples_leaf': [1, 2, 4, 8],
                        'n_estimators': [10, 100, 250, 500, 750, 1000],
                        'random_state': [random_state]
                    }
            
        rf = RandomForestClassifier()
        model = self.train(rf, param_grid = param_grid, cv = cv, n_jobs = n_jobs, verbose = verbose, scoring=scoring)
        y_pred = self.test(model)
        evals = self.eval_pred(y_pred)
        
        if model_path:
            Path(os.sep.join(model_path.split(os.sep)[:-1])).mkdir(parents=True, exist_ok=True)
            joblib.dump(model, model_path)

        return model, evals
    
    
    def train(self, model, param_grid={}, cv=10, n_jobs=-1, verbose = 1, scoring='f1'):
        model = GridSearchCV(estimator = model, param_grid = param_grid, cv = cv, n_jobs = n_jobs, verbose = verbose, scoring=scoring)
        model.fit(self.X_train, self.y_train)
        return model
    
    
    def test(self, model):
        return model.predict(self.X_test)
    
    
    def eval_pred(self, y_pred):
       clrep = classification_report(self.y_test, y_pred, target_names=None, output_dict=True)
       return {'n_samples_train': len(self.X_train), 
                'n_samples_test': len(self.X_test), 
                'accuracy': clrep['accuracy'],
                'f1': clrep['1']['f1-score'],
                'precision': clrep['1']['precision'],
                'recall': clrep['1']['recall'],
                'TNR': clrep['0']['recall'],
                }
        
        
    def get_feature_weights_random_forests(self, model_paths=[]):
        weights = []
        columns = self.X_train.columns
        for rf_path in  model_paths:
            clf = joblib.load(rf_path)
            data = list(clf.best_estimator_.feature_importances_)
            data.append(rf_path)
            weights.append(data)
            
        columns.append('model_path')
        df = pd.DataFrame(data=weights)

        df['model'] = df['model_path'].map(lambda x: x.split('/')[-1])
        return df
        
        
    # def permutation_test_random_forest(self, model_path, ratio, random_state=101):
    #     # random forest
    #     model = joblib.load(model_path)
        
    #     permutation_result = permutation_importance(
    #         model, self.X_train, self.y_train, n_repeats=10, random_state=random_state, n_jobs=5
    #     )
        
    #     return {
    #         'ratio': ratio,
    #         'dataset': self.dataset_name,
    #         'permutation_importances_mean': permutation_result.importances_mean,
    #         'permutation_importances_std': permutation_result.importances_std
    #     }