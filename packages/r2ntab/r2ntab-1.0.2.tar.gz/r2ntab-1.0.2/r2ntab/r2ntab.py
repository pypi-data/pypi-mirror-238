import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import copy

from tqdm import tqdm
from sklearn.metrics import accuracy_score, roc_auc_score

import math
import pandas as pd
import torch.nn.utils.prune as prune
import os
import itertools
import pickle
import torchvision


from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder, KBinsDiscretizer, LabelEncoder, LabelBinarizer
from sklearn.model_selection import train_test_split, KFold, StratifiedKFold

from numpy import ndarray
from pandas import DataFrame, Series
from sklearn.base import TransformerMixin
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

# noinspection PyPep8Naming
class FeatureBinarizer(TransformerMixin):
    '''Transformer for binarizing categorical and ordinal features.
    
    For use with BooleanRuleCG, LogisticRuleRegression and LinearRuleRegression
    '''
    def __init__(self, colCateg=[], numThresh=9, negations=False, threshStr=False, returnOrd=False, **kwargs):
        """
        Args:
            colCateg (list): Categorical features ('object' dtype automatically treated as categorical)
            numThresh (int): Number of quantile thresholds used to binarize ordinal variables
            negations (bool): Append negations
            threshStr (bool): Convert thresholds on ordinal features to strings
            returnOrd (bool): Also return standardized ordinal features
        """
        # List of categorical columns
        if type(colCateg) is pd.Series:
            self.colCateg = colCateg.tolist()
        elif type(colCateg) is not list:
            self.colCateg = [colCateg]
        else:
            self.colCateg = colCateg
        # Number of quantile thresholds used to binarize ordinal features
        self.numThresh = numThresh
        self.thresh = {}
        # whether to append negations
        self.negations = negations
        # whether to convert thresholds on ordinal features to strings
        self.threshStr = threshStr
        # Also return standardized ordinal features
        self.returnOrd = returnOrd

    def fit(self, X):
        '''Fit FeatureBinarizer to data
        
        Args:
            X (DataFrame): Original features
        Returns:
            FeatureBinarizer: Self
            self.maps (dict): Mappings for unary/binary columns
            self.enc (dict): OneHotEncoders for categorical columns
            self.thresh (dict(array)): Thresholds for ordinal columns
            self.NaN (list): Ordinal columns containing NaN values
            self.ordinal (list): Ordinal columns
            self.scaler (StandardScaler): StandardScaler for ordinal columns
        '''
        data = X
        # Quantile probabilities
        quantProb = np.linspace(1. / (self.numThresh + 1.), self.numThresh / (self.numThresh + 1.), self.numThresh)
        # Initialize
        maps = {}
        enc = {}
        thresh = {}
        NaN = []
        if self.returnOrd:
            ordinal = []

        # Iterate over columns
        for c in data:
            # number of unique values
            valUniq = data[c].nunique()

            # Constant or binary column
            if valUniq <= 2:
                # Mapping to 0, 1
                maps[c] = pd.Series(range(valUniq), index=np.sort(data[c].dropna().unique()))

            # Categorical column
            elif (c in self.colCateg) or (data[c].dtype == 'object'):
                # OneHotEncoder object
                enc[c] = OneHotEncoder(sparse=False, dtype=int, handle_unknown='ignore')
                # Fit to observed categories
                enc[c].fit(data[[c]])

            # Ordinal column
            elif np.issubdtype(data[c].dtype, np.integer) | np.issubdtype(data[c].dtype, np.floating):
                # Few unique values
                if valUniq <= self.numThresh + 1:
                    # Thresholds are sorted unique values excluding maximum
                    thresh[c] = np.sort(data[c].unique())[:-1]
                # Many unique values
                else:
                    # Thresholds are quantiles excluding repetitions
                    thresh[c] = data[c].quantile(q=quantProb).unique()
                if data[c].isnull().any():
                    # Contains NaN values
                    NaN.append(c)
                if self.returnOrd:
                    ordinal.append(c)

            else:
                print(("Skipping column '" + str(c) + "': data type cannot be handled"))
                continue

        self.maps = maps
        self.enc = enc
        self.thresh = thresh
        self.NaN = NaN
        if self.returnOrd:
            self.ordinal = ordinal
            # Fit StandardScaler to ordinal features
            self.scaler = StandardScaler().fit(data[ordinal])
        return self

    def transform(self, X):
        '''Binarize features
        
        Args:
            X (DataFrame): Original features
        Returns:
            A (DataFrame): Binarized features with MultiIndex column labels
            Xstd (DataFrame, optional): Standardized ordinal features
        '''
        data = X
        maps = self.maps
        enc = self.enc
        thresh = self.thresh
        NaN = self.NaN

        # Initialize dataframe
        A = pd.DataFrame(index=data.index,
                         columns=pd.MultiIndex.from_arrays([[], [], []], names=['feature', 'operation', 'value']))

        # Iterate over columns
        for c in data:
            # Constant or binary column
            if c in maps:
                # Rename values to 0, 1
                A[(str(c), '', '')] = data[c].map(maps[c]).astype(int)
                if self.negations:
                    A[(str(c), 'not', '')] = 1 - A[(str(c), '', '')]

            # Categorical column
            elif c in enc:
                # Apply OneHotEncoder
                Anew = enc[c].transform(data[[c]])
                Anew = pd.DataFrame(Anew, index=data.index, columns=enc[c].categories_[0].astype(str))
                if self.negations:
                    # Append negations
                    Anew = pd.concat([Anew, 1 - Anew], axis=1, keys=[(str(c), '=='), (str(c), '!=')])
                else:
                    Anew.columns = pd.MultiIndex.from_product([[str(c)], ['=='], Anew.columns])
                # Concatenate
                A = pd.concat([A, Anew], axis=1)

            # Ordinal column
            elif c in thresh:
                # Threshold values to produce binary arrays
                Anew = (data[c].values[:, np.newaxis] <= thresh[c]).astype(int)
                if self.negations:
                    # Append negations
                    Anew = np.concatenate((Anew, 1 - Anew), axis=1)
                    ops = ['<=', '>']
                else:
                    ops = ['<=']
                # Convert to dataframe with column labels
                if self.threshStr:
                    Anew = pd.DataFrame(Anew, index=data.index,
                                        columns=pd.MultiIndex.from_product([[str(c)], ops, thresh[c].astype(str)]))
                else:
                    Anew = pd.DataFrame(Anew, index=data.index,
                                        columns=pd.MultiIndex.from_product([[str(c)], ops, thresh[c]]))
                if c in NaN:
                    # Ensure that rows corresponding to NaN values are zeroed out
                    indNull = data[c].isnull()
                    Anew.loc[indNull] = 0
                    # Add NaN indicator column
                    Anew[(str(c), '==', 'NaN')] = indNull.astype(int)
                    if self.negations:
                        Anew[(str(c), '!=', 'NaN')] = (~indNull).astype(int)
                # Concatenate
                A = pd.concat([A, Anew], axis=1)

            else:
                print(("Skipping column '" + str(c) + "': data type cannot be handled"))
                continue

        if self.returnOrd:
            # Standardize ordinal features
            Xstd = self.scaler.transform(data[self.ordinal])
            Xstd = pd.DataFrame(Xstd, index=data.index, columns=self.ordinal)
            # Fill NaN with mean (which is now zero)
            Xstd.fillna(0, inplace=True)
            return A, Xstd
        else:
            return A

