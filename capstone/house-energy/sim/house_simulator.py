import numpy as np
import matplotlib.pyplot as plt
import math


class House():
    def __init__(self, K: float = 0.5, C: float = 0.3, Qhvac: float = 9, hvacON: float = 0, occupancy: float = 1, Tin_initial: float = 30):
        self.K = K  # thermal conductivity
        self.C = C  # thermal capacity
        self.Tin = Tin_initial  # Inside Temperature
        self.Qhvac = Qhvac  # Cooling capacity
        self.hvacON = hvacON  # control action = 0 (OFF) or 1 (ON)

        # 0 (no one in the room) or 1 (somebody in the room)
        self.occupancy = occupancy
        self.Phvac = Qhvac  # Electric power capacity

        self.minute = 0
        self.hours = 0
        self.total_power = 0  # total power consumption
        self.max_iterations = 0

        plt.close()
        self.fig, self.ax = plt.subplots(1, 1)

    def setup_schedule(self, max_iterations: int = 288, timestep: int = 5, schedule_index: int = 0, starting_hour=0, tset_day_start: int = 7, tset_day_end: int = 22, t_set_day=23, t_set_night=18, t_mid_point=25, t_amplitude=5):
        """ define the Tset_schedule, Tout_schedule, the length of schedule, timestep
        """
        self.timestep = max(
            1, timestep)  # keep in minutes here to keep number of minutes for days consistent
        starting_hour_index = self.__time_to_index(starting_hour, timestep)
        # an iteration spans 1 day
        self.max_iterations = max_iterations
        self.occupancy_schedule = np.full(self.max_iterations, 1)

        self.Tset_schedule = np.full(self.max_iterations, 25)
        a, b = self.__time_to_index(
            tset_day_start, timestep), self.__time_to_index(tset_day_end, timestep)
        self.Tset_schedule[:a] = t_set_night
        self.Tset_schedule[b:] = t_set_night
        self.Tset_schedule[a:b] = t_set_day

        # constant outside weather

        # generate sinus weather
        if schedule_index == 1:
            self.Tout_schedule = self.generate_Tout(
                t_mid_point=t_mid_point, t_amplitude=t_amplitude, timestep=timestep)

        # generate sinus weather add noise
        elif schedule_index == 2:
            self.Tout_schedule = self.generate_Tout(
                t_mid_point=t_mid_point, t_amplitude=t_amplitude, timestep=timestep)

            self.Tout_schedule = self.Tout_schedule + \
                np.random.normal(0, 0.25, size=len(self.Tout_schedule))
        else:
            self.Tout_schedule = np.full(self.max_iterations, 32)

        # # randomize
        # if schedule_index == 2:
        #     self.Tset_schedule = np.full(self.max_iterations, 25)
        #     self.Tout_schedule = np.full(self.max_iterations, 32)
        #     self.occupancy_schedule = np.full(self.max_iterations, 1)
        #     for d in range(days):
        #         # We assume people leave home between 9:00 and return at 17:00
        #         a = time_to_index(d, 9)
        #         b = time_to_index(d, 16)
        #         self.Tset_schedule[a:b]= np.random.randint(low=18, high=21)
        #         c = time_to_index(d, 8)
        #         d = time_to_index(d, 17)
        #         self.Tset_schedule[:c] = np.random.randint(low=17, high=20)
        #         self.Tset_schedule[d:-1] = np.random.randint(low=17, high=20)
        #         self.Tout_schedule[:c] = np.random.randint(low=22, high=26)
        #         self.Tout_schedule[d:-1] = np.random.randint(low=28, high=35)

        # simpler
        # if schedule_index == 2:
        #     self.Tset_schedule = np.full(self.max_iterations, 25)
        #     self.Tset_schedule[96:204] = 20
        #     self.Tout_schedule = np.full(self.max_iterations, 32)
        #     self.occupancy_schedule = np.full(self.max_iterations, 1)

        self.Tset_schedule = np.roll(self.Tset_schedule, -starting_hour_index)
        self.Tout_schedule = np.roll(self.Tout_schedule, -starting_hour_index)

        self.Tset = self.Tset_schedule[0]  # Set Temperature
        self.Tout = self.Tout_schedule[0]  # Outside temperature

        # self.Tset1 = self.Tset_schedule[1]  # Set Temperature i+1
        # self.Tset2 = self.Tset_schedule[2]  # Set Temperature i+2
        # self.Tset3 = self.Tset_schedule[3]  # Set Temperature i+3

        # For plotting only
        self.time_to_plot = [0]
        self.Tin_to_plot = [self.Tin]
        self.Tset_to_plot = [self.Tset]
        self.Tout_to_plot = [self.Tout]

        self.__iter__()

    def generate_Tout(self, t_mid_point: int = 25, t_amplitude: int = 5, timestep: int = 5):
        """Use a sinus function to create a change in temperature

        """
        weather = [
            t_amplitude*math.sin((x-6*60)*math.pi/(12*60))+t_mid_point for x in range(24*60)]

        filtered_weather = weather[::timestep]

        return filtered_weather

    def update_Tout(self, Tout_new):
        self.Tout = Tout_new  # Update to new outside temperature

    def update_Tset(self, Tset_new):
        self.Tset = Tset_new  # Update to new setpoint temperature

    def update_hvacON(self, hvacONnew):
        self.hvacON = hvacONnew  # update to new hvacON

    def update_occupancy(self, occupancy_new):
        self.occupancy = occupancy_new  # update to new occupancy

    def update_Tin(self):
        """Update inside temperation.
        Describes the inside temperature evolution as a function of all other variables. 
        """
        # Note timestep is converted to seconds here, in order to keep units consistent in SI for update.
        self.Tin = self.Tin - (self.timestep/60) / self.C * \
            (self.K * (self.Tin - self.Tout) + self.Qhvac * self.hvacON)

        self.__next__()
        self.Tset_to_plot.append(self.Tset)
        self.Tin_to_plot.append(self.Tin)
        self.Tout_to_plot.append(self.Tout)
        self.time_to_plot.append(self.iteration * 5)

    def update_time(self):
        self.minute, self.hours = self.__index_to_time(self.iteration)

    def update_total_power(self):
        self.total_power += self.get_Power()

    def get_Power(self):
        COP = 3
        power = self.Phvac * self.hvacON * COP
        return power

    def show(self):

        self.ax.clear()
        self.ax.plot(self.time_to_plot, self.Tin_to_plot, label='Tin')
        self.ax.plot(self.time_to_plot, self.Tset_to_plot, label='Tset')
        self.ax.plot(self.time_to_plot, self.Tout_to_plot, label='Tout')
        self.ax.set_xlabel('Time [min]')
        self.ax.set_ylabel(r'Temperature [$^\circ$C]')
        plt.legend()
        plt.pause(np.finfo(np.float32).eps)

 # print the object nicely
    def __str__(self):
        string_to_print = []
        for key in self.__dict__:
            string_to_print.append("{key}='{value}'".format(
                key=key, value=self.__dict__[key]))
        return ', '.join(string_to_print)

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        self.iteration = 0
        return self

    def __next__(self):
        if self.iteration < self.max_iterations:  # - 5
            self.update_Tset(self.Tset_schedule[self.iteration])
            # self.Tset1 = self.Tset_schedule[self.iteration+1]
            # self.Tset2 = self.Tset_schedule[self.iteration+2]
            # self.Tset3 = self.Tset_schedule[self.iteration+3]
            self.update_Tout(self.Tout_schedule[self.iteration])
            self.update_occupancy(self.occupancy_schedule[self.iteration])
            self.update_time()
            self.update_total_power()
            self.iteration += 1
        else:
            StopIteration

    def __time_to_index(self, hours, timestep=5):
        hours_index = int(hours * 60 / timestep)
        return hours_index

    def __index_to_time(self, iteration, timestep=5):
        minute = int(iteration * timestep % 60)
        hours = int(iteration*timestep/60 % 24)
        return minute, hours


if __name__ == '__main__':
    import random
    house = House(K=0.5, C=0.3, Qhvac=9)
    days = 7
    timestep = 5
    for episode in range(1):
        house.setup_schedule(timestep=timestep,
                             schedule_index=1,
                             starting_hour=12,
                             t_set_day=30,
                             t_set_night=30,
                             )

        for i in range(house.max_iterations):
            # house.update_hvacON(random.randint(0, 1))
            house.update_hvacON(1)
            house.update_Tin()
            print(f'Hour : {house.hours}', f'Minute : {house.minute}', f'Tout : {house.Tout}', f'Tin : {house.Tin}',
                  f'HvacOn : {house.hvacON}', f'Tset : {house.Tset}', f'Total Power : {house.total_power}')

            house.show()
