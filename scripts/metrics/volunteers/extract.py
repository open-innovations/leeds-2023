import os
import paramiko

TOP_DIR=os.path.realpath(os.path.join(os.path.dirname(__file__), '../../..'))

OUTPUT_DIR=f'{TOP_DIR}/working/metrics/rosterfy'

LEARN_HOSTS=False

if __name__ == '__main__':    
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with paramiko.client.SSHClient() as client:
        client.load_host_keys(f'{TOP_DIR}/.known_hosts')

        client.connect(
            os.environ['OI_SFTP_HOST'],
            username=os.environ['OI_SFTP_USERNAME'],
            password=os.environ['OI_SFTP_PASSWORD'],
        )

        with client.open_sftp() as sftp:
            for f in sftp.listdir('rosterfy/rosterfy'):
                sftp.get(f'rosterfy/rosterfy/{f}', f'{OUTPUT_DIR}/{f}')

