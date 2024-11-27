#!/usr/bin/env python
# coding: utf-8

# # Recording Google Search Results and Animating Result Differences based on Dates

# Notebook's Scenario: Retrieving Google SERP with a regular frequency and aggregating the data on the SERP for SEO Insights along with animating

# - 'Schedule' for Scheduling SERP Retrieving Timing
# - 'Advertools' for Using the Custom Search API of Google
# - 'Pandas' for **Data Maniuplation**
# - 'Plotly' for Animating the Differences
# - 'Glob' for Taking the CSV Files from Directory
# - 'Time' for Using the Schedule
# - 'Datetime' for Changing the Output Names with the actual time

# In[18]:


import schedule
import advertools as adv
import pandas as pd
import plotly.express as px
import glob
import time
from datetime import datetime


# - CSE stands for Custom Search Engine. You will need to create one: https://programmablesearchengine.google.com/cse/
# - API stands for "Custom Search API". I recommend you to not share it.

# In[19]:


cse_id = "7b8760de16d1e86bc" # Custom Search Engine ID
api_key = "AIzaSyAqUXT6JCU9bnpNv6ybAmgiJ2wPC-56CLA" # API Key for Custom Search API of Google


# - SERPHeartbeat() is the name of the Function for recording the SERP with a regular frequency.
# - It takes the "now", formats the time and Records the SERP within a CSV File with a 'prefix' and the 'formatted date'.

# In[20]:


def SERPheartbeat():
    """
    Calls the function with the determined frequency, for the determined queries.
    Creates a CSV Output with the name of the actual date which the function called.
    """
    date = datetime.now()
    date = date.strftime("%d%m%Y%H_%M_%S")
    df = adv.serp_goog(
        q=['Calories in Pizza', "Calories in BigMac"], key=api_key, cx=cse_id)
    df.to_csv(f'serp{date}' + '_' + 'scheduled_serp.csv')


# - Schedule the Function for every 30 Minutes.
# - You can put a limit with the 'n<Number' method.

# In[21]:


#schedule.every(30).minutes.do(SERPheartbeat) => Make the function call in every 30 Minutes.


"""
For making the Schedule work.

while True:
    schedule.run_pending()
    time.sleep(1)
"""


# - There is also a simpler way to do to same.

# In[22]:


"""

Another method

n=0
while n<99:
    SERPheartbeat()
    time.sleep(1)
    n += 1

"""



# ## Some other Examples for Scheduling a Function
# 
# - schedule.every().hour.do(record_serp) => Do something at every hour's beginning
# - schedule.every().day.at("13:25").do(record_serp) => Do something at 13:25, everyday.
# - schedule.every(5).to(10).minutes.do(record_serp) => Do something in every five to 10 tecons
# - schedule.every().monday.do(record_serp) => Do something in every Monday
# - schedule.every().wednesday.at("13:15").do(record_serp) => Do something in every Wednesday
# - schedule.every().minute.at(":17").do(record_serp) => Do something at every minutes' 17th second.
# 
# - For more: https://buildmedia.readthedocs.org/media/pdf/schedule/stable/schedule.pdf

# Taking the SERP Recording Outputs as CSV

# - Old Fashion Way for Uniting the SERP Recording Output Files

# In[23]:


#df_1 = pd.read_csv("str2712202015_09_06_scheduled_serp.csv", index_col='queryTime')
#df_2 = pd.read_csv("str2712202015_09_20_scheduled_serp.csv", index_col='queryTime')
#df_3 = pd.read_csv("str2712202015_09_31_scheduled_serp.csv", index_col='queryTime')
#df_4 = pd.read_csv("str2612202022_57_11_scheduled_serp.csv", index_col='queryTime')
#united_serp_df = df_1.append([df_2,df_3,df_4])
#united_serp_df.columns


# - New and More Pratic Methodology for Uniting the SERP Recording Output Files

# In[24]:


serp_csvs = sorted(glob.glob(("str*.csv")))
serp_csv = pd.concat((pd.read_csv(file) for file in serp_csvs), ignore_index=True)


# In[25]:


serp_csv.drop(columns="Unnamed: 0", inplace=True)
serp_csv.set_index("queryTime", inplace=True)
serp_csv


# ## Visualization of SERP Recording for the Query of "Calories in Pizza"
# 
# - Filter the "searchTerms" for the SERP you want to visualize.
# - Create a "Bubble Size" for the Scatter Plot
# - Choose an Animation Group and Animation Frame.
# - Run the code.

# In[26]:


pizza_serp = serp_csv[serp_csv['searchTerms'].str.contains("pizza", regex=True, case=False)]
pizza_serp['bubble_size'] = 35


# In[27]:


