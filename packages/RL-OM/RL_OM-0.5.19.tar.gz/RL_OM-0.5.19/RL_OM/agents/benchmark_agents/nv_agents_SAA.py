# AUTOGENERATED! DO NOT EDIT! File to edit: ../../../nbs/agents/benchmark_agents/02_SAA_agents.ipynb.

# %% auto 0
__all__ = ['FakePolicy', 'WSAAAgent', 'check_cu_co', 'SAAAgent']

# %% ../../../nbs/agents/benchmark_agents/02_SAA_agents.ipynb 4
# General libraries:
import numpy as np
from scipy.stats import norm
import numbers

from sklearn.ensemble import RandomForestRegressor
from sklearn.utils.validation import check_array
import pulp

# Mushroom libraries
from mushroom_rl.core import Agent

# %% ../../../nbs/agents/benchmark_agents/02_SAA_agents.ipynb 7
class FakePolicy():
    def reset():
        pass

class WSAAAgent(Agent):
    def __init__(self,
                 cu=None,
                 co=None,
                 criterion="mse",
                 n_estimators=100,
                 max_depth=None,
                 min_samples_split=6, # starndard 2
                 min_samples_leaf=3, # standard 1
                 min_weight_fraction_leaf=0.,
                 max_features="auto",
                 max_leaf_nodes=None,
                 min_impurity_decrease=0.,
                 bootstrap=True,
                 oob_score=False,
                 n_jobs=None,
                 random_state=None,
                 verbose=0,
                 warm_start=False,
                 ccp_alpha=0.0,
                 max_samples=None,
                 weight_function="w1",
                 agent_name = "wSAA"
                 ):
        self.criterion = criterion
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.min_weight_fraction_leaf = min_weight_fraction_leaf
        self.max_features = max_features
        self.max_leaf_nodes = max_leaf_nodes
        self.min_impurity_decrease = min_impurity_decrease
        self.bootstrap = bootstrap
        self.oob_score = oob_score
        self.n_jobs = n_jobs
        self.random_state = random_state
        self.verbose = verbose
        self.warm_start = warm_start
        self.ccp_alpha = ccp_alpha
        self.max_samples = max_samples
        self.weight_function = weight_function
        self.cu=cu
        self.co=co

        self.train_directly=True
        self.train_mode = "direct"
        self.policy = FakePolicy

        self._postprocessors=list()
        self._preprocessors=list() 

        self.name = agent_name
        self.fitted=False
        
    def _get_fitted_model(self, X, y):
        model = RandomForestRegressor(
            criterion=self.criterion,
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            min_samples_split=self.min_samples_split,
            min_samples_leaf=self.min_samples_leaf,
            min_weight_fraction_leaf=self.min_weight_fraction_leaf,
            max_features=self.max_features,
            max_leaf_nodes=self.max_leaf_nodes,
            min_impurity_decrease=self.min_impurity_decrease,
            bootstrap=self.bootstrap,
            oob_score=self.oob_score,
            n_jobs=self.n_jobs,
            random_state=self.random_state,
            verbose=self.verbose,
            warm_start=self.warm_start,
            ccp_alpha=self.ccp_alpha,
            max_samples=self.max_samples
        )

        self.model_ = model.fit(X, y)
        self.train_leaf_indices_ = model.apply(X)
        

    def _calc_weights(self, sample):
        sample_leaf_indices = self.model_.apply([sample])
        if self.weight_function == "w1":
            n = np.sum(sample_leaf_indices == self.train_leaf_indices_, axis=0)
            treeWeights = (sample_leaf_indices == self.train_leaf_indices_) / n
            weights = np.sum(treeWeights, axis=1) / self.n_estimators
        else:
            n = np.sum(sample_leaf_indices == self.train_leaf_indices_)
            treeWeights = (sample_leaf_indices == self.train_leaf_indices_) / n
            weights = np.sum(treeWeights, axis=1)
        
        weightPosIndex = np.where(weights > 0)[0]
        weightsPos = weights[weightPosIndex]

        return (weightsPos, weightPosIndex)
    

    def fit(self, features, demand):

        X=features
        y=demand

        cu = self.cu
        co = self.co

        self._get_fitted_model(X, y)

        if y.ndim == 1:
            y = np.reshape(y, (-1, 1))

        # Training data
        self.y_ = y
        self.X_ = X
        self.n_samples_ = y.shape[0]

        # Determine output settings
        self.n_outputs_ = y.shape[1]
        self.n_features_ = X.shape[1]

        self.cu = cu
        self.co = co

        self.fitted=True

        self.model_.verbose=0

        return self

    def _findQ(self, weights, weightPosIndices):
        
        y = self.y_
        yWeightPos = y[weightPosIndices]
        
        q = []
        
        for i in range(self.n_outputs_):
            serviceLevel = self.cu[i] / (self.cu[i] + self.co[i])
            
            indicesYSort = np.argsort(yWeightPos[:, i])
            ySorted = yWeightPos[indicesYSort, i]
            
            distributionFunction = np.cumsum(weights[indicesYSort])
            decisionIndex = np.where(distributionFunction >= serviceLevel)[0][0]
            
            q.append(ySorted[decisionIndex])
        
        return q

    def draw_action(self, X):   

        if self.fitted:  

            if X.ndim == 1:
                X = np.reshape(X, (-1, self.n_features_))
            
            weightsDataList = [self._calc_weights(row) for row in X]

            pred = [self._findQ(weights, weightPosIndices) 
                    for weights, weightPosIndices in weightsDataList]
            pred = np.array(pred).squeeze()

        else:
            pred = np.random.rand(1)  
        
        return pred


