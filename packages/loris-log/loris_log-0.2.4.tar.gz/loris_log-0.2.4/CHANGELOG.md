# v0.0.1 (2023-09-06)

The initial release of beta version of python log library.

Features:
- Interface to communication with the AWS CloudWatch.
- Interface to the communication with the FTP server.
- Interface to push debug level log message.
- Interface to push info level log message.
- Interface to push fatal level log message.
- Interface to push error level log message.
- Interface to push embedded device data.


# v0.2.1 (2023-09-08)

The update had been done onto the library to improve the atomicity. 

Features:
- CloudWatch Interface update: enables user to choose the AWS CloudWatch interface that they wanted to connect with.
- FTP Server Interface update: enables user to choose the FTP server interface that they wanted to connect with.

# v0.2.2 (2023-09-25)

The update had been done to improve the stability

Update change:
- Improve documentation.
- Improve README.
- Correcting spelling mistakes.

# v0.2.2 (2023-10-02)

An update has been made to add the support of more log message type. The update also include minor bug fix.

Update changes:
- Support construction of error, fatal, info and debug log for the sensor device.
- Minor bug fixing.
- Change parameter acceptance of filename to just file's name only without the extension.

# v0.2.3 (2023-10-18)

An update has been made to support concurrent folders creation from the root directory, for the log
file and folder creation within the FTP server. The comprehensive list of updates are as follow:

Update changes:
- Support the multiple folders and files creation with the FTP server from the parent directory.
- Update urllib3 to version 1.26.17 to combat vulnerabilities CVE-2023-43804. Did not upgraded to the
latest 2.0.6 due to the compatible issue with the AWS SDK.
- Fix bug of passing invalid uuid value to the data log.
- Improve error handling for better efficiency.

#  v0.2.4 (2023-10-30)

New features
- Support logging message with local timezone.

Bugfix
- Improper indention in logging message.