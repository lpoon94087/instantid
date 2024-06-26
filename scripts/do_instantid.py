from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import random
import time
import os
import shutil
import exiftool
import sys
import requests
import json
import subprocess
from datetime import datetime
from character import generate_random_character
from character import generate_hairstyle_prompt

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-setuid-sandbox")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")

# Define function to return random style+prompt
def get_random_prompt():
    if len(prompts) == 0:
        return generate_random_character()
    else:
        random_prompt = random.choice(prompts)

    if random_prompt.startswith("func:"):
          # The text starts with "func:"
        function_name = random_prompt.split(":")[1]  # Extract the function name after colon
        print(f"Function name: {function_name}")
        random_prompt = call_function_str(function_name)
    random_style = random.choice(styles)
    combine = random_style.format(prompt=random_prompt)
    return combine


def call_function_str(func_str):
    """calls the function given name of function.

    Args:
      func_str: A string containing the function name.

    Returns:
      The result of calling the function, or None if the function is not found.
    """
    function_name = func_str

    # Check if the function exists as a global variable (not recommended for large projects)
    if globals().get(function_name):
        # Call the function if it exists
        function = globals().get(function_name)
        return function()
    else:
        print(f"Function '{function_name}' not found.")
        exit()


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        names = data.get('names', [])
        prompts = data.get('prompts', [])
        styles = data.get('styles', [])
        poses = data.get('poses', [])
        img_namespace = data.get('img_namespace')
        return {
            'names': names,
            'prompts': prompts,
            'styles': styles,
            'poses': poses,
            'img_namespace': img_namespace
        }

def copy_with_sequence(source_file, destination_dir):
    """
    Copies a file to the destination directory with an increasing sequence 
    number if a file with the same name already exists.

    Args:
        source_file (str): Name of file to copy.
        destination_dir (str): Path to the destination directory.
    """
    base, ext = os.path.splitext(source_file)  # Split filename and extension
    i = 1
    new_filename = f"{base}{i}{ext}"
    destination_path = os.path.join(destination_dir, new_filename)

    while os.path.exists(destination_path):
        i += 1
        new_filename = f"{base}{i}{ext}"
        destination_path = os.path.join(destination_dir, new_filename)

    src_file_full_path = download_dir + "/" + source_file
    print(f"Copied '{src_file_full_path}' to '{destination_path}'")
    shutil.copy(src_file_full_path, destination_path)

def get_image_next_sequence_name(file_name, destination_dir):
    """
    Return a file name in the destination directory 
    with an increasing sequence number if a file with the same name already exists.

    Args:
        name (str): Name of file_name.  , such as "image.png"
        destination_dir (str): Path to the destination directory.
    """
    base, ext = os.path.splitext(file_name)  # Split filename and extension
    i = 1
    new_filename = f"{base}{i}{ext}"
    destination_path = os.path.join(destination_dir, new_filename)

    while os.path.exists(destination_path):
        i += 1
        new_filename = f"{base}{i}{ext}"
        destination_path = os.path.join(destination_dir, new_filename)

    # This file does not exist and can be used
    return destination_path


def add_metadata_to_png(input_file, metadata):
    with exiftool.ExifTool() as et:
        # Prepare the metadata in the correct format
        tags = {}
        for key, value in metadata.items():
            tags[f'PNG:{key}'] = value

        # Add metadata to the file
        et.execute(*[f'-{k}={v}' for k, v in tags.items()], input_file)
    
def sleep_with_progress(seconds):
    for _ in range(seconds):
        sys.stdout.write('.')
        sys.stdout.flush()  # This is the key! It forces Python to write the output immediately
        time.sleep(1)  # Sleep for 1 second
    print()  # Add a newline at the end
    
def get_image_url():
    """Fetch the image URL of the image container.   If the container is not available return empty string.
    """
    # Try to Locate image container
    try:
        image_container = driver.find_element(By.XPATH, image_container_element)
        innerHTML = image_container.get_attribute("innerHTML")
        # Extract the image URL
        start_index = innerHTML.find('src="') + 5  # Skip "src="
        end_index = innerHTML.find('"', start_index)  # Find the closing quote
        image_url = innerHTML[start_index:end_index]
        print(f"Image URL: {image_url}")
        return image_url

    except NoSuchElementException:
        print("image container not available")
        return ""
    
def download_image(file_name, imageurl):
    response = requests.get(imageurl)
    with open(file_name, "wb") as f:
        f.write(response.content)
    print(f"Image {imageurl} saved to {file_name}")

