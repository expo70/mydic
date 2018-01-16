MyDic
=====

A private word dictionary on the Web

Installation
------------
	1. Change 'USER' and 'PASS' strings in mydic-cgi.py into your MongoDB account.
	2. Then,
		$ cp mydic-cgi.py /your_server/cgi-bin/mydic.cgi
		$ cp mydic.html /your_server/html_dir/mydic.html
		$ cp loading.gif /your_server/image_dir/loading.gif

	3. Open mydic.html in a Web browser.

Requirements
------------
	* MongoDB
	* PyMongo
