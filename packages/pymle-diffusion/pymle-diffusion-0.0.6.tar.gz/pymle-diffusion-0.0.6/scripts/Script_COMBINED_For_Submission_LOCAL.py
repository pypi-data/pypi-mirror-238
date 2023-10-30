# ===============================================
# Initial Examples
# ===============================================

from pymle.models import OrnsteinUhlenbeck
import numpy as np

S0 = 0.4  # initial value of process
kappa = 3  # rate of mean reversion
mu = 0.3  # long term level of process
sigma = 0.2  # volatility

model = OrnsteinUhlenbeck()
model.params = np.array([kappa, mu, sigma])

from pymle.sim.Simulator1D import Simulator1D

T = 5  # num years of the sample
freq = 250  # observations per year
dt = 1. / freq  # time step (constant for the example)
seed = 123  # random seed: set to None to get new results each time

simulator = Simulator1D(S0, T * freq, dt, model).set_seed(seed)
sample = simulator.sim_path()

import matplotlib.pyplot as plt

plt.plot(sample)
plt.xlabel('t')
plt.ylabel(r' $S_t$')
plt.show()

"""
To fit using any of the estimation procedures, we must specify the parameter bounds we wish
the optimizer to enforce during the fit, along with an initial guess for the parameters:
"""
param_bounds = [(0, 10), (0, 4), (0.01, 1)]  # kappa, mu, sigma
guess = np.array([1, 0.1, 0.4])

from pymle.fit.AnalyticalMLE import AnalyticalMLE
from pymle.core.TransitionDensity import *

print('----------------------------------------------')
euler_est = AnalyticalMLE(sample, param_bounds, dt,
                          density=EulerDensity(model)).estimate_params(guess)
print('----------------------------------------------')
print('EULER Result: ')
print(euler_est)

print('----------------------------------------------')
ozaki_est = AnalyticalMLE(sample, param_bounds, dt,
                          density=OzakiDensity(model)).estimate_params(guess)
print('----------------------------------------------')
print('OZAKI Result: ')
print(ozaki_est)

print('----------------------------------------------')
shoji_ozaki_est = AnalyticalMLE(sample, param_bounds, dt,
                                density=ShojiOzakiDensity(model)).estimate_params(guess)
print('----------------------------------------------')
print('SHOJI OZAKI Result: ')
print(shoji_ozaki_est)

print('----------------------------------------------')
kessler_est = AnalyticalMLE(sample, param_bounds, dt,
                            density=KesslerDensity(model)).estimate_params(guess)

print('----------------------------------------------')
print('KESSLER Result: ')
print(kessler_est)

print('----------------------------------------------')
AitSahalia_est = AnalyticalMLE(sample, param_bounds, dt,
                               density=AitSahaliaDensity(model)).estimate_params(guess)
print('----------------------------------------------')
print('AIT-SAHALIA Result: ')
print(AitSahalia_est)
print('----------------------------------------------')

# ===============================================
# CTMC Examples
# ===============================================
from pymle.sim.Simulator1D import Simulator1D
from pymle.models import OrnsteinUhlenbeck
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

S0 = 0.2  # initial value of process
kappa = 4  # rate of mean reversion
mu = 0.2  # long term level of process
sigma = 0.4  # volatility

T = 5  # num years of the sample
freq = 250  # observations per year
dt = 1. / freq  # time step (constant for the example)
seed = 123  # random seed: set to None to get new results each time

model = OrnsteinUhlenbeck()
model.params = np.array([kappa, mu, sigma])

simulator = Simulator1D(S0, T * freq, dt, model).set_seed(seed)
sample = simulator.sim_path()

model = OrnsteinUhlenbeck()
model.params = np.array([kappa, mu, sigma])

from pymle.ctmc.StateSpace import StateSpace
from pymle.ctmc.Generator1D import Generator1D
from pymle.ctmc.CTMCEstimator import CTMCEstimator


def plot_CTMC_sample_vs_binned(path: np.ndarray, binned_path: np.ndarray):
    plt.plot(path, label='Original Path', linestyle='solid')
    plt.xlabel('time index', fontsize=12)
    plt.ylabel('process', fontsize=12)
    plt.plot(binned_path, label='Binned Path', linestyle='dashed')
    plt.legend()
    plt.show()


