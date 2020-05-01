# IP-Backend
Backed for the IP project

# Prerequisites
Make sure Python, Pip and Django are installed. To install Django use the following command: pip3 install django

# Running the server
Open a terminal, navigate to the /IP-Backend/Server folder and run the following command: python3 manage.py runserver 0.0.0.0:8000
You can also open the project in PyCharm Professional Edition and click run after changing the address and port in the running configuration. 

The server is expected to run on http://0.0.0.0:8000/
Images in binary format can be retrieved with get requests and uploaded with put requests. 

Get requests for the images should be sent to http://0.0.0.0:8000/app/get/id  where id is the id of the image you want.

Get requests for interogating whether the image was retrieved so far or not should be sent to http://0.0.0.0:8000/app/poll/id
They will return 1 if it wasn't retrieved yet and 0 otherwise.

Put requests with the image in binary format should be sent to http://0.0.0.0:8000/app/put

All the images are stored locally in the /IP-Backend/Server/images folder.

OCR & Translate api prerequisites:
- set environment variables: GOOGLE_APPLICATION_CREDENTIALS="[PATH]\UnityAR-98ae3738e859.json" and GCLOUD_PROJECT=unityar-1584957126753
- run the following commands to install Google APIs: 

        - pip install --upgrade google-api-python-client
	
        - pip install --upgrade google-cloud-vision
	
        - pip install google-cloud-translate==2.0.0
		
- if any of the commands fail in windows due to acces error, add --user at their end. Example: pip install --upgrade google-api-python-client --user

# Further Steps
There is another README in ImageProcessing. Make sure to also follow the steps listed there.
