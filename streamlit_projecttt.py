
import json
import streamlit as st
import pandas as pd
from mplsoccer import VerticalPitch

st.title("Euros 2024 Shot Map")
st.subheader("Filter to any team/player to see all their shots taken!")

df = pd.read_csv('euros_2024_shot_map(1).csv')

print(df.head())

df = df[df['type'] == 'Shot'].reset_index(drop=True)


df['location'] = df['location'].apply(json.loads)

team = st.selectbox('Select a Team',df['team'].sort_values().unique(), index=None)
player = st.selectbox('Select a Player',df[df['team'] == team]['player'].sort_values().unique(), index=None)
# Index as none = select box stays blank , if we use 0 , select box defaults to the first option 

def filter_data(df,team,player):    # Creating a function
    if team:
        df = df[df['team'] == team]
    if player:
        df = df[df['player'] == player]

    return df

filtered_df = filter_data(df, team, player)


pitch = VerticalPitch(pitch_type='statsbomb',half=True)
fig, ax = pitch.draw(figsize=(10,10))


def plot_shots(df,ax,pitch):
    for x in df.to_dict(orient='records'):
        pitch.scatter(
            x=float(x['location'][0]),
            y=float(x['location'][1]),
            ax=ax,
            s=1000 * x['shot_statsbomb_xg'],    # Scale the shot by(1000) based on xg of the shot
            color='green' if x['shot_outcome'] == 'Goal' else 'white',
            edgecolors='black',
            alpha=1 if x['type'] == 'goal' else .5,
            zorder=2 if x['type'] == 'goal' else 1   # Layer like in canva, if its a goal it appears over normal non goal shots
        )


plot_shots(filtered_df,ax,pitch)

st.pyplot(fig)
