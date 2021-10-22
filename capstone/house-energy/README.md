House Energy with MSFT Bonsai
========================================

## Objective

Control the temperature inside of a house according to the desired set temperatures just like a thermostat. The user can choose among 3 weather patterns: constant, sinusoidal, sinusoidal + noise, or add it's own list of fixed weather.

![](img/house-energy.PNG)

## Sim Package Build + storage on Azure Container Registry

To build your simulator package for sim-scaling on Project Bonsai, use the following `az acr` command, it will also store the container on the registry

```bash
registry_name="your_registry_name"
az acr build --image houseenergy:latest --file Dockerfile --registry $registry_name .
```
Follow these [instructions](https://docs.microsoft.com/en-us/bonsai/guides/add-simulator) to add a simulator to your bonsai workspace 

## Running Locally

Step 1: Register your sim

```bash
python main.py --config-setup True
```
Step 2: connect your registered sim to a brain

```bash
brain_name="your_brain_name"
bonsai simulator unmanaged connect -b $brain_name --action Train --concept-name SmartHome --simulator-name HouseEnergy
```

## States

| State | Units |
| ----- | ----- |
| Tin   | [°C]  |
| Tset  | [°C]  |
| Tout  | [°C]  |

## Actions

| Action | Discrete Value       |
| ------ | -------------------- |
| hvacON | 0 (ON)    or 1 (OFF) |


## Terminal Conditions

- Exceed 288 iterations in an episode

## Configuration Parameters

- K : thermal conductivity
- C : thermal capacity
- Qhvac : Cooling capacity
- schedule_index : (1) weather sinusoidal pattern (2) sinusoidal + white noise (-) else  constant weather pattern
- timestep : keep in minutes here to keep number of minutes for days consistent
- Tin_initial : Initial temperature
- max_iterations : Number of maximum iteration, by default it's 24 hours (1440 min) divided by timestep
- custom_t_out : list of custom weather pattern
- starting_hour : hours at which to start the simulation day
- tset_day_start : time to switch on "day mode" of cooling system
- tset_day_end : time to switch off "day mode" of cooling system,
- t_set_day : temperature for day mode
- t_set_night : temperature for night mode
- t_mid_point : average temperature for sinusoidal pattern
- t_amplitude : min-max temperature
- add_forecast_noise : add noise to weather forecast (1) noise (0) no noise

### Initial conditions

- Tin
- Tset
- Tout
- hvacON

## Simulator API - Python

- `setup_schedule()`
- `update_hvacON()`
- `update_Tin()`
- `show()`