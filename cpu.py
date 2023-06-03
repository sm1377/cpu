import psutil
import tkinter as tk


class CPUCore:
    def __init__(self):
        self.usage = psutil.cpu_percent()
        self.increment = 0

    def get_usage(self):
        return self.usage

    def increase_usage(self, increment):
        new_usage = self.usage + increment
        if new_usage < 0:
            new_usage = 0
        elif new_usage > 100:
            new_usage = 100
        self.usage = new_usage
        self.increment = increment


class CPUSystem:
    def __init__(self):
        self.cores = [CPUCore() for i in range(psutil.cpu_count())]

    def get_usage(self):
        return psutil.cpu_percent()

    def increase_usage(self, increment):
        for core in self.cores:
            core.increase_usage(increment)

    def get_core_usages(self):
        core_usages = []
        for core in self.cores:
            core_usages.append(core.get_usage())
        return core_usages


class App:
    def __init__(self, master):
        self.master = master
        master.title("CPU Usage Simulator")

        # create the CPU system object
        self.cpu_system = CPUSystem()

        # create the CPU core usage labels
        self.core_labels = []
        for i in range(psutil.cpu_count()):
            label = tk.Label(master, text="Core {}: {:.1f}%".format(i + 1, self.cpu_system.cores[i].get_usage()))
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            self.core_labels.append(label)

        # create the system usage label
        self.system_label = tk.Label(master, text="System: {:.1f}%".format(self.cpu_system.get_usage()))
        self.system_label.grid(row=psutil.cpu_count(), column=0, padx=10, pady=5, sticky="w")

        # create the increase usage entry and button
        self.increase_entry = tk.Entry(master, width=5)
        self.increase_entry.grid(row=psutil.cpu_count() + 1, column=0, padx=10, pady=5, sticky="w")
        self.increase_entry.insert(0, "10")
        self.increase_button = tk.Button(master, text="Increase Usage", command=self.increase_usage)
        self.increase_button.grid(row=psutil.cpu_count() + 1, column=1, padx=10, pady=5, sticky="w")

        # create the reset button
        self.reset_button = tk.Button(master, text="Reset Usage", command=self.reset_usage)
        self.reset_button.grid(row=psutil.cpu_count() + 2, column=1, padx=10, pady=5, sticky="w")

        # start the update loop
        self.update_loop()

    def update_loop(self):
        # update the core usage labels
        core_usages = self.cpu_system.get_core_usages()
        for i in range(psutil.cpu_count()):
            self.core_labels[i]["text"] = "Core {}: {:.1f}%".format(i + 1, core_usages[i])

        # update the system usage label
        system_usage = self.cpu_system.get_usage()
        self.system_label["text"] = "System: {:.1f}%".format(system_usage)

        # update the window title
        self.master.title("CPU Usage Simulator - System Usage: {:.1f}%".format(system_usage))

        # schedule the next update
        self.master.after(500, self.update_loop)

    def increase_usage(self):
        increment = int(self.increase_entry.get())
        self.cpu_system.increase_usage(increment)

    def reset_usage(self):
        self.cpu_system = CPUSystem()


# create the tkinter window
root = tk.Tk()
app = App(root)
root.mainloop()