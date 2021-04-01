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

def Plot_CreatedTicket(data, date, output_path):
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
    plot.figure.savefig(output_path + "/Numer_of_Tickets_Raised.png",  bbox_inches = "tight") # gets plot and saves it to png

def Plot_CompletedTicket(data, date, output_path):
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
    plot.figure.savefig(output_path + "/Numer_of_Tickets_Completed.png",  bbox_inches = "tight") # gets plot and saves it to png

def Plot_CreatedVSCompletedTicket(data, data2, date, output_path):
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
    #plot = Sum_ticketstypes.plot.bar(rot=0, title=date, color=['blue','darkgreen'])
    #plot.figure.savefig(output_path + "/Numer_of_Tickets_Created_vs_Completed.png",  bbox_inches = "tight") # gets plot and saves it to png

    # make index into a sep column 
    Sum_ticketstypes  = Sum_ticketstypes.reset_index()
    Sum_ticketstypes.columns = [ 'Types', 'Tickets created','Tickets completed']

    # melt table to long so that each x variable has two x rows but for different groups
    Sum_ticketstypes = pd.melt(Sum_ticketstypes, id_vars=['Types'], value_vars=['Tickets created','Tickets completed'])
    Sum_ticketstypes.value = Sum_ticketstypes.value.astype('int64')
    print(Sum_ticketstypes)

    plot = (ggplot(Sum_ticketstypes, aes(x = 'Types', y = 'value', fill = 'variable'))
            + geom_bar(stat = "identity", position = 'dodge')
            + labs(x = "", y='Number of Tickets', fill =  "", 
                    title = "Number of tickets created and completed")
            + theme_classic()
            + theme(text=element_text(family='DejaVu Sans',
                                    size=10),
                    axis_title=element_text(face='bold'),
                    axis_text=element_text(face='italic'),
                    plot_title=element_text(face='bold',
                                            size=12)))
    plot.save(output_path + "/Number_of_Tickets_Created_vs_Completed.png", height=6, width=10)

def Plot_Workload(all_data, output_path):
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
    plot.save(output_path + '/Workload.png', height=6, width=len(dates_list)+2)

def plot_month_workload(data, output_path):
    ## Add this months trend - different lines for different ticket types
    Sum_ticketstypes = data.sum(axis=1)
    upper_limit = max(Sum_ticketstypes)

    data_date = data.Date.str.replace(r'2021$', '', regex=True) # remove year
    data.drop(data.columns[0],axis=1,inplace=True) # drop date column in data df
    data = pd.concat([data_date, data], axis=1) # join new date format

    # Keep the order the dates are in at the moment, so its not alphabetical
    data.sort_values(by='Date').reset_index(drop = True)
    data['Date'] = pd.Categorical(data.Date, categories=pd.unique(data.Date))

    df  = pd.melt(data, id_vars=['Date'])

    plot = (ggplot(df, aes(x = 'Date', y = 'value', color = 'variable', group = 1))
            + geom_line()
            + geom_point()
            + facet_grid('variable ~ .')
            + scale_y_continuous(expand=(0,0,0,1), breaks=range(0, upper_limit))
            + labs(x = "", y='', color = " ",
                    title = "Months Workload")
            + theme_classic()
            + theme(text=element_text(family='DejaVu Sans',
                                    size=9),
                    axis_title=element_text(face='bold'),
                    axis_text_x=element_text(rotation=45, hjust=1),
                    plot_title=element_text(face='bold',
                                            size=12)))
                                            
    plot.save(output_path +'/Months_workload.png', height=10, width=18)

