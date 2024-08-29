from bs4 import BeautifulSoup  # Library for parsing HTML documents
import termcolor as tc  # Library for colored terminal output
import requests  # Module for sending HTTP requests
import random # to generate random values
import sys  # Module for system-specific parameters and functions
import os  # Module for interacting with the operating system

# GitHub website URL template
GITHUB_WEBSITE_URL = 'https://github.com/{}'

# ====================================== Function to download the page HTML =================================================
def get_page(page: str) -> BeautifulSoup:
  """
  Sends a GET request to the specified GitHub page and returns the parsed HTML content.

  Args:
    page (str): The URL of the GitHub page.

  Returns:
    BeautifulSoup: Parsed HTML content of the page.
  """
  try:
    # Perform a GET request to the page
    response = requests.get(page)

    # Check if the response status code is not 200 (OK)
    if response.status_code != 200:
      # Print an error message in red if the status code is not 200
      tc.cprint(f"Error ->\nRequest GET {page}\nResponse STATUS_CODE {response.status_code}", 'light_red')
      # Exit the script with code 1 (indicating an error)
      sys.exit(1)
    else:
      # Parse and return the HTML content using BeautifulSoup with the 'lxml' parser
      lxml_parsed_html_content = BeautifulSoup(response.content, 'lxml')
      return lxml_parsed_html_content

  except requests.ConnectionError as err:
    # Handle connection errors (e.g., no internet connection)
    tc.cprint("Please check your internet connection!\n", 'light_red')
    tc.cprint(err, 'light_red')


# ====================================== Function to extract profile data from the HTML ======================================
def load_profile_data(content: BeautifulSoup) -> dict:
  """
  Extracts important data from the GitHub profile page content.

  Args:
    content (BeautifulSoup): Parsed HTML content of the GitHub profile page.

  Returns:
    dict: A dictionary containing the profile data (name, username, repos count, followers, following, location, bio).
  """
  # Get the full name of the user
  name_tag = content.find("span", {'class': 'p-name vcard-fullname d-block overflow-hidden'})
  name = name_tag.text.strip() if name_tag else "Name not found!"

  # Get the username of the user
  username_tag = content.find("span", {"class": "p-nickname vcard-username d-block"})
  username = username_tag.text.strip() if username_tag else 'Username not found!'

  # Get the bio of the user
  bio_tag = content.find("div", {'class': "p-note user-profile-bio mb-3 js-user-profile-bio f4"})
  bio = str(bio_tag['data-bio-text']).strip() if bio_tag else 'Bio not found!'

  # Get the count of public repositories
  repos_count_tag = content.find("span", {"class": "Counter"})
  repos_count = repos_count_tag.text.strip() if repos_count_tag else 'Repos count not found!'

  # Get the location of the user
  location_tags = content.findAll('span', {'class': "p-label"})
  location = location_tags[0].text.strip() if location_tags and len(location_tags) > 1 else "Location not found!"

  # Get the followers count
  followers_tag = content.find("a", {"href": f"https://github.com/{username}?tab=followers"})
  followers = followers_tag.find("span").text.strip() if followers_tag else "Followers count not found!"

  # Get the following count
  following_tag = content.find("a", {"href": f"https://github.com/{username}?tab=following"})
  following = following_tag.find("span").text.strip() if following_tag else "Following count not found!"

  # Return the extracted data as a dictionary
  return {
    "name": name,
    "username": username,
    "repos-count": repos_count,
    "followers": followers,
    "following": following,
    "location": location,
    "bio": bio
  }


# ====================================== Function to display profile data ======================================
def display_profile_data(data: dict):
  """
  Displays the extracted GitHub profile data in a formatted way, optionally using ASCII templates.

  Args:
    data (dict): A dictionary containing the profile data.
  """
  name = data['name'] if data['name'] else 'not found'
  username = data['username'] if data['username'] else 'not found'
  repos_count = data['repos-count'] if data['repos-count'] else 'not found'
  followers = data['followers'] if data['followers'] else 'not found'
  following = data['following'] if data['following'] else 'not found'
  location = data['location'] if data['location'] else 'not found'
  bio = data['bio'] if['bio'] else 'not found'

  # Check if the ASCII templates directory exists || and if its not empty
  if os.path.exists("./ascii-templates") and os.path.isdir("./ascii-templates") and len(os.listdir('./ascii-templates')) > 0:
    # Try to load the appropriate ASCII template based on the first letter of the name
    try:
      # will open a random ascii template and then read it
      with open(f'./ascii-templates/{random.choice(os.listdir('./ascii-templates'))}', 'rb') as ascii_template_file:
        ascii_template = str(ascii_template_file.read().decode())
      ascii_template_file.close()

      # Format the ASCII template with the user's profile data
      ascii_template = ascii_template.format(name, username, repos_count, followers, following, location, bio)
      # display the formatted ASCII Template
      tc.cprint(ascii_template, random.choice(['light_blue','light_magenta','light_red','light_yellow','light_green','cyan']))
    except FileNotFoundError:
      # Handle the case where the template file is not found
      tc.cprint(f"please make sure that u have  all the ascii templates!", 'light_red')
  else:
    # Prompt the user to download the ASCII templates if the directory is missing
    tc.cprint("Please download the ASCII templates from my GitHub repo: https://github.com/zinedine0014/git-fetch", 'light_red')


if __name__ == '__main__':
  # Check if the script was run with exactly one argument (GitHub username)
  if len(sys.argv) == 2:
    # Store the page content in a variable
    content = get_page(GITHUB_WEBSITE_URL.format(sys.argv[1]))
    # Load the profile data from the content
    data = load_profile_data(content)
    # Display the profile data
    display_profile_data(data)
  else:
    # Print usage instructions if the script is run without the correct number of arguments
    tc.cprint(f"Usage:\npython3 {sys.argv[0]} <github-username>", 'light_red')
