#!/usr/bin/env python3
"""
SFTP Deploy Script
Automatically pulls from git, builds the project, and pushes to SFTP server
"""

import os
import sys
import logging
import subprocess
import shutil
import tempfile
from datetime import datetime
import paramiko


class SFTPDeployer:
    """Handles automated git pull, build, and SFTP deployment"""

    def __init__(self, sftp_host, sftp_port, sftp_user, sftp_password, remote_path="/"):
        """
        Initialize SFTP Deployer

        Args:
            sftp_host: SFTP server hostname
            sftp_port: SFTP server port
            sftp_user: SFTP username
            sftp_password: SFTP password
            remote_path: Remote path on SFTP server
        """
        self.sftp_host = sftp_host
        self.sftp_port = sftp_port
        self.sftp_user = sftp_user
        self.sftp_password = sftp_password
        self.remote_path = remote_path

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('SFTPDeployer')

        self.client = None
        self.sftp = None
        self.work_dir = None

    def log(self, message, level='info'):
        """Log a message with color"""
        colors = {
            'info': '\033[0;34m',
            'success': '\033[0;32m',
            'warning': '\033[1;33m',
            'error': '\033[0;31m'
        }
        reset = '\033[0m'

        color = colors.get(level, colors['info'])
        print(f"{color}[{level.upper()}]{reset} {message}")

        if level == 'error':
            self.logger.error(message)
        elif level == 'warning':
            self.logger.warning(message)
        else:
            self.logger.info(message)

    def run_command(self, cmd, cwd=None, capture_output=False):
        """Run a shell command"""
        self.log(f"Running: {cmd}")
        try:
            if capture_output:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    cwd=cwd,
                    capture_output=True,
                    text=True,
                    check=True
                )
                return result.stdout
            else:
                subprocess.run(cmd, shell=True, cwd=cwd, check=True)
                return None
        except subprocess.CalledProcessError as e:
            self.log(f"Command failed: {e}", 'error')
            if capture_output and e.stderr:
                self.log(f"Error output: {e.stderr}", 'error')
            raise

    def setup_work_directory(self):
        """Create a temporary working directory"""
        self.work_dir = tempfile.mkdtemp(prefix='sftp_deploy_')
        self.log(f"Working directory: {self.work_dir}")
        return self.work_dir

    def git_pull(self, repo_url, branch='main'):
        """Clone or pull from git repository"""
        self.log("=" * 70)
        self.log("Step 1: Pulling from Git")
        self.log("=" * 70)

        try:
            # Clone the repository
            self.log(f"Cloning repository: {repo_url}")
            self.run_command(f"git clone --depth 1 --branch {branch} {repo_url} .", cwd=self.work_dir)
            self.log("✓ Git clone successful", 'success')
            return True
        except Exception as e:
            self.log(f"Git pull failed: {e}", 'error')
            return False

    def build_project(self):
        """Build/prepare the project"""
        self.log("=" * 70)
        self.log("Step 2: Building Project")
        self.log("=" * 70)

        try:
            # Check if requirements.txt exists and install
            req_file = os.path.join(self.work_dir, 'requirements.txt')
            if os.path.exists(req_file):
                self.log("Installing Python dependencies...")
                self.run_command(f"pip install -q -r requirements.txt", cwd=self.work_dir)
                self.log("✓ Dependencies installed", 'success')

            # Run any build scripts if they exist
            build_script = os.path.join(self.work_dir, 'build.sh')
            if os.path.exists(build_script):
                self.log("Running build script...")
                os.chmod(build_script, 0o755)
                self.run_command("./build.sh", cwd=self.work_dir)
                self.log("✓ Build script completed", 'success')

            self.log("✓ Project build complete", 'success')
            return True

        except Exception as e:
            self.log(f"Build failed: {e}", 'error')
            return False

    def connect_sftp(self):
        """Connect to SFTP server"""
        self.log("=" * 70)
        self.log("Step 3: Connecting to SFTP")
        self.log("=" * 70)

        try:
            self.log(f"Connecting to {self.sftp_host}:{self.sftp_port}...")

            # Create SSH client
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect with password
            self.client.connect(
                hostname=self.sftp_host,
                port=self.sftp_port,
                username=self.sftp_user,
                password=self.sftp_password,
                timeout=30,
                allow_agent=False,
                look_for_keys=False
            )

            # Open SFTP session
            self.sftp = self.client.open_sftp()
            self.log(f"✓ Connected as {self.sftp_user}", 'success')
            return True

        except Exception as e:
            self.log(f"SFTP connection failed: {e}", 'error')
            return False

    def create_remote_dir(self, remote_dir):
        """Create remote directory recursively"""
        dirs = []
        current = remote_dir

        while current and current != '/':
            dirs.append(current)
            current = os.path.dirname(current)

        dirs.reverse()

        for directory in dirs:
            try:
                self.sftp.stat(directory)
            except FileNotFoundError:
                try:
                    self.sftp.mkdir(directory)
                    self.log(f"Created directory: {directory}")
                except Exception as e:
                    self.log(f"Could not create {directory}: {e}", 'warning')

    def upload_file(self, local_path, remote_path):
        """Upload a single file to SFTP"""
        try:
            # Create remote directory if needed
            remote_dir = os.path.dirname(remote_path)
            if remote_dir:
                self.create_remote_dir(remote_dir)

            # Upload file
            file_size = os.path.getsize(local_path)
            self.sftp.put(local_path, remote_path)

            # Verify
            remote_stat = self.sftp.stat(remote_path)
            if remote_stat.st_size == file_size:
                return True
            else:
                self.log(f"Size mismatch for {remote_path}", 'error')
                return False

        except Exception as e:
            self.log(f"Upload failed for {local_path}: {e}", 'error')
            return False

    def upload_directory(self, local_dir, remote_dir, exclude=None):
        """Upload entire directory to SFTP"""
        exclude = exclude or ['.git', '__pycache__', '*.pyc', '.gitignore', 'venv', 'env']

        self.log(f"Uploading {local_dir} -> {remote_dir}")

        uploaded = 0
        failed = 0

        for root, dirs, files in os.walk(local_dir):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if d not in exclude and not any(d.endswith(e.replace('*', '')) for e in exclude)]

            # Calculate relative path
            rel_path = os.path.relpath(root, local_dir)
            if rel_path == '.':
                current_remote = remote_dir
            else:
                current_remote = os.path.join(remote_dir, rel_path).replace('\\', '/')

            # Upload files
            for file in files:
                # Skip excluded patterns
                if any(file.endswith(e.replace('*', '')) for e in exclude if '*' in e):
                    continue
                if file in exclude:
                    continue

                local_file = os.path.join(root, file)
                remote_file = os.path.join(current_remote, file).replace('\\', '/')

                self.log(f"  Uploading: {file}")
                if self.upload_file(local_file, remote_file):
                    uploaded += 1
                else:
                    failed += 1

        self.log(f"✓ Uploaded {uploaded} files", 'success')
        if failed > 0:
            self.log(f"✗ Failed to upload {failed} files", 'error')

        return failed == 0

    def deploy(self, repo_url, branch='main'):
        """Execute full deployment pipeline"""
        self.log("=" * 70)
        self.log("  SFTP Deployment Pipeline")
        self.log("=" * 70)
        self.log(f"Repository: {repo_url}")
        self.log(f"Branch: {branch}")
        self.log(f"Remote: {self.sftp_user}@{self.sftp_host}:{self.remote_path}")
        self.log("=" * 70)
        print()

        try:
            # Setup working directory
            self.setup_work_directory()

            # Step 1: Pull from git
            if not self.git_pull(repo_url, branch):
                self.log("Deployment failed at git pull stage", 'error')
                return False

            # Step 2: Build project
            if not self.build_project():
                self.log("Deployment failed at build stage", 'error')
                return False

            # Step 3: Connect to SFTP
            if not self.connect_sftp():
                self.log("Deployment failed at SFTP connection stage", 'error')
                return False

            # Step 4: Upload files
            self.log("=" * 70)
            self.log("Step 4: Uploading Files to SFTP")
            self.log("=" * 70)

            if not self.upload_directory(self.work_dir, self.remote_path):
                self.log("Deployment failed at upload stage", 'error')
                return False

            # Success!
            print()
            self.log("=" * 70, 'success')
            self.log("  ✓ DEPLOYMENT SUCCESSFUL!", 'success')
            self.log("=" * 70, 'success')
            self.log(f"Files deployed to: {self.sftp_host}:{self.remote_path}", 'success')
            self.log(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 'success')
            self.log("=" * 70, 'success')

            return True

        except Exception as e:
            self.log(f"Deployment failed: {e}", 'error')
            return False

        finally:
            # Cleanup
            self.disconnect()
            if self.work_dir and os.path.exists(self.work_dir):
                try:
                    shutil.rmtree(self.work_dir)
                    self.log(f"Cleaned up working directory")
                except:
                    pass

    def disconnect(self):
        """Close SFTP connection"""
        try:
            if self.sftp:
                self.sftp.close()
            if self.client:
                self.client.close()
        except:
            pass


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='SFTP Deploy - Auto pull from git, build, and push to SFTP'
    )
    parser.add_argument('--repo', required=True, help='Git repository URL')
    parser.add_argument('--branch', default='main', help='Git branch (default: main)')
    parser.add_argument('--host', required=True, help='SFTP hostname')
    parser.add_argument('--port', type=int, default=22, help='SFTP port (default: 22)')
    parser.add_argument('--user', required=True, help='SFTP username')
    parser.add_argument('--password', required=True, help='SFTP password')
    parser.add_argument('--remote-path', default='/', help='Remote path on SFTP server')

    args = parser.parse_args()

    # Create deployer
    deployer = SFTPDeployer(
        sftp_host=args.host,
        sftp_port=args.port,
        sftp_user=args.user,
        sftp_password=args.password,
        remote_path=args.remote_path
    )

    # Run deployment
    success = deployer.deploy(args.repo, args.branch)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
