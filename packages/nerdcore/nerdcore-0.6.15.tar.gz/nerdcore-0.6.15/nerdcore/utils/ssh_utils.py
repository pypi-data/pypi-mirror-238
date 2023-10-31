import asyncssh
import asyncio
from paramiko.config import SSHConfig
import os


def _load_ssh_config():
    ssh_config = SSHConfig()
    user_config_file = os.path.expanduser("~/.ssh/config")
    if os.path.exists(user_config_file):
        with open(user_config_file) as f:
            ssh_config.parse(f)
    return ssh_config


class SSHConnection:
    instances = {}

    def __init__(self, server_name, dir_name='generic'):
        self.server_name = server_name
        self.dir_name = dir_name
        self.ssh_config = _load_ssh_config()
        self.ssh = None
        self.is_busy = False

        if self.server_name not in SSHConnection.instances:
            SSHConnection.instances[f'{self.server_name}_{self.dir_name}'] = []

        SSHConnection.instances[f'{self.server_name}_{self.dir_name}'].append(self)

    async def _connect(self):
        cfg = self.ssh_config.lookup(self.server_name)
        self.ssh = await asyncssh.connect(
            host=cfg['hostname'],
            username=cfg.get('user'),
            client_keys=[cfg.get('identityfile')[0]]
        )

    async def execute_command(self, command):
        if self.ssh is None:
            await self._connect()

        free_instance = self.get_free_instance()
        if free_instance is None:
            free_instance = SSHConnection(self.server_name, self.dir_name)
            await free_instance._connect()

        return await free_instance._execute_command(command)

    async def _execute_command(self, command):
        self.is_busy = True
        process = await self.ssh.create_process(command)
        stdout, stderr = await process.communicate()
        self.is_busy = False
        return process.exit_status, stdout, stderr

    def get_free_instance(self):
        for instance in SSHConnection.instances[f'{self.server_name}_{self.dir_name}']:
            if not instance.is_busy:
                return instance
        return None

    async def scp_file_to_server(self, local_path, remote_path):
        if self.ssh is None:
            await self._connect()
        async with self.ssh.start_sftp_client() as sftp:
            await sftp.put(local_path, remote_path)

    async def scp_file_from_server(self, remote_path, local_path):
        if self.ssh is None:
            await self._connect()
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        async with self.ssh.start_sftp_client() as sftp:
            await sftp.get(remote_path, local_path)

    async def close(self):
        if self.ssh:
            self.ssh.close()
            await self.ssh.wait_closed()
