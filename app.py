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

from app_functions import generate_cobweb_trajectory, make_cobweb_fig,\
    make_restitution_fig, make_apd_sequence



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

# Default model parameter values from Ravi
# y0=120, a=96.9, b=0.0104
# apdmax=216.9 (y0+a), alpha=96.9, tau=96 (1/b)

# Default model parameter values from Guevara et al. (1984)
# apdmax=207, alpha=136, tau=78


# Default model parameters
apdmax = 216.9 # y0+a
alpha = 96.9 # a
tau = 96 # 1/b
theta = 0
ts = 300

# Defualt simulation parameters
apd0 = 150 
nmax = 40

# Generate cobweb trajectory
apd_traj = generate_cobweb_trajectory(nmax, apd0, apdmax, alpha, tau, theta, ts)

# Make figures
fig_cobweb = make_cobweb_fig(apdmax, alpha, tau, theta, ts, apd_traj)
fig_restitution = make_restitution_fig(apdmax, alpha, tau)
fig_apd_sequence = make_apd_sequence(apd_traj)


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

apdmax_min = 100
apdmax_max = 300

alpha_min = 0
alpha_max = 200

tau_min = 10
tau_max = 190

theta_min = -20
theta_max = 20

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
      
    # Title section
    html.Div(
        html.H1('Restitution analysis',
                style={'textAlign':'center',
                       'fontSize':size_title,
                       'color':'black',
                       'padding-top':'10px',
                       'padding-left':'30px',
                       }
        )
    ),
                                    
    
# 		style={'width':'25%',
# 			   'height':'800px',
# 			   'fontSize':'10px',
# 			   'padding-left':'3%',
# 			   'padding-right':'2%',
# 			   'padding-bottom':'0px',
#                 'padding-top':'40px',
# 			   'vertical-align': 'middle',
# 			   'display':'inline-block'
#                 }    
    
    
    
    # Left half of app
 	html.Div([
        
        # html.H1('Restitution analysis',
        #           style={'textAlign':'left',
        #                 'fontSize':size_title,
        #                 'color':'black'}
        # ),

        # Slider for apd0
		html.Label('APD_0 = {} ms'.format(apd0),
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

        
        # Slider for apdmax
		html.Label('APD_max = {} ms'.format(apdmax),
 				   id='apdmax_slider_text',
 				   style={'fontSize':size_slider_text}),  
 				   
		dcc.Slider(id='apdmax_slider',
 				   min=apdmax_min, 
 				   max=apdmax_max, 
 				   # step=y0_step,
 				   # marks=y0_marks,
 				   value=apdmax
		),   

        
        # Slider for alpha
		html.Label('alpha = {} ms'.format(alpha),
 				   id='alpha_slider_text',
 				   style={'fontSize':size_slider_text}),  
 				   
		dcc.Slider(id='alpha_slider',
 				   min=alpha_min, 
 				   max=alpha_max, 
 				   value=alpha
		),           
        
        
        # Slider for tau
		html.Label('tau = {} ms'.format(tau),
 				   id='tau_slider_text',
 				   style={'fontSize':size_slider_text}),  
 				   
		dcc.Slider(id='tau_slider',
 				   min=tau_min, 
 				   max=tau_max, 
 				   value=tau,
		),           
        
        
        
        # Slider for theta
		html.Label('theta = {} ms'.format(theta),
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
		html.Label(r'$t_s = {} ms$'.format(ts),
 				   id='ts_slider_text',
 				   style={'fontSize':size_slider_text},
                    ),  
        
        # dcc.Markdown(r'$ E=mc^2 $', mathjax=True),
 				   
        
		dcc.Slider(id='ts_slider',
 				   min=ts_min, 
 				   max=ts_max, 
 				   # step=1,
 				   # marks=ts_marks,
 				   value=ts
		),],                  
         
		style={'width':'25%',
			   'height':'470px',
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
                   mathjax=True,
   				   figure = fig_restitution,
   				   # config={'displayModeBar': False},
   				   ),
   		 ],
  		style={'width':'30%',
  			   'height':'470px',
  			   'fontSize':'15px',
  			   'padding-left':'0%',
  			   'padding-right':'0%',
  			   'vertical-align': 'middle',
  			   'display':'inline-block'},
   	),
  
   	# Cobweb plot
   	html.Div(
  		[dcc.Graph(id='fig_cobweb',
                   mathjax=True,
   				   figure = fig_cobweb,
   				   # config={'displayModeBar': False},
   				   ),
   		 ],
  		style={'width':'30%',
  			   'height':'470px',
  			   'fontSize':'15px',
  			   'padding-left':'0%',
  			   'padding-right':'0%',
  			   'vertical-align': 'middle',
  			   'display':'inline-block'},
   	),     

   	# APD sequence
   	html.Div(
  		[dcc.Graph(id='fig_apd_sequence',
                   mathjax=True,
   				   figure = fig_apd_sequence,
   				   # config={'displayModeBar': False},
   				   ),
   		 ],
  		style={'width':'90%',
  			   'height':'320px',
  			   'fontSize':'15px',
  			   'padding-left':'5%',
  			   'padding-right':'5%',
  			   'vertical-align': 'middle',
  			   'display':'inline-block'},
   	),     


    # Footer
    html.Footer(
        [
            'Source code ',
        html.A('here',
               href='https://github.com/ThomasMBury/restitution-cobweb/', 
               target="_blank",
               ),
        ],
        style={'fontSize':'15px',
                          'width':'100%',
                           # 'horizontal-align':'middle',
                          'textAlign':'center',
               },
                
        ),

])
        

# #–-------------------
# # Callback functions
# #–--------------------
  
# Update text for sliders             
@app.callback(
        [
         Output('apd0_slider_text','children'),
         Output('nmax_slider_text','children'),
         Output('apdmax_slider_text','children'),
         Output('alpha_slider_text','children'),
         Output('tau_slider_text','children'),
         Output('theta_slider_text','children'),
         Output('ts_slider_text','children'),
          ],
        [
          Input('apd0_slider','value'),
          Input('nmax_slider','value'),
          Input('apdmax_slider','value'),
          Input('alpha_slider','value'),
          Input('tau_slider','value'),
          Input('theta_slider','value'),
          Input('ts_slider','value'),
          ]
)

def update_slider_text(apd0,nmax,apdmax,alpha,tau,theta,ts):
    
    # Slider text update
    text_apd0 = 'APD_0 = {} ms'.format(apd0)
    text_nmax = '# iterations = {}'.format(nmax)
    text_apdmax = 'APD_max = {} ms'.format(apdmax)
    text_alpha = 'alpha = {} ms'.format(alpha)
    text_tau = 'tau = {} ms'.format(tau)
    text_theta = 'theta = {} ms'.format(theta)
    text_ts = 'ts = {} ms'.format(ts)

    return text_apd0,text_nmax,text_apdmax,text_alpha,text_tau,text_theta,text_ts
            


# Update figures
@app.callback(
            Output('fig_restitution','figure'),
            Output('fig_cobweb','figure'),
            Output('fig_apd_sequence','figure'),
            [
          Input('apd0_slider','value'),
          Input('nmax_slider','value'),
          Input('apdmax_slider','value'),
          Input('alpha_slider','value'),
          Input('tau_slider','value'),
          Input('theta_slider','value'),
          Input('ts_slider','value'),      
            ],
            )

def update_figs(apd0, nmax, apdmax, alpha, tau, theta, ts):
    

    # Generate cobweb trajectory
    apd_traj = generate_cobweb_trajectory(nmax, apd0, apdmax, alpha, tau, theta, ts)
    
    # Make figures
    fig_cobweb = make_cobweb_fig(apdmax, alpha, tau, theta, ts, apd_traj)
    fig_restitution = make_restitution_fig(apdmax, alpha, tau)
    fig_apd_sequence = make_apd_sequence(apd_traj)

    return fig_restitution, fig_cobweb, fig_apd_sequence


#-----------------
# Add the server clause
#–-----------------
if __name__ == '__main__':
    app.run_server(
        debug=True,
        host='127.0.0.1',
        )



