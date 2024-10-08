import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import requests
from selenium.webdriver.support.ui import Select
from datetime import datetime
import pandas as pd
import json

df = pd.read_csv('./icici.csv', dtype={'checker': 'string',"laptop":"string"})  # Replace 'your_file.csv' with the actual filename

results = []  # To store the result of each row processing
# Setup browser options

options = webdriver.ChromeOptions()

# Function to run ADB commands
def run_adb_command(command):

    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error running ADB command: {e.stderr.decode('utf-8')}")
        return None


# Function to get the current IP address
def get_current_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        return response.json().get('ip')
    except requests.RequestException as e:
        print(f"Error fetching current IP: {e}")
        return None
    
# Function to change the IP address by toggling flight mode
def change_ip():
    try:
        print('Enabling flight mode...')
        run_adb_command('adb shell cmd connectivity airplane-mode enable')
        print('Waiting for 10 seconds...')
        time.sleep(10)
        
        print('Disabling flight mode...')
        run_adb_command('adb shell cmd connectivity airplane-mode disable')
        print('Waiting for 20 seconds...')
        time.sleep(20)  # Increase this wait time to allow the network to stabilize
        
        print('Waiting for IP to change...')
        time.sleep(10)

        
        new_ip = get_current_ip()
        
        if new_ip:
            print(f"New IP: {new_ip}")
        else:
            print("New IP not found!")

        return new_ip
    except Exception as error:
        print('Error during IP change:', error)
        return None

def is_ip_used(ip, filename='icici.txt'):
    
    try:
        # Open the file in read mode
        with open(filename, 'r') as file:
            used_ips = file.read().splitlines()
            
            # Loop through each line in the file
            for entry in used_ips:
                # Split the IP and the date (if present) and compare only the IP part
                stored_ip = entry.split(' - ')[0].strip()  # Extract the IP part and remove extra spaces
                if stored_ip == ip:
                    return True  # IP is already used
            return False  # IP not found in the file
    except FileNotFoundError:
        # If the file doesn't exist, consider that no IP has been used yet
        return False
    

# Function to save the IP address to a file
def save_ip(ip,gmail,phone, filename='./icici.txt'):
    # Get the current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Open the file in append mode and write the IP address with the date
    with open(filename, 'a') as file:
        file.write(f"{ip} - {current_date} - {gmail} - {phone}\n")