def predefined_dataset(name, binary_y=False):
    """
    Define how to read specific datasets and return structured X and Y data.
    
    Args
        name (str): the name of the dataset to read.
        binary_y (bool): if True, force the dataset to only have two classes.
        
    Returns
        table_X (DataFrame): instances, values can be strings or numbers.
        table_Y (DataFrame): labels, values can be strings or numbers.
        categorical_cols (list): A list of column names that are categorical data. 
        numerical_cols (list): A list of column names that are numerical data.
    """
    
    table = pd.read_csv(name, header=0, na_values='?', skipinitialspace=True).dropna()
    table_X = table.iloc[:, :-1].copy()
    table_Y = table.iloc[:, -1].copy()
    categorical_cols = None
    numerical_cols = None

    return table_X, table_Y, categorical_cols, numerical_cols

def transform_dataset(name, method='ordinal', negations=False, labels='ordinal'):
    """
    Transform values in datasets (from predefined_dataset) into real numbers or binary numbers.
    
    Args
        name (str): the name of the dataset.
        method (str): specify how the instances are encoded:
            'origin': encode categorical features as integers and leave the numerical features as they are (float).
            'ordinal': encode all features as integers; numerical features are discretized into intervals.
            'onehot': one-hot encode the integer features transformed using 'ordinal' method.
            'onehot-compare': one-hot encode the categorical features just like how they are done in 'onehot' method; 
                one-hot encode numerical features by comparing them with different threhsolds and encode 1 if they are smaller than threholds. 
        negations (bool): whether append negated binary features; only valid when method is 'onehot' or 'onehot-compare'. 
        labels (str): specify how the labels are transformed.
            'ordinal': output Y is a 1d array of integer values ([0, 1, 2, ...]); each label is an integer value.
            'binary': output Y is a 1d array of binary values ([0, 1, 0, ...]); each label is forced to be a binary value (see predefined_dataset).
            'onehot': output Y is a 2d array of one-hot encoded values ([[0, 1, 0], [1, 0, 0], [0, 0, 1]]); each label is a one-hot encoded 1d array.
    
    Return
        X (DataFrame): 2d float array; transformed instances.
        Y (np.array): 1d or 2d (labels='onehot') integer array; transformed labels;.
        X_headers (list|dict): if method='ordinal', a dict where keys are features and values and their categories; otherwise, a list of binarized features.
        Y_headers (list): the names of the labels, indexed by the values in Y.
    """
    
    METHOD = ['origin', 'ordinal', 'onehot', 'onehot-compare']
    LABELS = ['ordinal', 'binary', 'onehot']
    if method not in METHOD:
        raise ValueError(f'method={method} is not a valid option. The options are {METHOD}')
    if labels not in LABELS:
        raise ValueError(f'labels={labels} is not a valid option. The options are {LABELS}')
    
    table_X, table_Y, categorical_cols, numerical_cols = predefined_dataset(name, binary_y=labels == 'binary')

    # By default, columns with object type are treated as categorical features and rest are numerical features
    # All numerical features that have fewer than 5 unique values should be considered as categorical features
    if categorical_cols is None:
        categorical_cols = list(table_X.columns[(table_X.dtypes == np.dtype('O')).to_numpy().nonzero()[0]])
    if numerical_cols is None:
        numerical_cols = [col for col in table_X.columns if col not in categorical_cols and np.unique(table_X[col].to_numpy()).shape[0] > 5]
        categorical_cols = [col for col in table_X.columns if col not in numerical_cols]
            
    # Fill categorical nan values with most frequent value and numerical nan values with the mean value
    if len(categorical_cols) != 0:
        imp_cat = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
        table_X[categorical_cols] = imp_cat.fit_transform(table_X[categorical_cols])
    if len(numerical_cols) != 0:
        imp_num = SimpleImputer(missing_values=np.nan, strategy='mean')
        table_X[numerical_cols] = imp_num.fit_transform(table_X[numerical_cols])
        
    if np.nan in table_X or np.nan in table_Y:
        raise ValueError('Dataset should not have nan value!')
        
    # Encode instances
    X = table_X.copy()
    
    col_categories = []
    if method in ['origin', 'ordinal'] and len(categorical_cols) != 0:
        # Convert categorical strings to integers that represent different categories
        ord_enc = OrdinalEncoder()
        X[categorical_cols] = ord_enc.fit_transform(X[categorical_cols])
        col_categories = {col: list(categories) for col, categories in zip(categorical_cols, ord_enc.categories_)}

    col_intervals = []
    if method in ['ordinal', 'onehot'] and len(numerical_cols) != 0:
        # Discretize numerical values to integers that represent different intervals
        kbin_dis = KBinsDiscretizer(encode='ordinal', strategy='kmeans')
        X[numerical_cols] = kbin_dis.fit_transform(X[numerical_cols])
        col_intervals = {col: [f'({intervals[i]:.2f}, {intervals[i+1]:.2f})' for i in range(len(intervals) - 1)] for col, intervals in zip(numerical_cols, kbin_dis.bin_edges_)}

        if method in ['onehot']:
            # Make numerical values to interval strings so that FeatureBinarizer can process them as categorical values
            for col in numerical_cols:
                X[col]  = np.array(col_intervals[col]).astype('object')[X[col].astype(int)]

    if method in ['onehot', 'onehot-compare']:
        # One-hot encode categorical values and encode numerical values by comparing with thresholds
        fb = FeatureBinarizer(colCateg=categorical_cols, negations=negations)
        X = fb.fit_transform(X)
    
    if method in ['origin']:
        # X_headers is a list of features
        X_headers = [column for column in X.columns]
    if method in ['ordinal']:
        # X_headers is a dict where keys are features and values and their categories
        X_headers = {col: col_categories[col] if col in col_categories else col_intervals[col] for col in table_X.columns}
    else:
        # X_headers is a list of binarized features
        X_headers = ["".join(map(str, column)) for column in X.columns]
        
    if method not in ['origin']:
        X = X.astype(int)
    
    # Encode labels
    le = LabelEncoder()
    Y = le.fit_transform(table_Y).astype(int)
    Y_headers = le.classes_
    if labels == 'onehot':
        lb = LabelBinarizer()
        Y = lb.fit_transform(Y)
    
    return X, Y, X_headers, Y_headers

