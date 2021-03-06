# -*- coding: utf-8 -*-
import importer
import networkx as nx
# from fastest_path.naive import naive
from fastest_path.naive import naive_path
from fastest_path.vehicle import EV
#from fastest_path.dijkstra import single_source_dijkstra_path_length
from fastest_path.roadnetwork import RoadNetwork
from fastest_path.rn_algorithms import fastest_path_greedy
from linearprogramming import linearProgramming
from test_utils import *
import subprocess
import time

def experiment_cs_density(ev, iterations, path_distance, file_name='cs_density.csv'):
    with open(file_name, 'a') as f:
        f.write('CS density,naive-time,naive-fail,greedy-time,greedy-fail\n')

    rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))
    s, t, dist = s_and_t(rn, path_distance)
    for cs_dist in range(8,55,3):
        print 'CS density experiment. currently at: ', cs_dist
        rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))

        charge_station_density(rn, cs_dist)
        naive_t,greedy_t = 0,0
        naive_f, greedy_f = 0,0

        for iteration in range(iterations):
            ### NAIVE
            _, time = naive_path(rn, s, t, ev)
            naive_t += time if time!=float('inf') else 0
            naive_f += 0 if time!=float('inf') else 1

            ### Greedy
            _, time = fastest_path_greedy(rn, s, t, 1, ev) # 1 for slope
            greedy_t += time if time!=float('inf') else 0
            greedy_f += 0 if time!=float('inf') else 1

        with open(file_name, 'a') as f:
            f.write('%s,%s,%s,%s,%s\n' % (
                                              cs_dist,
                                              naive_t/(iterations-naive_f) if iterations != naive_f else 'inf',
                                              naive_f,
                                              greedy_t/(iterations-greedy_f) if iterations != greedy_f else 'inf',
                                              greedy_f,
                                             ))
        subprocess.call(["say", str(greedy_t/(iterations-greedy_f)) if iterations != greedy_f else 'inf'])

def experiment_runtime_compexity(ev, iterations, path_distance, CS_density, step_size, file_name='time_complexity.csv'):
    rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))
    charge_station_density(rn, CS_density)
    number_of_nodes = 400000

    with open(file_name, 'a') as f:
        f.write('nodes,dijkstra,greedy\n')

    while number_of_nodes > 0:
        actual_nodes = set_roadnetwork_complexity(rn, number_of_nodes)

        dijkstra_t,greedy_t = 0,0
        for x in range(iterations):
            s,t,dist = s_and_t(rn, path_distance)

            ### Dijkstras
            start_time = time.time()
            nx.single_source_dijkstra_path_length(rn, s, weight='t')
            dijkstra_t += time.time() - start_time

            ### Greedy
            start_time = time.time()
            fastest_path_greedy(rn, s, t, 1, ev)
            greedy_t += time.time() - start_time

        with open(file_name, 'a') as f:
            f.write('%s,%s\n' % (actual_nodes, dijkstra_t/iterations, greedy_t/iterations ))

        number_of_nodes -= step_size

def experiment_ev_consumption(iterations, path_distance,con_rate_variance, CS_density, file_name='ev_consumption.csv'):
    rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))
    charge_station_density(rn, cs_dist)
    s, t, dist = s_and_t(rn, path_distance)
    with open(file_name, 'a') as f:
        f.write('CS density,naive-time,naive-fail,greedy-time,greedy-fail\n')

    ev_number = 0
    for ev in scale_cons_rate(con_rate_variance): #Create vehicles
        print 'charge station experiment. currently at EV: ', ev_number

        scale_charge_rates(rn, 1+(scale_factor/100.0))

        naive_t, greedy_t = 0,0
        naive_f, greedy_f = 0,0
        for iteration in range(iterations):
            ### NAIVE
            _, time = naive_path(rn, s, t, ev)
            naive_t += time if time!=float('inf') else 0
            naive_f += 0 if time!=float('inf') else 1

            ### Greedy
            _, time = fastest_path_greedy(rn, s, t, 1, ev) # 1 for slope
            greedy_t += time if time!=float('inf') else 0
            greedy_f += 0 if time!=float('inf') else 1


        with open(file_name, 'a') as f:
            f.write('%s,%s,%s,%s,%s\n' % (
                                            scale_factor,
                                            naive_t/(iterations-naive_f) if iterations != naive_f else 'inf',
                                            naive_f,
                                            greedy_t/(iterations-greedy_f) if iterations != greedy_f else 'inf',
                                            greedy_f,
                                            ))
        ev_number += 1

def experiment_charge_rate(ev, iterations,charge_rate_variance, path_distance, CS_density, step_size, file_name='charge_rate.csv'):
    with open(file_name, 'a') as f:
        f.write('Charge rate scale,naive-time,naive-fail,greedy-time,greedy-fail\n')
    rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))
    s, t, dist = s_and_t(rn, path_distance)


    for scale_factor in range(-charge_rate_variance, charge_rate_variance, step_size):
        print 'charge station experiment. currently at: ', 1+(scale_factor/100.0)
        rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))
        set_roadnetwork_complexity(rn, 500000)
        charge_station_density(rn, CS_density)

        scale_charge_rates(rn, 1+(scale_factor/100.0))

        naive_t, greedy_t = 0,0
        naive_f, greedy_f = 0,0
        for iteration in range(iterations):
            ### NAIVE
            _, time = naive_path(rn, s, t, ev)
            naive_t += time if time!=float('inf') else 0
            naive_f += 0 if time!=float('inf') else 1

            ### Greedy
            _, time = fastest_path_greedy(rn, s, t, 1, ev) # 1 for slope
            greedy_t += time if time!=float('inf') else 0
            greedy_f += 0 if time!=float('inf') else 1

        with open(file_name, 'a') as f:
            f.write('%s,%s,%s,%s,%s,%s,%s\n' % (
                                              scale_factor,
                                              naive_t/(iterations-naive_f) if iterations != naive_f else 'inf',
                                              naive_f,
                                              greedy_t/(iterations-greedy_f) if iterations != greedy_f else 'inf',
                                            greedy_f,
                                             ))