def get_element_with_wait(driver, by, value):
    while True:
        try:
            return driver.find_element(by, value)
        except NoSuchElementException:
            print(f"Element {value} not found, waiting...")
            sleep_with_progress(5)

def check_and_convert_to_png(file_path):

    # Check if the file exists
    if os.path.isfile(file_path):
        return
    
    # Get the directory and base name of the file
    directory, file_name = os.path.split(file_path)
    
    # Construct the output file path with .png extension
    base_name = os.path.splitext(file_name)[0]
    output_file = os.path.join(directory, f"{base_name}.png")
    input_file = os.path.join(directory, f"{base_name}.jpg")

    # Run the magick command to convert the file to PNG
    try:
        subprocess.run(["magick", input_file, output_file], check=True)
        print(f"Converted {input_file} to {output_file}.")
        sleep_with_progress(5)
    except subprocess.CalledProcessError as e:
        print(f"Failed to convert {file_path} to PNG. Error: {e}")

def get_date_tag():
    """
    Return the date tag as day/month/hour/minute
    such as 07241212
    """
    return datetime.now().strftime("%m%d%H%M")

def get_config_tag(config_path):
    """
    Return a base name of the config file: cfg_xyz.json => xyz
    """
    # Construct the get the name part of file
    some_name = os.path.splitext(config_path)[0]
    cfg_name = some_name.replace("cfg_", "")
    return cfg_name

def create_dated_directory(directory_name):
    """ 
    Create a directory if one does not exist
    """
    try:
        os.makedirs(directory_name)
        print(f"Directory {directory_name} created successfully.")
    except FileExistsError:
        print(f"Directory {directory_name} already exists.")
    except Exception as e:
        print(f"An error occurred while creating the directory: {e}")
    return directory_name

def get_circular_index(arr, idx):
    """
    This function takes an array and an index and returns a new index 
    following a circular pattern.

    Args:
        arr: The input array.
        idx: The starting index.

    Returns:
        The new circular index.
    """
    array_length = len(arr)
    new_idx = (idx + 1) % array_length
    return new_idx

def get_image_path_from_name(name):
    image_path = img_dir + name + "_main.png"
    return image_path

# Check if all names (images) exist
def check_names():
    for name in names:
        image_path = get_image_path_from_name(name)
        check_and_convert_to_png(image_path)


# ----------------------------------------------------------------------------------
# PROGRAM BEGIN
# ----------------------------------------------------------------------------------

# default site: openxlab
site = 'openxlab'

# Check if there are command-line arguments passed, else print usage
if len(sys.argv) > 1:
    config_file = sys.argv[1]
    if len(sys.argv) > 2:
        site = sys.argv[2]
else:
    print(f"Usage: python {sys.argv[0]} [config.json] (site, huggingface or openxlab")
    print("Where config.json consists of arrays of names, prompts and styles")
    exit()
    
# Set up XPATHs of elements
if site == 'openxlab':
    target_url = "https://openxlab.org.cn/apps/detail/InstantX/InstantID"
    text_element = '//*[@id="component-7"]/label/textarea'
    dropdown_arrow_element = '//*[@id="component-9"]/label/div/div[1]/div/div'
    dropdown_element = '//*[@id="component-9"]/label/div/div/div/input'
    submit_button_element = '//*[@id="component-8"]'
    input_image_element = '//*[@id="component-5"]/div[2]/div/button/input'
    pose_image_element = '//*[@id="component-6"]/div[2]/div/button/input'
    image_container_element = '//*[@id="component-23"]/button/div'
    
elif site == 'huggingface':
    target_url = "https://huggingface.co/spaces/InstantX/InstantID"
    text_element = '//*[@id="component-8"]/label/textarea'
    dropdown_arrow_element = '//*[@id="component-11"]/label/div/div[1]/div/div'
    dropdown_element = '//*[@id="component-11"]/label/div/div/div/input'
    submit_button_element = '//*[@id="component-9"]'
    input_image_element = '//*[@id="component-6"]/div[2]/div/button/input'
    pose_image_element = '//*[@id="component-7"]/div[2]/div/button/input'
    image_container_element = '//*[@id="component-32"]/button/div'

else:
    print("Unknown site: " + site)
    exit()

print("config file: " + config_file)
config = read_json_file(config_file)
prompts = config['prompts']
styles = config['styles']
names = config['names']
poses = config['poses']
img_namespace = config['img_namespace']
if img_namespace == None:
    img_namespace = "id"

# Printing the variables to verify their contents
print("Names:", names)
print(f"Number of Prompts: {len(prompts)}")
print(f"Number of Styles: {len(styles)}")
print("Target URL: " + target_url)


