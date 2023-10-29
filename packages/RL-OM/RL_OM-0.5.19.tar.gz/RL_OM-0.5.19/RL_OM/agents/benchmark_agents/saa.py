# AUTOGENERATED! DO NOT EDIT! File to edit: ../../../nbs/agents/benchmark_agents/02_SAA_multi_period_agents.ipynb.

# %% auto 0
__all__ = ['SAA_MP_Agent', 'round_none', 'SAA_MP_Policy', 'WSAA_MP_Agent', 'WSAA_MP_Policy']

# %% ../../../nbs/agents/benchmark_agents/02_SAA_multi_period_agents.ipynb 4
# General libraries:
import numpy as np
import pulp as pl
from tqdm import tqdm
# import time

# Mushroom libraries
from mushroom_rl.core import Agent

# ML:
from sklearn.neighbors import KNeighborsRegressor

# %% ../../../nbs/agents/benchmark_agents/02_SAA_multi_period_agents.ipynb 7
class SAA_MP_Agent(Agent):

    train_directly = True
    train_mode = "direct"

    def __init__(self,
                    mdp_info,
                    mdp,
                    h,
                    cu,
                    l,
                    horizon=10,
                    unit_size=0.01,
                    num_scenarios=3,
                    preprocessors = None,
                    postprocessors = None,
                    agent_name = "SAA_MP",
                    precision=5,
                    ):

        self.name = agent_name
        
        policy = SAA_MP_Policy(
            h=h,
            cu=cu,
            l=l,
            horizon=horizon,
            gamma=mdp_info.gamma,
            num_scenarios=num_scenarios,
            mdp = mdp,
            unit_size=unit_size,
            precision=precision,
            preprocessors=preprocessors,
            postprocessors=postprocessors,
        )

        self.precision = precision

        self.train_directly = True
        self.train_mode = "direct"
        self.skip_val = True #! Make true

        super().__init__(mdp_info, policy)

    def fit(self, features = None, demand=None):

        self.policy.get_scenarios(demand)

def round_none(a, b):
    if a is None:
        return None
    else:
        return np.round(a, b)

