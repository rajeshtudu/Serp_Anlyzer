import schedule
import advertools as adv
import pandas as pd
import plotly.express as px
import streamlit as st
import time
from datetime import datetime

# Google Custom Search Engine credentials
cse_id = "c293893b6c614495f"  # Replace with your CSE ID
api_key = "AIzaSyBxxZF9roT69aIy3pO7e96TCpBzUffqJeo"  # Replace with your API Key

def get_keyword():
    """
    Prompt the user to enter a single keyword interactively.
    Returns the entered keyword.
    """
    keyword = st.text_input("Enter a keyword (e.g., 'Banana')", "")
    return keyword.strip()

def SERPheartbeat(keywords):
    """
    Fetches SERP data for the specified keywords and saves it to a CSV file.
    Returns the filename of the saved CSV.
    """
    date = datetime.now().strftime("%d%m%Y%H_%M_%S")
    df = adv.serp_goog(q=keywords, key=api_key, cx=cse_id)
    filename = f'serp_{date}_scheduled_serp.csv'
    df.to_csv(filename, index=False)
    print(f"SERP data recorded for keywords: {keywords}")
    return filename

def visualize_serp_data_separately(filename):
    """
    Visualizes SERP data from a CSV file using Plotly Express.
    """
    df = pd.read_csv(filename)
    
    # Ensure no unexpected columns cause issues
    df.drop(columns=[col for col in ['Unnamed: 0', 'Unnamed:0'] if col in df.columns], inplace=True)

    # Adding a constant size for bubbles in the scatter plot for consistency across plots
    df['bubble_size'] = 50

    # Create a selectbox for choosing the search term
    search_term = st.selectbox('Select a Search Term', df['searchTerms'].unique())

    # Filter DataFrame based on the selected search term
    filtered_df = df[df['searchTerms'] == search_term]

    # Create the scatter plot using Plotly Express
    fig = px.scatter(filtered_df, x="displayLink", y="rank",
                     color="displayLink", hover_name="link", hover_data=["searchTerms", "title", "rank"],
                     size="bubble_size", text="displayLink", template="plotly_white",
                     title=f"SERP Rankings for: {search_term}",
                     height=600, width=800,
                     range_x=[-1, 11],
                     range_y=[1, max(10, filtered_df['rank'].max() + 1)])

    # Update layout and axes
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="white")
    fig.update_yaxes(tickmode='array', tickvals=list(range(1, 11)))

    # Display the figure in Streamlit
    st.plotly_chart(fig)

def main():
    """
    Main function to execute the SERP heartbeat recording process and visualization.
    """
    st.title("SERP Data Visualization")

    # Get keywords interactively
    keywords = get_keyword()

    if st.button('Fetch SERP Data'):
        if keywords:
            filename = SERPheartbeat(keywords)
            st.success(f"Fetched SERP data for '{keywords}'.")
            visualize_serp_data_separately(filename)
        else:
            st.warning("Please enter a valid keyword.")

if __name__ == "__main__":
    main()