def split_dataset(X, Y, test=0.2, shuffle=None):    
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=test, random_state=shuffle)
    
    return X_train, X_test, Y_train, Y_test

def kfold_dataset(X, Y, k=5, shuffle=None):
    kf = StratifiedKFold(n_splits=k, shuffle=bool(shuffle), random_state=shuffle)
    datasets = [(X.iloc[train_index], X.iloc[test_index], Y[train_index], Y[test_index]) 
                for train_index, test_index in kf.split(X, Y if len(Y.shape) == 1 else Y.argmax(1))]
    
    return datasets

def nested_kfold_dataset(X, Y, outer_k=5, inner_k=5, shuffle=None):
    inner_kf = StratifiedKFold(n_splits=inner_k, shuffle=bool(shuffle), random_state=shuffle)
    
    datasets = []
    for dataset in kfold_dataset(X, Y, k=outer_k, shuffle=shuffle):
        X_train_valid, X_test, Y_train_valid, Y_test = dataset
        
        nested_datasets = []
        for train_index, valid_index in inner_kf.split(
            X_train_valid, Y_train_valid if len(Y.shape) == 1 else Y_train_valid.argmax(1)):
            X_train = X.iloc[train_index]
            X_valid = X.iloc[valid_index]
            Y_train = Y[train_index]
            Y_valid = Y[valid_index]
            nested_datasets.append([X_train, X_valid, Y_train, Y_valid])
        datasets.append([X_train_valid, X_test, Y_train_valid, Y_test, nested_datasets])
    
    return datasets

