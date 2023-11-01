import os
import requests
import pandas as pd


def filename(language, file_name):
    file_name = str(file_name).strip().replace("/","-")
    if file_name[-1] == ".":
        file_name += "pdf"
    else:
        file_name += ".pdf"
    return "output/"+ str(language).lower().strip().capitalize() + "/" + file_name
    

def download_pdf(url, file_name, headers, language):

    try:
        response = requests.get(url, headers=headers, timeout=60)
    except Exception as e:
        with open('check.txt', 'a') as the_file:
            the_file.write(str(url) + " --|||-- " + str(file_name) + " --|||-- " + str(language) + "\n")
        return None
    
    
    print("pdf downloaded")
    
    filepath = filename(language, file_name)
    print(filepath)
    
    if response.status_code == 200:
        with open(filepath, "wb") as f:
            f.write(response.content)
        print("pdf saved")
    else:
        print(response.status_code)


def start(type, filename, pdf_name_column, grouping_column, link, parent_dir, zip=False, aws=False):
    """
        type="excel",                             # filetype: csv or excel
        filename="pdf_download_input.xlsx",       # filename along with its path
        pdf_name_column={file_name},                 # column name containing the file_name
        grouping_column={grouping_column},               # column name by which it is to be grouped
        link={urls_to_download},                  # column name containing the link
        parent_dir="output",                      # create a folder and pass its path here
        zip="zip -r tmp.zip output_folder,        # optional parameter: pdf.zip: output zip name; output: output folder name
        aws="aws s3 cp tmp.zip  s3://{path}"      # optional parameter: pdf.zip: zip file to export; s3://raw-data/: s3 bucket name
    """
    headers = {"User-Agent": "Chrome/51.0.2704.103"}

    if type == "excel":
        df = pd.read_excel(filename, engine='openpyxl')
    elif type == "csv":
        df = pd.read_csv(filename)
    
    data = df[[pdf_name_column, grouping_column, link]].values

    # parent_dir = "/home/ubuntu/environment/pdfs download/output"
    directories = list(
        set(
            list(
                map(
                    lambda x: x.lower().strip().capitalize(), 
                    list(df[grouping_column].values)
                )
            )
        )
    )

    for directory in directories:
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)

    for i, x in enumerate(data):
        print(str(i+1) + "/" + str(len(data)))
        download_pdf(x[2], x[0], headers, x[1])

    if zip:
        os.system(zip)

    if aws:
        os.system(aws)
