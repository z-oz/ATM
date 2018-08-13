'''A simple program to create an html file froma given string,
and call the default web browser to display the file.
https://anh.cs.luc.edu/python/hands-on/3.1/handsonHtml/webtemplates.html'''

contents = '''<!DOCTYPE html>
<html lang="en">
<head>
<title>ATM Receipt</title>
<meta charset="utf-8">
<style>
.p {
	margin-left: 6em;
}
.p1 {
	padding: 0.5em;
}
h2 {
	margin-left: 2.5em;
}
td { 
	padding: 0.5em;
	/*border: 1px solid black;*/
}
.len {
	margin-left: 0;
	width: 25%;
}
</style>
</head>
<body>
	<main>
	<h2>BANK ATM</h2>
	<p class="p1">114 W.Schamburg Rd, Schaumburg 60193 IL</p>
	<p class="p">(847)354-9942</p>
	<table>
		<tr>
			<td>DATE : </td>
			<td>xxxxxxxxxxxxxx</td>
		</tr>
		<tr>
			<td>TIME : </td>
			<td>xxxxxxxxxxxxxx</td>
		</tr>
		<tr>
			<td>CARD NUMBER : </td>
			<td>xxxxxxxxxxxxxx</td>
		</tr>
		<tr>
			<td>CARDHOLDER : </td>
			<td>xxxxxxxxxxxxxx</td>
		</tr>
		<tr>
			<td>TRANSACTION : </td>
			<td>xxxxxxxxxxxxxx</td>
		</tr>
		<tr>
			<td>PREVIOUS BALANCE : </td>
			<td>xxxxxxxxxxxxxx</td>
		</tr>
		<tr>
			<td>CURRENT BALANCE : </td>
			<td>xxxxxxxxxxxxxx</td>
		</tr>
	</table>
	<p class="p1">-------Thankyou For Choosing Our Bank-------</p>
	</main>
</body>
</html>

'''

def main():
    browseLocal(contents)

def strToFile(text, filename):
    """Write a file with the given name and the given text."""
    output = open(filename,"w")
    output.write(text)
    output.close()

def browseLocal(webpageText, filename='tempBrowseLocal.html'):
    '''Start your webbrowser on a local file containing the text
    with given filename.'''
    import webbrowser, os.path
    strToFile(webpageText, filename)
    webbrowser.open("file:///" + os.path.abspath(filename))

main()