class RuleFunction(torch.autograd.Function):
    '''
    The autograd function used in the Rules Layer.
    The forward function implements the equation (1) in the paper.
    The backward function implements the gradient of the foward function.
    '''
    @staticmethod
    def forward(ctx, input, weight, bias):
        ctx.save_for_backward(input, weight, bias)

        output = input.mm(weight.t())
        output = output + bias.unsqueeze(0).expand_as(output)
        output = output - (weight * (weight > 0)).sum(-1).unsqueeze(0).expand_as(output)
        return output
    
    @staticmethod
    def backward(ctx, grad_output):
        input, weight, bias = ctx.saved_tensors

        grad_input = grad_output.mm(weight)
        grad_weight = grad_output.t().mm(input) - grad_output.sum(0).unsqueeze(1).expand_as(weight) * (weight > 0)
        grad_bias = grad_output.sum(0)
        grad_bias[(bias >= 1) * (grad_bias < 0)] = 0

        return grad_input, grad_weight, grad_bias
    
class LabelFunction(torch.autograd.Function):
    '''
    The autograd function used in the OR Layer.
    The forward function implements the equations (4) and (5) in the paper.
    The backward function implements the standard STE estimator.
    '''
    
    @staticmethod
    def forward(ctx, input, weight, bias):
        ctx.save_for_backward(input, weight, bias)

        output = input.mm((weight.t() > 0).float())
        output += bias.unsqueeze(0).expand_as(output)
        
        return output
    
    @staticmethod
    def backward(ctx, grad_output):
        input, weight, bias = ctx.saved_tensors

        grad_input = grad_output.mm(weight)
        grad_weight = grad_output.t().mm(input)
        grad_bias = grad_output.sum(0)

        return grad_input, grad_weight, grad_bias
    
