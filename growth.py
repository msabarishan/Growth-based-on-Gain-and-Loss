import streamlit as st
import numpy as np
import pandas as pd
# import seaborn as sns
import plotly.express as px
import altair as alt

st.write("""
# Wealth progression Assignment
""")

np.random.seed(9)

def run_experiment(i_w, f_g,s_g,p_g):
    # num of time steps
    t_N = 60

    # num of people
    p_N = 1000

    evt_data = {}
    gain_data = {}

    data_load_state = st.text('Running Experiment ...')

    # generate data for every person
    for i in range(p_N):
        # start with initial amount as leverage
        person_gain = i_w
        
        # generate random events of gain / loss for N time steps
        evts = np.random.binomial(1,p_g,size=t_N)
        
        # temp state store for interim gains
        gains = [person_gain]
        
        # calc gain progression
        for e in evts:
            if e == 0:
                person_gain = (person_gain * (1 + s_g))
            else:
                person_gain = (person_gain * (1 + f_g))
            
            gains.append(person_gain)

    #         print(person_gain, e)
            
        # append gain data - events, gain progression, to a dictionary
        evt_data[f"p_evt_{i+1}"] = evts
        gain_data[f"p_gain_{i+1}"] = gains


    df_gain = pd.DataFrame(gain_data)
    df_gain = df_gain.reset_index()

    df_ens = pd.DataFrame()
    df_ens["ens_avg"] = df_gain.apply(np.mean, axis=1)
    df_ens = df_ens.reset_index()
    df_melt=pd.melt(df_gain, id_vars=['index'], value_vars=['p_gain_1','p_gain_2','p_gain_3','p_gain_1000'],
        var_name='person', value_name='wealth')

    data_load_state.text('Experiment Completed!')
    st.dataframe(df_melt)
    
    st.subheader('Ensemble Average')
    chart1=alt.Chart(df_ens).mark_line().encode(                             
    alt.X('index', title='timestep'),
    alt.Y('ens_avg', title='ensemble avg. at timestep')
    )

    st.altair_chart(chart1,use_container_width=True)
    
    df_gain1 = df_gain[(df_gain.index==60)]
    df_gain1 =df_gain1.drop(['index'],axis=1)
    df_gain1 = df_gain1.T
    max=df_gain1.max(numeric_only=True).max()
    min=df_gain1.min(numeric_only=True).min()
    
    st.subheader('End Wealth Distribution')
    chart2 = alt.Chart(df_gain1).transform_joinaggregate(
    total='count(*)'
    ).transform_calculate(
    pct='1 / datum.total'
    ).mark_bar().encode(
    alt.X('60:Q', bin = alt.Bin(maxbins = 10)),
    alt.Y('sum(pct):Q', axis=alt.Axis(format='%'),title='Percentage of Total individuals')
    )
    meadian_line = alt.Chart(df_gain1).mark_rule(color ='red').encode(
    x=alt.X('mean(60):Q', title='End Wealth(With Mean marked in Red)'),
    size=alt.value(1)
    )

    st.altair_chart(chart2+meadian_line,use_container_width=True)
    
    st.subheader('Wealth Distribution Progression')
    alt.Chart(df_gain1).mark_line().encode(
    x='date',
    y='price',
    color='symbol',
    strokeDash='symbol',
    )
    
    
sl_i_w = st.sidebar.slider('Initial Wealth', 1000, 1000000, 1000)
sl_f_g = st.sidebar.slider('Fast Growth %', 0.0, 1.0, 0.5)
sl_s_g = st.sidebar.slider('Slow Growth %', 0.0, 1.0, 0.5)
sl_p_g = st.sidebar.slider('Probaility of Fast Growth', 0.0, 1.0, 1.0)

st.write(f"""
## Experiment Parameters

* Initial Wealth = ${sl_i_w}
* Fast Growth % = {sl_f_g}
* Slow Growth % = {sl_s_g}
* Probability of Fast Growth = {sl_p_g}
* Time Steps = 60
* Number of Sequences = 1000
""")

if st.sidebar.button("Run Experiment", "run-exp-btn"):
    run_experiment(sl_i_w, sl_f_g, sl_s_g, sl_p_g)

# initial_amount = 1000
# gain_pct = 0.5
# loss_pct = 0.4
# leverage = 1.0



# fig.show()
# sns.lineplot(x=df_ens.index, y=df_ens["ens_avg"], )

# sns.lineplot(x=df_gain.index, y=df_gain["p_gain_100"])

# Altair codes
# Ensemble Average using Altair


    

