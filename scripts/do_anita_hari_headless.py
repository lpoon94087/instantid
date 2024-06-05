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

# Set up the download directory
download_dir = os.path.abspath("/Users/lpoon/Downloads")  # Update this path to your desired download directory
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

# Path to the image file you want to upload
name = "anita"
image_path = "/Users/lpoon/instantDownload/" + name + "_main.jpg"
pose_path = "/Users/lpoon/instantDownload/nancy_main.jpg"

def generate_hairstyle_prompt():
    shot_types = ["closeup", "profile view", "three-quarter view", "overhead shot"]
    hair_types = ["curly", "straight", "wavy", "coily", "kinky", "fine", "thick"]
    hair_lengths = ["short", "medium", "long", "pixie cut", "shoulder-length"]
    hair_colors = ["jet black", "auburn"]
    hair_styles = [
        "bob", "asymmetrical cut", "undercut", "pompadour", "bun", "braids",
        "dreadlocks", "bangs", "side part", "top knot", "shag"
    ]
    hair_textures = ["", "silky", "frizzy", "smooth", "voluminous", "sleek"]
    styling_elements = ["", "highlights", "lowlights"]

    prompt = (
        f"Asian female, {random.choice(shot_types)}, "
        "high-resolution portrait, "
        f"{random.choice(hair_types)} hair, {random.choice(hair_lengths)} length, "
        f"{random.choice(hair_colors)}, {random.choice(hair_styles)}, "
        f"{random.choice(hair_textures)}, {random.choice(styling_elements)}, "
        "professional photography, studio lighting, fashion magazine aesthetic"
    )
    return prompt


# Define function to return random style+prompt
def get_random_prompt():
    """
    random_prompt = random.choice(prompts)
    random_style = random.choice(styles)
    combine = random_style.format(prompt=random_prompt)
    return combine
    """
    return generate_hairstyle_prompt()

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
        image_container = driver.find_element(By.XPATH, '//*[@id="component-23"]/button/div')
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


# Initialize the WebDriver (using Chrome in this example)
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the target URL
    driver.get("https://openxlab.org.cn/apps/detail/InstantX/InstantID")

    # Need to resize to make sure elements are visible
    driver.set_window_size(1900, 1200)

    # Wait for the page to load completely
    sleep_with_progress(seconds=5)  # You may need to adjust the sleep time depending on your internet speed

    frame = driver.find_element(By.XPATH, '//iframe')
    # driver.switch_to.frame(frame)
    # Wait until the frame is present and visible
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it(frame)
    )

    # Locate the file input element (first input field)
    #file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
    file_input = get_element_with_wait(driver, By.CSS_SELECTOR, 'input[type="file"]')

    # Upload the image file
    file_input.send_keys(image_path)

    # Locate the pose input file element
    pose_input = get_element_with_wait(driver, By.XPATH, '//*[@id="component-6"]/div[2]/div/button/input')
    pose_input.send_keys(pose_path)

    # Wait for the file upload to complete
    sleep_with_progress(seconds=5)  # Adjust as necessary

    # Locate the text input element (assuming it's the first input of type text)
    text_input = driver.find_element(By.XPATH, '//*[@id="component-7"]/label/textarea')

    # Randomly select one of the prompts and enter
    selected_prompt = get_random_prompt()
    print(selected_prompt)
    text_input.send_keys(selected_prompt)

    # Select the dropdown style to No style (up 1 from Watercolor)
    dropdown_arrow = driver.find_element(By.XPATH, '//*[@id="component-9"]/label/div/div[1]/div/div')
    dropdown_arrow.click()

    dropdown = driver.find_element(By.XPATH, '//*[@id="component-9"]/label/div/div/div/input')
    dropdown.send_keys(Keys.ARROW_UP)
    dropdown.send_keys(Keys.ENTER)
    sleep_with_progress(seconds=5)

    # Locate and click the submit button (assuming a button element)
    submit_button = get_element_with_wait(driver, By.XPATH, '//*[@id="component-8"]')

    # Wait to observe the result
    sleep_with_progress(seconds=10)  # Adjust as necessary

    prev_image_url = get_image_url()

    # Loop to submit many times
    for i in range(1000):
        submit_button.click()
        # Scroll to top
        driver.switch_to.default_content()
        driver.execute_script("window.scrollTo(0, 0);")
        driver.switch_to.frame(frame)
        print(f"Generation image number {i + 1}...")
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
            if time_taken > 60*5:
                print("Image generation time exceeded")
                break
        print(f"Time taken: {time_taken}")
        #
        prev_image_url = image_url


        """# Locate and click the download image button (assuming a button element)
        download_button = driver.find_element(By.XPATH, '//*[@id="component-23"]/div[2]/a/button')
        download_button.click()

        sleep_with_progress(seconds=5)
        """
        destination_dir = "/Users/lpoon/Downloads"
        source_file = name + ".png"
        image_file = destination_dir + "/" + source_file

        download_image(image_file, image_url)

        # Add metadata to image file
        metadata = {
            'Artist': 'Laurie Poon',
            'Source': image_url,
            'Description': selected_prompt
        }
        add_metadata_to_png(image_file, metadata)

        copy_with_sequence(source_file, destination_dir)

        # Randomly select one of the prompts and enter
        selected_prompt = get_random_prompt()
        print(selected_prompt)
        text_input.clear()
        text_input.send_keys(selected_prompt)

finally:
    # Close the WebDriver
    driver.quit()
