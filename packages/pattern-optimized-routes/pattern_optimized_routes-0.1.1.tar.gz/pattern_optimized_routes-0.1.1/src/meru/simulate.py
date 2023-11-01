import os
import sys
import time

from tqdm import tqdm
import libsumo as traci
import traci.constants as tc

from xml.dom import minidom

import pandas as pd


def save_results(to_save, save_path = '/'):

    # Define the file paths
    output_file = save_path+'simulation_results.csv'

    # Read the existing CSV file
    try:
        df = pd.read_csv(output_file)
    except FileNotFoundError:
        pd.DataFrame(columns = list(to_save)).to_csv(output_file, index = False)
        df = pd.read_csv(output_file)

    # Append the new row to the DataFrame
    df = df.append(to_save, ignore_index=True)

    # Write the updated DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

    return df

def simulate_sumo_paths(paths_and_measures, road_network_path, route_filename, max_steps = 36000):
    total_vehicles = len(paths_and_measures['paths'])

    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)

    sumo_binary = os.environ['SUMO_HOME']+"/bin/sumo"
    def_options = [sumo_binary, "-n", road_network_path, "-r", route_filename]
    opt_options = "-W --ignore-junction-blocker 20 --time-to-impatience 30 --time-to-teleport 120 --scale 1".split(' ')
    options = def_options + opt_options

    conn = traci.start(options)
    sumo_version = conn[1]
    print(f"{sumo_version} and TraffiCO2 version 2.03")

    # start time
    start_t = time.time()

    # simulation variables
    step, vehicles_arrived = 0, 0

    with tqdm(total=total_vehicles, desc="Vehicles Arrived") as pbar:
        while vehicles_arrived < total_vehicles and step < max_steps:

            vehicles_step = 0

            traci.simulationStep()
            vehicle_list = traci.vehicle.getIDList()

            # Subscriptions (only once when the vehicle enters the simulation)
            for veh_id in traci.simulation.getDepartedIDList():
                traci.vehicle.subscribe(veh_id, [tc.VAR_CO2EMISSION])

            for vehicle in vehicle_list:

                # get the results from the Subscription
                res_sub = traci.vehicle.getSubscriptionResults(vehicle)
                co2_emissions = res_sub[tc.VAR_CO2EMISSION]

                # update the data structure that collects the measures
                paths_and_measures['measures']['CO2 Tons'] += co2_emissions
                paths_and_measures['measures']['Vehicles Traveltime'] += 1

            # collect number of teleported vehicles
            paths_and_measures['measures']['N Teleports'] += traci.simulation.getStartingTeleportNumber()

            step += 1
            vehicles_arrived += traci.simulation.getArrivedNumber()
            pbar.update(vehicles_arrived - pbar.n)

    paths_and_measures['measures']['CO2 Tons'] /= 10**9

    elapsed = time.time() - start_t

    #close traci
    traci.close()

    to_return = {'Execution time (s)' : elapsed,
                 'Number of teleports' : paths_and_measures['measures']['N Teleports'],
                 'Total CO2 Tons' : paths_and_measures['measures']['CO2 Tons'],
                 'Total travletime (s)' : paths_and_measures['measures']['Vehicles Traveltime']}

    return to_return

def create_xml_vehicles(dict_vehicles, filename):

    # xml creation
    root = minidom.Document()
    xml = root.createElement("routes")
    xml.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    xml.setAttribute("xsi:noNamespaceSchemaLocation", "http://sumo.dlr.de/xsd/routes_file.xsd")
    root.appendChild(xml)

    #vehicle type(s)
    element = root.createElement("vType")
    element.setAttribute("id", "type1")
    element.setAttribute("accel", "2.6")
    element.setAttribute("decel", "4.5")
    element.setAttribute("sigma", "0.5")
    element.setAttribute("length", "5")
    element.setAttribute("maxSpeed", "70")
    xml.appendChild(element)

    valid_list = []
    invalid_list = []

    # sort the dict
    dict_vehicles_time_sorted = dict(sorted(dict_vehicles.items(),
                                            key=lambda item: item[1]['time']))


    for traj_id in dict_vehicles_time_sorted.keys():

            edge_list = dict_vehicles_time_sorted[traj_id]['edges']

            valid_list.append(traj_id)

            start_second = str(dict_vehicles_time_sorted[traj_id]['time'])

            try:
                col = str(dict_vehicles_time_sorted[traj_id]['color'])
            except:
                col = "blue"

            element = root.createElement("vehicle")
            element.setAttribute("color", col)
            element.setAttribute("id", traj_id)
            element.setAttribute("type", "type1")
            element.setAttribute("depart", start_second)

            route_element = root.createElement("route")
            route_element.setAttribute("edges", edge_list)
            element.appendChild(route_element)

            xml.appendChild(element)

    xml_str = root.toprettyxml(indent="\t")

    with open(filename, "w") as f:
        f.write(xml_str)

    return {'valid':valid_list, 'invalid': invalid_list}

def save_sumo_routes(final_paths, dict_md, save_path, name):

    dict_sumo = {}

    for trip_id in list(dict_md.keys()):

        route_trip_id = final_paths[trip_id]
        selected_path = route_trip_id[0]["edges"]
        new_id = name+"_"+trip_id.split("_")[1]
        dep_time = dict_md[trip_id]['time']

        dict_sumo[new_id] = {'edges':str(selected_path).replace(",","").replace("'","")[1:-1], 'time': dep_time}

    create_xml_vehicles(dict_sumo, f"{save_path}sumo_routes_{name}.rou.xml")