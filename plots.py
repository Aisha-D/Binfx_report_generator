# Plot figures from helpdesk 
import pandas as pd
import numpy
import matplotlib.pyplot as plt
import datetime
import os
from plotnine import *
import argparse

# arguements to point data folder containing csv files (2101 and alldata)
def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-m', '--month_data_path',
        help='path to the month data folder',
        required=True
        )
        
    parser.add_argument(
        '-a', '--all_data_path',
        help='path to the all data folder',
        required=True
        )
    
    parser.add_argument(
        '-d', '--date',
        help='Date in short hand M Y e.g Jan 2021',
        required=True
        )
    
    args = parser.parse_args()

    return args

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

def Plot_Workload(all_data, path):
    all_tickets = all_data.sum(axis=1)
    all_tickets = pd.DataFrame(all_tickets)
    all_tickets.columns = ['Tickets raised']
    # convert the date to short format
    dates_list = list(all_data.index)
    dates_list = [datetime.datetime.strptime(i, "%B %Y") for i in dates_list]
    dates_list = [i.strftime("%b %Y") for i in dates_list]
    dates = pd.DataFrame({'Dates': dates_list})
    all_tickets.index = dates.Dates # make index with new date format
    all_tickets = all_tickets.reset_index() # make index into a sep column 
    all_tickets.columns = [ 'Dates', 'Tickets raised']
    # Keep the order the dates are in at the moment, so its not alphabetical
    all_tickets.sort_values(by='Dates').reset_index(drop = True)
    all_tickets['Dates'] = pd.Categorical(all_tickets.Dates, categories=pd.unique(all_tickets.Dates))
    # Plot dot and join lines (group = 1 helps points be joined)
    plot = (ggplot(all_tickets, aes(x = 'Dates', y = 'Tickets raised', group = 1))
            + geom_point()
            + geom_line()
            + labs(x = "", y='Tickets raised', title = "Workload trend")
            + theme_classic()
            + theme(text=element_text(family='DejaVu Sans',
                                    size=10),
                    axis_title=element_text(face='bold'),
                    axis_text=element_text(face='italic'),
                    plot_title=element_text(face='bold',
                                            size=12)))
    plot.save(path + '/Workload.png', height=6, width=len(dates_list)+2)

## Run functions
def main():

    current_path = os.getcwd()
    args = parse_args()

    # Read in this months created data
    data_path = current_path + '/' + args.month_data_path
    print(data_path)

    # created csv
    data_file =  [f for f in os.listdir(data_path) if f.startswith('Created_request')]
    print(data_file[0])
    created_data = pd.read_csv(data_path + '/' + data_file[0], sep=',')
    # resolved csv
    data_file =  [f for f in os.listdir(data_path) if f.startswith('Requests_completed')]
    print(data_file[0])
    resolved_data = pd.read_csv(data_path + '/' + data_file[0], sep=',')

    # Read in all of data generated on helpdesk
    all_data_path = current_path + '/' + 'data/all_data'
    all_data_file =  [f for f in os.listdir(all_data_path) if f.startswith('Created_request')]
    print(all_data_file[0])
    all_data = pd.read_csv(all_data_path + '/' + all_data_file[0], sep=',', index_col=0)

    date = args.date
    Plot_CreatedTicket(created_data, date)
    Plot_CompletedTicket(resolved_data, date)
    Plot_CreatedVSCompletedTicket(created_data,resolved_data, date)
    Plot_Workload(all_data, data_path)

if __name__ == "__main__":

    main()
