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

from app_functions import generate_cobweb_trajectory, make_cobweb_fig, make_restitution_fig



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

# Default model parameter values
y0 = 120
a = 96.9
b = 0.0104
theta = 20
ts = 400

# Defualt simulation parameters
apd0 = 150 
nmax = 40

# Generate cobweb trajectory
apd_traj = generate_cobweb_trajectory(nmax, apd0, y0, a, b, theta, ts)

# Make figures
fig_cobweb = make_cobweb_fig(y0, a, b, theta, ts, apd_traj)
fig_restitution = make_restitution_fig(y0, a, b)

#--------------------
# App layout
#–-------------------

# Font sizes
size_slider_text = '15px'
size_title = '30px'

# Parameter bounds
apd0_min = 0
apd0_max = 250
# apd0_step = 1
# apd0_marks = {x:str(x) for x in np.arange(apd0_min,apd0_max,100)}


nmax_min = 0
nmax_max = 100
# nmax_step = 20
# nmax_marks = {float(x):str(round(x,2)) for x in np.arange(nmax_min,nmax_max,20)}


y0_min = 0
y0_max = 200
# y0_step = 10
# y0_marks = {float(x):str(round(x,2)) for x in np.arange(y0_min,y0_max,10)}


a_min = 0
a_max = 200
a_marks = {float(x):str(round(x,2)) for x in np.arange(a_min,a_max,10)}

b_min = 0.005
b_max = 0.05
b_marks = {float(x):str(round(x,4)) for x in np.arange(b_min,b_max,0.01)}

theta_min = 0
theta_max = 50
# theta_step = 20
theta_marks = {float(x):str(round(x,2)) for x in np.arange(theta_min,theta_max,10)}

ts_min = 100
ts_max = 500
# ts_step = 100
# ts_marks = {float(x):str(round(x,2)) for x in np.arange(ts_min,ts_max,100)}


# # PDF image of text
# image_filename = 'diff_eqn.png' # replace with your own image
# encoded_image = base64.b64encode(open(image_filename, 'rb').read())




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
        
        html.H1('Restitution analysis',
                  style={'textAlign':'left',
                        'fontSize':size_title,
                        'color':'black'}
        ),

        # Slider for apd0
		html.Label('APD_0 = {}'.format(apd0),
 				   id='apd0_slider_text',
 				   style={'fontSize':size_slider_text}),  
		dcc.Slider(id='apd0_slider',
 				   min=apd0_min, 
 				   max=apd0_max, 
 				   # step=apd0_step,
 				   # marks=apd0_marks,
 				   value=apd0,
		),
        
         
		# Slider for nmax
		html.Label('Nmax = {}'.format(nmax),
 				   id='nmax_slider_text',
 				   style={'fontSize':size_slider_text}),  
 				   
		dcc.Slider(id='nmax_slider',
 				   min=nmax_min, 
 				   max=nmax_max, 
 				   # step=nmax_step, 
 				   # marks=nmax_marks,
 				   value=nmax
		),

        
        # Slider for y0
		html.Label('Initial condition = {}'.format(y0),
 				   id='y0_slider_text',
 				   style={'fontSize':size_slider_text}),  
 				   
		dcc.Slider(id='y0_slider',
 				   min=y0_min, 
 				   max=y0_max, 
 				   # step=y0_step,
 				   # marks=y0_marks,
 				   value=y0
		),   

        
        # Slider for a
		html.Label('Initial condition = {}'.format(a),
 				   id='a_slider_text',
 				   style={'fontSize':size_slider_text}),  
 				   
		dcc.Slider(id='a_slider',
 				   min=a_min, 
 				   max=a_max, 
 				   # step=a_step,
 				   # marks=a_marks,
 				   value=a
		),           
        
        
        # Slider for b
		html.Label('Initial condition = {}'.format(b),
 				   id='b_slider_text',
 				   style={'fontSize':size_slider_text}),  
 				   
		dcc.Slider(id='b_slider',
 				   min=b_min, 
 				   max=b_max, 
 				   # step=b_step,
 				   marks=b_marks,
 				   value=b
		),           
        
        
        
        # Slider for theta
		html.Label('Initial condition = {}'.format(theta),
 				   id='theta_slider_text',
 				   style={'fontSize':size_slider_text}),  
 				   
		dcc.Slider(id='theta_slider',
 				   min=theta_min, 
 				   max=theta_max, 
 				   # step=theta_step,
 				   # marks=theta_marks,
 				   value=theta,
		),           
        
        
        # Slider for ts
		html.Label('Initial condition = {}'.format(ts),
 				   id='ts_slider_text',
 				   style={'fontSize':size_slider_text}),  
 				   
		dcc.Slider(id='ts_slider',
 				   min=ts_min, 
 				   max=ts_max, 
 				   # step=ts_step,
 				   # marks=ts_marks,
 				   value=ts
		),],                  
         
		style={'width':'25%',
			   'height':'800px',
			   'fontSize':'10px',
			   'padding-left':'3%',
			   'padding-right':'2%',
			   'padding-bottom':'0px',
               'padding-top':'40px',
			   'vertical-align': 'middle',
			   'display':'inline-block'
               }
        ),
        
     
    # Restitution plot
   	html.Div(
  		[dcc.Graph(id='fig_restitution',
   				   figure = fig_restitution,
   				   # config={'displayModeBar': False},
   				   ),
   		 ],
  		style={'width':'30%',
  			   'height':'800px',
  			   'fontSize':'10px',
  			   'padding-left':'0%',
  			   'padding-right':'0%',
  			   'vertical-align': 'middle',
  			   'display':'inline-block'},
   	),
  
   	# Cobweb plot
   	html.Div(
  		[dcc.Graph(id='fig_cobweb',
   				   figure = fig_cobweb,
   				   # config={'displayModeBar': False},
   				   ),
   		 ],
  		style={'width':'30%',
  			   'height':'800px',
  			   'fontSize':'10px',
  			   'padding-left':'0%',
  			   'padding-right':'0%',
  			   'vertical-align': 'middle',
  			   'display':'inline-block'},
   	),     


])
        
        
     
     

        
        # # Model description
        # html.P(model_text_2_line1,
        #         style={'fontSize':15,
        #               'color':'black',
        #               # 'textAlign':'left',
        #               }),
        # html.Br(),
        # html.P(model_text_2_line2,
        #         style={'fontSize':15,
        #               'color':'black',
        #               # 'textAlign':'left',
        #               }),        
         
        # html.Br(),
        

   
        
        
        
