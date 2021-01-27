import pycurl
import cStringIO
import sys
argv = "https://cddis.nasa.gov/archive/doris/data/cs2/2017/"
# Set the archive directory to the command line argument
# archiveDirectory = sys.argv[1]
archiveDirectory = argv

# Initialize the response object for the directory listing
response = cStringIO.StringIO()

# Initialize the cURL python object
curl = pycurl.Curl()

# Set the cURL URL to the directory passed in with '*?list' added to get a directory listing
curl.setopt(curl.URL, archiveDirectory + '*?list')

# Tell cURL to follow redirects, needed to allow user login
curl.setopt(curl.FOLLOWLOCATION, True)

# Set the requirement that cURL use a .netrc file found in the users home directory
curl.setopt(curl.NETRC, 2)

# Set the file used to store the login cookie
curl.setopt(curl.COOKIEJAR, 'cookie.txt')

# Tell cURL to write the response from the cURL call to the response object
curl.setopt(curl.WRITEFUNCTION, response.write)

# Execute the cURL call
curl.perform()

# Get the text response and store it in a variable
output = response.getvalue()

# Split the output into lines, based on a new line character
lines = output.split('\n')

# Iterate over the lines of the listing
for line in lines:
    # Do not include the index.html file or some comments that are returned
    if ((('index.html') not in line) and (('#') not in line)):
        # Split the line so we have only the filename as a variable
        filename = line.split(' ')[0].strip()
        # Drop some blank lines that can occur
        if (len(filename) > 0):
            # Print the filename for logging purposes
            print(archiveDirectory + filename)
            # Set the cURL URL to a new URL, defined by the original directory + the filename from the listing
            curl.setopt(curl.URL, archiveDirectory + filename)

            # Open a new file on the local host, with the filename calculated above
            fpointer = open(filename, 'wb')

            # Tell cURL to write this response to a file
            curl.setopt(curl.WRITEFUNCTION, fpointer.write)

            # Execute this cURL command
            curl.perform()

# Clean up and close the cURL object
curl.close()
