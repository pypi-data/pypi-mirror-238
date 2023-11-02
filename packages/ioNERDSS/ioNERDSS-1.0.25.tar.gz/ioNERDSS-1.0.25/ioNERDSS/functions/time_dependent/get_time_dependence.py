import matplotlib.pyplot as plt


def get_time_dependence(filename, components):
    times = []
    counts = []
    components = sorted(components)  # Sort the components to ensure consistent matching

    current_time = None
    count_for_time = 0

    with open(filename, "r") as f:
        for line in f:
            if "Time (s):" in line:
                if current_time is not None:
                    times.append(current_time)
                    counts.append(count_for_time)
                current_time = float(line.split(":")[1].strip())
                count_for_time = 0
            else:
                count, comp = line.split("\t")
                comp_list = sorted(comp.strip().split(". ")[:])
                comp_list[-1] = comp_list[-1][:-1]
                if components == comp_list:
                    count_for_time += int(count)

        # Add the last time point
        if current_time is not None:
            times.append(current_time)
            counts.append(count_for_time)

    return times, counts


def plot_time_dependence(times, counts):
    plt.plot(times, counts)
    plt.xlabel("Time (s)")
    plt.ylabel("Copy Number")
    plt.title("Time Dependence of Complex Copy Numbers")
    plt.show()