def Plot_resolution_SLAs(data,output_path):
    data_resolve = data
    data_resolve = data_resolve.sum(axis=0)
    data_resolve = pd.Series.to_frame(data_resolve)
    data_resolve = data_resolve.drop('Date')
    data_resolve.columns = ['Time_to_resolution']
    data_resolve[['Ticket_type']] = data_resolve.index
    data_resolve[['Ticket_type','Met_vs_Breached']] = data_resolve['Ticket_type'].str.split(' - ',expand=True)
    data_resolve.reset_index(drop=True, inplace=True)

    # Take out total time to resolve
    data_resolve = data_resolve.drop([0,6])
    data_resolve = data_resolve.sort_values(by=['Ticket_type'])

    # At the moment Time_to_resolution is not seen as numeric but as 'object'
    # which is categorical instead of numeric so convert to numeric
    data_resolve.dtypes
    data_resolve.Time_to_resolution = data_resolve.Time_to_resolution.astype('int64')
    data_resolve.dtypes
    upper_limit = max(data_resolve.Time_to_resolution)
    print(data_resolve)


    plot = (ggplot(data_resolve, aes(x = 'Ticket_type', y = 'Time_to_resolution', fill = 'Met_vs_Breached'))
            + geom_bar(stat = "identity", position = 'dodge')
            # + facet_grid('Met vs Breached ~ .')
            + labs(x = "", y='Tickets', title = "Time to resolve tickets SLAs - Met vs Breached")
            + scale_y_continuous(expand=(0,0,0,1), breaks=range(0, upper_limit+1)) # Expand 1 value on y axis and add 1 breaks
            + theme_classic()
            + theme(text=element_text(family='DejaVu Sans',
                                    size=10),
                    axis_title=element_text(face='bold'),
                    axis_text=element_text(face='italic'),
                    plot_title=element_text(face='bold',
                                            size=12)))

    plot.save(output_path +'/resolution_SLAs.png', height=6, width=15)

def Plot_respond_SLAs(data,output_path):
    data_respond = data
    data_respond = data_respond.sum(axis=0)
    data_respond = pd.Series.to_frame(data_respond)
    data_respond = data_respond.drop('Date')
    data_respond.columns = ['Time_to_respond']
    data_respond[['Ticket_type']] = data_respond.index
    data_respond[['Ticket_type','Met_vs_Breached']] = data_respond['Ticket_type'].str.split(' - ',expand=True)
    data_respond.reset_index(drop=True, inplace=True)

    # Take out total time to respond
    data_respond = data_respond.drop([0,6])
    data_respond = data_respond.sort_values(by=['Ticket_type'])

    # At the moment Time_to_respond is not seen as numeric but as 'object'
    # which is categorical instead of numeric so convert to numeric
    data_respond.dtypes
    data_respond.Time_to_respond = data_respond.Time_to_respond.astype('int64')
    data_respond.dtypes
    upper_limit = max(data_respond.Time_to_respond)
    print(data_respond)

    plot = (ggplot(data_respond, aes(x = 'Ticket_type', y = 'Time_to_respond', fill = 'Met_vs_Breached'))
            + geom_bar(stat = "identity", position = 'dodge')
            # + facet_grid('Met vs Breached ~ .')
            + labs(x = "", y='Tickets', title = "Time to respond tickets SLAs - Met vs Breached")
            + scale_y_continuous(expand=(0,0,0,1), breaks=range(0, upper_limit+1)) # Expand 1 value on y axis and add 1 breaks
            + theme_classic()
            + theme(text=element_text(family='DejaVu Sans',
                                    size=10),
                    axis_title=element_text(face='bold'),
                    axis_text=element_text(face='italic'),
                    plot_title=element_text(face='bold',
                                            size=12)))

    plot.save(output_path +'/response_SLAs.png', height=6, width=15)

def group_status(data, column_header):
    data = data.groupby('Status').count()
    data.columns = [column_header]
    data = data.astype('int64')
    return data

def plot_currentstatus(data, output_path):
    data = data[['Issue Type', 'Status']]

    # filter ticket type from dataframe
    Emailed_request = data.loc[data['Issue Type'] == 'Emailed request']
    Inform_us = data.loc[data['Issue Type'] == 'Inform us']
    Reanalysis = data.loc[data['Issue Type'] == 'Reanalysis']
    Urgent_Reanalysis = data.loc[data['Issue Type'] == 'Urgent Reanalysis']
    Submit_a_request_or_incident = data.loc[data['Issue Type'] == 'Submit a request or incident']
    Ask_a_question = data.loc[data['Issue Type'] == 'Ask a question']

    # make a count table based on status per ticket type
    Emailed_request2 = group_status(Emailed_request, 'Emailed request')
    Inform_us2 = group_status(Inform_us, 'Inform us')
    Reanalysis2 = group_status(Reanalysis, 'Reanalysis')
    Urgent_Reanalysis2 = group_status(Urgent_Reanalysis, 'Urgent Reanalysis')
    Submit_a_request_or_incident2 = group_status(Submit_a_request_or_incident, 'Submit a request or incident')
    Ask_a_question2 = group_status(Ask_a_question, 'Ask a question')

    # concat all dataframes based on type
    data = pd.concat([Emailed_request2, Inform_us2, Reanalysis2, Urgent_Reanalysis2, Submit_a_request_or_incident2, Ask_a_question2], axis=1)
    data = data.fillna(0) # replace NaN with 0's
    data = data.astype(int)

    # reset the index to be a column
    data = data.reset_index()
    data.columns = ['Status', 'Emailed request', 'Inform us', 'Standard Reanalysis',
        'Urgent Reanalysis', 'Submit a request or incident', 'Ask a question']


    data = pd.melt(data, id_vars=['Status']) # melt dataframe to plot side by side
    upper_limit = max(data.value) # this will set the highest value on y axis

    plot = (ggplot(data, aes(x = 'variable', y = 'value', fill = 'Status'))
            + geom_bar(stat = "identity", position = 'dodge')
            + geom_col(position = 'dodge')
            + scale_y_continuous(expand=(0,0,0,1), breaks=range(0, upper_limit+1))
            + labs(x = "", y='', fill =  "Statuses", 
                    title = "Current Tickets Statuses")
            + scale_fill_manual(values=("deeppink", "orange", "darkgrey", "brown")) 
            + theme_classic()
            + theme(text=element_text(family='DejaVu Sans',
                                    size=10),
                    axis_title=element_text(face='bold'),
                    axis_text=element_text(face='italic'),
                    plot_title=element_text(face='bold',
                                            size=12)))
    plot.save(output_path +'/Current_Statuses.png', height=6, width=15)


## Run functions
def main():

    current_path = os.getcwd()
    args = parse_args()
    output_path = current_path + '/' + args.month_data_path

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

    # resolution SLA
    data_file = [f for f in os.listdir(data_path) if f.startswith('Breached_SLAs_Time_to_resolution')]
    print(data_file[0])
    data_sla_resolve = pd.read_csv(data_path + '/' + data_file[0], sep=',')

    # respond SLA
    data_file = [f for f in os.listdir(data_path) if f.startswith('Breached_SLAs_Time_to_respond')]
    print(data_file[0])
    data_sla_respond = pd.read_csv(data_path + '/' + data_file[0], sep=',')

    # current statuses SLA
    data_file = [f for f in os.listdir(data_path) if f.startswith('EMEE_')]
    print(data_file[0])
    data_current_status = pd.read_csv(data_path + '/' + data_file[0], sep=',')

    # Read in all of data generated on helpdesk
    all_data_path = current_path + '/' + 'data/all_data'
    all_data_file =  [f for f in os.listdir(all_data_path) if f.startswith('Created_request')]
    print(all_data_file[0])
    all_data = pd.read_csv(all_data_path + '/' + all_data_file[0], sep=',', index_col=0)

    date = args.date
    # Plot_CreatedTicket(created_data, date, output_path)
    # Plot_CompletedTicket(resolved_data, date, output_path)
    Plot_CreatedVSCompletedTicket(created_data,resolved_data, date, output_path)
    Plot_Workload(all_data, output_path)
    plot_month_workload(created_data, output_path)
    Plot_resolution_SLAs(data_sla_resolve, output_path)
    Plot_respond_SLAs(data_sla_respond, output_path)
    plot_currentstatus(data_current_status, output_path)

if __name__ == "__main__":

    main()

def plot_month_workload(data, output_path):
    ## Add this months trend - different lines for different ticket types
    Sum_ticketstypes = data.sum(axis=1)
    upper_limit = max(Sum_ticketstypes)

    data_date = data.Date.str.replace(r'2021$', '', regex=True) # remove year
    data.drop(data.columns[0],axis=1,inplace=True) # drop date column in data df
    data = pd.concat([data_date, data], axis=1) # join new date format

    Sum_ticketstypes = data.sum(axis=0)
    Sum_all = Sum_ticketstypes.sum(axis=1)
    # Keep the order the dates are in at the moment, so its not alphabetical
    data.sort_values(by='Date').reset_index(drop = True)
    data['Date'] = pd.Categorical(data.Date, categories=pd.unique(data.Date))

    df  = pd.melt(data, id_vars=['Date'])

    plot = (ggplot(df, aes(x = 'Date', y = 'value', color = 'variable', group = 1))
            + geom_line()
            + geom_point()
            + facet_grid('variable ~ .')
            + scale_y_continuous(expand=(0,0,0,1), breaks=range(0, upper_limit))
            + labs(x = "", y='', color = " ",
                    title = "Months Workload")
            + theme_classic()
            + theme(text=element_text(family='DejaVu Sans',
                                    size=9),
                    axis_title=element_text(face='bold'),
                    axis_text_x=element_text(rotation=45, hjust=1),
                    plot_title=element_text(face='bold',
                                            size=12)))
                                            
    plot.save(output_path +'/Months_workload.png', height=10, width=18)

