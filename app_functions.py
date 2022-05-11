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





def cobweb_map(apd, apdmax, alpha, tau, theta, ts):
    '''
    Function for the cobweb map APD_{i+1} = f(APD_i)
    As in Guevara et al. 1984
    '''
    
    # Use smallest N such that N*t_s-apd > theta
    args = np.arange(1,10)*ts - apd
    arg = args[args > theta][0]
    
    # Apply restitution curve
    apd_next = apdmax - alpha*np.exp(-arg/tau)
    
    return apd_next




def generate_cobweb_trajectory(nmax, apd0, apdmax, alpha, tau, theta, ts):
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
        apd = cobweb_map(apd, apdmax, alpha, tau, theta, ts)
        list_apd.append(apd)

    return list_apd




def make_cobweb_fig(apdmax, alpha, tau, theta, ts,
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
    yVals = np.array([cobweb_map(x, apdmax, alpha, tau, theta, ts) for x in xVals])
    # # Insert nan at discontinuities
    pos = np.where(np.abs(np.diff(yVals)) >= 1)[0]
    xVals[pos] = np.nan
    yVals[pos] = np.nan
    
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
        title=r'$\text{APD}_{i} \text{ (ms)}$',
    )
    
    fig.update_yaxes(
        range=[0,250],
        title=r'$\text{APD}_{i+1} \text{ (ms)}$',
    )
    
    fig.update_layout(
        # width=500, height=500,
        margin=dict(l=50,r=10,t=100,b=10),
        title=r'$\text{Cobweb plot}\\ \text{APD}_{i+1} = g(Nt_s-\text{APD}_i)$',
        )
       
    return fig





def make_restitution_fig(apdmax, alpha, tau):
    
    # Data points from Ravi (SFU)
    x_data = [293.21, 153.69, 73.31, 42.60, 27.52]
    y_data = [214.71, 189.54, 176.78, 156.91, 139.48]
    
    
    
    # Restitution curve
    x = np.linspace(0,300,1000)
    y = apdmax - alpha * np.exp(-x/tau)
    
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=x, y=y,
                   showlegend=False,
                   mode='lines',
                   )
    )
    fig.add_trace(
        go.Scatter(x=x_data, y=y_data,
                   showlegend=False,
                   mode='markers',
                   )
    )
    fig.update_xaxes(title = r'$\text{DI (ms)}$', range=[0,300])
    fig.update_yaxes(title = r'$\text{APD (ms)}$', range=[50,250])
    
    fig.update_layout(
        # width=500, height=500,
        margin=dict(l=50,r=10,t=100,b=10),
        title=r'$\text{Restitution curve}\\ g(\text{DI})=\text{APD}_{\text{max}} - \alpha \exp^{-\frac{\text{DI}}{\tau}}$',
        )
    
    return fig    



def make_apd_sequence(apd_traj):
    
    x = np.arange(len(apd_traj))
    y = apd_traj

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=x, y=y,
                   showlegend=False,
                   mode='markers+lines',
                   )
    )
    fig.update_xaxes(title = r'$\text{Iteration}$',)
    fig.update_yaxes(title = r'$\text{APD (ms)}$',range=[0,500])
    
    fig.update_layout(
        height=300,
        margin=dict(l=50,r=10,t=30,b=10),
        title=r'$\text{APD sequence}$',
        )
    
    return fig    




#----------------
# Test functions
#------------------- 



# Test function to generate a trajectory
apdmax = 300
alpha = 100
tau = 100
theta = 0
ts = 300

apd0 = 300
nmax = 10

apd_traj = generate_cobweb_trajectory(nmax, apd0, apdmax, alpha, tau, theta, ts)

# fig_cobweb_map = make_cobweb_fig(apdmax, alpha, tau, theta, ts, apd_traj)
# fig_cobweb_map.write_html('temp.html')

fig_apd_sequence = make_apd_sequence(apd_traj)
fig_apd_sequence.write_html('temp.html')




# fig = make_restitution_plot()
# fig.write_html('temp.html')