# %% ../../../nbs/agents/benchmark_agents/02_SAA_agents.ipynb 8
def check_cu_co(cu, co, n_outputs):
    """Validate under- and overage costs.

    Parameters
    ----------
    cu : {ndarray, Number or None}, shape (n_outputs,)
       The underage costs per unit. Passing cu=None will output an array of ones.
    co : {ndarray, Number or None}, shape (n_outputs,)
       The overage costs per unit. Passing co=None will output an array of ones.
    n_outputs : int
       The number of outputs.
    Returns
    -------
    cu : ndarray, shape (n_outputs,)
       Validated underage costs. It is guaranteed to be "C" contiguous.
    co : ndarray, shape (n_outputs,)
       Validated overage costs. It is guaranteed to be "C" contiguous.
    """
    costs = [[cu, "cu"], [co, "co"]]
    costs_validated = []
    for c in costs:
        if c[0] is None:
            cost = np.ones(n_outputs, dtype=np.float64)
        elif isinstance(c[0], numbers.Number):
            cost = np.full(n_outputs, c[0], dtype=np.float64)
        else:
            cost = check_array(
                c[0], accept_sparse=False, ensure_2d=False, dtype=np.float64,
                order="C"
            )
            if cost.ndim != 1:
                raise ValueError(c[1], "must be 1D array or scalar")

            if cost.shape != (n_outputs,):
                raise ValueError("{}.shape == {}, expected {}!"
                                 .format(c[1], cost.shape, (n_outputs,)))
        costs_validated.append(cost)
    cu = costs_validated[0]
    co = costs_validated[1]
    return cu, co

class SAAAgent(Agent):

    #BaseNewsvendor, ClassicMixin

    def __init__(self,
                 cu=None,
                 co=None,
                 agent_name="SAA"
                 ):
        self.cu = cu
        self.co = co

        self.train_directly=True
        self.train_mode = "direct"
        self.policy = FakePolicy

        self._postprocessors=list()
        self._preprocessors=list() 

        self.name = agent_name
        self.fitted=False

    def _calc_weights(self):
        weights = np.full(self.n_samples_, 1 / self.n_samples_)
        return weights

    def fit(self, demand, features):

        y=demand
       
        y = check_array(y, ensure_2d=False, accept_sparse='csr')

        if y.ndim == 1:
            y = np.reshape(y, (-1, 1))

        # Training data
        self.y_ = y
        self.n_samples_ = y.shape[0]

        # Determine output settings
        self.n_outputs_ = y.shape[1]

        # Check and format under- and overage costs
        self.cu_, self.co_ = check_cu_co(self.cu, self.co, self.n_outputs_)

        self.q_star = np.array(self._findQ(self._calc_weights()))

        self.fitted=True

        return self

    def _findQ(self, weights):
        """Calculate the optimal order quantity q"""

        y = self.y_
        q = []

        for k in range(self.n_outputs_):
            alpha = self.cu_[k] / (self.cu_[k] + self.co_[k])
            q.append(np.quantile(y[:, k], alpha, interpolation="higher"))

        return q

    def draw_action(self, *args, **kwargs):

        if self.fitted:
            pred = self.q_star
            
        else:
            pred = np.random.rand(1)  
        return pred