def experiment_driving_dist(ev, CS_density,min_dist, max_dist, step_size, iterations, file_name='driving_dist.csv'):
    print('loading road network...')
    rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))
    print('setting charge stations...')
    charge_station_density(rn, CS_density)

    with open(file_name, 'a') as f:
        f.write('driving distance, naive-time, naive-fail, greedy-time, greedy-fail\n')

    for distance in range(min_dist, max_dist, step_size):
        print 'driving distance experiment. currently at: ', distance
        naive_t, greedy_t = 0,0
        naive_f, greedy_f = 0,0
        for iteration in xrange(iterations):
            s, t, dist = s_and_t(rn, distance)
            print 'iteration: ', iteration + 1, ' distance: ', dist
            print 's: ', rn.edges([s], data=True)[0], ' t: ', rn.edges([t], data=True)[0]
            ### NAIVE
            print 'Initialising Naive...'
            _, time = naive_path(rn, s, t, ev)
            naive_t += time if time!=float('inf') else 0
            naive_f += 0 if time!=float('inf') else 1

            linear_t1, cur = linearProgramming(rn, _, ev, ev.curbat)


            print 'done'

            ### Greedy
            print 'Initialising Greedy...'
            _, time = fastest_path_greedy(rn, s, t, 1, ev) # 1 for slope
            greedy_t += time if time!=float('inf') else 0
            greedy_f += 0 if time!=float('inf') else 1
            linear_t2, cur = linearProgramming(rn, _, ev, ev.curbat)
            print naive_t, linear_t1, greedy_t, linear_t2


            print 'done'

        with open(file_name, 'a') as f:
            f.write('%s,%s,%s,%s,%s\n' % (
                                              distance,
                                              naive_t/(iterations-naive_f) if iterations != naive_f else 'inf',
                                              naive_f,
                                              greedy_t/(iterations-greedy_f) if iterations != greedy_f else 'inf',
                                              greedy_f,
                                              ))

def lp_driving_dist(ev, CS_density,min_dist, max_dist, step_size, iterations, file_name='lpdriving_dist.csv'):
    print('loading road network...')
    rn = RoadNetwork(nx.read_gpickle('pickle_experiment'))
    print('setting charge stations...')
    charge_station_density(rn, CS_density)

    with open(file_name, 'a') as f:
        f.write('driving distance, naive-time, naive-fail, greedy-time, greedy-fail\n')

    for distance in range(min_dist, max_dist, step_size):
        print 'driving distance experiment. currently at: ', distance
        naive_t, greedy_t = 0,0
        naive_f, greedy_f = 0,0
        for iteration in xrange(iterations):
            s, t, dist = s_and_t(rn, distance)
            print 'iteration: ', iteration + 1, ' distance: ', dist
            print 's: ', rn.edges([s], data=True)[0], ' t: ', rn.edges([t], data=True)[0]
            ### NAIVE
            print 'Initialising Naive...'
            _, time = naive_path(rn, s, t, ev)
            print _
            print time 
            naive_t += time if time!=float('inf') else 0
            naive_f += 0 if time!=float('inf') else 1
           

            #linear_t1, cur = linearProgramming(rn, _, ev, ev.curbat)


            print 'done'

            ### Greedy
            print 'Initialising Greedy...'
            _, time = fastest_path_greedy(rn, s, t, 1, ev) # 1 for slope
            print _
            print time
            greedy_t += time if time!=float('inf') else 0
            greedy_f += 0 if time!=float('inf') else 1

            print 'Initialising LP'
            _, time = fastest_path_greedy(rn, s, t, 0, ev) # 1 for slope
            print _
            print time
            print 'done'
        
        with open(file_name, 'a') as f:
            f.write('%s,%s,%s,%s,%s\n' % (
                                              distance,
                                              naive_t/(iterations-naive_f) if iterations != naive_f else 'inf',
                                              linear_t1,
                                              greedy_t/(iterations-greedy_f) if iterations != greedy_f else 'inf',
                                              linear_t2,
                                              ))


ev = EV(50, 10, lambda x: (0.019*x**2 - 0.770*x + 184.4) * 10**(-3))  # ((0.04602*x**2 +  0.6591*x + 173.1174)* 10**(-3)))

#experiment_cs_density(ev, 1, 300)

#experiment_runtime_compexity(ev, 1, 300, 200, 20)

#experiment_ev_consumption(5, 300, 30)

#experiment_charge_rate(ev, 5, 30, 300, 30, 5)

lp_driving_dist(ev, 10, 400, 450, 50, 1)
