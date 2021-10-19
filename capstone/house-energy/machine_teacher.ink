inkling "2.0"
using Number
using Goal
using Math

const MaxDeviation = 1
const timestep = 5

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
    starting_hour: number,
    timestep: number, # Min
    max_iterations: number, # Alters schedule generation
    total_power: number, # total power consumption
    tset_day_start: number,
    tset_day_end: number,
    t_set_day: number,
    t_set_night: number,
    t_mid_point: number,
    t_amplitude: number,
}

function TempDiff(Tin:number, Tset:number) {
    return Math.Abs(Tin - Tset)
}

function HoursToIteration(hour: number, timestep2: number): Number.Int32 {  
    return hour * 60 / timestep2
  }

simulator SmartHouseSim (Action: SimAction, Config: SimConfig): ObservableState {
    package "SmartHouse"      
}

graph (input: ObservableState): SimAction {
    concept SmartHouse(input): SimAction {
        
        curriculum {
            source SmartHouseSim
            goal (State: ObservableState) {
                minimize `Temp Deviation`:
                    TempDiff(State.Tin, State.Tset) in Goal.RangeBelow(MaxDeviation)

                # minimize `Total Power Consumption`:
                #     State.total_power in Goal.RangeBelow(1)
            }

            training {
                EpisodeIterationLimit:  HoursToIteration(24,timestep)
            }

            lesson `Tout Constant` {
                scenario {
                    K: 0.5,
                    C: 0.3,
                    Qhvac: 9,
                    Tin_initial: 21,
                    max_iterations: HoursToIteration(24,timestep),
                    timestep: timestep,
                    starting_hour: 0,
                    tset_day_start: 7,
                    tset_day_end: 22,
                    t_set_day: 21,
                    t_set_night: 21,
                    t_mid_point: 25,
                    t_amplitude: 5,
                }
            }

            lesson `Tout changing` {
                scenario {
                    K: 0.5,
                    C: 0.3,
                    Qhvac: 9,
                    Tin_initial: 21,
                    max_iterations: HoursToIteration(24,timestep),
                    timestep: timestep,
                    starting_hour: 0,
                    schedule_index: 2,
                    tset_day_start: 7,
                    tset_day_end: 22,
                    t_set_day: 21,
                    t_set_night: 21,
                    t_mid_point: 25,
                    t_amplitude: 5,
                }
            }

            lesson `Change t initial`{
                scenario {
                    K: 0.5,
                    C: 0.3,
                    Qhvac: 9,
                    Tin_initial: 21,
                    max_iterations: HoursToIteration(24,timestep),
                    timestep: timestep,
                    starting_hour: 0,
                    schedule_index: 2,
                    tset_day_start: 7,
                    tset_day_end: 22,
                    t_set_day: 21,
                    t_set_night: 21,
                    t_mid_point: 25,
                    t_amplitude: 5,
                }
            }

            lesson `Change starting hour`{
                scenario {
                    K: 0.5,
                    C: 0.3,
                    Qhvac: 9,
                    Tin_initial: number<10 .. 30>,
                    max_iterations: HoursToIteration(24,timestep),
                    timestep: timestep,
                    starting_hour: number<0 .. 23>,
                    schedule_index: 2,
                    tset_day_start: 7,
                    tset_day_end: 22,
                    t_set_day: 21,
                    t_set_night: 21,
                    t_mid_point: 25,
                    t_amplitude: 5,
                }
            }

            lesson `Change tset day & night` {
                scenario {
                    K: 0.5,
                    C: 0.3,
                    Qhvac: 9,
                    Tin_initial: number<10 .. 30>,
                    max_iterations: HoursToIteration(24,timestep),
                    timestep: timestep,
                    starting_hour: number<0 .. 23>,
                    schedule_index: 2,
                    tset_day_start: 7,
                    tset_day_end: 22,
                    t_set_day: number<18 .. 23>,
                    t_set_night: number<15 .. 21>,
                    t_mid_point: 25,
                    t_amplitude: 5,
                }
            }

            lesson `Fully Tout & Tin random` {
                scenario {
                    K: 0.5,
                    C: 0.3,
                    Qhvac: 9,
                    Tin_initial: number<10 .. 30>,
                    max_iterations: HoursToIteration(24,timestep),
                    timestep: timestep,
                    starting_hour: number<0 .. 23>,
                    schedule_index: 2,
                    tset_day_start: number<4 .. 11>,
                    tset_day_end: number<18 .. 23>,
                    t_set_day: number<18 .. 23>,
                    t_set_night: number<15 .. 21>,
                    t_mid_point: number<20 .. 30>,
                    t_amplitude: number<3 .. 10>,
                }
            }


            # lesson `Fully random` {
            #     scenario {
            #         K: number<0.5 .. 0.7>,
            #         C: number<0.3 .. 0.7>,
            #         Qhvac: number<5 .. 15>,
            #         Tin_initial: number<10 .. 30>,
            #         max_iterations: HoursToIteration(24,timestep),
            #         timestep: timestep,
            #         starting_hour: number<0 .. 23>,
            #         schedule_index: 2,
            #         tset_day_start: number<4 .. 11>,
            #         tset_day_end: number<18 .. 23>,
            #         t_set_day: number<18 .. 23>,
            #         t_set_night: number<15 .. 21>,
            #         t_mid_point: number<20 .. 30>,
            #         t_amplitude: number<3 .. 10>,
            #     }
            # }
        }
    }
}
