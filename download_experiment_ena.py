from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time, os, shutil, gzip, sys
from zipfile import ZipFile

#Program is opening for example like:
#python download_experiment_ena.py SRX647352

accesion = sys.argv[1]

# setting the downloading folder and getting the ENA page --------------------------------------------
PATH = 'C:\Program Files\chromedriver.exe'
prefs = {"download.default_directory": os.path.dirname(os.path.realpath(__file__))}
options = Options()
options.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome(PATH , options = options)
browser.get(f'https://www.ebi.ac.uk/ena/browser/view/{accesion}?show=reads') 

time.sleep(5)
print('-------------------------------')
soup = BeautifulSoup(browser.page_source, 'html.parser')
content = soup.find('div', class_='attributes ng-star-inserted')

# checking if Library Layout is single or paired
time.sleep(5)
attributes = soup.find_all('div', class_='attribute row ng-star-inserted')
for attribute in attributes:
    if attribute.find('div', class_='attribute-name col-lg-3').text == 'Library Layout:':
        time.sleep(5)
        div = attribute.find('div', class_='col-lg-9 content-justify')
        time.sleep(5)
        Layout = div.find('span', class_='ng-star-inserted').text.strip()

        time.sleep(3)
        Run_acc = browser.find_element_by_css_selector("td[class='mat-cell cdk-column-run_accession mat-column-run_accession ng-star-inserted'] a[class='no-underline']").text

        if Layout == 'SINGLE': 
            # if the library layout is single, then get the link to a file and download it in .zip format
            print('Library Layout: SINGLE')

            
            time.sleep(3)
            link = browser.find_element_by_xpath("//label[@for='mat-checkbox-52-input']//div[@class='mat-checkbox-inner-container']")
            browser.execute_script("arguments[0].click();", link) #click the fastq.gz link

            time.sleep(3)
            yes = browser.find_element_by_xpath("//span[normalize-space()='Download selected files']")
            browser.execute_script("arguments[0].click();", yes) # download the fastq's in zip file

            time.sleep(2)
            print('Downloading...') 

            
            for i in range(120): 
                # program is waiting for downloading the files (because the files can have a big size)
                if os.path.exists(f'{os.path.dirname(os.path.realpath(__file__))}/ena_files.zip'):
                    # Extract all the contents of zip file in current directory
                    print('Unpacking the .zip files...')
                    with ZipFile('ena_files.zip', 'r') as zipObj:
                        zipObj.extractall()
                    
                    # Move the file to the python program folder        
                    shutil.move(f'{Run_acc}/{Run_acc}.fastq.gz', f'{os.path.dirname(os.path.realpath(__file__))}/{Run_acc}.fastq.gz')

                    # unpack the .gz file to .fastq file
                    with gzip.open(f'{Run_acc}.fastq.gz', 'rb') as folder_in:
                        with open(f'{Run_acc}.fastq', 'wb') as folder_out:
                            shutil.copyfileobj(folder_in, folder_out)
                    
                    # remove all the useless stuff
                    print('Removing useless files...')
                    time.sleep(5)
                    os.rmdir(f'{Run_acc}')
                    time.sleep(3)
                    os.remove('ena_files.zip')
                    time.sleep(3)
                    os.remove(f'{Run_acc}.fastq.gz')
                    break
                
                else:
                    time.sleep(30)
        
            
        else:
            print('Library Layout: PAIRED') # library layout is paired

            time.sleep(3)
            # find all the links to files in .fastq format from the page
            fastqs = (browser.find_elements_by_partial_link_text('fastq.gz'))
            links = list()
            for fastq in fastqs:
                links.append(fastq.text)

            # get the right link to the first file (...._1.fastq)
            time.sleep(3)
            start = 52
            for i in range(len(links)):
                if links[i] == f'{Run_acc}_1.fastq.gz':
                    start = start + links.index(f'{Run_acc}_1.fastq.gz')

            # get the 2 fastq links and download them in a .zip file
            time.sleep(3)
            link1 = browser.find_element_by_xpath(f"//label[@for='mat-checkbox-{start}-input']//div[@class='mat-checkbox-inner-container']")
            browser.execute_script("arguments[0].click();", link1) #click the FIRST fastq.gz link

            time.sleep(2)
            link2 = browser.find_element_by_xpath(f"//label[@for='mat-checkbox-{start+1}-input']//div[@class='mat-checkbox-inner-container']")
            browser.execute_script("arguments[0].click();", link2) #click the SECOND fastq.gz link
            
            time.sleep(3)
            yes = browser.find_element_by_xpath("//span[normalize-space()='Download selected files']")
            browser.execute_script("arguments[0].click();", yes) # download the fastq's in zip file

            time.sleep(2)
            print('Downloading...')
            for i in range(120):
                if os.path.exists(f'{os.path.dirname(os.path.realpath(__file__))}/ena_files.zip'):
                    print('Unpacking the .zip files...')
                    with ZipFile('ena_files.zip', 'r') as zipObj: # Extract all the contents of zip file in current directory
                        zipObj.extractall()

                    time.sleep(3)   
                    shutil.move(f'{Run_acc}/{Run_acc}_1.fastq.gz', f'{os.path.dirname(os.path.realpath(__file__))}/{Run_acc}_1.fastq.gz') # Move the file to the python program folder

                    time.sleep(3)
                    shutil.move(f'{Run_acc}/{Run_acc}_2.fastq.gz', f'{os.path.dirname(os.path.realpath(__file__))}/{Run_acc}_2.fastq.gz') # Move the file to the python program folder

                    time.sleep(3)
                    with gzip.open(f'{Run_acc}_1.fastq.gz', 'rb') as folder_in: # unpacking the .gz file to .fastq file
                        with open(f'{Run_acc}_1.fastq', 'wb') as folder_out:
                            shutil.copyfileobj(folder_in, folder_out)

                    time.sleep(3)
                    with gzip.open(f'{Run_acc}_2.fastq.gz', 'rb') as folder_in: # unpacking the .gz file to .fastq file
                        with open(f'{Run_acc}_2.fastq', 'wb') as folder_out:
                            shutil.copyfileobj(folder_in, folder_out)
                        
                    time.sleep(5)
                    print('Removing useless files...')
                    os.rmdir(f'{Run_acc}')
                    os.remove('ena_files.zip')
                    os.remove(f'{Run_acc}_1.fastq.gz')
                    os.remove(f'{Run_acc}_2.fastq.gz')
                    break
                
                else:
                    time.sleep(30)

        time.sleep(3)
        print(f'DONE!\nThe fastq file from {accesion} was succesfully downloaded', '\n', '--------------------------------')
        
        time.sleep(3)
        close = input('Would you like to close the ENA page? (Y/N)')
        if close.upper() == 'N':
            print('Okey!')
        elif close.upper() == 'Y':
            browser.quit()
        else:
            print('Wrong letter!')
