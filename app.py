import streamlit as st
import pandas as pd
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.drawing.image import Image
from io import BytesIO

# Load the Excel file
file_path = 'health_check_3.xlsx'
xls = pd.ExcelFile(file_path)

# Create a dictionary to store the color icons
color_icons = {'Green': '🟢', 'Yellow': '🟡', 'Red': '🔴'}

# Function to calculate the trend arrow
def calculate_trend_arrow(green_votes, yellow_votes, red_votes):
    max_votes = max(green_votes, yellow_votes, red_votes)
    total_votes = green_votes + yellow_votes + red_votes
    
    if max_votes == green_votes and max_votes == total_votes - max_votes:
        return '🔽'  # Arrow down
    elif max_votes == red_votes and max_votes == total_votes - max_votes:
        return '🔼'  # Arrow up
    else:
        return ''  # No arrow

# Define descriptions for the colors
color_descriptions = {
    '🟢': "The squad is happy with this, and see no major need for improvement right now.",
    '🔴': "This really sucks and needs to be improved.",
    '🟡': "There are some important problems that need addressing, but it’s not a disaster.",
    '🔼': "There is a trend that the squad can improve",
    '🔽': "There is a trend that the squad needs improvement"
}

# Create a Streamlit dropdown menu to select a team
selected_team = st.sidebar.selectbox("Select a squad", ['All'] + xls.sheet_names)

# Check if "All" is selected
if selected_team == 'All':
    # Create an empty DataFrame to store the overview data
    overview_data = pd.DataFrame()

    # Iterate through each sheet in the Excel file
    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name)
        max_colors = df.iloc[:, 1:].idxmax(axis=1)
        max_color_icons = max_colors.map(color_icons)

        # Calculate and add trend arrows to the max_color_icons
        trend_arrows = df.apply(lambda row: calculate_trend_arrow(row['Green'], row['Yellow'], row['Red']), axis=1)

        # Combine max_color_icons and trend_arrows into a single string
        max_color_icons_with_arrows = max_color_icons + " " + trend_arrows

        overview_data[sheet_name] = max_color_icons_with_arrows

    # Set the row index of the overview_data DataFrame to category names
    category_names = df['Category / Color']
    overview_data.set_index(category_names, inplace=True)

    # Set up Streamlit
    st.title("AGN Squads Health Check Overview")

    # Display the overview data using st.write() with dataframe option
    st.dataframe(overview_data, height=430)
    
    # Create columns layout for Voting Results and Color Legend
    voting_results_col, color_legend_col = st.columns([1, 2])

    # Display color legend descriptions in the Color Legend column
    with color_legend_col:
        st.subheader("Color Legend")
        for color, description in color_descriptions.items():
            st.markdown(f"{color}: {description}")


else:
    # Create an empty DataFrame to store the team's voting results
    team_data = pd.DataFrame()

    # Parse the selected team's sheet from the Excel file
    df = xls.parse(selected_team)
    max_colors = df.iloc[:, 1:].idxmax(axis=1)
    max_color_icons = max_colors.map(color_icons)

    # Calculate and add trend arrows to the max_color_icons
    trend_arrows = df.apply(lambda row: calculate_trend_arrow(row['Green'], row['Yellow'], row['Red']), axis=1)

    # Combine max_color_icons and trend_arrows into a single string
    max_color_icons_with_arrows = max_color_icons + " " + trend_arrows

    # Use the max_color_icons for row values
    team_data['Result'] = max_color_icons_with_arrows
    team_data['Green'] = df['Green']
    team_data['Yellow'] = df['Yellow']
    team_data['Red'] = df['Red']

    # Set the row index of the team_data DataFrame to category names
    category_names = df['Category / Color']
    team_data.set_index(category_names, inplace=True)

    # Set up Streamlit
    st.title(f"{selected_team} Squad Health Check Voting Result")

    # Display the overview data using st.write() with dataframe option
    st.dataframe(team_data, height=430)

    # Create columns layout for Voting Results and Color Legend
    voting_results_col, color_legend_col = st.columns([1, 2])

    # Display color legend descriptions in the Color Legend column
    with color_legend_col:
        st.subheader("Color Legend")
        for color, description in color_descriptions.items():
            st.markdown(f"{color}: {description}")


# Instructions for interactivity
st.sidebar.markdown("### Instructions")
st.sidebar.markdown("- Each Team : Select a team above to view squad level voting result.")
st.sidebar.markdown("- All : Choose 'All' to view the entire squads voting result.")
# Footer
st.sidebar.markdown("Made with ❤️ 💡 by Yelin")