for index, row in df.iterrows():

    print(f"Processing row {index}: {row.to_dict()}")
    # Change IP before starting the browser automation
    if pd.isna(row['checker']) or row['checker'] == "false":
        print('Checker is False or NA. Proceeding with this row.')
        new_ip = change_ip()
        if new_ip and not is_ip_used(new_ip):
            # https://www.iciciprulife.com/term-insurance-plans/iprotect-smart-term-insurance-calculator.html
            # http://www.phoenixads.net/track/click.asp?cid=22614&pid=677&did=21772&code=987598
            browser = webdriver.Chrome(options=options)
            browser.set_window_size(360, 800)
            # Step 1: Open the specified URL
            browser.get('https://www.iciciprulife.com/term-insurance-plans/iprotect-smart-term-insurance-calculator.html')

            # Step 2: Add random delay
            delay = random.uniform(3, 4)
            time.sleep(delay)

            try:
                # Step 3: Perform select action
                element3 = browser.find_element(By.XPATH, "/html/body/div[@class='contentpar parsys']/div[@class='data-input parbase section']/div[@class='main-container cal-hide']/div[@class='container1']/div[@class='first-page-container pb-lg-5']/section[2]/div[@class='container']/div[@class='row']/div[@class='col-12 lead-form-content py-3 mt-lg-5']/form[@class='new-lead-form']/div[@class='lead-form-container mr-3']/div[@class='lead-input-section']/div[@class='d-flex desk-hg width-all']/div[@class='form-group mr-lg-3 mr-3 width-adjust']/select[@id='myDropDown']")
                select = Select(element3)
                select.select_by_visible_text(row['Gender'])

                # Step 4: Add random delay
                delay = random.uniform(3, 4)
                time.sleep(delay)

                # Step 5: Perform input action
                element5 = browser.find_element(By.XPATH, "/html/body/div[@class='contentpar parsys']/div[@class='data-input parbase section']/div[@class='main-container cal-hide']/div[@class='container1']/div[@class='first-page-container pb-lg-5']/section[2]/div[@class='container']/div[@class='row']/div[@class='col-12 lead-form-content py-3 mt-lg-5']/form[@class='new-lead-form']/div[@class='lead-form-container mr-3']/div[@class='lead-input-section']/div[@class='d-flex desk-hg width width-all']/div[@class='form-group mr-lg-3 mr-3 position-relative width-adjust']/input[@class='form-control input-field']")
                element5.clear()
                element5.send_keys(row['DOB'])

                # Step 6: Add random delay
                delay = random.uniform(3, 4)
                time.sleep(delay)

                # Step 7: Perform input action
                element7 = browser.find_element(By.XPATH, "/html/body/div[@class='contentpar parsys']/div[@class='data-input parbase section']/div[@class='main-container cal-hide']/div[@class='container1']/div[@class='first-page-container pb-lg-5']/section[2]/div[@class='container']/div[@class='row']/div[@class='col-12 lead-form-content py-3 mt-lg-5']/form[@class='new-lead-form']/div[@class='lead-form-container mr-3']/div[@class='lead-input-section']/div[@class='d-flex desk-hg width width-all']/div[@class='form-group width-adjust']/span[@class='valid_check valid_check_tick mob_input_div hide']/input[@id='leadMobileNo']")
                element7.clear()
                element7.send_keys(row['Mobile'])

                # Step 8: Add random delay
                delay = random.uniform(3, 4)
                time.sleep(delay)

                # Step 9: Perform input action
                element9 = browser.find_element(By.XPATH, "/html/body/div[@class='contentpar parsys']/div[@class='data-input parbase section']/div[@class='main-container cal-hide']/div[@class='container1']/div[@class='first-page-container pb-lg-5']/section[2]/div[@class='container']/div[@class='row']/div[@class='col-12 lead-form-content py-3 mt-lg-5']/form[@class='new-lead-form']/div[@class='lead-form-container mr-3']/div[@class='lead-input-section']/div[@class='form_normal_ips']/div[@class='form-group mb-20']/span[@class='valid_check hide']/input[@class='form-control input-field']")
                element9.clear()
                element9.send_keys(row['Email'])

                # Step 10: Add random delay
                delay = random.uniform(5, 6)
                time.sleep(delay)

                # Step 11: Perform select action
                element11 = browser.find_element(By.XPATH, "/html/body/div[@class='contentpar parsys']/div[@class='data-input parbase section']/div[@class='main-container cal-hide']/div[@class='container1']/div[@class='first-page-container pb-lg-5']/section[2]/div[@class='container']/div[@class='row']/div[@class='col-12 lead-form-content py-3 mt-lg-5']/form[@class='new-lead-form']/div[@class='lead-form-container mr-3']/div[@class='lead-input-section']/div[@class='form_normal_ips']/div[@class='d-flex desk-hg width-all'][1]/div[@class='form-group mr-lg-3 mr-3 width-adjust']/select[@id='myDropDown2']")
                select = Select(element11)
                select.select_by_visible_text(row['occupation'])

                # Step 12: Add random delay
                delay = random.uniform(5, 6)
                time.sleep(delay)

                # Step 13: Perform select action
                element13 = browser.find_element(By.XPATH, "/html/body/div[@class='contentpar parsys']/div[@class='data-input parbase section']/div[@class='main-container cal-hide']/div[@class='container1']/div[@class='first-page-container pb-lg-5']/section[2]/div[@class='container']/div[@class='row']/div[@class='col-12 lead-form-content py-3 mt-lg-5']/form[@class='new-lead-form']/div[@class='lead-form-container mr-3']/div[@class='lead-input-section']/div[@class='form_normal_ips']/div[@class='d-flex desk-hg width-all'][1]/div[@class='form-group width-adjust position-relative']/div[@class='AnnualIncomeSelect annIncomeDropdownPartnerPersona']/select[@id='myDropDown1']")
                select = Select(element13)
                select.select_by_visible_text(row['annual income'])

                # Step 14: Add random delay
                delay = random.uniform(5, 6)
                time.sleep(delay)

                # Step 15: Perform select action
                element15 = browser.find_element(By.XPATH, "/html/body/div[@class='contentpar parsys']/div[@class='data-input parbase section']/div[@class='main-container cal-hide']/div[@class='container1']/div[@class='first-page-container pb-lg-5']/section[2]/div[@class='container']/div[@class='row']/div[@class='col-12 lead-form-content py-3 mt-lg-5']/form[@class='new-lead-form']/div[@class='lead-form-container mr-3']/div[@class='lead-input-section']/div[@class='form_normal_ips']/div[@class='d-flex desk-hg width-all'][2]/div[@class='form-group mr-lg-3 mr-3 width-adjust']/select[@id='myDropDown3']")
                select = Select(element15)
                select.select_by_visible_text(row['Educational'])

                # Step 16: Add random delay
                delay = random.uniform(6, 7)
                time.sleep(delay)

                # Step 17: Perform input action
                element17 = browser.find_element(By.XPATH, "/html/body/div[@class='contentpar parsys']/div[@class='data-input parbase section']/div[@class='main-container cal-hide']/div[@class='container1']/div[@class='first-page-container pb-lg-5']/section[2]/div[@class='container']/div[@class='row']/div[@class='col-12 lead-form-content py-3 mt-lg-5']/form[@class='new-lead-form']/div[@class='lead-form-container mr-3']/div[@class='lead-input-section']/div[@class='form_normal_ips']/div[@class='d-flex desk-hg width-all'][2]/div[@class='form-group width-adjust pincode_map_nri']/input[@id='calc_pincode']")
                element17.clear()
                element17.send_keys(row['Pin code'])

                # Step 18: Add random delay
                delay = random.uniform(10, 15)
                time.sleep(delay)

                # Step 19: Perform click action
                element19 = browser.find_element(By.XPATH, "/html/body/div[@class='contentpar parsys']/div[@class='data-input parbase section']/div[@class='main-container cal-hide']/div[@class='container1']/div[@class='first-page-container pb-lg-5']/section[2]/div[@class='container']/div[@class='row']/div[@class='col-12 lead-form-content py-3 mt-lg-5']/form[@class='new-lead-form']/div[@class='lead-form-container mr-3']/div[@id='SingleFoldViewbtn1']/button[@class='btn button lead-form-btn chk-prem-btn emp-var']")
                element19.click()

                # Step 20: Add random delay
                delay = random.uniform(15, 20)
                time.sleep(delay)

                df.at[index,'checker'] = "true"
                df.at[index,'laptop'] = "PC429"
                print("row {index} processed successfully")
                save_ip(new_ip,gmail = row['Email'],phone = row['Mobile'])
           
            except Exception as e:
                print(f"Error processing row {index}: {e}")
                df.at[index, 'checker'] = "false"
                df.at[index,'laptop'] = "PC429"

            finally:
                browser.quit()           
        else:
            print(f"Checker is not false or could not be changed.skipping row {index}")
            df.at[index, 'checker'] = "false"
            df.at[index,'laptop'] = "PC429"

    else:
        results.append(f"Checker is already true or could not be changed.skipping row {index}")       

    df.to_csv('./icici.csv',index=False)


with open('results.json', 'w') as f:
    json.dump(results, f)