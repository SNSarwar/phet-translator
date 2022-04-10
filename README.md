PHET Simulation Translation Tool User Guide 
Shomeek Sarwar

Google Doc link with screen shots: https://docs.google.com/document/d/1KVzf5iUOHVrBfmULAym-VFMeRNrYIJWbwhouIskYhF4/edit?usp=sharing 

Introduction
We have developed a software tool to help with easy translation of PHET simulation HTML pages to Bangla. This tool utilizes Google translation tools to automatically perform the translation task. It also provides the user with the functionality to edit, delete, or add to any translated text if the automatic translation fails to provide the desired Bangla text.
Description of the software package
We have built the software using the Python programming language. We have added a user interface (UI) for easy operation of the translation process. The main input to the tool is a valid PHET simulation file in HTML format that has been downloaded to the local disk (e.g., download https://phet.colorado.edu/sims/html/masses-and-springs/latest/masses-and-springs_en.html).

Building the software

NOTE: The tool requires python 3.9 or higher. Please use anaconda distribution for installing python
Download the code:
Clone the github repository https://github.com/SNSarwar/phet-translator.git
go to the folder

The tool consists of two python files and a requirements.txt file

phet_translator_tool.py 
g_trans.py
requirements.txt

Install the required packages (first time only)

Make sure to download all the required Python packages by running the command:
'pip3 install -r requirements.txt'

NOTE: It may take several minutes to install the packages.

How to use the software
Downloading a PHET File: 
First go to the PHET simulation file that you would like to translate. For example:
 https://phet.colorado.edu/sims/html/masses-and-springs/latest/masses-and-springs_en.html 

Save the HTML file to your disk by using: 
File → Save As as shown below (Make sure to select Webpage, HTML only option)



Once the file is saved (It will be saved in the download folder)



Run the PHET Translator Software
c:>python phet_translator_tool.py

It will create a web server and will print an url as shown below


You can start the tool by clicking on the printed URL, in this case http://127.0.0.1:8070/ 

Once the tool starts, it should look like:


Open the file to translate:
You can simply click on the box below the header and a open file dialog will appear, you can select the file and click open or “drag and drop” the file into the box.



Or drag and drop as shown below:



Then the html file will be analyzed and the necessary strings will be translated, it may take a few minutes depending on the Internet connection speed. The working indicator will flash.



Once the translation is done you should see the translated Table that looks like the following:





The table has three columns, out of which the first two have been extracted from the HTML file and the third column holds the translated text. The third column is completely editable. One can edit, delete, or add to the translations to make sure the translation is correct. Automatic translation may not always produce the correct or desired result.

Once done, just hit the Download button below to save the translated file.



The file is saved as translated_html_file.html and is never overwritten. The browser creates a new file every time it is downloaded. 
Here is an example of an automatically generated translation of the PHET simulation:



Editing translations
As can be seen from the following table, the automatic translator mistakenly translated ‘Masses and springs’ to ‘জনসাধারণ  এবং স্প্রিং‘ instead of the correct ‘ভর এবং স্প্রিং‘ this can easily be corrected as shown below:

Wrong:


corrected:


And the HTML File reflects the corrected input



