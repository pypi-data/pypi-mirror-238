"""
The example of how to use this library.
"""


import sys 
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import uuid
import datetime
from loris_log.boto3Client import Boto3Client
from loris_log.customLog import CustomLog
from loris_log.ftpClient import FtpClient

def get_log_group_sample():
    """
    The example of getting the log group names.
    """
    target_region_name = ""
    target_aws_key = ""
    target_aws_secret = ""
    boto3Client = Boto3Client(target_region_name, target_aws_key, target_aws_secret)
    response = boto3Client.get_log_groups()
    print(response)
    
def get_log_stream_sample():
    """
    The example of creating the log stream.
    """
    target_log_group = "sample"
    target_region_name = ""
    target_aws_key = ""
    target_aws_secret = ""
    boto3Client = Boto3Client(target_region_name, target_aws_key, target_aws_secret)
    response = boto3Client.get_log_stream(target_log_group)
    print("response: ", response)
    
def set_custom_message_sample():
    """
    The example of setting various log message.

    Returns:
        string: various log mesasges.
    """
    id = uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org')
    target_name = "my_application_name"
    target_error_message = ["[404]", "File not found exception."]
    target_debug_message = ["[200]", "Running the time calculation"]
    target_fatal_message = ["[500]", "System Halt"]
    target_info_message = ["[200]", "model accuracy", "0.99"]

    error_message = CustomLog.set_error_message(id, target_name, target_error_message)
    debug_message = CustomLog.set_debug_message(id, target_name, target_debug_message)
    fatal_message = CustomLog.set_fatal_message(id, target_name, target_fatal_message)
    info_message = CustomLog.set_info_message(id, target_name, target_info_message)
    return error_message, debug_message, fatal_message, info_message

def set_log_info_message_for_sensor_sample():
    """
    The example of pushing sensor log message onto the cloudwatch
    """
    target_log_group = "sample"
    target_log_stream = "sample-log"
    target_region_name = ""
    target_aws_key = ""
    target_aws_secret = ""
    region_country = ""
    boto3Client = Boto3Client(target_region_name, target_aws_key, target_aws_secret)
    boto3Client.set_log_message(
        target_log_group, 
        target_log_stream, 
        CustomLog.set_sensor_info_message(
            "sensor-id-#3345",
            "main",
            ["[200]", "[camera 0]", "camera ok"]
        ),
        region_country
    )
    
def set_log_message_sample():
    """
    The example of how to pushing log message onto the cloudwatch.
    """
    target_log_group = "sample"
    target_log_stream = "sample-log"
    target_region_name = ""
    target_aws_key = ""
    target_aws_secret = ""
    region_country = "Asia/Singapore"
    boto3Client = Boto3Client(target_region_name, target_aws_key, target_aws_secret)
    boto3Client.create_log_group_stream(target_log_group, target_log_stream)
    error_message, debug_message, fatal_message, info_message = set_custom_message_sample()
    boto3Client.set_log_message(target_log_group, target_log_stream, error_message, 
                                region_country)
    boto3Client.set_log_message(target_log_group, target_log_stream, debug_message,
                                region_country)
    boto3Client.set_log_message(target_log_group, target_log_stream, fatal_message,
                                region_country)
    boto3Client.set_log_message(target_log_group, target_log_stream, info_message,
                                region_country)
       
            
            
def set_log_data_ftp_example():
    """Example of how to log data onto the csv log file.
    """
    id = uuid.uuid4()
    target_hostname = ""
    target_port = 00
    target_username = ""
    target_password = ""
    ftp_client = FtpClient(target_hostname, target_port, target_username, target_password)
    ftp_client.create_ftp_log_data("log_testing/data", "id", True)
        
    start_time = datetime.datetime.now()
    target_start_time = start_time.strftime("%H:%M:%S")
    end_time = datetime.datetime.now()
    target_end_time = end_time.strftime("%H:%M:%S")
    target_result = "32"
    target_ground_truth = "3"
    file_data_message = CustomLog.set_ftp_log_data(str(id),
                                    target_start_time, 
                                    target_end_time, 
                                    target_result, 
                                    target_ground_truth)
    for i in range(5):
        ftp_client.set_ftp_log_data("log_testing/data", "id", file_data_message)
        
def set_log_file_ftp_example():
    """Example of how to log logging message to the log file
    """
    id = uuid.uuid4()
    target_hostname = ""
    target_port = 00
    target_username = ""
    target_password = ""
    country_region = "Asia/Singapore"
    ftp_client = FtpClient(target_hostname, target_port, target_username, target_password)
    ftp_client.create_ftp_log_file("log_testing/data", "filename",
                                              True)
      
    target_name = "sample log"
    target_info_message = ["model accuracy", "0.99"]
    for i in range(5):
        ftp_client.set_ftp_log_file(
            "log_testing/data",
            "filename",
            CustomLog.set_fatal_message(
                id, target_name, target_info_message
            ), country_region
        )
        
def create_ftp_log_file():
    host = ""
    port = 00
    username = ""
    password = ""
    country_region = "Asia/Singapore"
    client = FtpClient(
        host, port, username, password
    )
    for i in range(3):
        client.create_ftp_log_file(
            f"testing/{i}_sample", "sample", True
        )
    client.set_ftp_log_file(
        "testing/1_sample",
        "sample",
        CustomLog.set_sensor_debug_message(
            "sensor_1", "sample", ["ok", "sample"]
        ),
        country_region
    )
    
def create_ftp_log_data():
    host = ""
    port = 00
    username = ""
    password = ""
    client = FtpClient(
        host, port, username, password
    )
    for i in range(3):
        client.create_ftp_log_data(
            f"testing/{i}_sample", "sample", True
        )
        
    start_time = datetime.datetime.now()
    target_start_time = start_time.strftime("%H:%M:%S")
    end_time = datetime.datetime.now()
    target_end_time = end_time.strftime("%H:%M:%S")
    target_result = "32"
    target_ground_truth = "3"
    file_data_message = CustomLog.set_ftp_log_data(str(uuid.uuid4()),
                                    target_start_time, 
                                    target_end_time, 
                                    target_result, 
                                    target_ground_truth)
    client.set_ftp_log_data(
        "testing/1_sample", "sample",
        file_data_message
    )
            

def main():
    set_log_info_message_for_sensor_sample()

if __name__=="__main__":
    main()