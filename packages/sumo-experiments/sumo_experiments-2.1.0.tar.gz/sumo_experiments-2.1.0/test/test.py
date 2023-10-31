from src.sumo_experiments import Experiment
from src.sumo_experiments.preset_networks import LineNetwork
from src.sumo_experiments.traci_util import *

net = LineNetwork()

exp = Experiment(
    name='test',
    infrastructures=net.generate_infrastructures,
    flows=net.generate_flows_all_directions
)

exp.set_parameter('nb_intersections', 5)
exp.set_parameter('flow_frequency', 300)
exp.set_parameter('green_time', 30)
exp.set_parameter('yellow_time', 3)
exp.set_parameter('lane_length', 100)
exp.set_parameter('simulation_duration', 1000)
exp.set_parameter('stop_generation_time', 1000)
exp.set_parameter('distribution', 'binomial')
exp.set_parameter('max_speed', 50)

tw = TraciWrapper()
tw.add_stats_function(get_co2_emissions_data)

data = exp.run_traci(tw.final_function)

exp.clean_files()

print(data)




