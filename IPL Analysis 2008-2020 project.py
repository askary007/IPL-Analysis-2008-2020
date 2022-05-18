#!/usr/bin/env python
# coding: utf-8

# # Importing Necessary Libraries

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.simplefilter(action="ignore",category=FutureWarning)


# # Importing the data

# In[2]:


df=pd.read_csv("C:\\Users\\Dell\\Desktop\\PG in Data Analysis EDU Bridge\\Project\\IPL Ball-by-Ball 2008-2020.csv")


# In[3]:


df1=pd.read_csv("C:\\Users\\Dell\\Desktop\\PG in Data Analysis EDU Bridge\\Project\\IPL Matches 2008-2020.csv")


# In[4]:


#display the first 5 rows from the dataset
df.head()


# In[63]:


df.tail()


# In[5]:


#display the last 5 rows from the dataset
df1.head()


# In[62]:


df1.tail()


# In[6]:


#Find the shape of our dataset
df.shape


# In[7]:


df1.shape


# # Data Cleaning

# In[8]:


#checking the null values
df.isnull().sum()


# In[9]:


(df.isnull().sum()/df.shape[0])*100


# In[10]:


df.drop(["dismissal_kind","player_dismissed","fielder","extras_type"],axis=1,inplace=True)


# In[12]:


#replace the null values with mode in bowlimg_team
x=df["bowling_team"].mode()[0]
df["bowling_team"].fillna(x,inplace=True)


# In[13]:


df.isnull().sum()


# In[14]:


df1.isnull().sum()


# In[15]:


(df1.isnull().sum()/df1.shape[0])*100


# In[16]:


df1.drop(["method"],axis=1,inplace=True)


# In[17]:


df1.boxplot()
plt.xticks(rotation="vertical")
plt.show()


# In[18]:


cols=["city","player_of_match","winner","result","eliminator"]
p=df1["city"].mode()[0]
df1["city"].fillna(p,inplace=True)

r=df1["player_of_match"].mode()[0]
df1["player_of_match"].fillna(r,inplace=True)

s=df1["winner"].mode()[0]
df1["winner"].fillna(s,inplace=True)

t=df1["result"].mode()[0]
df1["result"].fillna(t,inplace=True)

u=df1["eliminator"].mode()[0]
df1["eliminator"].fillna(u,inplace=True)

q=df1["result_margin"].median()
df1["result_margin"].fillna(q,inplace=True)


# In[19]:


df1.isnull().sum()


# In[20]:


df1.info()


# # Data Analysing & Visualising

# In[21]:


df1.columns


# In[22]:


#Total matches so far played 2008 - 2020
df1.shape[0]


# In[23]:


#to get which cities the matches played in 2008-2020
df1["city"].unique()


# In[24]:


#total number of teams participated in Ipl
df1["team1"].unique()


# In[25]:


#extraxt the year value from the date
df1["year"]=pd.DatetimeIndex(df1["date"]).year


# In[26]:


df1.head(1)


# In[27]:


#to get the list of seasons from the dataset
df1["year"].unique()


# In[28]:


match_per_year=df1.groupby(["year"])["id"].count().reset_index().rename(columns={"id":"matches"})


# In[29]:



match_per_year


# In[30]:


sns.countplot(df1["year"])
plt.xticks(rotation=45,fontsize=10)
plt.yticks(fontsize=10)
plt.xlabel("year",fontsize=10)
plt.ylabel("count",fontsize=10)
plt.title("Total matches played in each year",fontsize=10)
plt.show()


# In[31]:



year_data=df1[["id","year"]].merge(df,left_on="id",right_on="id",how="left")
year_data.head()


# In[61]:


season=year_data.groupby(["year"])["total_runs"].sum().reset_index()
season


# In[33]:


#to check total runs score in each season
season=year_data.groupby(["year"])["total_runs"].sum().reset_index()
t=season.set_index("year")
ax=plt.axes()
ax.set(facecolor="yellow")
sns.lineplot(data=t,palette="magma",marker="o")
plt.xlabel("Year",fontsize=15)
plt.ylabel("Runs",fontsize=15)
plt.title("Total runs in each season",fontsize=22)
plt.show()


# In[34]:


#runs scored per match in each season
runs_per_season=pd.concat([match_per_year,season.iloc[:,1]],axis=1)
runs_per_season["Runs scored per match"]=runs_per_season["total_runs"]/runs_per_season["matches"]
runs_per_season.set_index("year")
runs_per_season


# In[35]:


toss=df1["toss_winner"].value_counts()


# In[36]:


toss


# In[37]:



plt.figure(figsize=(10,7))
toss=df1["toss_winner"].value_counts()
ax=plt.axes()
ax.set(facecolor="black")
sns.barplot(y=toss.index,x=toss)
plt.title("Number of tosses won by each team")
plt.xlabel("Number of tosses won")
plt.ylabel("Teams")
plt.show()


# In[38]:


