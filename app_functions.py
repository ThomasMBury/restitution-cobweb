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


def phase_map(phi):
    '''
    Function for the phase map phi{i+1} = f(phi_{i})
    for modulated parasystole with delay.

    '''
    
    if (0<=phi) and (phi<2/3):
        phi_next = (3/2)*phi
    else:
        phi_next = (3/2)*phi - 1

    return phi_next



def generate_phase_trajectory(phase_map, nmax, phi0):
    '''
    Generate a phase trajectory by iterating the function phase_map.
    
    Input:
        phase_map: function phi_{i+1} = f(phi_{i})
        nmax: number of iterations
        phi0: initial condition
    '''
    # Generate a phase trajectory
    list_phi = []
    phi=phi0
    list_phi.append(phi0)
    for n in range(nmax):
        phi = phase_map(phi)
        list_phi.append(phi)

    return list_phi



def make_phase_map(phase_map,
                   phi_traj,
                   ):
    '''
    Make phase map of model: modulated parasystole with conduction delay.
    Plot the trajectory that is converged to.
    
    Input:
        phase_map: function phi_{i+1} = f(phi_{i})
        phi_traj (list): trajectory of phi values
        
    Ouptut:
        Plotly figure of map and stable trajectory
    '''

    # Create values for plot of phase map
    xVals = np.linspace(0,1,1000)
    yVals = np.array([phase_map(x) for x in xVals])
    # Insert nan at discontinuities
    pos = np.where(np.abs(np.diff(yVals)) >= 0.01)[0]
    xVals[pos] = np.nan
    yVals[pos] = np.nan
    
    # Collect phi data and put in form for plotting lines
    phi_traj_plot = []
    # First line
    phi_traj_plot.append((phi_traj[0],0))
    for i in range(len(phi_traj)-1):
        phi_traj_plot.append((phi_traj[i],phi_traj[i+1]))
        phi_traj_plot.append((phi_traj[i+1],phi_traj[i+1]))


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
        go.Scatter(x=np.linspace(0,1,100),
                   y=np.linspace(0,1,100),
                   line={'dash':'dash',
                         'color':'gray'},
                   showlegend=False,
        )
    )
    
    # Trace for phase trajectory
    fig.add_trace(
        go.Scatter(x=[tup[0] for tup in phi_traj_plot],
                   y=[tup[1] for tup in phi_traj_plot],
                   showlegend=False,
                   line={'color':'royalblue'},
        )
    )
    
    
    fig.update_xaxes(
        range=[0,1],
        title='x_{t}',
    )
    
    fig.update_yaxes(
        range=[0,1],
        title='x_{t+1}',
    )
    
    fig.update_layout(
        width=500,
        height=500,
        # title='Cobweb plot',
        )

       
    return fig



# #----------------
# # Test functions
# #------------------- 



# # Test function to generate a trajectory
# phi0=0.2
# nmax=10
# phi_traj = generate_phase_trajectory(phase_map, nmax, phi0)


# # Test function to make figure of phase map
# fig_phase_map = make_phase_map(phase_map,
#                                 phi_traj,
#                                 )
# fig_phase_map.write_html('temp.html')



