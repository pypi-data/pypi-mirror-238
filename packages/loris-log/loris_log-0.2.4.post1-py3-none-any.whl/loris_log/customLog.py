"""
The CustomLogMessage that contains the custom log message
"""
import os
import inspect
import uuid
import sys
from .myException import InvalidMessageException,\
    EmptyParameterException,\
    NoneValueException,\
    InvalidAttributeException

# pylint: disable=W0212
class CustomLog:
    """
    Class to construct the log message (info, error, debug, fatal, log data).
    """

    @staticmethod
    def set_error_message(uu_id, name, message):
        """
        Set up the format of the error message.

        Args:\n
            uu_id (string): The generated uuid.
            name (string): The name of the application or API.
            message (array): The error message.

        Returns:\n
            string: The custom error message.
            
        Raises NoneValueException:\n
            If the uu_id, name or message of a None.
            
        Raises EmptyParameterException:\n
            If the uu_id is not of length 36, or name is
            or the message is empty.
            
        Raises InvalidAttributeException:\n
            If the uu_id is not of type uuid, name is not of type string,
            and message is not of type list.
            
        Raises InvalidMessageException:\n
            if the error message creation is a failure.
        """
        if uu_id is None or name is None or message is None:
            raise NoneValueException()

        if isinstance(uu_id, uuid.UUID) is False or\
            isinstance(name, str) is False or\
            isinstance(message, list) is False:
            raise InvalidAttributeException()

        if len(str(uu_id)) != 36 or len(str(name)) == 0 or \
            len(message) == 0:
            raise EmptyParameterException()

        try:
            error_message = f" [ERROR] [{str(uu_id)}] [{str(name)}] [{os.path.basename(inspect.stack()[1].filename)}] [line {sys._getframe().f_back.f_lineno}]: {' '.join(word for word in message)}"
            return error_message
        except TypeError as exc:
            raise InvalidMessageException() from exc

    @staticmethod
    def set_debug_message(uu_id, name, message):
        """
        Set up the format of the debug message

        Args:\n
            uu_id (string): The generated uuid.
            name (string): The name of the application/ API/ function/ feature.
            message (list): The error message.

        Returns:\n
            string: The custom debug message.
            
        Raises NoneValueException:\n
            If the uu_id, name or message is a none value.
            
        Raises EmptyParameterException:\n
            If the uu_id is not of length 36 or the name 
            or the message is empty.
            
        Raises InvalidAttributeException:\n
            If the uu_id is not of type uuid, name is not
            of type string, and message is not of type list.
            
        Raises InvalidMessageException:\n
            If the log creation failed.
        """
        if uu_id is None or name is None or message is None:
            raise NoneValueException()

        if isinstance(uu_id, uuid.UUID) is False or\
            isinstance(name, str) is False or\
            isinstance(message, list) is False:
            raise InvalidAttributeException()

        if len(str(uu_id)) != 36 or len(str(name)) == 0 or\
            len(message) == 0:
            raise EmptyParameterException()

        try:
            debug_message = f" [DEBUG] [{uu_id}] [{name}] [{os.path.basename(inspect.stack()[1].filename)}] [line {sys._getframe().f_back.f_lineno}]: {' '.join(word for word in message)}"
            return debug_message
        except TypeError as exc:
            raise InvalidMessageException() from exc

    @staticmethod
    def set_fatal_message(uu_id, name, message):
        """
        Set up the format of the fatal message.

        Args:\n
            uu_id (string): The generated uuid.
            name (string): The name of the application/api/function/feature.
            message (list): The error message.

        Returns:\n
            string: The custom fatal message.
            
        Raises NoneValueException:\n
            If the uu_id, name or message is a none value.
            
        Raises EmptyParameterException:\n
            If the uu_id is not of length 36 or the name 
            or the message is empty.
            
        Raises InvalidAttributeException:\n
            If the uu_id is not of type uuid, name is not
            of type string, and message is not of type list.
            
        Raises InvalidMessageException:\n
            If the log creation failed.
        """
        if uu_id is None or name is None or message is None:
            raise NoneValueException()

        if isinstance(uu_id, uuid.UUID) is False or\
            isinstance(name, str) is False or\
            isinstance(message, list) is False:
            raise InvalidAttributeException()

        if len(str(uu_id)) != 36 or len(str(name)) == 0 or \
            len(message) == 0:
            raise EmptyParameterException()

        try:
            fatal_message = f" [FATAL] [{uu_id}] [{name}] [{os.path.basename(inspect.stack()[1].filename)}] [line {sys._getframe().f_back.f_lineno}]: {' '.join(word for word in message)}"
            return fatal_message
        except TypeError as exc:
            raise InvalidMessageException() from exc

    @staticmethod
    def set_info_message(uu_id, name, message):
        """
        Set up the format of the info message.

        Args:\n
            uu_id (string): The generated uuid.
            name (string): The name of the application or API
            message (list): The error message.

        Returns:\n
            string: The custom info message.
        
        Raises NoneValueException:\n
            If the uu_id, name or message is a none value.
            
        Raises EmptyParameterException:\n
            If the uu_id is not of length 36 or the name 
            or the message is empty.
            
        Raises InvalidAttributeException:\n
            If the uu_id is not of type uuid, name is not
            of type string, and message is not of type list.
            
        Raises InvalidMessageException:\n
            If the log creation failed.
        """
        if uu_id is None or name is None or message is None:
            raise NoneValueException()

        if isinstance(uu_id, uuid.UUID) is False or\
            isinstance(name, str) is False or\
            isinstance(message, list) is False:
            raise InvalidAttributeException()

        if len(str(uu_id)) != 36 or len(str(name)) == 0 or \
            len(message) == 0:
            raise EmptyParameterException()

        try:
            info_message = f" [INFO] [{uu_id}] [{name}] [{os.path.basename(inspect.stack()[1].filename)}] [line {sys._getframe().f_back.f_lineno}]: {' '.join(word for word in message)}"
            return info_message
        except TypeError as exc:
            raise InvalidMessageException() from exc

    @staticmethod
    def set_sensor_info_message(sensor_id, name, message):
        """
        Set up the info log message for the sensors.

        Args:\n
            sensor_id (str): The sensor id.
            name (string): The name of application/ service/ or remote request IP address.
            message (list): The content of message.

        Raises NoneValueException:\n
            If the sensor_id, name, or message is of none value.
             
        Raises EmptyParameterException:\n
            If the sensor_id, name or message is empty.
            
        Raises InvalidAttributeException:\n
            If the sensor_id and name is not of type string, or
            message is not of type list.
            
        Raises InvalidMessageException:\n
            If there is an issue is creating the custom info message
            for a sensor.

        Returns:\n
            string: The sensor info log message.
        """
        if sensor_id is None or name is None or message is None:
            raise NoneValueException()

        if isinstance(sensor_id, str) is False or\
            isinstance(name, str) is False or\
            isinstance(message, list) is False:
            raise InvalidAttributeException()

        if len(str(sensor_id)) == 0 or len(str(name)) == 0 or\
            len(message) == 0:
            raise EmptyParameterException()

        try:
            info_message = f" [INFO] [{sensor_id}] [{name}] [{os.path.basename(inspect.stack()[1].filename)}] [line {sys._getframe().f_back.f_lineno}]: {' '.join(word for word in message)}"
            return info_message
        except TypeError as exc:
            raise InvalidMessageException() from exc

    @staticmethod
    def set_sensor_debug_message(sensor_id, name, message):
        """
        Set the debug log message for an sensor.

        Args:\n
            sensor_id (string): The sensor id.
            name (string): The name of the API/ application/ service or remote 
                            request IP address.
            message (string): The log message.

        Raises NoneValueException:\n
            If the sensor_id, name and message is of type none.
            
        Raises EmptyParameterException:\n
            If the sensor_id, name and message is an empty value.
            
        Raises InvalidAttributeException:\n
            If the sensor_id and name is not type string, and 
            message is not of type list.
            
        Raises InvalidMessageException:\n
            If the creating the debug log_message is failed.

        Returns:\n
            string: The debug log message.
        """
        if sensor_id is None or name is None or message is None:
            raise NoneValueException()

        if isinstance(sensor_id, str) is False or\
            isinstance(name, str) is False or\
            isinstance(message, list) is False:
            raise InvalidAttributeException()

        if len(str(sensor_id)) == 0 or len(str(name)) == 0 or\
            len(message) == 0:
            raise EmptyParameterException()

        try:
            debug_message = f" [DEBUG] [{sensor_id}] [{name}] [{os.path.basename(inspect.stack()[1].filename)}] [line {sys._getframe().f_back.f_lineno}]: {' '.join(word for word in message)}"
            return debug_message
        except TypeError as exc:
            raise InvalidMessageException() from exc

    @staticmethod
    def set_sensor_error_message(sensor_id, name, message):
        """
        The set up of the error message for the sensor.

        Args:
            sensor_id (string ): The sensor id.
            name (string): The name of application/ API/ request remote IP.
            message (list): The error log message.

        Raises NoneValueException:\n
            If the sensor_id, name, or message is of none value.
            
        Raises EmptyParameterException:\n
            If the sensor_id, name and message is empty.
            
        Raises InvalidAttributeException:\n
            If the sensor_id and name is not of type string, while
            message is not of type list.
            
        Raises InvalidMessageException:\n
            If the operation to create the error log message is a
            failure.

        Returns:
            string: The sensor error message.
        """
        if sensor_id is None or name is None or message is None:
            raise NoneValueException()

        if isinstance(sensor_id, str) is False or\
            isinstance(name, str) is False or\
            isinstance(message, list) is False:
            raise InvalidAttributeException()

        if len(str(sensor_id)) == 0 or len(str(name)) == 0 or\
            len(message) == 0:
            raise EmptyParameterException()

        try:
            error_message = f" [ERROR] [{sensor_id}] [{name}] [{os.path.basename(inspect.stack()[1].filename)}] [line {sys._getframe().f_back.f_lineno}]: {' '.join(word for word in message)}"
            return error_message
        except TypeError as exc:
            raise InvalidMessageException() from exc

    @staticmethod
    def set_sensor_fatal_message(sensor_id, name, message):
        """
        Set up the fatal log message for a sensor.

        Args:\n
            sensor_id (string): The sensor id.
            name (string): The name of application/ API or remote request IP.
            message (list): The fatal log message

        Raises NoneValueException:\n
            If the sensor_id, name or message is a none value.
            
        Raises EmptyParameterException:\n
            If the sensor_id, name or message is empty.
            
        Raises InvalidAttributeException:\n
            If the sensor_id and name is not of type string, or 
            the message is not a list.
            
        Raises InvalidMessageException:\n
            If the operation to create the fatal log message is a 
            failure.

        Returns:
            string: the fatal log message.
        """
        if sensor_id is None or name is None or message is None:
            raise NoneValueException()

        if isinstance(sensor_id, str) is False or\
            isinstance(name, str) is False or\
            isinstance(message, list) is False:
            raise InvalidAttributeException()

        if len(str(sensor_id)) == 0 or len(str(name)) == 0 or\
            len(message) == 0:
            raise EmptyParameterException()

        try:
            fatal_message = f" [FATAL] [{sensor_id}] [{name}] [{os.path.basename(inspect.stack()[1].filename)}] [line {sys._getframe().f_back.f_lineno}]: {' '.join(word for word in message)}"
            return fatal_message
        except TypeError as exc:
            raise InvalidMessageException() from exc

    @staticmethod
    def set_ftp_log_data(uu_id, starttime, endtime, result, groundtruth):
        """
        Set up the log message for the FTP system.

        Args:\n
            uuid (string): The generated uuid.
            starttime (string): the start time of an operation.
            endtime (string): the end time of an operation.
            result (string): the result of the embedded device/ system/ model etc.
            groundtruth (string): the result of the embedded device/ system/ model etc.

        Returns:\n
            string: a list of log data.
            
        Raises NoneValueException:\n
            If the uu_id, name or message is a none value.
            
        Raises EmptyParameterException:\n
            If the uu_id is not of length 36 or the name 
            is empty.
            
        Raises InvalidAttributeException:\n
            If the uu_id is not of type uuid, name is not
            of type string, and message is not of type list.
            
        Raises InvalidMessageException:\n
            If the log creation failed.
        """
        if uu_id is None or starttime is None\
           or endtime is None or result is None or\
           groundtruth is None:
            raise NoneValueException()

        if isinstance(uu_id, str) is False or\
            isinstance(starttime, str) is False or\
            isinstance(endtime, str) is False:
            raise InvalidAttributeException()

        if len(str(uu_id)) == 0 or len(str(starttime)) == 0\
            or len(str(endtime)) == 0 or len(result) == 0\
            or len(str(groundtruth)) == 0:
            raise EmptyParameterException()

        try:
            data_message = bytes(f"{uu_id},{str(starttime)},{str(endtime)},{float(result)},{float(groundtruth)}\n", encoding='utf-8')
            return data_message
        except ValueError as exc:
            raise InvalidMessageException() from exc
