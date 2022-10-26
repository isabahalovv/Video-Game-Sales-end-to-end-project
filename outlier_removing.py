import numpy as np
import pandas as pd

class ZscoreMethod:
    def __init__(self, data, target):
        self.data = data.copy()
        self.cols = self.data.select_dtypes(exclude='O')
        self.target = target.copy()
        
    def remove_outliers(self):
        print('\033[1m'+'Data shape before:'+'\033[0m', self.data.shape)
        print('\033[1m'+'Target shape before:'+'\033[0m', self.target.shape)
        
        for col in self.cols:

            if self.data[col].nunique() > 5:
            
                mean = self.data[col].mean()
                std = self.data[col].std()
                lower_bound = mean - 3*std
                upper_bound = mean + 3*std

                outliers = self.data[(self.data[col] < lower_bound) | (self.data[col] > upper_bound)].index
                self.data.drop(index = outliers, axis=0, inplace=True)
                self.target.drop(index = outliers, axis=0, inplace=True)
                
                print('='*50)
                print('Col name : {}\nMean : {}\nStd : {}\nBounds : {} and {}'.format(col, round(mean,3), round(std,3), round(lower_bound, 3), round(upper_bound, 3)))
                print(f"Outliers removed : {len(outliers)}")
                
        print('\033[1m'+'Data shape after:'+'\033[0m', self.data.shape)
        print('\033[1m'+'Target shape after:'+'\033[0m', self.target.shape)
                    
        return self.data, self.target




class IQR_Method:
    def __init__(self, data, target, q1=25, q3=75, coeff=1.5):
        self.data = data.copy()
        self.target = target.copy()
        self.columns = self.data.select_dtypes(exclude='O')
        self.q1 = q1
        self.q3 = q3
        self.coeff = coeff
        self.size = None
        self.outliers = []
        
    def _calculate_bounds(self, column):
        Q1,Q3 = np.percentile(self.data[column] , [self.q1,self.q3])
        IQR = Q3 - Q1
        upper_bound = Q3+self.coeff*IQR
        lower_bound = Q1-self.coeff*IQR
        return (lower_bound, upper_bound) 

    def _remove_outliers(self, column):
        self.outliers = []
        lb, ub = self._calculate_bounds(column)
        self.outliers = self.data[column][(self.data[column] > ub) | (self.data[column] < lb)].index
        self.data.drop(index = self.outliers, axis=0, inplace=True)
        self.size = len(self.outliers)
        return self.data
        
    def remove_all(self):
        print('\033[1m'+'Data shape before:'+'\033[0m', self.data.shape)
        print('\033[1m'+'Target shape before:'+'\033[0m', self.target.shape)
        for col in self.columns:
            if self.data[col].nunique() > 5:
                print('\033[1m'+'Feature: '+col.title()+'\033[0m')
                self._remove_outliers(col)
                self.target.drop(index=self.outliers, axis=0, inplace=True)
                print(f"Outliers removed: {self.size}")
                print('~'*100)
        print('\033[1m'+'Data shape after:'+'\033[0m', self.data.shape)
        print('\033[1m'+'Target shape after:'+'\033[0m', self.target.shape)
        
        return self.data, self.target       