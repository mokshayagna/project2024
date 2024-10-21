import requests
import csv
import os
# url = "https://content.civicplus.com/api/assets/bb030133-2fbc-44d4-bf71-8b49199a8b3b?cache=1800"
# response = requests.get(url)

# if response.status_code == 200:
#     with open("downloaded_file.pdf", "wb") as file:
#         file.write(response.content)
#     print("PDF downloaded successfully!")

def accessfiles(filename):
    rfd = open(filename, 'rt')
    chd = csv.reader(rfd)
    rows = []
    for row in chd:
        rows.append(row)  
    rfd.close()  
    return rows  

def download_files(url,index):
    response = requests.get(url)
   # print(response)
    if response.status_code == 200:
        folder_name = "downloding_file"
        os.makedirs(folder_name,exist_ok=True)
        print(f"folder{folder_name} is created")
        file_name = f"example {index}.pdf"
        file_path = os.path.join(folder_name, file_name)
        with open(file_path, "wb") as file:  
            file.write(response.content)  
        print(f"PDF '{file_name}' downloaded successfully!")
    else:
        print(f"Failed to download from {url}, status code: {response.status_code}")




def main():
    filename = "links.csv"
    rows = accessfiles(filename)
    for index, row in enumerate(rows[1:], start=1): 
        url = row[1].strip()  
        if url:  
            download_files(url,index) 



if __name__ == "__main__":
    main()