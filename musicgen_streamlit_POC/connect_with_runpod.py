import paramiko
import os
import logging

logging.basicConfig(level=logging.INFO)

def transfer_files_and_cleanup(ssh, result, local_output_dir):
    try:
        output_files = result.split(";")
        local_files = []
        sftp = ssh.open_sftp()
        for output_file in output_files:
            logging.info(f"Transferring file: {output_file}")  
            local_path = os.path.join(local_output_dir, os.path.basename(output_file))
            sftp.get(output_file, local_path)
            local_files.append(local_path)
            logging.info(f"File transferred: {local_path}")
        sftp.close()
        ssh.close()
        return local_files[-1] if local_files else None, None, 100  
    except Exception as e:
        logging.error(f"Exception during SCP operation: {e}")
        return None, str(e), 0

def run_inference_on_runpod(prompt):
    ssh_host = "38.128.233.175"
    ssh_port = 39818
    ssh_user = "root"
    ssh_key_path = os.path.expanduser("~/.ssh/id_ed25519")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    local_output_dir = os.path.abspath(os.path.join(base_dir, '..', "generated_data", "musicgen_output"))

    try:
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ssh_host, port=ssh_port, username=ssh_user, key_filename=ssh_key_path)
        logging.info("SSH connection established successfully.")
        
        
        command = f'python3 /workspace/output/inference5.py "{prompt}"'
        logging.info(f"Running command: {command}")
        
        stdin, stdout, stderr = ssh.exec_command(command)
        
        
        while not stdout.channel.exit_status_ready():
            continue
        
        if stdout.channel.recv_exit_status() != 0:
            error = stderr.read().decode().strip()
            logging.error(f"Error from inference script: {error}")
            ssh.close()
            return None, error, 30  #

        logging.info("Inference script executed successfully.")
        
        result = stdout.read().decode().strip()
        logging.info(f"Result: {result}")  
        result = ";".join([f"{path}.wav" for path in result.split(";")])
        return transfer_files_and_cleanup(ssh, result, local_output_dir)
        
    except Exception as e:
        logging.error(f"Exception during SSH/SCP operation: {e}")
        return None, str(e), 0