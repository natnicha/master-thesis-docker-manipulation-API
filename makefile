run:
	python .\__main__.py

server-run:
	cd .\server\ && flask run -p 6000

test:
	cd C:\Users\natni\Downloads\apache-jmeter-5.6.3\bin && jmeter -n -t "Thread Group.jmx"