class Binarization(torch.autograd.Function):
    '''
    The autograd function for the binarization activation in the Rules Layer.
    The forward function implements the equations (2) in the paper. Note here 0.999999 is used to cancel the rounding error.
    The backward function implements the STE estimator with equation (3) in the paper.
    '''
    
    @staticmethod
    def forward(ctx, input):
        ctx.save_for_backward(input)
        output = (input > 0.999999).float()
        
        return output

    @staticmethod
    def backward(ctx, grad_output):
        input, = ctx.saved_tensors
        grad_input = grad_output.clone()
        grad_input[(input < 0)] = 0
        grad_input[(input >= 1) * (grad_output < 0)] = 0

        return grad_input

def sparse_linear(name):
    if name == 'linear':
        return Linear
    elif name == 'l0':
        return L0Linear
    elif name == 'reweight':
        return ReweightLinear
    else:
        raise ValueError(f'{name} linear type not supported.')

class Linear(nn.Linear):
    def __init__(self, in_features, out_features,  bias=True, linear=F.linear, **kwargs):
        super(Linear, self).__init__(in_features, out_features, bias=bias, **kwargs)
        
        self.linear = linear
        
    def forward(self, input):
        output = self.linear(input, self.weight, self.bias)
        
        return output
    
    def sparsity(self):
        sparsity = (self.weight == 0).float().mean().item()
        
        return sparsity
    
    def masked_weight(self):
        masked_weight = self.weight
        
        return masked_weight
    
    def regularization(self):
        regularization = 0
        
        return regularization

class L0Linear(nn.Linear):
    def __init__(self, in_features, out_features,  bias=True, linear=F.linear, loc_mean=0, loc_sdev=0.01, 
                 beta=2 / 3, gamma=-0.1, zeta=1.1, fix_temp=True, **kwargs):
        super(L0Linear, self).__init__(in_features, out_features, bias=bias, **kwargs)
        
        self._size = self.weight.size()
        self.loc = nn.Parameter(torch.zeros(self._size).normal_(loc_mean, loc_sdev))
        self.temp = beta if fix_temp else nn.Parameter(torch.zeros(1).fill_(beta))
        self.register_buffer("uniform", torch.zeros(self._size))
        self.gamma = gamma
        self.zeta = zeta
        self.gamma_zeta_ratio = math.log(-gamma / zeta)
        self.linear = linear
        
        self.penalty = 0

    def forward(self, input):
        mask, self.penalty = self._get_mask()
        masked_weight = self.weight * mask
        output = self.linear(input, masked_weight, self.bias)
        
        return output
    
    def sparsity(self):
        sparsity = (self.masked_weight() == 0).float().mean().item()
        
        return sparsity
    
    def masked_weight(self):
        mask, _ = self._get_mask()
        masked_weight = self.weight * mask
        
        return masked_weight
    
    def regularization(self, mean=True, axis=None):
        regularization = self.penalty
        if mean:
            regularization = regularization.mean() if axis == None else regularization.mean(axis)

        return regularization
    
    def _get_mask(self):
        def hard_sigmoid(x):
            return torch.min(torch.max(x, torch.zeros_like(x)), torch.ones_like(x))

        if self.training:
            self.uniform.uniform_()
            u = torch.autograd.Variable(self.uniform)
            s = torch.sigmoid((torch.log(u) - torch.log(1 - u) + self.loc) / self.temp)
            s = s * (self.zeta - self.gamma) + self.gamma
            penalty = torch.sigmoid(self.loc - self.temp * self.gamma_zeta_ratio)
        else:
            s = torch.sigmoid(self.loc) * (self.zeta - self.gamma) + self.gamma
            penalty = 0
            
        return hard_sigmoid(s), penalty
    
class ReweightLinear(nn.Linear):
    def __init__(self, in_features, out_features, bias=True, linear=F.linear, 
                 prune_neuron=False, prune_always=True, factor=0.1):
        super(ReweightLinear, self).__init__(in_features, out_features, bias=bias)
        
        self.prune_neuron = prune_neuron
        self.prune_always = prune_always
        self.factor = factor
        self.linear = linear

    def forward(self, input):
        if self.eval():
            weight = self.masked_weight()
        else:
            weight = self.masked_weight() if self.prune_always else self.weight
        out = self.linear(input, weight, self.bias)
        
        return out
    
    def sparsity(self):
        sparsity = (self.weight.abs() <= self._threshold()).float().mean().item()
        
        return sparsity
    
    def masked_weight(self):
        masked_weight = self.weight.clone()
        masked_weight[self.weight.abs() <= self._threshold()] = 0
        
        return masked_weight

    def regularization(self, mean=True, axis=None):
        regularization = self.weight.abs()
        if mean:
            regularization = regularization.mean() if axis == None else regularization.mean(axis)
            
        return regularization
    
    def _threshold(self):
        if self.prune_neuron:
            threshold = self.factor * self.weight.std(1).unsqueeze(1)
        else:
            threshold = self.factor * self.weight.std()
        
        return threshold

