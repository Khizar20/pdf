import os
import requests
import zipfile
import io
import sys

def download_chromedriver():
    # Chrome version (using major version 137)
    chrome_version = "137.0.7151.104"
    major_version = chrome_version.split('.')[0]
    
    # Determine platform
    if sys.platform == "win32":
        platform = "win32"
        driver_name = "chromedriver.exe"
    else:
        platform = "linux64"
        driver_name = "chromedriver"
    
    # Download URL (using the latest version for Chrome 137)
    url = f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{chrome_version}/{platform}/chromedriver-{platform}.zip"
    
    print(f"Downloading ChromeDriver for Chrome version {chrome_version}...")
    
    try:
        # Download the zip file
        response = requests.get(url)
        response.raise_for_status()
        
        # Extract the zip file
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            # Extract chromedriver to the current directory
            zip_file.extract(f"chromedriver-{platform}/chromedriver.exe" if platform == "win32" else f"chromedriver-{platform}/chromedriver", 
                           os.path.dirname(os.path.abspath(__file__)))
            
            # Rename the file if needed
            extracted_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                        f"chromedriver-{platform}", 
                                        "chromedriver.exe" if platform == "win32" else "chromedriver")
            target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                     "chromedriver.exe" if platform == "win32" else "chromedriver")
            
            if os.path.exists(target_path):
                os.remove(target_path)
            os.rename(extracted_path, target_path)
            
            # Clean up the extracted directory
            os.rmdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"chromedriver-{platform}"))
        
        # Make the file executable on Unix-like systems
        if sys.platform != "win32":
            os.chmod(target_path, 0o755)
        
        print("ChromeDriver downloaded and extracted successfully!")
        
    except Exception as e:
        print(f"Error downloading ChromeDriver: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    download_chromedriver() 