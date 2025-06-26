import os
import sys
import requests
import zipfile
import io
import subprocess

def get_chrome_version():
    if sys.platform == "win32":
        try:
            output = subprocess.check_output(
                'reg query "HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon" /v version',
                shell=True
            ).decode()
            version = output.strip().split()[-1]
            return version
        except:
            return None
    return None

def download_chromedriver():
    chrome_version = get_chrome_version()
    if not chrome_version:
        print("Could not determine Chrome version")
        return False
    
    # Extract major version
    major_version = chrome_version.split('.')[0]
    
    # Download the latest matching version
    url = f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{chrome_version}/win64/chromedriver-win64.zip"
    
    try:
        print(f"Downloading ChromeDriver for Chrome version {chrome_version}...")
        response = requests.get(url)
        response.raise_for_status()
        
        # Extract the zip file
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            # Extract chromedriver.exe to the tests directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            zip_file.extract("chromedriver-win64/chromedriver.exe", current_dir)
            
            # Move the file to the correct location
            os.rename(
                os.path.join(current_dir, "chromedriver-win64", "chromedriver.exe"),
                os.path.join(current_dir, "chromedriver.exe")
            )
            
            # Clean up the extracted directory
            os.rmdir(os.path.join(current_dir, "chromedriver-win64"))
        
        print("ChromeDriver setup completed successfully!")
        return True
    except Exception as e:
        print(f"Error setting up ChromeDriver: {str(e)}")
        return False

if __name__ == "__main__":
    download_chromedriver() 