#         ],       
# 		style={'width':'25%',
# 			   'height':'800px',
# 			   'fontSize':'10px',
# 			   'padding-left':'0%',
# 			   'padding-right':'0%',
# 			   'padding-bottom':'0px',
#                'padding-top':'40px',
# 			   'vertical-align': 'middle',
# 			   'display':'inline-block'},
#         ),




# #–-------------------
# # Callback functions
# #–--------------------

  
# Update text for sliders             
@app.callback(
        [
         Output('apd0_slider_text','children'),
         Output('nmax_slider_text','children'),
         Output('y0_slider_text','children'),
         Output('a_slider_text','children'),
         Output('b_slider_text','children'),
         Output('theta_slider_text','children'),
         Output('ts_slider_text','children'),
          ],
        [
          Input('apd0_slider','value'),
          Input('nmax_slider','value'),
          Input('y0_slider','value'),
          Input('a_slider','value'),
          Input('b_slider','value'),
          Input('theta_slider','value'),
          Input('ts_slider','value'),
          ]
)

def update_slider_text(apd0,nmax,y0,a,b,theta,ts):
    
    # Slider text update
    text_apd0 = 'APD_0 = {}'.format(apd0)
    text_nmax = '# iterations = {}'.format(nmax)
    text_y0 = 'y0 = {}'.format(y0)
    text_a = 'a = {}'.format(a)
    text_b = 'b = {}'.format(b)
    text_theta = 'theta = {}'.format(theta)
    text_ts = 'ts = {}'.format(ts)

    return text_apd0, text_nmax, text_y0, text_a, text_b, text_theta, text_ts
            


# Update figures
@app.callback(
            Output('fig_restitution','figure'),
            Output('fig_cobweb','figure'),
            [
              Input('apd0_slider','value'),
              Input('nmax_slider','value'),
              Input('y0_slider','value'),
              Input('a_slider','value'),
              Input('b_slider','value'),
              Input('theta_slider','value'),
              Input('ts_slider','value'),        
            ],
            )

def update_figs(apd0, nmax, y0, a, b, theta, ts):
    

    # Generate cobweb trajectory
    apd_traj = generate_cobweb_trajectory(nmax, apd0, y0, a, b, theta, ts)
    
    # Make figures
    fig_cobweb = make_cobweb_fig(y0, a, b, theta, ts, apd_traj)
    fig_restitution = make_restitution_fig(y0, a, b)

    return fig_restitution, fig_cobweb

#-----------------
# Add the server clause
#–-----------------
if __name__ == '__main__':
    app.run_server(
        debug=True,
        host='127.0.0.1',
        )