name_index = random.randrange(len(names))

# Program director 
prog_dir = "/Users/lpoon/instantDownload/"
img_dir = prog_dir + img_namespace + "/"
print("img dir: " + img_dir)

check_names()

# Set up the download directory
date_tag = get_date_tag()
cfg_tag = get_config_tag(config_file)
download_name = f"run_{cfg_tag}_{date_tag}"
create_dated_directory(download_name)  # Update this path to your desired download directory
download_dir = prog_dir + download_name
print("download dir: " + download_dir)

prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

# Initialize the WebDriver (using Chrome in this example)
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the target URL
    driver.get(target_url)

    # Need to resize to make sure elements are visible
    driver.set_window_size(1900, 1200)

    # Wait for the page to load completely
    sleep_with_progress(seconds=15)  # You may need to adjust the sleep time depending on your internet speed

    frame = driver.find_element(By.XPATH, '//iframe')
    # Wait until the frame is present and visible
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it(frame)
    )

    # Wait for the file upload to complete
    sleep_with_progress(seconds=5)  # Adjust as necessary

    # Locate the text input element (assuming it's the first input of type text)
    text_input = driver.find_element(By.XPATH, text_element)

    # Select the dropdown style to No style (up 1 from Watercolor)
    dropdown_arrow = driver.find_element(By.XPATH, dropdown_arrow_element)
    dropdown_arrow.click()
    dropdown = driver.find_element(By.XPATH, dropdown_element)
    dropdown.send_keys(Keys.ARROW_UP)
    dropdown.send_keys(Keys.ENTER)

    # Locate the submit button (assuming a button element)
    submit_button = get_element_with_wait(driver, By.XPATH, submit_button_element)

    prev_image_url = get_image_url()
    prev_name = ""
    prev_pose = ""

    # failed timeout count
    failed_time_out_count = 0

    # Loop to submit many times
    for i in range(1000):

        # Path to the image file you want to upload
        name_index = get_circular_index(names, name_index)
        name = names[name_index]
        image_path = get_image_path_from_name(name)
        check_and_convert_to_png(image_path)
        pose = random.choice(poses)
        pose_path = img_dir + pose

        print(f"Generate image number {i + 1} : {name} {pose} ...")

        if prev_name != name:
            # Locate the file input element (first input field)
            file_input = get_element_with_wait(driver, By.XPATH, input_image_element)
            # Upload the image file
            file_input.send_keys(image_path)
        prev_name = name

        if prev_pose != pose:
            # Locate the pose input file element
            pose_input = get_element_with_wait(driver, By.XPATH, pose_image_element)
            # Uploadthe pose image file
            pose_input.send_keys(pose_path)
        prev_pose = pose

        # Randomly select one of the prompts and enter
        selected_prompt = get_random_prompt()
        print("Prompt: " + selected_prompt)
        text_input.clear()
        text_input.send_keys(selected_prompt)

        # Give some time to upload
        sleep_with_progress(seconds=15)

        # Click submit!!! and cross fingers
        submit_button.click()

        # Scroll to top
        driver.switch_to.default_content()
        driver.execute_script("window.scrollTo(0, 0);")
        driver.switch_to.frame(frame)
        sleep_with_progress(seconds=50)  # Wait for generation
        time_taken = 50

        # Addition wait/sleep until image urls are different
        while True:
            image_url = get_image_url()
            if image_url != prev_image_url:
                break;
            # inner HTML has not changed, sleep for another 10 seconds
            print("image has not yet changed, sleeping for another 10 seconds...")
            sleep_with_progress(seconds=10)
            time_taken += 10
            if time_taken > 60*10:
                print(f"Image generation time exceeded! Failed count: {failed_time_out_count}")
                failed_time_out_count += 1
                break
        print(f"Time taken: {time_taken} seconds")

        # If too many timeouts, sleep for an hour
        if failed_time_out_count > 2:
            print("Sleeping for an hour")
            sleep_with_progress(60 * 60)
            failed_time_out_count = 0
            continue
        #

        # Download only if image url changed
        if image_url != prev_image_url:
            destination_dir = download_dir
            output_file = name + "_" + cfg_tag + "_" + date_tag + ".png"
            image_file = get_image_next_sequence_name(output_file, destination_dir)
            download_image(image_file, image_url)

            # Add metadata to image file
            metadata = {
                'Artist': 'Laurie Poon',
                'Source': image_url,
                'Description': selected_prompt
            }
            add_metadata_to_png(image_file, metadata)

        prev_image_url = image_url

finally:
    # Close the WebDriver
    driver.quit()
