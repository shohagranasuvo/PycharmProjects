from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pickle
import time

# Path to your msedgedriver executable
msedgedriver_path = 'C:/Users/shoha/PycharmProjects/Whatsappautomaticrply/msedgedriver.exe'

# Initialize WebDriver for Edge
service = EdgeService(executable_path=msedgedriver_path)
driver = webdriver.Edge(service=service)
driver.get('https://web.whatsapp.com')

# Load cookies
try:
    with open('whatsapp_cookies.pkl', 'rb') as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
    driver.refresh()
    print("Cookies have been loaded.")
except FileNotFoundError:
    print("No cookies file found. Please run the save_cookies script first.")
    driver.quit()
    exit()

def check_for_new_messages():
    try:
        # Locate chat list items
        chat_list_items = driver.find_elements(By.CSS_SELECTOR, "div[aria-label='Chat list'] div[role='row']")

        for chat_item in chat_list_items:
            # Check if the chat item has an unread message indicator
            unread_indicator = chat_item.find_elements(By.CSS_SELECTOR, "span[aria-label*='unread message']")
            if unread_indicator:
                # Click on the chat item to open the chat
                chat_item.click()
                time.sleep(3)  # Wait for chat to open

                # Locate the chat input box using JavaScript to ensure it's focused
                chat_input = driver.find_element(By.XPATH, "//div[@contenteditable='true'][@data-tab='1']")
                driver.execute_script("arguments[0].focus();", chat_input)  # Focus on the input box
                time.sleep(1)  # Ensure input box is focused

                # Type the message
                chat_input.send_keys("Hi, how are you?")
                time.sleep(1)  # Wait a bit before sending

                # Send the message
                chat_input.send_keys(Keys.RETURN)

                print("Sent automated response.")
                time.sleep(2)  # Wait a bit before checking again
                break  # Only respond to one new message per check to avoid spamming

    except Exception as e:
        print(f"An error occurred: {e}")

# Main loop to keep checking for new messages
while True:
    check_for_new_messages()
    time.sleep(10)  # Check every 10 seconds
