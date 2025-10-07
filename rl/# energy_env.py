
import gym
from gym import spaces
import numpy as np

class EnergyEnv(gym.Env):
    """
    A simple energy management environment.
    State: [solar_forecast, demand_forecast, soc, tariff]
    Action: discrete:
      0 = do nothing
      1 = charge battery (from solar/grid)
      2 = discharge battery (to meet demand)
      3 = export to grid (curtail or sell)
    Reward: encourage using renewable & battery to meet demand, penalize grid import & battery extremes/degradation.
    """

    def __init__(self, episode_len=96, max_soc=100.0):
        super(EnergyEnv, self).__init__()
        self.episode_len = episode_len
        self.t = 0
        self.max_soc = max_soc

        # Observations: solar_forecast, demand_forecast, soc, tariff
        low = np.array([0.0, 0.0, 0.0, 0.0], dtype=np.float32)
        high = np.array([200.0, 500.0, self.max_soc, 10.0], dtype=np.float32)
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)

        # Discrete actions
        self.action_space = spaces.Discrete(4)

        # Battery parameters
        self.batt_capacity_kwh = 200.0   # capacity for simulation
        self.batt_power_kw = 50.0        # charge/discharge power limit per timestep
        self.soc = 50.0                  # percent

        # For stochasticity
        self.rng = np.random.RandomState(42)

        # Episode data
        self.last_grid_import = 0.0

    def reset(self):
        self.t = 0
        # initialize forecasts with synthetic daily pattern + noise
        self.solar_profile = self._generate_solar_profile()
        self.demand_profile = self._generate_demand_profile()
        self.tariff_profile = self._generate_tariff_profile()
        self.soc = 50.0 * (0.8 + 0.4 * self.rng.rand())  # 40-60%
        self.last_grid_import = 0.0
        return self._get_obs()

    def step(self, action):
        """
        Execute action:
         - uses forecast / actual values at current timestep
         - updates SOC
         - computes grid import (positive = import from grid)
        """
        done = False
        solar = self.solar_profile[self.t]
        demand = self.demand_profile[self.t]
        tariff = self.tariff_profile[self.t]

        # available battery energy in kWh given SOC %
        batt_energy = (self.soc / 100.0) * self.batt_capacity_kwh

        # convert batt power to kWh for 15-min timestep
        timestep_hours = 0.25
        max_batt_energy_step = self.batt_power_kw * timestep_hours

        grid_import = 0.0
        grid_export = 0.0
        used_solar = 0.0
        used_batt = 0.0

        # baseline: solar first goes to meet demand
        if solar >= demand:
            used_solar = demand
            surplus = solar - demand
        else:
            used_solar = solar
            surplus = 0.0
            remaining_demand = demand - solar

        # actions:
        if action == 0:
            # do nothing special: battery idle
            # meet remaining demand with battery or grid
            if solar < demand:
                # discharge battery if possible
                discharge = min(max_batt_energy_step, batt_energy, demand - solar)
                used_batt = discharge
                batt_energy -= discharge
                grid_import = max(0.0, demand - solar - discharge)
            else:
                # solar surplus is wasted (or exported)
                grid_export = surplus  # simplified
        elif action == 1:
            # charge battery (prefer solar charging; if insufficient, allow grid charge)
            # charge amount:
            charge_possible = min(max_batt_energy_step, self.batt_capacity_kwh - batt_energy)
            # prefer solar surplus
            if surplus >= charge_possible:
                batt_energy += charge_possible
                used_solar += charge_possible
                surplus -= charge_possible
            else:
                # use all solar surplus then grid for rest
                batt_energy += surplus
                used_solar += surplus
                grid_import += (charge_possible - surplus)  # grid charges battery
                batt_energy += (charge_possible - surplus)
                surplus = 0.0
            # demand served by solar used_solar, remaining demand handled by battery or grid
            if solar + 0.0 < demand:
                remaining = demand - solar
                discharge = min(max_batt_energy_step, batt_energy, remaining)
                used_batt += discharge
                batt_energy -= discharge
                grid_import += max(0.0, remaining - discharge)
        elif action == 2:
            # discharge heavily to meet demand (aggressive)
            discharge = min(max_batt_energy_step, batt_energy, max(0.0, demand - solar))
            used_batt = discharge
            batt_energy -= discharge
            grid_import = max(0.0, demand - solar - discharge)
            # if solar > demand, export surplus
            if solar > demand:
                grid_export = solar - demand
        elif action == 3:
            # export mode: export solar surplus and prioritize not charging battery
            if solar > demand:
                grid_export = solar - demand
            else:
                # meet demand with battery if available else grid
                discharge = min(max_batt_energy_step, batt_energy, max(0.0, demand - solar))
                used_batt = discharge
                batt_energy -= discharge
                grid_import = max(0.0, demand - solar - discharge)

        # update SOC
        self.soc = (batt_energy / self.batt_capacity_kwh) * 100.0
        # clip
        self.soc = float(np.clip(self.soc, 0.0, 100.0))

        # compute reward:
        # penalize grid import (cost), encourage renewable use & low battery cycling penalty
        cost_grid = grid_import * tariff  # simple cost
        reward = - cost_grid  # minimize cost

        # bonus for using solar to meet demand
        reward += 0.1 * used_solar
        # small penalty for deep SOC cycles (to model degradation)
        if self.soc < 10 or self.soc > 95:
            reward -= 5.0

        # small penalty for exports (optional, or can reward if selling)
        reward -= 0.01 * grid_export

        # bookkeeping
        self.last_grid_import = grid_import

        # advance time
        self.t += 1
        if self.t >= self.episode_len:
            done = True

        obs = self._get_obs()
        info = {
            'grid_import': grid_import,
            'grid_export': grid_export,
            'used_solar': used_solar,
            'used_batt': used_batt,
            'soc': self.soc,
            'tariff': tariff
        }
        return obs, reward, done, info

    def _get_obs(self):
        # use "forecast" as current step's values (simplified)
        solar_forecast = self.solar_profile[self.t] if self.t < len(self.solar_profile) else 0.0
        demand_forecast = self.demand_profile[self.t] if self.t < len(self.demand_profile) else 0.0
        tariff = self.tariff_profile[self.t] if self.t < len(self.tariff_profile) else 1.0
        return np.array([solar_forecast, demand_forecast, self.soc, tariff], dtype=np.float32)

    def _generate_solar_profile(self):
        # simple bell-shaped daily solar profile + noise
        center = self.episode_len // 2
        hours = np.arange(self.episode_len)
        base = 150.0 * np.exp(-0.5 * ((hours - center) / (self.episode_len/6))**2)  # peak ~150 kW
        noise = self.rng.normal(0, 10, size=self.episode_len)
        return np.clip(base + noise, 0, None)

    def _generate_demand_profile(self):
        # daily demand with morning/evening peaks
        hours = np.arange(self.episode_len)
        morning = 200 * np.exp(-0.5 * ((hours - self.episode_len*0.25) / (self.episode_len/10))**2)
        evening = 300 * np.exp(-0.5 * ((hours - self.episode_len*0.75) / (self.episode_len/8))**2)
        base = 200 + morning + evening
        noise = self.rng.normal(0, 20, size=self.episode_len)
        return np.clip(base + noise, 50, None)

    def _generate_tariff_profile(self):
        # higher tariff during evening peak (example)
        tariffs = np.ones(self.episode_len) * 1.0
        peak_start = int(self.episode_len * 0.65)
        peak_end = int(self.episode_len * 0.85)
        tariffs[peak_start:peak_end] = 3.0  # peak is expensive
        return tariffs

    def render(self, mode='human'):
        print(f"t={self.t}, SOC={self.soc:.1f}%")