#checking the toss decision across the seasons
plt.figure(figsize=(10,7))
sns.countplot(x="year",hue="toss_decision",data=df1)
ax=plt.axes()
ax.set(facecolor="grey")
plt.xticks(rotation=60,fontsize=10)
plt.yticks(fontsize=10)
plt.title("Toss decision")
plt.xlabel("Year",fontsize=15)
plt.ylabel("Count",fontsize=15)

plt.show()


# In[39]:



#cheking the results of the matches comparing whose batting first or second
#here we can see batting second wins the highest number of matches
df1["result"].value_counts()


# In[40]:



#highest number of teams winning by wickets in which statuim
df1.venue[df1.result=="wickets"].mode()


# In[41]:


#highest number of teams winning by runs in which statuim
df1.venue[df1.result!="wickets"].mode()


# In[42]:


#which is best chasing team those who batting second
df1.winner[df1.result=="wickets"].mode()


# In[43]:


#which is best defending team those who batting first
df1.winner[df1.result=="runs"].mode()


# In[44]:


#to check whether toss winner is the winner of the match
toss=df1["toss_winner"]==df1["winner"]
sns.countplot(toss)
plt.show()


# In[45]:


#to check whether batting or fielding first can choose the winner
sns.countplot(df1.toss_decision[df1.toss_winner==df1.winner])
plt.show()


# In[46]:



#top ten batsman score highest runs in th ipl
runs=df.groupby(["batsman"])["batsman_runs"].sum().reset_index()
runs.columns=["Batsman","runs"]
y=runs.sort_values(by="runs",ascending=False).head(10).reset_index().drop("index",axis=1)
y


# In[47]:


plt.figure(figsize=(10,7))
ax=plt.axes()
ax.set(facecolor="grey")
sns.barplot(x=y["Batsman"],y=y["runs"],palette="rocket")
plt.xticks(rotation=90,fontsize=10)
plt.yticks(fontsize=10)
plt.xlabel("Players",fontsize=15)
plt.ylabel("Total runs",fontsize=15)
plt.title("Top ten batsman in IPL")
plt.show()


# In[48]:


#top ten bowler takes highest wickettaker in th ipl
wicket=df.groupby(["bowler"])["is_wicket"].sum().reset_index()
wicket.columns=["Bowler","Wicket"]
z=wicket.sort_values(by="Wicket",ascending=False).head(10).reset_index().drop("index",axis=1)
z


# In[49]:


plt.figure(figsize=(10,7))
ax=plt.axes()
ax.set(facecolor="yellow")
sns.barplot(x=z["Bowler"],y=z["Wicket"],palette="rocket")
plt.xticks(rotation=90,fontsize=10)
plt.yticks(fontsize=10)
plt.xlabel("Players",fontsize=15)
plt.ylabel("Total wickets",fontsize=15)
plt.title("Top ten bowler in IPL")
plt.show()


# In[50]:


#to check most player of the match award winner
x=df1["player_of_match"].mode()
x


# In[51]:


plt.figure(figsize=(10,7))
ax=plt.axes()
ax.set(facecolor="orange")
df1.player_of_match.value_counts()[:5].plot(kind="bar",color="purple")
plt.xlabel("Players",fontsize=15)
plt.ylabel("Count",fontsize=15)
plt.title("Top Five MoM award Winners",fontsize=15)
plt.show()


# In[52]:


x=df1.winner.value_counts()[:5]
x


# In[53]:


plt.figure(figsize=(10,7))
x=["Mumbai Indians","Chennai Super Kings","Kolkata Knight Riders","Royal Challengers Bangalore","Kings XI Punjab"]
y=[124,106,99,91,88]
plt.pie(y,autopct="%0.2f%%",labels=x)
plt.title("Top 5 best teams",fontsize=15)
plt.show()


# In[54]:


#top five Teams scoring highest runs in th ipl season
runs=df.groupby(["batting_team"])["total_runs"].sum().reset_index()
runs.columns=["Teams","runs"]
r=runs.sort_values(by="runs",ascending=False).head(5).reset_index().drop("index",axis=1)
r


# In[55]:


plt.figure(figsize=(10,7))
ax=plt.axes()
ax.set(facecolor="black")
sns.barplot(x=r["Teams"],y=r["runs"],palette="rocket")
plt.xticks(rotation=90,fontsize=10)
plt.yticks(fontsize=10)
plt.xlabel("Teams",fontsize=15)
plt.ylabel("Total runs",fontsize=15)
plt.title("Top five teams scoring highest runs in IPL")
plt.show()


# # Conclusion

# In[56]:


Following are the conclusion of the above IPL Analysis 2008 to 2020 are below
1.we can see here that the best team throughout the season is Mumbai indians,best batsman is virat kholi,
  best bowler is SL Malinga and the MOM of the series is AB de Villiers
2.In this season toss winner get little high chance to win the matches we shown in line number 48.
3.In this season toss winner had decided to field got a very high chance to win the matches as shown in line number 49