fig = px.scatter(pizza_serp, # Data Frame Name
            x="displayLink", # X-axis Value (Domain Names)
            y="rank", # Y-axis Value (Ranking Data)
            animation_frame=pizza_serp.index, # Animation Frame - Animation based on what??
            animation_group="displayLink", # Animation Point - What to animate?
            color="displayLink", # For grouping the data with colors.
            hover_name="link", # Name to be shown after hover effect.
            hover_data=["searchTerms","title","rank"], # Data to be shown after hover efect.
            log_y=False, # Optional. If it is True, the animation bubble can fit better.
            height=900, # Height of plot.
            width=900, # Width of plot.
            range_x=[-1,11], # X ticks range.
            range_y=[1,11],  # Y ticks range.
            size="bubble_size", # Bubble size for the bubbles.
            text="displayLink", # Text to be shown on bubbles.
            template="plotly_white", # Color scheme of the Plot.
            title="Heartbeat of SERP for 'Calories in Pizza'", # Title of the Plot.
            labels={"rank":"Rankings","displayLink":"Domain Names"}) # Labels for axes.



#fig['layout'].pop('updatemenus')


fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 500 # Animation Frame Duration.
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 1000 # Animation Transition Duration.


"""

For arranging the "margin and background color".

fig.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
    paper_bgcolor="white",
)

"""

# Updating the X-axis Title Font and Margin.
fig.update_xaxes(
        title_font = {"size": 20},
        title_standoff = 45)

# Updating the Y-axis Title Font and Margin.
fig.update_yaxes(
        title_font = {"size": 20},
        title_standoff = 45)


# Calling the plot within the notebook.
fig.show(renderer='notebook')


# - Another Example with the "Calories in BigMac"

# In[28]:


bigmac_serp = serp_csv[serp_csv['searchTerms'].str.contains("bigmac", regex=True, case=False)]
bigmac_serp['bubble_size'] = 35
bigmac_serp


# ## Visualization of SERP Recording for the Query of "Calories in BigMac"

# In[29]:


fig = px.scatter(bigmac_serp, 
                 x="displayLink", 
                 y="rank", 
                 animation_frame=bigmac_serp.index, 
                 animation_group="displayLink",
                 color="displayLink", 
                 hover_name="link", 
                 hover_data=["title"],
                 log_y=False, 
                 height=900, 
                 width=1100, 
                 range_x=[-1,11], 
                 range_y=[1,11],  
                 size="bubble_size", 
                 text="displayLink", 
                 template="plotly_dark", 
                 title="Heartbeat of SERP for 'Calories in BigMac'", 
                 labels={"rank":"Rankings","displayLink":"Domain Names"})

#fig['layout'].pop('updatemenus')

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 450
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 1500


"""fig.update_layout(
    margin=dict(l=20, r=20, t=20, b=20)
)"""


fig.update_xaxes(
        title_font = {"size": 20},
        title_standoff = 45)

fig.update_yaxes(
        title_font = {"size": 20},
        title_standoff = 45)

fig.show(renderer='notebook')


# ## Watching the Most Expensive Queries on Google for Just 10 Hours

# - I have recorded the SERP for the Most Expensive Queries which are "Insurance, Medical Coding Services, Business Services, Credit Calculation" on Google
# - I have recorded the SERP per 30 Minutes
# - I have Visualized the SERP for each Expensive Query to see Google's Routine Dance in Slow Motion

# In[30]:


cse_id = "7b8760de16d1e86bc" # Custom Search Engine ID
api_key = "AIzaSyAAJ9BhKPKafDGg5uBMgzR346ngGEz7GDQ" # API Key for Custom Search API of Google

def SERPheartbeat():

    """Calls the function with the determined frequency, for the determined queries.
    Creates a CSV Output with the name of the actual date which the function called."""

    date = datetime.now()
    date = date.strftime("%d%m%Y%H_%M_%S")
    
    df = adv.serp_goog(
        
        q=['Credit Calculation', "Insurance", "Medical Coding Services", "Business Services"], key=api_key, cx=cse_id)
    
    df.to_csv(f'expensive{date}' + '_' + 'scheduled_serp.csv')



# schedule.every(30).minutes.do(record_serp)

"""
For making the Schedule work.

n=0
while n<5:
    record_serp()
    time.sleep(3600)
    n+=1

"""


# In[74]:


# serp_csvs = sorted(glob.glob(("expensive*.csv")))
# serp_csv = pd.concat((pd.read_csv(file) for file in serp_csvs), ignore_index=True)
# serp_csv.drop("Unnamed: 0", axis=1, inplace=True)
# serp_csv.set_index("queryTime", inplace=True)
# serp_csv.to_excel("united_expensive.csv")
serp_csv = pd.read_excel("united_expensive.xlsx")


# In[75]:


credit_calculation = serp_csv[serp_csv["searchTerms"]=="Credit Calculation"]
credit_calculation["bubble_size"] = 35
credit_calculation.to_csv("credit_calculation.csv")
credit_calculation = pd.read_csv("credit_calculation.csv")


# In[76]:


credit_calculation.set_index("queryTime", inplace=True)
credit_calculation


# In[77]:


fig = px.scatter(credit_calculation, 
                 x="displayLink", 
                 y="rank", 
                 animation_frame=credit_calculation.index, 
                 animation_group="displayLink",
                 color="displayLink", 
                 hover_name="link", 
                 hover_data=["title"],
                 log_y=False, 
                 height=900, 
                 width=1100, 
                 range_x=[-1,11], 
                 range_y=[1,11],  
                 size="bubble_size", 
                 text="displayLink", 
                 template="plotly_dark", 
                 title="Credit Calculation SERP Recording per Minute for 10 Hours", 
                 labels={"rank":"Rankings","displayLink":"Domain Names"})

#fig['layout'].pop('updatemenus')

"""
fig.update_layout(
    margin=dict(l=20, r=20, t=20, b=20)
)"""


fig.update_yaxes(categoryorder="total ascending", title_font=dict(size=25))
fig.update_xaxes(categoryorder="total ascending", title_font=dict(size=25), title_standoff=45)

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 100
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 2000

fig.update_yaxes(categoryorder="total ascending")

fig.show(renderer='notebook')


# In[ ]:





# ## Comparing Top 10 Domain's Performance Based on Queries and Rankings with Visualization for the Different Dates

# - Taking an HTML Table from the Open Web

# In[35]:


culinary_fruits_df = pd.read_html("https://en.wikipedia.org/wiki/List_of_culinary_fruits", header=0)
culinary_fruits_merge_df = pd.concat(culinary_fruits_df)


# - Devariation of the Queries

# In[36]:


culinary_fruits_queries = ["calories in " + i.lower() for i in culinary_fruits_merge_df['Common name']] + ["nutrition in " + i.lower() for i in culinary_fruits_merge_df['Common name']]
culinary_fruits_queries


# ## Recording the SERP in Different Dates

# - In this example, I have recorded SERP randomly. That's why we don't have a "time" dependency here.

# In[37]:


#serp_df = adv.serp_goog(cx=cse_id, key=api_key, q=culinary_fruits_queries[0:30], gl=["us"]) # For Recording


# In[38]:


#serp_df.to_csv("next-serp.csv") # For Taking Output


# In[39]:


serp_df = pd.read_csv("serp_calories.csv")
serp_df2 = pd.read_csv("serp_calories-2.csv")
serp_df3 = pd.read_csv("serp_calories-3.csv")


# In[40]:


serp = serp_df.append([serp_df2,serp_df3])
serp.drop(columns={"Unnamed: 0"}, inplace=True)


# In[41]:


serp.to_csv("united_serp.csv")


# ## Adding the Query Day as a New Column for Comparison and Plotting

# In[42]:


serp["queryTime"] = serp["queryTime"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f+00:00"))
serp['queryDay'] = serp['queryTime'].apply(lambda x: datetime.strftime(x, "%Y-%m-%d"))
serp['queryDay']


# ### Taking the Top 10 Domain from the SERP Recording Files

# In[43]:


top10_domains = serp.displayLink.value_counts()[:10].index
top10_df = serp[serp['displayLink'].isin(top10_domains)] 


# ### Checking the New Column for the SERP Retrieving Date

# In[44]:


top10_df['queryDay']


# ## Sorting and Adding the Size for Scatter Plot

# In[45]:


top10_df.sort_values(["queryDay", "searchTerms", "rank"], inplace=True)
top10_df['bubble_size'] = 75


# An Optional, Ipython Output Preference Setting
# 
# from IPython.core.interactiveshell import InteractiveShell
# InteractiveShell.ast_node_interactivity = "last_expr"
# 
# %%javascript
# IPython.OutputArea.auto_scroll_threshold = 9999;

# ### From 2020-12-18 to 2021-01-05: Same 30 Query and Their Results for the Top 10 Domains with Changes

# In[46]:


fig = px.bar(top10_df, 
           x="rank", 
           y="displayLink", 
           color="rank", 
           hover_name="link", 
           hover_data=["title","link","searchTerms"],
           log_y=False, 
           height=1000, 
           width=1000, 
           template="plotly_white", 
           facet_col="queryDay", 
           facet_col_wrap=1, 
           labels={"displayLink":"Domain Names", "rank":"Ranking Results"}, 
           title="Best 10 Domains' Ranking Differences Based on Different Dates")

"""
fig.update_layout(
    margin=dict(l=20, r=20, t=20, b=20)
)"""


#matches="none"


fig.update_yaxes(categoryorder="total ascending", title_font=dict(size=25))
fig.update_xaxes(categoryorder="total ascending", title_font=dict(size=25))
fig.show(renderer='notebook')


# density_heatmap (Optional)


# ## Plotting and Animating Multiple SERP for Multiple Queries at the Same Time

# - I recommend you to "Filter Queries" so that You Shall not Broke Plotly API.

# In[47]:


serp['searchTerms'].unique()


# In[48]:


serp['bubble_size'] = 15
filtered_serp = serp[serp.searchTerms.isin(["calories in apple", "calories in quince"])]


# In[49]:


fig = px.scatter(filtered_serp,
           x="displayLink", 
           y="rank", 
           color="displayLink", 
           hover_name="link", 
           hover_data=["title","link","searchTerms"],
           log_y=False, 
           size="bubble_size", 
           size_max=15,
           height=1000, 
           width=1000,range_y=[0,10], 
           template="plotly_white", 
           animation_group="displayLink", 
           animation_frame="queryDay",
           opacity=0.60, 
           facet_col="searchTerms", 
           facet_col_wrap=1,facet_row_spacing=0.01,
           text="displayLink", 
           title="Multiple SERP Animating for the Ranking Differences", 
           labels={"rank":"Rankings", "displayLink":"Domain Names"})

#fig['layout'].pop('updatemenus')

"""
fig.update_layout(
    margin=dict(l=20, r=20, t=20, b=20)
)"""


fig.update_yaxes(categoryorder="total ascending", title_font=dict(size=25))
fig.update_xaxes(categoryorder="total ascending", title_font=dict(size=25), title_standoff=45)

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 2000

fig.update_yaxes(categoryorder="total ascending")

fig.show(renderer='notebook')


# ## Animating the Same SERPs for only Top 10 Domains (It will Broke Plotly)

# In[50]:


fig = px.scatter(top10_df, 
           x="displayLink", 
           y="rank", color="displayLink", 
           hover_name="link", 
           hover_data=["title","link","searchTerms"],
           log_y=False, 
           size="bubble_size",
           height=5000, 
           width=1000,range_y=[0,10], 
           template="plotly_white", 
           animation_group="displayLink", 
           animation_frame="queryDay",
           opacity=0.60, 
           facet_col="searchTerms", 
           facet_col_wrap=1,
           facet_row_spacing=0.01,
           title="Multiple SERP Animating for the Ranking Differences", 
           labels={"rank":"Rankings", "displayLink":"Domain Names"})

#fig['layout'].pop('updatemenus')
"""
fig.update_layout(
    margin=dict(l=20, r=20, t=20, b=20)
)"""

fig.update_yaxes(categoryorder="total ascending", title_font=dict(size=25))
fig.update_xaxes(categoryorder="total ascending", title_font=dict(size=25), title_standoff=45)
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 2000
fig.update_yaxes(categoryorder="total ascending")
fig.show(renderer='notebook')


# ## Animating The All SERPs for All Domains (It will Broke Plotly)

# In[51]:


fig = px.scatter(serp, x="displayLink", 
                 y="rank", 
                 color="displayLink", 
                 hover_name="link", 
                 hover_data=["title","link","searchTerms"],
                 log_y=False, size="bubble_size",
                 height=5000, 
                 width=1000,
                 range_y=[0,10], 
                 template="plotly_white", 
                 animation_group="displayLink", 
                 animation_frame="queryDay",
                 opacity=0.60, 
                 facet_col="searchTerms", 
                 facet_col_wrap=1,
                 facet_row_spacing=0.01,
                 title="Multiple SERP Animating for the Ranking Differences", 
                 labels={"rank":"Rankings", "displayLink":"Domain Names"})
#fig['layout'].pop('updatemenus')
"""
fig.update_layout(
    margin=dict(l=20, r=20, t=20, b=20)
)"""
fig.update_yaxes(categoryorder="total ascending", title_font=dict(size=25))
fig.update_xaxes(categoryorder="total ascending", title_font=dict(size=25), title_standoff=45)
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 2000
fig.update_yaxes(categoryorder="total ascending")
fig.show(renderer='notebook')


# ## To Examine The SERP Data with Data Science, Continue to the Serp.ipynb File

# - A Small Example for Coverage, Average Ranking and Result Count per Domain

# A Simple Example:

# In[52]:


(serp.pivot_table("rank", "displayLink", aggfunc=["count", "mean"])
.sort_values([("count", "rank"), ("mean", "rank")], ascending=[False,True])
.assign(coverage=lambda df:df[("count", "rank")] / len(serp_df)*1).head(10)
.style.format({("coverage", ""):"{:.1%}", ("mean", "rank"): '{:.2f}'}))


# **Let's continue!**

# In[ ]:




