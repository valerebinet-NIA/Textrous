<!DOCTYPE html>
<html style="height:100%">
<head>
<link rel="stylesheet" type="text/css" href="t.css"/>
</head>
<body style="height:100%">

<div style="width:1000px;height:100px;position:absolute;left:0;top:0;overflow:hidden;background-color:#617f10">
	<img style="position:absolute;top:5px;left:45px" src="logo2.bmp" height=90px>
	<ul id="main-nav">
		<li id="main-navli"><a id="main-navli" href="query.php">Home</a></li>
		<li id="main-navli"><a id="main-navli" href="features.php">Features</a></li>
		<li id="main-navli"><a id="main-navli" href="#"><u>Tutorial</u></a></li>
		<li id="main-navli"><a id="main-navli" href="about.php">About</a></li>
		<li id="main-navli"><a id="main-navli" href="contact.php">Contact</a></li>
	</ul>
</div>

<div style="width:1000px;height:50px;position:absolute;left:0;top:100px;overflow:hidden;background-color:#7A991A"> 
	<h1 style="color:#FFFFFF;margin:0;padding:5px;font-family:Verdana,Geneva,sans-serif;position:absolute;left:50px">SEARCH</h1>
	<p> 
		<form style="position:absolute;left:500px;top:25%" name = "input" action = "client.cgi" method="GET">
		<input type="text" id="text" name ="genes">
		<input type="submit" id="submit" value="Submit">
		</form> 
	</p>
</div>

<div style="width:1000px;position:absolute;left:0px;top:150px;bottom:10px;overflow:auto;background-color:#EEEEEE">
	<div style="width:700px;height:100%;position:absolute;left:150px;top:0px;bottom:10px;overflow:auto:background-color:#FFFFFF">
	<h3>Finding related words to your gene set</h3>
	<hr />
	<p style="text-indent:50px">Either type official gene symbols delimited by whitespace into the search bar above, or copy and paste the gene symbols from an excel spreadsheet. <i>Textrous!</i> is not case sensitive, and all non-alphanumeric characters will be removed from your query. Click on the Submit button to view the results.</p>

	<h3>Interpreting the results </h3>
	<hr />
	<p style="text-indent:50px">Once you click Submit, a new navigation bar will appear underneath the search bar. Click on Table (Cosine), Table (Z-Scores), Table (p-Values), Hierarchical Cloud, or Heat Map to access the appropriate features. The cosine similarity between a gene set and a word is directly proportional to the relevance of that word. Z-Scores are determined from the cosine similarities, and are defined by the number of standard deviations away from the mean (negative for below, positive for above). Finally, p-Values are equal to the probability that searching a random gene will produce a result as extreme as the Z-scores obtained by your gene set.</p>
	<p style="text-indent:50px">For hierarchical clouds, the size of words are proportional to their Cosine Similarity. The colors of words are proportional to the &ldquo;joins&rdquo; in agglomerative hierarchical clustering. The closer two words are, the more related they are. Refreshing the page will slightly change the layout.</p>
	<p style="text-indent:50px">For heat maps, grey-colored cells represent a low level of similarity. Blue-colored cells represent a high level of similarity, proportional to their opacity. To obtain fullscreen mode, click &ldquo;(fullscreen)&rdquo; on the top left corner of the heat map. </p>
	
	<h3>Obtaining phrases from words </h3>
	<hr />
	<p style="text-indent:50px"> To obtain phrases from words, simply click on any word on a table, hierarchical cloud, or heat map. Top phrases will be listed for you, sorted by cosine similarity. </p>
	
	<h3>Seeing omitted genes</h3>
	<hr />
	<p style="text-indent:50px"> Unfortunately, <i>Textrous!</i> is not able to find all genes in a large gene set, due to the relative obscurity of certain genes. The number of genes successfully found will be listed in the upper right corner of the screen, right of the Submit button. To see the names of genes omitted by the search process, click on the number of genes found. This action will send you to a page with a list of excluded genes. To return, click any item on the navigation bar, or press &ldquo;back&rdquo; on your browser.</p>
	
	<h3>Exporting genes</h3>
	<hr />
	<p style="text-indent:50px"> To export data, tables can be copied and pasted into excel. Heat maps and hierarchical clouds must be exported via screenshot. Zoom in and out by pressing Ctrl+ and Ctrl- on your keyboard, and capture the screen by pressing &ldquo;Print Screen&rdquo; on the keyboard. Paste the resulting image onto Powerpoint, MS Paint, or the software of your choice. </p>

	<h3>Locating sources</h3>
	<hr />
	<p style="text-indent:50px"> To locate the original articles containing returned phrases, click on the noun phrase. Since <i>Textrous!</i> is capable of finding indirect links and may occasionally produce false positives, such an article may or may not be found. </p>

	<h3>Searching a new set of genes </h3>
	<hr />
	<p style = "text-indent:50px">To search a new set of genes, repeat the process by typing the new set into the search bar.</p>
	</div>
</div>

</body>
</html>
