import streamlit as st
import numpy as np
import pandas as pd
# import seaborn as sns
import plotly.express as px
import altair as alt

st.write("""
# Ergodicity Experiment
""")

np.random.seed(9)

def run_experiment(initial_amount, gain_pct, loss_pct, leverage):
    # num of time steps
    t_N = 60

    # num of people
    p_N = 100000

    evt_data = {}
    gain_data = {}

    data_load_state = st.text('Running Experiment ...')

    # generate data for every person
    for i in range(p_N):
        # start with initial amount as leverage
        person_gain = initial_amount
        
        # generate random events of gain / loss for N time steps
        evts = np.random.randint(0,2, t_N)
        
        # temp state store for interim gains
        gains = [person_gain]
        
        # calc gain progression
        for e in evts:
            if e == 0:
                person_gain = (person_gain * (1 - leverage)) + (person_gain * leverage * (1 - loss_pct))
            else:
                person_gain = (person_gain * (1 - leverage)) + (person_gain * leverage * (1 + gain_pct))
            
            gains.append(person_gain)

    #         print(person_gain, e)
            
        # append gain data - events, gain progression, to a dictionary
        evt_data[f"p_evt_{i+1}"] = evts
        gain_data[f"p_gain_{i+1}"] = gains


    df_gain = pd.DataFrame(gain_data)
    df_gain = df_gain.reset_index()
    
    df_gain1 = df_gain[["index","p_gain_100"]]

    df_ens = pd.DataFrame()
    df_ens["ens_avg"] = df_gain.apply(np.mean, axis=1)
    df_ens["ens_med"] = df_gain.apply(np.median, axis=1)
    df_ens = df_ens.reset_index()

    data_load_state.text('Experiment Completed!')
    
    st.subheader('Ensemble Average')
    chart1=alt.Chart(df_ens).mark_line().encode(                             
    alt.X('index', title='timestep'),
    alt.Y('ens_avg', title='ensemble avg. at timestep')
    )

    st.altair_chart(chart1,use_container_width=True)
    
    data_load_state.text('Experiment Completed!')
    
    st.subheader('Specific case')
    chart2=alt.Chart(df_gain1).mark_line().encode(                             
    alt.X('index', title='timestep'),
    alt.Y('p_gain_100', title='gain at timestep')
    )# p_gain_100

    st.altair_chart(chart2,use_container_width=True)
    
    st.subheader('Histogram')
    residue= df_gain.iloc[-1].value_counts().reset_index()
    residue.rename(columns = {60 : 'box'}, inplace = True)
    
    chart3 = alt.Chart(residue).mark_bar().encode(
       alt.X('index',title='index'),
       alt.Y('box',title='box')
       ). properties(
                width=350,
                height=300,
                title='Histogram')
    st.altair_chart(chart3)
    
sl_initial_amount = st.sidebar.slider('Initial Amount', 1000, 1000000, 1000)
sl_gain_pct = st.sidebar.slider('Gain %', 0.0, 1.0, 0.5)
sl_loss_pct = st.sidebar.slider('Loss %', 0.0, 1.0, 0.4)
sl_leverage = st.sidebar.slider('Leverage', 0.0, 1.0, 1.0)

st.write(f"""
## Experiment Parameters

* Initial Amount = ${sl_initial_amount}
* Gain = {sl_gain_pct}
* Loss = {sl_loss_pct}
* Leverage = {sl_leverage}
* Time Steps = 60
* Number of Sequences = 100,000
""")

if st.sidebar.button("Run Experiment", "run-exp-btn"):
    run_experiment(sl_initial_amount, sl_gain_pct, sl_loss_pct, sl_leverage)

# initial_amount = 1000
# gain_pct = 0.5
# loss_pct = 0.4
# leverage = 1.0



# fig.show()
# sns.lineplot(x=df_ens.index, y=df_ens["ens_avg"], )

# sns.lineplot(x=df_gain.index, y=df_gain["p_gain_100"])



# Altair codes
# Ensemble Average using Altair


    