class SAA_MP_Policy():
    def __init__(self,
        h,
        cu,
        l,
        horizon,
        gamma,
        num_scenarios,
        mdp,
        unit_size,
        precision,
        preprocessors,
        postprocessors
    ):
        self.h = h
        self.cu = cu
        self.l = l
        self.horizon=horizon
        self.gamma = gamma
        self.num_scenarios = num_scenarios

        if preprocessors is None:
            self.preprocessors = list()
        else:
            self.preoprocessors = (preprocessors)
        if postprocessors is None:
            self.postprocessors = list()
        else:
            self.postprocessors = (postprocessors)
        
        self.all_scenarios = np.array([[x for x in range(self.horizon)]])
        self.counter=0
        self.features=False

    def draw_action(self, input):
        for preprocessor in self.preprocessors:
            input = preprocessor(input)
        
        optimization_results = self.optimize(input)
        action = optimization_results['Order']
        
        return np.array([action])

    def optimize(self, state):

        # building_model_start = time.time()
        scenarios, weights = self.sample_scenarios(state)
        if self.features:
            state = {'inventory': state[self.num_features], 'pipeline': state[self.num_features+1:]}
        else:
            state = {'inventory': state[0], 'pipeline': state[1:]}
        cu = self.cu
        l = self.l
        h = self.h
        horizon = self.horizon
        gamma = self.gamma

        T_ = range(horizon)

        # Create the model
        model = pl.LpProblem("Lost_Sales", pl.LpMinimize)

        # Create the decision variables
        ts = []
        for t in T_:
            for s in scenarios.keys():
                ts.append((t,s))

        q = pl.LpVariable.dicts("q", ts, lowBound=0)
        I = pl.LpVariable.dicts("i", ts, lowBound=0)
        u = pl.LpVariable.dicts("u", ts, lowBound=0)

        # Add the objective function
        model += pl.lpSum([(gamma**t)*(weights[s]*(cu*u[t,s] + h*I[t,s])) for t,s in ts])

        # Add the constraints
        I_start = state['inventory']
        p = state['pipeline']
        p = p[::-1]

        for s in scenarios:
            model += q[0,s] == q[0,0]

        for s in scenarios:
            for t in T_:
                if t == 0:
                    if l == 0:
                        model += I[t,s] == q[t-l, s] + I_start  - scenarios[s][t] + u[t,s]
                        model += u[t,s] >= scenarios[s][t] - I_start - q[t-l, s]
                    else:
                        model += I[t,s] == p[t] + I_start - scenarios[s][t] + u[t,s]
                        model += u[t,s] >= scenarios[s][t] - I_start - p[t]
                elif t < l:
                    model += I[t,s] == p[t] + I[t-1,s] - scenarios[s][t] + u[t,s]
                    model += u[t,s] >= scenarios[s][t] - I[t-1,s] - p[t]
                else:
                    model += I[t,s] == q[t-l,s] + I[t-1,s] - scenarios[s][t] + u[t,s]
                    model += u[t,s] >= scenarios[s][t] - I[t-1,s] - q[t-l,s]

        # Solve the optimization problem
        # # model.solve(pl.HiGHS_CMD())
        # model.solve()

        # building_model_end = time.time()
        # solving_model_start = time.time()

        solver = pl.GUROBI_CMD()  # Change this to the solver you are using
        solver.msg = False  # Turn off solver output
        model.solve(solver)
        # Print the results
        # solving_model_end = time.time()
        results = {
            "Cost": sum([weights[s] * (cu*u[t,s].varValue + h*I[t,s].varValue) for t,s in ts]),
            "Order": q[0,0].varValue,
            }
        
        # print(f"Building model: {round_none(building_model_end - building_model_start, 2)}s, Solving model: {round_none(solving_model_end - solving_model_start, 2)}s")
        
        self.counter +=1

        # print(p)
        # print(I_start)
        # for t, s in ts:
        #     if s == 0:
        #         if t<l:
        #             order_minus_l = p[t]
        #         else:
        #             order_minus_l = q[t-l,s].varValue
        #         if t == 0:
        #             I_prev = I_start
        #         else:
        #             I_prev = I[t-1,s].varValue
        #         print(f"{t}, {s}: I_prev: {round_none(I_prev, 2)}, Q_arriving: {round_none(order_minus_l, 2)}, D={scenarios[s][t]}, I={round_none(I[t, s].varValue, 2)}, U={round_none(u[t, s].varValue, 2)}, Q={round_none(q[t, s].varValue, 2)}")
        print(f"\rselected: {results['Order']:.2f} in iteration: {self.counter}", end="")

        return results
    
    def sample_scenarios(self, state):
        
        scenarios = {}
        weights = {}

        if self.num_scenarios >= self.all_scenarios.shape[0]:
            # Use all available scenarios
            for i, scenario in enumerate(self.all_scenarios):
                scenarios[i] = scenario
                weights[i] = 1 / self.all_scenarios.shape[0]
        
        else:
            # Sample scenarios
            sampled_indices = np.random.choice(self.all_scenarios.shape[0], self.num_scenarios)
            for i, idx in enumerate(sampled_indices):
                scenarios[i] = self.all_scenarios[idx, :]
                weights[i] = 1 / self.num_scenarios

        return scenarios, weights

    def get_scenarios(self, demand):

        self.all_scenarios = np.empty((len(demand) - self.horizon, self.horizon))
        for i in range(len(demand) - self.horizon):
            demand_scenario = np.array(demand[i:i+self.horizon]).squeeze()
            self.all_scenarios[i, :] = demand_scenario

        print("got", self.all_scenarios.shape[0], "scenarios")

    def reset(*args, **kwargs): 
        pass