class CancelOut(nn.Module):

    def __init__(self, input_size):
        super(CancelOut, self).__init__()
        self.weight = nn.Parameter(torch.zeros(input_size, requires_grad = True) + 4)
        self.relu = nn.ReLU()

    def forward(self, x):
        result = x * self.relu(self.weight.float())
        
        return result
    
    def regularization(self):
        weights_co = self.relu(self.weight)
        
        return torch.norm(weights_co, 1) / len(weights_co)
    
    
class CancelBinarization(torch.autograd.Function):

    @staticmethod
    def forward(ctx, input):
        ctx.save_for_backward(input)
        
        output = (input > 0.000001).float()
        
        return output

    @staticmethod
    def backward(ctx, grad_output):
        input, = ctx.saved_tensors
        
        grad_input = grad_output.clone()
        
        grad_input[input <= 0] = 0
        
        return grad_input
    

class R2NTab(nn.Module):
    def __init__(self, in_features, num_rules, out_features):

        super(R2NTab, self).__init__()

        self.n_features = in_features
        
        self.linear = sparse_linear('l0')
        self.cancelout_layer = CancelOut(in_features)
        self.and_layer = self.linear(in_features, num_rules, linear=RuleFunction.apply)
        self.or_layer = self.linear(num_rules, out_features, linear=LabelFunction.apply)
        
        self.and_layer.bias.requires_grad = False
        self.and_layer.bias.data.fill_(1)
        self.or_layer.weight.requires_grad = False
        self.or_layer.weight.data.fill_(1)
        self.or_layer.bias.requires_grad = False
        self.or_layer.bias.data.fill_(-0.5)
        
    def forward(self, input):
        out = self.cancelout_layer(input)
        out = CancelBinarization.apply(out)
        out = self.and_layer(out)
        out = Binarization.apply(out)
        out = self.or_layer(out)
        
        return out
        
    def reweight_layer(self):
        with torch.no_grad():
            indices = torch.where(self.cancelout_layer.weight < 0)[0]
            for index in indices:
                self.and_layer.weight[:,index] = 0
    
    def regularization(self):
        sparsity = ((self.and_layer.regularization(axis=1)+1) * self.or_layer.regularization(mean=False)).mean()
        
        return sparsity
            
    def extract_rules(self, header=None, print_rules=False):
        self.eval()
        self.to('cpu')

        prune_weights = self.and_layer.masked_weight()
        valid_indices = self.or_layer.masked_weight().nonzero(as_tuple=True)[1]
        rules = np.sign(prune_weights[valid_indices].detach().numpy()) * 0.5 + 0.5

        if header != None:
            rules_exp = []
            for weight in prune_weights[valid_indices]:
                rule = []
                for w, h in zip(weight, header):
                    if w < 0:
                        rule.append('not ' + h)
                    elif w > 0:
                        rule.append(h)
                rules_exp.append(rule)
            rules = rules_exp
            
            if print_rules:
                print("Rulelist:")
                for index, rule in enumerate(rules):
                    if index == 0:
                        print('if', end=' ')
                    else:
                        print('else if', end=' ')

                    print('[', end=' ')
                    for index, condition in enumerate(rule):
                        print(condition, end=' ')
                        if index != len(rule) - 1:
                            print('&&', end=' ')

                    print(']:')        
                    print('  prediction = true')
                print('else')
                print('  prediction = false')

        return rules 

    def predict(self, X):
        X = np.array(X)
        rules = self.extract_rules()
        
        results = []
        for x in X:
            indices = np.where(np.absolute(x - rules).max(axis=1) < 1)[0]
            result = int(len(indices) != 0)
            results.append(result)
            
        return np.array(results)
    
    def score(self, Y_pred, Y, metric='auc'):
        
        assert metric == 'accuracy' or metric == 'auc', 'Invalid metric provided.'
        
        if metric == 'accuracy':
            return accuracy_score(Y_pred, Y)
        elif metric == 'auc':
            return roc_auc_score(Y_pred, Y)
        
    def check_cancel_potential(self, epoch_accus, old_cancelled, old_accu):
        new_accu = sum(epoch_accus) / len(epoch_accus)
        n_old_cancelled = len(torch.where(old_cancelled.weight < 0)[0])
        n_new_cancelled = len(torch.where(self.cancelout_layer.weight < 0)[0])

        if old_accu > new_accu and n_new_cancelled > n_old_cancelled:
            if old_accu - new_accu >= 0.01:
                self.cancelout_layer = old_cancelled

            return False, old_accu, old_cancelled

        old_accu = new_accu
        old_cancelled = copy.deepcopy(self.cancelout_layer)
        
        return True, old_accu, old_cancelled

    def fit(self, train_set, test_set=None, device='cpu', lr_rules=1e-2, lr_cancel=5e-3, and_lam=1e-2, or_lam=1e-5, cancel_lam=1e-4, epochs=2000, num_alter=500, batch_size=400, dummy_index=None, fs=False, 
            max_conditions=None):
        def compute_score(out, y):
            y_labels = (out >= 0).float()
            y_corrs = (y_labels == y.reshape(y_labels.size())).float()

            return y_corrs

        assert batch_size <= len(train_set), f"Batch size ({batch_size}) should be equal or smaller than the number of training examples ({len(train_set)})."

        if max_conditions is not None:
            epochs=20000
            headers = ['a' + str(i) for i in range(1, self.n_features)]

        reg_lams = [and_lam, or_lam]

        optimizers = [optim.Adam(self.and_layer.parameters(), lr=lr_rules),
                      optim.Adam(self.or_layer.parameters(), lr=lr_rules)]
        optimizer_cancel = optim.Adam(self.cancelout_layer.parameters(), lr=lr_cancel)

        criterion = nn.BCEWithLogitsLoss().to(device)

        train_loader = torch.utils.data.DataLoader(train_set, batch_size=batch_size, drop_last=True, shuffle=True)
        
        self.to(device)
        self.train()

        dummies, epoch_accus, point_aucs, point_rules, point_conds = [], [], [], [], []

        old_accu = 0
        old_cancelled = copy.deepcopy(self.cancelout_layer)
        perform_cancel = True
        
        for epoch in tqdm(range(epochs), ncols=50):
            self.to(device)
            self.train()
            batch_corres = []

            if epoch%50 == 0 and epoch > 0 and perform_cancel:
                perform_cancel, old_accu, old_cancelled = self.check_cancel_potential(epoch_accus, old_cancelled, old_accu)
                epoch_accus = []

                if perform_cancel == False and fs:
                    break;

            if epoch%100 == 0 and epoch > 0 and max_conditions is not None:
                rules = self.extract_rules(headers)
                n_conds = sum(map(len, rules))
                if type(max_conditions) == list:
                    if n_conds < max_conditions[-1]:
                        max_conditions.pop()
                        self.to('cpu')
                        self.eval()
                        with torch.no_grad():
                            test_auc = roc_auc_score(self.predict(test_set[:][0]), test_set[:][1])
                        point_aucs.append(test_auc)
                        point_rules.append(len(rules))
                        point_conds.append(n_conds)
                        if not len(max_conditions):
                            return point_aucs, point_rules, point_conds
                elif n_conds < max_conditions:
                    break

                self.to(device)
                self.train()

            for index, (x_batch, y_batch) in enumerate(train_loader):
                x_batch = x_batch.to(device)
                y_batch = y_batch.to(device)

                out = self(x_batch)

                phase = int((epoch / num_alter) % 2)

                optimizers[phase].zero_grad()
                optimizer_cancel.zero_grad()

                loss = criterion(out, y_batch.reshape(out.size())) + reg_lams[phase] * self.regularization() + cancel_lam * self.cancelout_layer.regularization()

                loss.backward()

                optimizers[phase].step()
                if perform_cancel:
                    optimizer_cancel.step()

                corr = compute_score(out, y_batch).sum()

                batch_corres.append(corr.item())

            epoch_accu = torch.Tensor(batch_corres).sum().item() / len(train_set)
            epoch_accus.append(epoch_accu)

        self.reweight_layer()
        
        assert not torch.all(self.cancelout_layer.weight == 4), "CancelOut Layer not updating."
