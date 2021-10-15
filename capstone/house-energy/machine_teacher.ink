inkling "2.0"
using Number
using Goal
using Math

const MaxDeviation = 2

type ObservableState {
    Tset: Number.Float32,
    Tin: Number.Float32,
    Tout: Number.Float32,
    total_power: Number.Float32
}

type SimAction {
    hvacON: Number.Int8 <off=0, on=1>
}

type SimConfig {
    K: Number.Float32, # Thermal conductivity
    C: Number.Float32, # Thermal Capacity
    Qhvac: Number.Float32, # Heat Flux
    Tin_initial: number, # C
    schedule_index: Number.Int8, # 0 - fixed 1 - realistic (sinusoidal), 2 - realistic + noise
    number_of_days: number,
    timestep: number, # Min
    max_iterations: number, # Alters schedule generation
    total_power: number, # total power consumption
    day_start: number,
    day_end: number,
    t_set_day: number,
    t_set_night: number,
    t_mid_point: number,
    t_amplitude: number,
}

function TempDiff(Tin:number, Tset:number) {
    return Math.Abs(Tin - Tset)
}


graph (input: ObservableState): SimAction {
    concept SmartHouse(input): SimAction {
        curriculum {
            source simulator (Action: SimAction, Config: SimConfig): ObservableState {

            }
            goal (State: ObservableState) {
                minimize `Temp Deviation`:
                    TempDiff(State.Tin, State.Tset) in Goal.RangeBelow(MaxDeviation)

                minimize `Total Power Consumption`:
                    State.total_power in Goal.RangeBelow(1)
            }

            training {
                EpisodeIterationLimit: 100
            }

            lesson `Lesson 1` {
                scenario {
                    K: 0.5,
                    C: 0.3,
                    Qhvac: 9,
                    Tin_initial: number<18 .. 30>,
                    timestep: 5,
                    schedule_index: 1,
                    day_start: 7,
                    day_end: 22,
                    t_set_day: 23,
                    t_set_night: 18,
                    t_mid_point: 25,
                    t_amplitude: 5,
                }
            }
        }
    }
}
