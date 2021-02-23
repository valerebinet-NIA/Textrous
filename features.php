<!DOCTYPE html>
<html style="height:100%">
<head>
<link rel="stylesheet" type="text/css" href="t.css"/>
<script async type="text/javascript" id="_fed_an_ua_tag" src="https://dap.digitalgov.gov/Universal-Federated-Analytics-Min.js?agency=HHS&subagency=NIH-NIA"></script>
</head>
<body style="height:100%">

<div style="width:1000px;height:100px;position:absolute;left:0;top:0;overflow:hidden;background-color:#617f10">
	<img style="position:absolute;top:5px;left:45px" src="logo2.bmp" height=90px>
	<ul id="main-nav">
		<li id="main-navli" ><a id="main-navli" href="query.php">Home</a></li>
		<li id="main-navli" ><a id="main-navli" href="#"><u>Features</u></a></li>
		<li id="main-navli" ><a id="main-navli" href="tutorial.php">Tutorial</a></li>
		<li id="main-navli" ><a id="main-navli" href="about.php">About</a></li>
		<li id="main-navli" ><a id="main-navli" href="contact.php">Contact</a></li>
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
	<h3>Introduction</h3>
	<hr />
	<p style="text-indent:50px"><i>Textrous!</i> is a free web framework designed to automatically retrieve English words from a gene set. <i>Textrous!</i> aims to search "gene-documents", collections of genes and their associated literature based upon databases from PubMed, Jackson Laboratories, and the Online Mendelian Inheritance in Man. The algorithm behind <i>Textrous!</i> is latent semantic indexing, a technique used to discover the semantic structure of documents by examining statistical co-occurence patterns. As a result, <i>Textrous!</i> is capable of extracting both direct and indirect links between genes and words. </p>
	<h3>Features</h3>
	<hr />
	<p style="text-indent:50px">
		<ul>
			<li> <b>Different Methodologies</b> - We are capable of processing gene sets in two different ways: collectively and individually.</li>
			<li> <b>Collective Processing</b> - The features of every gene are combined into an "average" gene. Advantages: Nothing is discounted. Words that are not statistically significant for each respective gene may be significant for the gene set. Disadvantages: Sensitivity to outliers. </li>
			<li> <b>Individual Processing</b> - Every gene-word association is computed individually. Advantages: Outliers are accounted for. Disadvantages: Gene independence is assumed, which may not be true. </li>
			<li><b>Data Tables</b> - Shows the top related words to the <i>collectively processed</i> gene set, and their associated cosine similarity, z-score, or p-value.</li>
			<li><b>Hierarchical Cloud</b> - Shows the top related words to the <i>collectively processed</i> gene set in a word cloud/tree hybrid. Words are clustered with an agglomerative hierarchical clustering algorithm.</li>
			<li><b>Heat Map</b> - Shows the top related words to each <i>individually processed</i> gene. White cells and colored cells represent statistical non-significance and significance, respectively.</li>
			<li><b>Phrasing</b> - Shows the top phrases associated with a word, sorted by their association with your gene set. Only noun phrases are supported.</li>
		</ul>
	</p>
	<h3>Stopwords</h3>
	<hr />
	<p style="text-indent:50px"><i>Textrous!</i> uses a list of words excluded from the searching algorithm. To view the list, click <a href="gene2word/stoplist">here</a>.</p>
	<h3>Requirements</h3>
	<hr />
	<p style="text-indent:50px">Current versions of the following: Firefox, Google Chrome, Internet Explorer, Safari, Opera.</p>
	<p style="text-indent:50px">Copy-and-paste from Excel spreadsheets may not function with Internet Explorer.</p>

	</div>
</div>

</body>
</html>
