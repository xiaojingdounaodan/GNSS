import sys
import pycurl
argv = ["https://cddis.nasa.gov/archive/doris/data/cs2/2017/", "cs2rx17001.001.Z"]
# Set the archiveLocation to the first command line argument
archiveLocation = argv[0]

# Set the fileName to the second command line argument
fileName = argv[1]

# Initialize the cURL connection object
curl = pycurl.Curl()

# Define the url to use
curl.setopt(curl.URL, archiveLocation + fileName)

# Set curl to follow redirects, needed to allow user login
curl.setopt(curl.FOLLOWLOCATION, True)

# Set the requirement that cURL use a netrc file found in users home directory
curl.setopt(curl.NETRC, 2)

# Set the file used to store cookie
# curl.setopt(curl.COOKIEJAR, '.cddis_cookies')
post = "username=littlebird&pwd=Zhang-chao1"
# curl.setopt(curl.CURLOPT_POSTFIELDS, post)
curl.setopt(curl.COOKIEJAR, '.cddis_cookies')

# Writes the remote file to a new file with the same name
with open(fileName, 'wb') as f:
    curl.setopt(curl.WRITEFUNCTION, f.write)
    curl.perform()

# Clean up and close the cURL object
curl.close()
