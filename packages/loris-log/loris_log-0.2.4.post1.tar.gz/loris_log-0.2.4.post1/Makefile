unittest:
	python -m coverage run -m unittest
	python -m coverage html -i

example:
	python example/example.py 

pdoc:
	pdoc ./loris_log/boto3Client.py ./loris_log/customLog.py ./loris_log/ftpClient.py ./loris_log/myException.py --no-show-source -o ./doc

.IPHONY: unittest example pdoc