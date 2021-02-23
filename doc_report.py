from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches
import argparse
import datetime
import os 

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-p', '--data_path',
        help='path to the data folder',
        required=True
        )

    args = parser.parse_args()

    return args

def Format_date(folder_date):
    date_y = folder_date[-4:-2] #subract fourth to second last char
    date_m = folder_date[-2:] #substracts last two char
    date = date_y + " " + date_m
    folder_date = date_y + date_m
    date_formatted = datetime.datetime.strptime(date, "%y %m")
    date = date_formatted.strftime("%b %Y")
    return date, folder_date

def Open_document(current_path):
    document = Document(current_path + '/templates/Report_template.docx')
    return document

## Add date under header
def Add_date(date, document):
    p = document.add_paragraph(date)
    p.alignment = 1
    p.add_run().size = Pt(14)
    document.add_paragraph(' ')

## Add Agents to user ratio
def Add_agent2user(document):
    table = document.add_table(rows=1, cols=2)
    table.style = 'Grid Table 4 Accent 5'
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Agents'
    hdr_cells[1].text = 'Users'
    row_cells = table.add_row().cells
    row_cells[0].text = '11'
    row_cells[1].text = '51'
    document.add_paragraph(' ')

## Add helpdesk header
def Add_HelpdeskSection(document, path):
    document.add_heading('Helpdesk', level=1)
    document.add_paragraph(' ')
    ### Helpdesk workload
    document.add_paragraph(
        'Since August 2020, we moved to the EMEE helpdesk solve to any bioinformatics related issues or queries. Steadily, more staff are raising issues via the helpdesk.'
        )
    document.add_paragraph(' ')
    my_image = document.add_picture(path+'/Cumulative_workload.png', width=Inches(5))
    last_paragraph = document.paragraphs[-1] 
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_paragraph(' ')
    ### Number of tickets created vs completed this month
    document.add_paragraph(
        'The helpdesk is designed to categorise different tickets into groups to help us understand what common issues are .'
        'We can see reanalysis, both standard and urgent, are highly requested and we meet respond back quickly within the month if there are no issues.'
        'Cases where there are more completed tickets than raised, the closed tickets are those raised in the last month.'
        )
    document.add_paragraph(' ')
    my_image = document.add_picture(path+'/Numer_of_Tickets_Created_vs_Completed.png', width=Inches(4))
    last_paragraph = document.paragraphs[-1] 
    last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_paragraph(' ')


def Close_document(document, path):
    document.save(path + '/Report_Jan2021.docx')
    print("Updated the report and saved in: " + path + '/Report_Jan2021.docx')


def main():

    current_path = os.getcwd()
    current_path = current_path[:-5]

    args = parse_args()

    date, folder_date = Format_date(args.data_path)

    path = current_path + '/data/' + folder_date

    print(date)

    print(folder_date)

    print(path)

    document = Open_document(current_path)
    
    Add_date(date, document)

    Add_agent2user(document)

    Add_HelpdeskSection(document, path)

    Close_document(document, path)


if __name__ == "__main__":

    main()
