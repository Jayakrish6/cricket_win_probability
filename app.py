import streamlit as st
import pickle
import pandas as pd

st.set_page_config(page_title='ODI Win Predictor', page_icon='🏏', layout='wide')

THEME = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600&display=swap');

:root {
    --green: #0f9d58;
    --amber: #ffb703;
    --navy: #081c24;
    --card: rgba(255, 255, 255, 0.94);
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 20% 20%, #f3ffe7 0%, #e8f5ff 40%, #fde5d0 90%);
    font-family: 'Space Grotesk', sans-serif;
    color: var(--navy);
}

[data-testid="stHeader"], [data-testid="stToolbar"] {background: transparent;}

[data-testid="stColumn"] > div {
    background: var(--card);
    border-radius: 18px;
    padding: 1rem;
    box-shadow: 0 15px 30px rgba(8, 28, 36, 0.08);
}

.stButton > button {
    width: 100%;
    border-radius: 999px;
    background: linear-gradient(135deg, #0f9d58, #34a853);
    color: #fff;
    font-weight: 600;
    border: none;
    padding: 0.85rem 1.2rem;
    box-shadow: 0 10px 25px rgba(15, 157, 88, 0.35);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 32px rgba(15, 157, 88, 0.4);
}

.result-card {
    padding: 1.4rem;
    border-radius: 20px;
    color: #fff;
    text-align: center;
    box-shadow: 0 18px 35px rgba(8, 28, 36, 0.18);
}

.result-card h3 {
    margin: 0 0 0.4rem;
    font-size: 1.1rem;
    letter-spacing: 0.03em;
}

.result-card p {
    margin: 0;
    font-size: 2.8rem;
    font-weight: 600;
}

.result-card.batting {background: linear-gradient(135deg, #0f9d58, #1cc58f);} 
.result-card.bowling {background: linear-gradient(135deg, #f12711, #f5af19);} 

.metrics-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.85rem;
    margin-top: 1.2rem;
}

.metric-pill {
    flex: 1;
    min-width: 160px;
    border-radius: 999px;
    padding: 0.55rem 1rem;
    background: rgba(8, 28, 36, 0.08);
    font-weight: 500;
    text-align: center;
}
</style>
"""

st.markdown(THEME, unsafe_allow_html=True)

pipe = pickle.load(open('model.pkl', 'rb'))

teams = [
    'India',
    'England',
    'New Zealand',
    'Australia',
    'Sri Lanka',
    'South Africa',
    'Bangladesh',
    'Pakistan',
    'Afghanistan',
    'Netherlands'
]

cities = [
    'Dhaka', 
    'Chandigarh', 
    'Colombo', 
    'Johannesburg', 
    'London',
    'Centurion', 
    'Potchefstroom', 
    'Southampton', 
    'Bloemfontein',
    'Cardiff', 
    'Lahore', 
    'Kandy', 
    'Hambantota', 
    'Chattogram',
    'Harare',
    'Bulawayo', 
    'Karachi', 
    'Rawalpindi', 
    'Benoni', 
    'Hamilton',
    'Auckland', 
    'Chennai', 
    'Visakhapatnam', 
    'Mumbai', 
    'Kimberley',
    'Indore', 
    'Raipur', 
    'Hyderabad', 
    'Thiruvananthapuram', 
    'Kolkata',
    'Guwahati', 
    'Sydney', 
    'Adelaide', 
    'Delhi', 
    'Ranchi', 
    'Lucknow',
    'Cairns', 
    'Rotterdam', 
    'Manchester', 
    'Chester-le-Street',
    'Amstelveen', 
    'Mount Maunganui', 
    'Doha', 
    'Cape Town', 
    'Paarl',
    'Birmingham', 
    'Pune', 
    'Wellington', 
    'Christchurch', 
    'Dunedin',
    'Canberra', 
    'Unknown', 
    'Bengaluru', 
    'Rajkot', 
    'Leeds',
    'Nottingham', 
    'Taunton', 
    'Bristol', 
    'Dubai', 
    'Abu Dhabi',
    'Sharjah', 
    'Port Elizabeth', 
    'Nagpur', 
    'Napier', 
    'Durban',
    'Melbourne', 
    'Nelson', 
    'Hobart', 
    'Brisbane', 
    'Dharamsala',
    'Kanpur', 
    'East London', 
    'Dublin', 
    'Cuttack', 
    'Perth',
    'Dharmasala', 
    'Chittagong', 
    'Mirpur', 
    'St Kitts', 
    'Guyana',
    'Ahmedabad', 
    'Fatullah', 
    'Bangalore', 
    'Jaipur', 
    'Trinidad',
    'Jamaica', 
    'Kochi', 
    'Vadodara', 
    'Gwalior', 
    'Darwin', 
    'Faisalabad',
    'Belfast', 
    'St Lucia', 
    'Grenada', 
    'Barbados', 
    'Antigua', 
    'Margao',
    'Kuala Lumpur', 
    'Jamshedpur', 
    'Faridabad', 
    'Bogra', 
    'Queenstown',
    'Canterbury', 
    'Dambulla', 
    'Peshawar', 
    'Multan', 
    'Gqeberha'
]

st.title('🏏 ODI Win Probability')
st.caption('Live chase assistant: blend match context, chase pressure, and win odds in one glance.')
st.markdown('### Match Setup')
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select Batting Team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select Bowling Team', sorted(teams))

st.markdown('### Venue & Target')
venue_col, target_col = st.columns([2, 1])

with venue_col:
    venue = st.selectbox('Select Venue', sorted(cities))
with target_col:
    score = st.number_input('1st Innings Score', min_value=0)

st.markdown('### Chase Snapshot')
col3, col4, col5 = st.columns(3)

with col3:
    current_score = st.number_input('Current Score', min_value=0)
with col4:
    overs = st.number_input('Overs Done', min_value=0.0, max_value=50.0, step=0.1, format="%.1f")
with col5:
    wickets = st.number_input('Wickets Out', min_value=0, max_value=10, step=1)

st.markdown('### Prediction')
if st.button('Predict Probability'):
    runs_left = score - current_score
    balls_left = max(0, 300 - (overs * 6))
    wickets_left = max(0, 10 - wickets)
    crr = 0 if overs == 0 else current_score / overs

    if balls_left <= 0:
        st.error('No balls remaining. Please ensure overs are less than 50 before predicting.')
    elif wickets_left <= 0:
        st.error('All wickets have fallen. Reduce the wickets-out value to continue.')
    else:
        rrr = (runs_left * 6) / balls_left

        input_df = pd.DataFrame(
            {
                'batting_team': [batting_team],
                'bowling_team': [bowling_team],
                'city': [venue],
                'runs_left': [runs_left],
                'balls_left': [balls_left],
                'wickets_left': [wickets_left],
                'total_runs_x': [score],
                'crr': [crr],
                'rrr': [rrr]
            }
        )

        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        gain = result[0][1]

        bat_col, bowl_col = st.columns(2)
        bat_col.markdown(
            f"""
            <div class='result-card batting'>
                <h3>{batting_team} Win Probability</h3>
                <p>{gain * 100:.1f}%</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        bowl_col.markdown(
            f"""
            <div class='result-card bowling'>
                <h3>{bowling_team} Win Probability</h3>
                <p>{loss * 100:.1f}%</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(min(max(gain, 0.0), 1.0))

        st.markdown(
            f"""
            <div class='metrics-row'>
                <div class='metric-pill'>Runs Left: {runs_left}</div>
                <div class='metric-pill'>Balls Left: {int(balls_left)}</div>
                <div class='metric-pill'>Required RR: {rrr:.2f}</div>
                <div class='metric-pill'>Current RR: {crr:.2f}</div>
                <div class='metric-pill'>Wickets in Hand: {int(wickets_left)}</div>
            </div>
            """,
            unsafe_allow_html=True

        )