def plot_CTMC_Counts_C_Matrix(estimator: CTMCEstimator):
    C = pd.DataFrame(estimator.transition_counts)
    ax = sns.heatmap(C, cmap=sns.color_palette("Blues", as_cmap=True),
                     linewidths=.5, yticklabels=False, xticklabels=5)
    plt.xlabel('state')
    plt.show()


# First plot the binned path, with fewer states just to illustrate
N_states = 30  # Set low just to illustrate the binning
state_space = StateSpace.from_sample(sample, is_positive=True, N_states=N_states)
binned_path, state_index = state_space.bin_path(sample)

plot_CTMC_sample_vs_binned(path=sample, binned_path=binned_path)

# Now illustrate how the CTMC estimator forms the transition density estimate
generator = Generator1D(model)
generator.states = state_space.states
ctmc_estimator = CTMCEstimator(binned_path, state_index, dt, generator, param_bounds)

plot_CTMC_Counts_C_Matrix(estimator=ctmc_estimator)

# Now estimate with a more realistic number of states (e.g. 300)
N_states = 300
state_space = StateSpace.from_sample(sample, is_positive=True, N_states=N_states)
binned_path, state_index = state_space.bin_path(sample)

generator = Generator1D(model)
generator.states = state_space.states

param_bounds = [(0, 10), (0, 4), (0.01, 1)]  # kappa, mu, sigma
guess = np.array([1, 0.1, 0.4])

ctmc_estimator = CTMCEstimator(binned_path, state_index, dt, generator,
                               param_bounds)

print('----------------------------------------------')
ctmc_est = ctmc_estimator.estimate_params(guess)

print('----------------------------------------------')
print('CTMC Result: ')
print(ctmc_est)
print('----------------------------------------------')

sns.set_style('whitegrid')

# ===============================================
# Real FX Rate Data Examples
# ===============================================
import pandas as pd
import matplotlib.pyplot as plt
from pymle.models.CIR import CIR
from pymle.core.TransitionDensity import *
import seaborn as sns
import matplotlib.dates as mdates
import datetime

sns.set_style('whitegrid')
# As a first step, we read the data into a pandas ‘DataFrame’ from the data directory:
from pymle.data.loader import load_FX_USD_EUR

df = load_FX_USD_EUR()

# To generate Figure 4 with properly formatted dates, we run the following:
skip = 20  # Change to sample time series at a different freq
dt = skip / 252.
sample = df['Rate'].values[:-1:skip]
df['Date'] = [datetime.datetime.strptime(d, "%m/%d/%Y").date() for d in df['Date']]
fig, ax = plt.subplots()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

ax.plot(df['Date'].values, df['Rate'].values)
plt.xlabel('Date')
plt.ylabel('Exchange Rate')
fig.autofmt_xdate()
plt.show()

# We then initialize the CIR model as follows, and supply an initial guess and parameter bounds
# for the fit
model = CIR()
guess = np.asarray([.24, 1.0, 0.1])  # kappa, mu, sigma
param_bounds = [(0.01, 5), (0.01, 2), (0.01, 0.9)]

from pymle.fit.AnalyticalMLE import AnalyticalMLE
from pymle.core.TransitionDensity import *

print('----------------------------------------------')
euler_est = AnalyticalMLE(sample, param_bounds, dt,
                          density=EulerDensity(model)).estimate_params(guess)

print('\nEuler: --------------------')
print(euler_est)

print('----------------------------------------------')
exact_est = AnalyticalMLE(sample, param_bounds, dt,
                          density=ExactDensity(model)).estimate_params(guess)

print('\nExact MLE: --------------------')
print(exact_est)

print('----------------------------------------------')
ozaki_est = AnalyticalMLE(sample, param_bounds, dt,
                          density=OzakiDensity(model)).estimate_params(guess)

print('\nOzaki: --------------------')
print(ozaki_est)

print('----------------------------------------------')
shoji_ozaki_est = AnalyticalMLE(sample, param_bounds, dt,
                                density=ShojiOzakiDensity(model)).estimate_params(guess)

print('\nShoji-Ozaki: --------------------')
print(shoji_ozaki_est)

print('----------------------------------------------')
kessler_est = AnalyticalMLE(sample, param_bounds, dt,
                            density=KesslerDensity(model)).estimate_params(guess)

print('\nKessler: --------------------')
print(kessler_est)

print('----------------------------------------------')
AitSahalia_est = AnalyticalMLE(sample, param_bounds, dt,
                               density=AitSahaliaDensity(model)).estimate_params(guess)
print('\nAit-Sahalia: --------------------')
print(AitSahalia_est)
