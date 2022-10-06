import logging
import paramiko

from dotenv import load_dotenv

import os

load_dotenv()


def get_connection():
    sftp_host = os.getenv('OI_SFTP_HOST')
    username = os.getenv('OI_SFTP_USERNAME')
    password = os.getenv('OI_SFTP_PASSWORD')
    known_hosts_file = ".known_hosts"
    hostkeys = paramiko.hostkeys.HostKeys(filename=known_hosts_file)
    host_fingerprint = hostkeys.lookup(sftp_host)['ssh-ed25519']

    try:
        tp = paramiko.Transport(sftp_host, 22)
        tp.connect(username=username, password=password,
                   hostkey=host_fingerprint)
    except paramiko.ssh_exception.AuthenticationException as err:
        logging.error(
            "Can't connect due to authentication error [{}]", str(err))
    except Exception as err:
        logging.error("Can't connect due to other error [{}]", str(err))
    return tp


def get(remotepath, localpath):
    with get_connection() as tp:
        try:
            with paramiko.SFTPClient.from_transport(tp) as sftp_client:
                sftp_client.get(remotepath=remotepath,
                                localpath=localpath)
        except Exception as err:
            logging.error("SFTP failed due to [{}]", str(err))
