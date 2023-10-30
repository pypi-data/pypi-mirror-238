"""
The library to push log message to FTP server.
"""

import io
import datetime
import ipaddress
from ftplib import FTP, all_errors
import pytz
from .myException import FTPConnectionFailedException,\
    FTPFileCreationException,\
    NoneValueException,\
    InvalidAttributeException,\
    EmptyParameterException,\
    InvalidFTPHostNameException,\
    InvalidFTPPortNumberException,\
    InvalidFTPUserNameException,\
    InvalidFTPPasswordException

# pylint: disable=E0302
# pylint: disable=W0212
class FtpClient:
    """Class to establish connection and writing to FTP server.
    """

    def __init__(self, hostname, port_num, username, password):
        """
        Establish communication with the remote FTP server.

        Args:\n
            hostname (string): FTP server hostname.
            port_num (integer): FTP server port number.
            username (string): FTP server username.
            password (string): FTP server password.

        Raise InvalidFTPPortNumberException:\n
            If the port number is not of type int and is equal or less
            than zero.
            
        Raise InvalidFTPUserNameException:\n
            If the username is not of type string or it is an empty 
            string or it is a None value.
            
        Raise InvalidFTPPasswordException:\n
            If the password is not of type string or it is an empty
            string or it is a None value.
            
        Raise FTPConnectionFailedException:\n
            If the connection to the FTP remote server was not 
            a success.
            
        Raise InvalidFTPHostNameException:\n
            If any of the port number, username, and password
            are invalid.
        """

        if isinstance(port_num, int) is False\
            or port_num <= 0:
            raise InvalidFTPPortNumberException()

        if isinstance(username, str) is False\
            or username is None or\
            username == "":
            raise InvalidFTPUserNameException()

        if isinstance(password, str) is False\
            or password is None or\
            password == "":
            raise InvalidFTPPasswordException()

        try:
            ipaddress.ip_address(hostname)
            self.ftp_client = FTP()
            self.ftp_client.connect(hostname, port_num)
            self.ftp_client.login(username, password)
        except all_errors as exc:
            raise FTPConnectionFailedException() from exc
        except ValueError as valuerr:
            raise InvalidFTPHostNameException() from valuerr

    def __get_ftp_directories(self):
        """
        To retrieve all the directories and files that are present 
        in the current working directory inside this directory 
        in this FTP server.

        Returns:\n
            list: A complete list of directories and files that are 
                currently available in present working directory.
        """
        dir_list = []
        self.ftp_client.retrlines('NLST', dir_list.append)
        return [item.split(" ")[-1] for item in dir_list]

    def __get_datetime(self):
        """
        Get the today date.

        Returns:\n
            string: Today's date.
        """
        return datetime.datetime.now().strftime("%Y-%m-%d")

    def __set_data_file_name(self, file_name):
        """
        Set the complete filename of the desired csv file.

        Args:
            file_name (string): The name of the csv file that wanted
                to be named.

        Returns:\n
            string: The complete filename of a csv file.
        """
        return self.__get_datetime() + "_"  + str(file_name) + ".csv"

    def __set_log_file_name(self, file_name):
        """
        Get the complete filename of the desired log file.

        Args:\n
            file_name (string): The name of the log file that wanted
                to be named.

        Returns:\n
            string: The complete fiilename of a log file.
        """
        return self.__get_datetime() + "_"  + str(file_name) + ".log"

    def create_ftp_log_data(self, directory_path, file_name, root):
        """
        Create the log file the sensors, or devices data log. The creation
        of the log file is based on the defined directory path and file name.
        The user also been giving the ability to customize the file creation
        of whether to create the log file start from parent directory or 
        otherwise.

        Args:\n
            directory_path (string): The directory path of the log file.
            file_name (string): The name of the log file (for device data).
            root (bool): Whether the folder and file creation is to
                                start from root directory.

        Raises:\n
            FTPFileCreationException: If the required data for log file
                creation is not fulfilling the desire requirements; or
                is attempt to parsing the invalid log file or directory.
        """
        # check the parameter `file_name`'s validity.
        if file_name == "" or\
            isinstance(file_name, str) is False:
            raise FTPFileCreationException()

        # check the parameter `directory_path`'s validity.
        if directory_path == "" or\
            isinstance(directory_path, str) is False:
            raise FTPFileCreationException()

        # check the parameter `from_parent`'s validity.
        if isinstance(root, bool) is False:
            raise FTPFileCreationException()

        try:
            # start traverse the defined directory path for
            # directory creation
            for directory in directory_path.split("/"):
                # if the directory was not existed, create
                # the directory
                if directory not in self.__get_ftp_directories():
                    self.ftp_client.mkd(directory)
                    self.ftp_client.cwd(directory)
                # otherwise, just move forward to the next
                # level of directory.
                else:
                    self.ftp_client.cwd(directory)

            # set the log file's file name
            filename = self.__set_data_file_name(file_name)
            if filename not in self.__get_ftp_directories():
                buf = io.BytesIO()
                buf.write(b'uuid,start,end,result,groundtruth\n')
                buf.seek(0)
                self.ftp_client.storbinary(f"STOR {filename}", buf)
            # move to the parent directory if the user is desired.
            if root is True:
                self.ftp_client.cwd("/")

        except all_errors as error:
            raise FTPFileCreationException() from error

    def set_ftp_log_data(self, directory_path, file_name, log_data):
        """
        Set the csv log file with the desired log data. The new log data
        will continue log onto the existing file, if the log file was
        present. Otherwise, new file gonna be created for this new log data.
        Please do take note that the file type must be of csv type.

        Args:\n
            directory_path (string): The path to the csv log file.
            file_name (string): The name of the csv log file.
            log_data (bytes): The log data.
            
        Raise NoneValueException:\n
            If the directory path, file name or the data to be logged
            is of None value.
        
        Raise InvalidAttributeException:\n
            If the directory path, file name is not the type of string,
            while the log data is not type of byte.
            
        Raise EmptyParameterException:\n
            If the directory path, file name or log data is empty.
        """
        if directory_path is None or file_name is None or\
            log_data is None:
            raise NoneValueException()

        if isinstance(directory_path, str) is False or\
            isinstance(file_name, str) is False or\
            isinstance(log_data, bytes) is False:
            raise InvalidAttributeException()

        if len(directory_path) == 0 or len(file_name) == 0 or\
            log_data == b"":
            raise EmptyParameterException()

        # get the desired directory name
        directories = directory_path.split('/')
        # loop through all the directory name
        for directory in directories:
            # if the name present move to the next directory
            if directory in self.__get_ftp_directories():
                self.ftp_client.cwd(directory)

        filename = self.__set_data_file_name(file_name)
        # check if the corrresponding file name present
        if filename in self.__get_ftp_directories():
            # if present write the log message to the relevant log file
            buf=io.BytesIO()
            buf.write(log_data)
            buf.seek(0)
            self.ftp_client.storbinary(f"APPE {filename}", buf, 1)

    def create_ftp_log_file(self, directory_path, file_name, root):
        """
        Create the ftp log file based on the user defined directory
        path, file name, and user decision of whether to have the 
        creation of log file started from the root directory.

        Args:\n
            directory_path (string): The log file directory path.
            file_name (string): The log file's file name.
            root (boolean): The decision to start from root directory

        Raises:\n
            FTPFileCreationException: If the required parameters are
            not fulfilled, or attempt to parse the non-existed file
            or folder.
        """
        if file_name == "" or\
            isinstance(file_name, str) is False:
            raise FTPFileCreationException()

        if directory_path == "" or\
            isinstance(directory_path, str) is False:
            raise FTPFileCreationException()

        if isinstance(root, bool) is False:
            raise FTPFileCreationException()

        try:
            # loop over user defined path, while
            # create the folder is it was not
            # previously present.
            for directory in directory_path.split("/"):
                if directory not in self.__get_ftp_directories():
                    self.ftp_client.mkd(directory)
                    self.ftp_client.cwd(directory)
                else:
                    self.ftp_client.cwd(directory)

            # Subsequently create the relevant log file.
            filename = self.__set_log_file_name(file_name)
            if filename not in self.__get_ftp_directories():
                buf = io.BytesIO()
                buf.seek(0)
                self.ftp_client.storbinary(f"STOR {filename}", buf)

            # if it is user choice to have the folder and file
            # generated from root directory, revisit the root
            # directory.
            if root is True:
                self.ftp_client.cwd("/")

        except all_errors as error:
            raise FTPFileCreationException from error

    def set_ftp_log_file(self, directory_path, file_name, message,
                        country_region):
        """
        Set the log file with application or system log. If the log file was 
        already existed, the new log will continue appended on to the existing log
        file. Otherwise, new log file gonna be created.

        Args:\n
            directory_path (string): The path to the log file.
            file_name (string): The log file name.
            message (string): The log message.
            country_region(string): The pytz library local timezone.
            
        Raise NoneValueException:\n
            If the directory path, file name is a type None.
            
        Raise InvalidAttributeException:\n
            If the directory path, file name, region or log message is
            not the type string.
            
        Raise EmptyParameterException:\n
            If the directory path, file name, region or log message is
            not empty.
        """
        if directory_path is None or file_name is None or\
            message is None or country_region is None:
            raise NoneValueException()

        if isinstance(directory_path, str) is False or\
            isinstance(file_name, str) is False or\
            isinstance(message, str) is False or\
            isinstance(country_region, str) is False:
            raise InvalidAttributeException()

        if len(directory_path) == 0 or len(file_name) == 0 or\
            len(message) == 0 or len(country_region) == 0:
            raise EmptyParameterException()

        self.ftp_client.cwd("/")

        # get the directories name
        directories = directory_path.split('/')
        # move to the corresponding directory if it
        # present
        for directory in directories:
            if directory in self.__get_ftp_directories():
                self.ftp_client.cwd(directory)

        # check for log file existence. If it exist only
        # write the log onto the corresponding log file.
        filename = self.__set_log_file_name(file_name)
        if filename in self.__get_ftp_directories():
            buf = io.BytesIO()
            buf.write(bytes("["+datetime.datetime.now(pytz.timezone(country_region)).\
                strftime('%Y-%m-%d %H:%M:%S')+"]"+message+"\n",
                        'utf-8'))
            buf.seek(0)
            self.ftp_client.storbinary(f"APPE {filename}", buf, 1)

    def __del__(self):
        self.ftp_client.quit()
