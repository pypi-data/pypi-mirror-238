import numpy as np
import numpy.random as npr
import pandas as pd
import logging


class Subsampler:
    
    def __init__(self, df_data, columns_keep_ratio, allowed_deviation=.2):

        # df_ratio = df_ratio.dropna(subset=[column_target])  # remove entries in target column with NaN
        
        self.df_data = df_data  # complete input data
        self.df_ratio = df_data[columns_keep_ratio]  # the dataframe with the columns in which to keep the ratio
        self.allowed_deviation = allowed_deviation  # the allowed deviation from the ratio in the subsampled dataframe in the columns 'columns_keep_ratio' from 0 to 1
        self.categorical_columns = self.df_ratio.columns[~self.df_ratio.columns.isin(self.df_ratio._get_numeric_data().columns)]
        
        # df to compare mean deviation against when subsampling
        self.df_mean_orig = None  # will be set in preprocessing in "_make_mean_reference"

        # attributes to be filled by methods
        self._test_df = None  # contains test data, created by 'extract_test' if test_size > 0

        # init steps
        self._preprocess()
        
    def _normalize_numerical_columns(self):
        # normalize columns
        for col in self.df_ratio:
            if self.df_ratio[col].dtype in ['float64', 'int64', 'bool']:
                self.df_ratio.loc[:, col] = self.column_normalize(self.df_ratio[col])
                
    def _make_mean_reference(self):
        df = self.df_ratio
        
        if len(self.categorical_columns):
            df = df.drop(self.categorical_columns, axis=1).join(pd.get_dummies(df[self.categorical_columns]))
            
        self.df_mean_orig = df.mean()
        
        
    def _preprocess(self):
        self._normalize_numerical_columns()
        # important to make mean reference after normalization
        self._make_mean_reference()
            
    
    def extract_test(self, test_size=.2, random_state=101):
        """_summary_

        Args:
            test_size (float, optional): percentage of datapoints in test dataset which will be excluded from subsampling. Defaults to .2.
            random_state (int, optional): the random seed. Defaults to 101.

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        
        if type(test_size) not in [int, float] or not 1 >= test_size >= 0:
            raise ValueError('Parameter "test_size" has to be a value in the range from 0 to 1.')
        
        # return empty dataframe with columns 
        if test_size == 0:
            return pd.DataFrame(columns=self.df_data.columns)
        # subsample with equal data distributions
        self._test_df = self.subsample(test_size, random_state=random_state)
        if self._test_df is None:
            return None
        
        # remove test data points from df_data to exclude it in the subsampling process
        self.df_ratio = self.df_ratio[~self.df_ratio.index.isin(self._test_df.index)]
        
        return self._test_df
        
    
    def subsample(self, subsample_factor, random_state=101, raise_exception=False):
        npr.seed(random_state)
        # subsample each label category inidividually to keep intrinsic ratios
        
        # use one hot encoding to calculate the distribution of the categorical features
        if len(self.categorical_columns):
            df_ratio_one_hot_encoded = self.df_ratio.drop(self.categorical_columns, axis=1).join(pd.get_dummies(self.df_ratio[self.categorical_columns]))
        else:
            df_ratio_one_hot_encoded = self.df_ratio
        df_subsampled = df_ratio_one_hot_encoded.sample(frac=subsample_factor, replace=False, random_state=random_state)

        # check for allowed divergence
        for col, col_mean in df_subsampled.mean().items():
            deviation = np.abs(self.df_mean_orig[col] - col_mean)
            if deviation > self.allowed_deviation:
                message = f'Could not find subsample with seed {random_state} due to mean deviation {deviation} in column {col}.'
                if raise_exception:
                    raise Exception(message)
                else:
                    logging.warning(message)
                    return None
            
        indices = set(df_subsampled.index)

        df_subsampled = self.df_data[self.df_data.index.isin(indices)]

        return df_subsampled
   
    
    @staticmethod
    def column_normalize(col):
        col_min = col.min()
        col_max = col.max()
        if col_min == col_max == 0:
            # all 0s
            return col
        return (col - col_min) / (col_max - col_min)

