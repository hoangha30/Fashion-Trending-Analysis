import instaloader
from datetime import datetime
import time
import os

# Initialize Instaloader
L = instaloader.Instaloader()

# Login to Instagram
L.login("jreef__", ".ha3072003tanh.")
# L.load_session_from_file("jreef__", filename="session-jreef__")

# Set main directory where all images will be saved
folder = "insta_hashtag_img"

# Create main folder if it doesn't exist
if not os.path.exists(folder):
    os.makedirs(folder)

# List of hashtags to download from
hashtags = [
    "mensstreetwear", "ootdmen", "cleanstyle", "cleanfit", "bestofstreetwear",
    "streetstyle", "streetwearfashion", "streetwearstyle", "fashionman", "mensfashion",
    "mensootd", "menoutfit", "menswearblogger", "menswear", "menswearfashion"
]

# Time limit: only get posts after October 1, 2024
DATE_LIMIT = datetime(2024, 10, 1)

# Process each hashtag
for tag_name in hashtags:
    try:
        print(f"→ Downloading from #{tag_name} ...")
        hashtag = instaloader.Hashtag.from_name(L.context, tag_name)
        count = 0
        
        # Create separate folder for each hashtag in the main folder
        hashtag_folder = os.path.join(folder, tag_name)
        if not os.path.exists(hashtag_folder):
            os.makedirs(hashtag_folder)
        
        # Get posts with this hashtag
        for post in hashtag.get_posts():
            # Check if post is after our date limit
            if post.date_utc > DATE_LIMIT:
                # Download post to the hashtag-specific folder
                L.download_post(post, target=hashtag_folder)
                count += 1
                
                # Optional: limit number of downloads per hashtag
                if count >= 50:  # Adjust this number as needed
                    break
        
        print(f"✔️  Completed: {count} images from #{tag_name}\n")
        time.sleep(15)  # Pause between hashtags to avoid being blocked
    except Exception as e:
        print(f"❌ Error processing #{tag_name}: {e}")
