<h1>Project</h1>

<h2><strong>School project to emulate Airbnb</strong></h2>

<p>To emulate Airbnb as closely as possible, we need to collect tourism-related data. We must use open datas from https://www.data.gouv.fr/
<br>
To meet this requirement, we are using DATAtourisme, an API that aggregates tourims-related data.
<br>
Here are the API documentation links:
<br>
https://api.datatourisme.fr/v1/docs
<br>
https://api.datatourisme.fr/v1/swagger/</p>
<br>

<h2><strong>How to get an API's KEY</strong></h2>
<h3>Authentication Key Acquisition</h3>
<br>
<p>Get your key at https://info.datatourisme.fr/utiliser-les-donnees
<br>
The API uses a unique authentication key to secure requests. You can provide this key in two ways.
<br>
<br>
<em>Method 1: HTTP Header (Recommended)</em>
<br>
Include the key in the X-API-Key header of your request.
<br>
<code>X-API-Key: your_unique_api_key</code>
<br>
<br>
<em>Method 2: Query Parameter</em>
<br>
Add the key as the api_key parameter in the URL of your request.
<br>
<code>GET /v1/catalog?api_key=your_unique_api_key</code></p>


<h2><strong>How to use the API's KEY</strong></h2>
<br>
<p>Create a .env file in the root of your project, then add this variable : <code>API_KEY=your_unique_api_key</code></p>
