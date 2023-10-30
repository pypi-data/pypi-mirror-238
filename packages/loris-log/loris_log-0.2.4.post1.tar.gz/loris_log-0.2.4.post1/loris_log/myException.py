"""This library own customized exception.
"""

class InvalidFTPHostNameException(Exception):
    """
    Custom exception for the invalid FTP hostname.

    Args:\n
        Exception (string): The error message.
    """
    def __str__(self):
        return repr("Invalid FTP Host name.")

class InvalidFTPPortNumberException(Exception):
    """
    Custom exception for the invalid FTP port number.

    Args:\n
        Exception (string): The error message.
    """
    def __str__(self):
        return repr("Invalid FTP Port Number.")

class InvalidFTPUserNameException(Exception):
    """
    Custom exceptionf or the invalid FTP username.

    Args:\n
        Exception (string): The error message.
    """
    def __str__(self):
        return repr("Invalid FTP Username.")

class InvalidFTPPasswordException(Exception):
    """
    Custom exception for the invalid FTP password.

    Args:\n
        Exception (string): The error message.
    """
    def __str__(self):
        return repr("Invalid FTP Password.")

class InvalidMessageException(Exception):
    """
    Custom Exception for the invalid message.
    
    Args:\n
        Exception (string): The error message.
    """
    def __str__(self):
        return repr("Invalid message.")

class InvalidRoleSecretException(Exception):
    """
    Custom exception for the invalid role secret.

    Args:\n
        Exception (string): The error message.
    """
    def __str__(self):
        return repr("Invalid role secret.")

class EmptyParameterException(Exception):
    """
    Custom exception for the empty parameter.

    Args:\n
        Exception (string): The error message.
    """
    def __str__(self):
        return repr("Attempt to enter empty input.")

class InvalidRoleAccessKeyException(Exception):
    """
    Custom exception for the invalid role access key.

    Args:\n
        Exception (string): The error message.
    """
    def __str__(self):
        return repr("Invalid role access key.")

class NoneValueException(Exception):
    """Custom exception for the non value.

    Args:\n
        Exception (string): The error message.
    """
    def __str__(self):
        return repr("The input value should not be none.")

class InvalidAttributeException(Exception):
    """Custom exception for attribute error.

    Args:\n
        Exception (string): The error message.
    """
    def __str__(self):
        return repr("Attribute error.")

class InvalidRegionNameException(Exception):
    """Custom exception for invalid region name.

    Args:\n
        Exception (string): Invalid region name.
    """
    def __str__(self):
        return repr("Invalid region name.")

class FTPConnectionFailedException(Exception):
    """
    Custom exception for FTP Connection Failure.

    Args:\n
        Exception (string): The error message.
    """
    def __str__(self):
        return repr("FTP Server Connection Failure.")

class FTPFileCreationException(Exception):
    """
    Custom exception for file or folder creation failure.

    Args:\n
        Exception (string): The error message.
    """
    def __str__(self):
        return repr("File or folder creation error.")
