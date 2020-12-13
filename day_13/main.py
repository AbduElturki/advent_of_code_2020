import operator as op
from sympy.ntheory.modular import crt

if __name__ == "__main__":
    with open("input.txt") as f:
        earliest_depart = int(f.readline().strip())
        services = f.readline().strip().split(",")
    active_service = [int(x) for x in services if x != "x" ]
    possible_times = {x: (earliest_depart - (earliest_depart % x)) + x
                      for x in active_service}
    earliest_bus = min(possible_times.keys(),
                       key=(lambda k: possible_times[k]))
    print("Part 1:", (possible_times[earliest_bus] - earliest_depart) * \
          earliest_bus)

    bus_mod = {int(services[x]): x for x in range(len(services))
               if services[x] != 'x'}
    # Bus X appears at time I and departs at T+I, where T+I is multiple of X
    # T+I % X == 0
    # T % K == -I
    print("Part 2:", crt(bus_mod.keys(), map(op.neg, bus_mod.values())))
