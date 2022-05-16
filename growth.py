import streamlit as st
import numpy as np
import pandas as pd
# import seaborn as sns (Not used in this project)
# import plotly.express as px (Not used in this project)
import altair as alt

st.write("""
# Wealth progression Assignment
""")

np.random.seed(9)

def run_experiment(initial_wealth, fast_growth,slow_growth,prob_fastgrowth):
    # num of time steps
    time = 60
    
    fast_growth=fast_growth/100
    slow_growth=slow_growth/100
    # num of people
    no_people = 1000

    evt_data = {}
    gain_data = {}

    data_load_state = st.text('Running Experiment ...')

    # generate data for every person
    for i in range(no_people):
        # start with initial amount as leverage
        person_gain = initial_wealth
        
        # generate random events of gain / loss for N time steps
        evts = np.random.binomial(1,prob_fastgrowth,size=time)
        
        # temp state store for interim gains
        gains = [person_gain]
        
        # calc gain progression
        for e in evts:
            if e == 0:
                person_gain = (person_gain * (1 + slow_growth))
            else:
                person_gain = (person_gain * (1 + fast_growth))
            
            gains.append(person_gain)

    #         print(person_gain, e)
            
        # append gain data - events, gain progression, to a dictionary
        evt_data[f"p_evt_{i+1}"] = evts
        gain_data[f"prob_fastgrowthain_{i+1}"] = gains


    dfast_growthain = pd.DataFrame(gain_data)
    dfast_growthain = dfast_growthain.reset_index()

    df_ens = pd.DataFrame()
    df_ens["ens_avg"] = dfast_growthain.apply(np.mean, axis=1)
    df_ens = df_ens.reset_index()
    df_melt=pd.melt(dfast_growthain, id_vars=['index'],  # This code will convert all the columns data except mentioned in id_vars into a column
        var_name='person', value_name='wealth',)

    data_load_state.text('Experiment Completed!')
    
  
    st.subheader('Ensemble Average')
    chart1=alt.Chart(df_ens).mark_line().encode(                             
    alt.X('index', title='timestep'),
    alt.Y('ens_avg', title='ensemble avg. at timestep')
    )

    st.altair_chart(chart1,use_container_width=True)
    
    dfast_growthain1 = dfast_growthain[(dfast_growthain.index==60)]
    dfast_growthain1 =dfast_growthain1.drop(['index'],axis=1)
    dfast_growthain1 = dfast_growthain1.T
    max=dfast_growthain1.max(numeric_only=True).max()
    min=dfast_growthain1.min(numeric_only=True).min()
    df_dif = (max-min)/10
    
    st.subheader('End Wealth Distribution')
    chart2 = alt.Chart(dfast_growthain1).transform_joinaggregate(
    total='count(*)'
    ).transform_calculate(
    pct='1 / datum.total'
    ).mark_bar().encode(
    alt.X('60:Q', bin=alt.Bin(extent=[min, max], step=df_dif)),
    alt.Y('sum(pct):Q', axis=alt.Axis(format='%'),title='Percentage of Total individuals'))
    meadian_line = alt.Chart(dfast_growthain1).mark_rule(color ='red').encode(
    x=alt.X('mean(60):Q', title='End Wealth(With Mean marked in Red)'),
    size=alt.value(1)
    )

    st.altair_chart(chart2+meadian_line,use_container_width=True)
    
    st.subheader('Wealth Distribution Progression')
    chart3=alt.Chart(df_melt).mark_line().encode(
    alt.X('index',title= 'progression of time'),
    alt.Y('wealth',title='Wealth'),
    color=alt.Color('person',legend = None)
    )
    st.altair_chart(chart3,use_container_width=True)
    
sl_initial_wealth = st.sidebar.slider('Initial Wealth', 1000, 1000000, 1000)
sl_fast_growth = st.sidebar.slider('Faster Growth %', 0, 100, 20)
sl_slow_growth = st.sidebar.slider('Slower Growth %', -100, 100, 2)
sl_prob_fastgrowth = st.sidebar.slider('Probability of Fast Growth', 0.0, 1.0, 0.05)

st.write(f"""
## Experiment Parameters

* Initial Wealth = ${sl_initial_wealth}
* Fast Growth % = {sl_fast_growth}
* Slow Growth % = {sl_slow_growth}
* Probability of Fast Growth = {sl_prob_fastgrowth}
* Time Steps = 60
* Number of Sequences = 1000
""")

if st.sidebar.button("Run Experiment", "run-exp-btn"):
    run_experiment(sl_initial_wealth, sl_fast_growth, sl_slow_growth, sl_prob_fastgrowth)

    

