<h1> How this section works ?</h1>

<h2>Script</h2>

<p>First of all, you have to be at the root of the project otherwise it won't work. You have to install all the dependencies first with this line :<br>
<code>pip3 install -r requirements.txt</code>
<br><br></p>

<p>After the download completed, you have to run the script with this line :
<br>
<br>
<strong>Linux</strong>
<br>
<code>python3 -m data_download</code>
<br>
<br>
<strong>Windows</strong>
<br>
<code>python -m data_download</code>
</p>
<br>

<h2>Tree</h2>

<p><code>.
├── doc
│   ├── downloader # Folder containing all Python doc
│   │   ├── datatourisme_download.html
│   │   └── picture.html
│   ├── downloader.html
│   ├── index.html
│   └── search.js
├── downloader # Folder containing all Python scripts
│   ├── api_client.py
│   ├── checkpoint.py
│   ├── extractor.py
│   ├── picture.py # Download images from raw data
│   └── writer.py
├── __main__.py  # Entry point of the application
├── README.md
└── tests # Folder containign all Python tests
    ├── test_deployment_datatourisme_download.py
    └── test_unit_datatourisme_download.py
</code></p>

