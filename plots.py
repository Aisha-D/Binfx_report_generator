# Plot figures from helpdesk 

import pandas as pd
import numpy
import matplotlib.pyplot as plt
import datetime

data = pd.read_csv('/home/aisha/Documents/Projects/Binfx_Service_Reports/2101/Created_requests_Summary_2021-01-01_to_2021-01-31_by_day.csv', sep=',')
data2 = pd.read_csv('/home/aisha/Documents/Projects/Binfx_Service_Reports/2101/Requests_completed_Summary_2021-01-01_to_2021-01-31_by_day.csv', sep=',')

Total_tickets = data.sum(axis=1)
Total_tickets = numpy.sum(Total_tickets)
print(Total_tickets)

date = 'Jan 2021'

def Plot_CreatedTicket(data, date):
    """Plots the number of tickets raised/created 

    Args:
        data (panda): Dataframe of data from this month
    """
    Sum_ticketstypes = data.sum(axis=0)
    Sum_ticketstypes = pd.Series.to_frame(Sum_ticketstypes)
    Sum_ticketstypes = Sum_ticketstypes.drop('Date')
    Sum_ticketstypes.columns = ['Number of tickets raised']
    print(Sum_ticketstypes)
    Sum_ticketstypes.index = ['Submit a request\nor incident', 'Ask a\nquestion', 'Emailed\nrequest','Standard\nReanalysis', 'Urgent\nReanalysis']
    plot = Sum_ticketstypes.plot.bar(rot=0, title=date)
    plot.figure.savefig("Numer_of_Tickets_Raised.png",  bbox_inches = "tight") # gets plot and saves it to png

def Plot_CompletedTicket(data, date):
    """Plots the number of tickets completed 

    Args:
        data (panda): Dataframe of data from this month
    """
    Sum_ticketstypes = data.sum(axis=0)
    Sum_ticketstypes = pd.Series.to_frame(Sum_ticketstypes)
    Sum_ticketstypes = Sum_ticketstypes.drop('Date')
    Sum_ticketstypes.columns = ['Number of tickets completed']
    print(Sum_ticketstypes)
    Sum_ticketstypes.index = ['Submit a request\nor incident', 'Ask a\nquestion', 'Emailed\nrequest','Standard\nReanalysis', 'Urgent\nReanalysis']
    plot = Sum_ticketstypes.plot.bar(rot=0, title=date,color='darkgreen')
    plot.figure.savefig("Numer_of_Tickets_Completed.png",  bbox_inches = "tight") # gets plot and saves it to png

def Plot_CreatedVSCompletedTicket(data, data2, date):
    """Plots the number of tickets created vs completed

    Args:
        data (panda): Dataframe of created tickets from this month
        data2 (panda):Dataframe of completed tickets from this month
    """
    # make a table of created tickets types
    Sum_ticketstypes_created = data.sum(axis=0)
    Sum_ticketstypes_created = pd.Series.to_frame(Sum_ticketstypes_created)
    Sum_ticketstypes_created = Sum_ticketstypes_created.drop('Date')
    Sum_ticketstypes_created.columns = ['Number of tickets created']
    print(Sum_ticketstypes_created)
    # make a table of completed ticket types
    Sum_ticketstypes_completed = data2.sum(axis=0)
    Sum_ticketstypes_completed = pd.Series.to_frame(Sum_ticketstypes_completed)
    Sum_ticketstypes_completed = Sum_ticketstypes_completed.drop('Date')
    Sum_ticketstypes_completed.columns = ['Number of tickets completed']
    print(Sum_ticketstypes_completed)
    # join the table and make side by side bar plot
    Sum_ticketstypes = pd.concat([Sum_ticketstypes_created, Sum_ticketstypes_completed], axis=1)
    Sum_ticketstypes.index = ['Submit a request\nor incident', 'Ask a\nquestion', 'Emailed\nrequest','Standard\nReanalysis', 'Urgent\nReanalysis']
    plot = Sum_ticketstypes.plot.bar(rot=0, title=date, color=['blue','darkgreen'])
    plot.figure.savefig("Numer_of_Tickets_Created_vs_Completed.png",  bbox_inches = "tight") # gets plot and saves it to png

Plot_CreatedTicket(data, 'Jan 2021')
Plot_CompletedTicket(data2, 'Jan 2021')
Plot_CreatedVSCompletedTicket(data,data2, 'Jan 2021')

###workload trend

All_created = pd.read_csv('/home/aisha/Documents/Projects/Binfx_Service_Reports/AllData/Created_requests_Summary_2020-03-01_to_2021-02-22_by_month.csv', 
                            sep = ',', index_col=0)
#def Plot_Workload(data):
data = All_created
data2 = data.sum(axis=1)
data2.columns = ['Number of tickets raised']
x = pd.Index.tolist(data2.index)
x2 = [datetime.datetime.strptime(i, "%B %Y") for i in x]
x = [i.strftime("%b %Y") for i in x2]
y = pd.Index.tolist(data2)
fig, ax = plt.subplots()
plt.figure(figsize=(15,8))
xs = range(len(x))
plt.axes(ax[0])
plt.plot(xs, y)
plt.xticks(xs, x)
plt.tight_layout()
plt.title("Workload", weight='bold')
plt.savefig("Cumulative_workload.png",  bbox_inches = "tight") 

#Plot_Workload(All_created)