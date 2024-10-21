import csv
import os
import requests
import re

def accessfiles(filename):
    rfd = open(filename, 'rt')
    chd = csv.reader(rfd)
    rows = []
    for row in chd:
        rows.append(row)  
    rfd.close()  
    return rows  

def main():
    filename = "links.csv"
    rows = accessfiles(filename)  
    for row in rows:
        print("done")


def clean_filename(url):
    name = re.sub(r'https?://', '', url)  # Remove 'http://' or 'https://' from the start
    name = re.sub(r'[^a-zA-Z0-9-_\.]', '_', name)  # Replace invalid characters with underscores
    return name  # Return the cleaned name

def download_pdfs(rows):
    folder_name = "downloaded_files"
    os.makedirs(folder_name, exist_ok=True)
    
    print(f"Folder '{folder_name}' created or already exists.")
    for index,row in enumerate(rows[1:],start=1):
        url = row[1].strip()
        name = clean_filename(url)
        file_name = f"{name}_{index}.pdf"
        file_path = os.path.join(folder_name, file_name)
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            with open(file_path, "wb") as pdf_file:
                pdf_file.write(response.content)
            print(f"PDF '{name}' downloaded successfully and saved as {file_path}")
        


def main():
    filename = "links.csv"
    rows = accessfiles(filename)  
    download_pdfs(rows)


if __name__ == "__main__":
    main()
