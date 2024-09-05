import requests
import os

# Base URL for the API
base_url = "http://192.168.144.25:82//cgi-bin/media.cgi"

# Define the directories and media list endpoints
directories_endpoint = "/api/v1/getdirectories"
medialist_endpoint = "/api/v1/getmedialist"

# Define the media type (0 for images, 1 for videos)
media_type = 0  # Change to 1 for videos if needed

# Directory where the images will be saved locally
save_directory = "downloaded_images"
os.makedirs(save_directory, exist_ok=True)

# Step 1: Request the directories
def get_directories():
    url = f"{base_url}{directories_endpoint}"
    params = {
        "media_type": media_type
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200 and response.json().get('success'):
        directories = response.json().get('data', {}).get('directories', [])
        return directories
    else:
        print(f"Error getting directories: {response.json().get('message', 'Unknown error')}")
        return []

# Step 2: Request the media files in each directory
def get_media_list(path, start=0, count=10):
    url = f"{base_url}{medialist_endpoint}"
    params = {
        "media_type": media_type,
        "path": path,
        "start": start,
        "count": count
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200 and response.json().get('success'):
        media_list = response.json().get('data', {}).get('list', [])
        return media_list
    else:
        print(f"Error getting media list: {response.json().get('message', 'Unknown error')}")
        return []

# Step 3: Download and save images from URLs
def download_image(name, url):
    response = requests.get(url)
    if response.status_code == 200:
        file_path = os.path.join(save_directory, name)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Image {name} saved successfully at {file_path}")
    else:
        print(f"Failed to download {name}")

# Main function to request directories, get media list, and download images
def main():
    directories = get_directories()
    
    if directories:
        for directory in directories:
            print(f"Fetching images from directory: {directory['name']}")
            media_list = get_media_list(directory['path'])
            
            for media in media_list:
                image_name = media['name']
                image_url = media['url']
                download_image(image_name, image_url)
    else:
        print("No directories found or error in fetching directories.")

# Execute the main function
if __name__ == "__main__":
    main()
