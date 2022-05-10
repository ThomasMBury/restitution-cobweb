#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 13:11:06 2020

@author: tbury
"""

import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go








def cobweb_map(apd, y0, a, b, theta, ts):
    '''
    Function for the cobweb map APD_{i+1} = f(APD_i)

    '''
    
    # Use smallest N such that N*t_s-apd > theta
    args = np.arange(1,10)*ts - apd
    arg = args[args > theta][0]
    
    # Apply restitution curve
    apd_next = y0 + a*(1-np.exp(-b*arg))
    
    return apd_next





def generate_cobweb_trajectory(nmax, apd0, y0, a, b, theta, ts):
    '''
    Generate a cobweb trajectory by iterating the function cobweb_map.
    
    Input:
        nmax: number of iterations
        apd0: initial condition
    '''
    # Generate a phase trajectory
    list_apd = []
    apd=apd0
    list_apd.append(apd0)
    for n in range(nmax):
        apd = cobweb_map(apd, y0, a, b, theta, ts)
        list_apd.append(apd)

    return list_apd


# # Test
# out = generate_cobweb_trajectory(cobweb_map, nmax, apd0, y0, a, b, theta, ts)


def make_cobweb_fig(y0, a, b, theta, ts,
                    apd_traj,
                    ):
    '''
    Make cobweb map of model (draw lines connecting subsequent states)
    Plot the trajectory that is converged to.
    
    Input:
        cobweb_map: function phi_{i+1} = f(phi_{i})
        apd_traj (list): trajectory of apd values
        
    Ouptut:
        Plotly figure of map and stable trajectory
    '''

    # Create values for plot of phase map
    xVals = np.linspace(0,600,1000)
    yVals = np.array([cobweb_map(x, y0, a, b, theta, ts) for x in xVals])
    # # Insert nan at discontinuities
    # pos = np.where(np.abs(np.diff(yVals)) >= 0.01)[0]
    # xVals[pos] = np.nan
    # yVals[pos] = np.nan
    
    # Collect apd data and put in form for plotting lines
    apd_traj_plot = []
    # First line
    apd_traj_plot.append((apd_traj[0],0))
    for i in range(len(apd_traj)-1):
        apd_traj_plot.append((apd_traj[i],apd_traj[i+1]))
        apd_traj_plot.append((apd_traj[i+1],apd_traj[i+1]))


    fig = go.Figure()
    
    # Trace for phase map
    fig.add_trace(
        go.Scatter(x=xVals,
                   y=yVals,
                   showlegend=False,
                   line={'color':'black'},
        )
    )
    
    # Trace for line y=x
    fig.add_trace(
        go.Scatter(x=np.linspace(0,600,1000),
                   y=np.linspace(0,600,1000),
                   line={'dash':'dash',
                         'color':'gray'},
                   showlegend=False,
        )
    )
    
    # Trace for phase trajectory
    fig.add_trace(
        go.Scatter(x=[tup[0] for tup in apd_traj_plot],
                   y=[tup[1] for tup in apd_traj_plot],
                   showlegend=False,
                   line={'color':'royalblue'},
        )
    )
    
    
    fig.update_xaxes(
        range=[0,250],
        title='APD_{i}',
    )
    
    fig.update_yaxes(
        range=[0,250],
        title='APD_{i+1}',
    )
    
    fig.update_layout(
        # width=500, height=500,
        margin=dict(l=50,r=10,t=70,b=10),
        )


       
    return fig





def make_restitution_fig(y0=120, a=96.9, b=0.0104):
    
    # Create values for plot of phase map
    x = np.linspace(0,300,1000)
    y = y0 + a*(1-np.exp(-b*x))
    
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=x, y=y,
                   showlegend=False,
                   mode='lines',
                   )
    )
    fig.update_xaxes(title = 'DI (ms)', range=[0,300])
    fig.update_yaxes(title = 'APD (ms)', range=[50,250])
    
    fig.update_layout(
        # width=500, height=500,
        margin=dict(l=50,r=10,t=70,b=10),
        )
    
    return fig    








# #----------------
# # Test functions
# #------------------- 



# # Test function to generate a trajectory
# y0=120
# a=96.9
# b=0.0104
# theta = 20
# ts = 400

# apd0 = 300
# nmax = 100



# apd_traj = generate_cobweb_trajectory(nmax, apd0, y0, a, b, theta, ts)


# # Test function to make figure of phase map
# fig_cobweb_map = make_cobweb_fig(y0, a, b, theta, ts, apd_traj)
# fig_cobweb_map.write_html('temp.html')





# fig = make_restitution_plot()
# fig.write_html('temp.html')

