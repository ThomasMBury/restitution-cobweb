#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 14 Nov 2020

Dash app for cobweb plot

@author: tbury
"""

import os
import numpy as np
import pandas as pd

import base64

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app_functions import phase_map, generate_phase_trajectory, make_phase_map


#-------------
# Launch the dash app
#---------------

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Get mathjax for latex
external_scripts = ['https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML']



app = dash.Dash(__name__, 
				external_stylesheets=external_stylesheets,
                external_scripts = external_scripts,
				)


print('Launching dash')
server = app.server


#-----------------
# Generate figures
#-------------------


# Defualt values for simulation
phi0 = 0.2 # initial condition
nmax = 2 # number of iterations

# Create phase map function (might want to add extra parameters here)
def phase_map_specific(phi):
    return phase_map(phi)

# Generate phi trajectory
phi_traj = generate_phase_trajectory(phase_map_specific, nmax, phi0)


# Make figure of phase map and stable trajectory
fig_phase_map = make_phase_map(phase_map_specific,
                               phi_traj,
                               )


#--------------------
# App layout
#–-------------------


# Font sizes
size_slider_text = '15px'
size_title = '30px'


# Parameter bounds
phi0_min = 0
phi0_max = 1
phi0_marks = {x:str(round(x,2)) for x in np.arange(0,1.1,0.2)}

nmax_min = 0
nmax_max = 1000
nmax_marks = {float(x):str(round(x,2)) for x in np.arange(0,nmax_max,100)}


# # PDF image of text
# image_filename = 'diff_eqn.png' # replace with your own image
# encoded_image = base64.b64encode(open(image_filename, 'rb').read())



model_text = \
'''
Phase map:
$$ x_{t+1} = 
\\begin{cases}
\\frac{3}{2} x_t & 0 \leq x_t < \\frac{2}{3},\\\\
\\frac{3}{2} x_t - 1 & \\frac{2}{3} \leq x_t < 1
\\end{cases}
$$
'''

model_text_2_line1 = \
'''
x_{t+1} = (3/2)x_t for 0 <= x_t < 2/3
'''
model_text_2_line2 = \
'''
x_{t+1} = (3/2)x_t - 1 for 2/3 <= x_t < 1
'''


app.layout = html.Div([
      
    
    # html.Div(
    #     html.H1('Cobweb plot',
    #              	style={'textAlign':'center',
    #                     'fontSize':size_title,
    #                     'color':'black'}
    #             )
    #     ),
    
    # Left half of app
 	html.Div([
        
        
        html.H1('Cobweb plot',
                 style={'textAlign':'left',
                        'fontSize':size_title,
                        'color':'black'}
                ),
        

        
        # Model description
        html.P(model_text_2_line1,
                style={'fontSize':15,
                      'color':'black',
                      # 'textAlign':'left',
                      }),
        html.Br(),
        html.P(model_text_2_line2,
                style={'fontSize':15,
                      'color':'black',
                      # 'textAlign':'left',
                      }),        
         
        html.Br(),
        
        # Slider for phi0
		html.Label('Initial condition = {}'.format(phi0),
 				   id='phi0_slider_text',
 				   style={'fontSize':size_slider_text}),  
 				   
		dcc.Slider(id='phi0_slider',
 				   min=phi0_min, 
 				   max=phi0_max, 
 				   step=0.001,
 				   marks=phi0_marks,
 				   value=phi0
		),          
         
         
		# Slider for nmax
		html.Label('Number of iterations = {}'.format(nmax),
 				   id='nmax_slider_text',
 				   style={'fontSize':size_slider_text}),  
 				   
		dcc.Slider(id='nmax_slider',
 				   min=nmax_min, 
 				   max=nmax_max, 
 				   step=1.0, 
 				   marks=nmax_marks,
 				   value=nmax
		),
        
        
        ],       
		style={'width':'30%',
			   'height':'500px',
			   'fontSize':'10px',
			   'padding-left':'5%',
			   'padding-right':'5%',
			   'padding-bottom':'0px',
               'padding-top':'40px',
			   'vertical-align': 'middle',
			   'display':'inline-block'},
        ),


 	# Phase map figure
 	html.Div(
		[dcc.Graph(id='phase_plot',
 				   figure = fig_phase_map,
 				   # config={'displayModeBar': False},
 				   ),
 		 ],
		style={'width':'55%',
			   'height':'500px',
			   'fontSize':'10px',
			   'padding-left':'0%',
			   'padding-right':'5%',
			   'vertical-align': 'middle',
			   'display':'inline-block'},
 	),


])
        

# #–-------------------
# # Callback functions
# #–--------------------

  
# Update text for sliders             
@app.callback(
        [Output('phi0_slider_text','children'),
         Output('nmax_slider_text','children'),
          ],
        [
          Input('phi0_slider','value'),
          Input('nmax_slider','value'),
          ]
)

def update_slider_text(phi0,nmax):
    
    # Slider text update
    text_phi0 = 'Initial condition = {}'.format(phi0)
    text_nmax = 'Number of iterations = {}'.format(nmax)      

    return text_phi0, text_nmax
            
         

# Update figures
@app.callback(
            Output('phase_plot','figure'),
            [
              Input('phi0_slider','value'),
              Input('nmax_slider','value'),           
            ],
            )

def update_figs(phi0, nmax):
    
    # Phase map
    def phase_map_specific(phi):
        return phase_map(phi) 
    
    # Generate phi trajectory
    phi_traj = generate_phase_trajectory(phase_map_specific, nmax, phi0)
    
        
    # Make figure of phase map and stable trajectory
    fig_phase_map = make_phase_map(phase_map_specific,
                                   phi_traj,
                                   )

    return fig_phase_map


#-----------------
# Add the server clause
#–-----------------

if __name__ == '__main__':
    app.run_server(
        debug=True,
        host='127.0.0.1',
        )