# %% ../../../nbs/agents/benchmark_agents/02_SAA_multi_period_agents.ipynb 8
class WSAA_MP_Agent(Agent):

    train_directly = True
    train_mode = "direct"

    def __init__(self,
                    mdp_info,
                    mdp,
                    h,
                    cu,
                    l,
                    horizon=10,
                    unit_size=0.01,
                    num_scenarios=3,
                    preprocessors = None,
                    postprocessors = None,
                    agent_name = "SAA_MP",
                    precision=5,
                    method="kNN",
                    ):

        self.name = agent_name
        
        policy = WSAA_MP_Policy(
            num_features = mdp.num_features,
            h=h,
            cu=cu,
            l=l,
            horizon=horizon,
            gamma=mdp_info.gamma,
            num_scenarios=num_scenarios,
            mdp = mdp,
            unit_size=unit_size,
            precision=precision,
            preprocessors=preprocessors,
            postprocessors=postprocessors,
            method=method,
        )

        self.precision = precision

        self.train_directly = True
        self.train_mode = "direct"
        self.skip_val = True #! Make true

        super().__init__(mdp_info, policy)

    def fit(self, features = None, demand=None):

        self.policy.get_scenarios(features, demand)

def round_none(a, b):
    if a is None:
        return None
    else:
        return np.round(a, b)

class WSAA_MP_Policy(SAA_MP_Policy):
    def __init__(self,
        num_features,
        h,
        cu,
        l,
        horizon,
        gamma,
        num_scenarios,
        mdp,
        unit_size,
        precision,
        preprocessors,
        postprocessors,
        method="kNN"
    ):
        self.method=method

        super().__init__(h, cu, l, horizon, gamma, num_scenarios, mdp, unit_size, precision, preprocessors, postprocessors)

        self.features = True
        self.num_features = num_features
        self.fitted=False
        self.all_scenarios_demand = np.array([[x for x in range(self.horizon)]])
    
    def sample_scenarios(self, state):
        
        scenarios = {}
        weights = {}

        if ((self.num_scenarios >= self.all_scenarios_demand.shape[0]) or (self.fitted==False)):
            # Use all available scenarios
            for i, scenario in enumerate(self.all_scenarios_demand):
                scenarios[i] = scenario
                weights[i] = 1 / self.all_scenarios_demand.shape[0]
        
        else:
            if self.method == "kNN":
                features = np.array(state[:self.num_features]).reshape(1, -1)
                scenarios_ml_dist, scenarios_ml_idx = self.model.kneighbors(features, self.num_scenarios, return_distance=True)
                scenarios_ml_idx = scenarios_ml_idx.squeeze()

            for i in range(self.num_scenarios):
                scenarios[i] = self.all_scenarios_demand[scenarios_ml_idx[i], :]
                weights[i] = 1 / self.num_scenarios

        return scenarios, weights

    def get_scenarios(self, features, demand):

        self.all_scenarios_demand = np.empty((len(demand) - self.horizon, self.horizon))
        for i in range(len(demand) - self.horizon):
            demand_scenario = np.array(demand[i:i+self.horizon]).squeeze()
            self.all_scenarios_demand[i, :] = demand_scenario
        self.all_scenarios_features = np.empty((len(features) - self.horizon, self.horizon, features.shape[1]))
        self.all_scenarios_features = features[:-self.horizon]
        if self.num_scenarios >= self.all_scenarios_demand.shape[0]: 
            print("WARNING: all scenarios are used, no conditional weights are used")
        else:
            if self.method == "kNN":
                self.model = KNeighborsRegressor(n_neighbors=self.num_scenarios)
                self.model.fit(self.all_scenarios_features, self.all_scenarios_demand)
                self.fitted=True
            else:
                print("method either not recognized or not implemented yet")

        print("got", self.all_scenarios_demand.shape[0], "scenarios")

    def reset(*args, **kwargs): 
        pass
