USER_LOCAL = ipmon
SERVICE_NAME = ip_monitor.service
PYTHON_SCRIPT = ip_monitor.py
SSH_CONFIG_SRC = ssh_config
KEY_FILE = /home/$(USER_LOCAL)/.ssh/sshlog
REMOTE_ALIAS = sshlog

.PHONY: all setup_user generate_key config_ssh install_service deploy_key start clean

# Default target: Performs all local initialization steps
all: setup_user generate_key config_ssh install_service

# 1. Create the local 'ipmon' system user
setup_user:
	@if id "$(USER_LOCAL)" >/dev/null 2>&1; then \
		echo "User [$(USER_LOCAL)] already exists."; \
	else \
		sudo useradd -m -s /bin/bash $(USER_LOCAL); \
	fi

# 2. Generate an Ed25519 key pair for secure, high-performance authentication
generate_key:
	@sudo -u $(USER_LOCAL) mkdir -p /home/$(USER_LOCAL)/.ssh
	@sudo -u $(USER_LOCAL) chmod 700 /home/$(USER_LOCAL)/.ssh
	@if [ ! -f $(KEY_FILE) ]; then \
		sudo -u $(USER_LOCAL) ssh-keygen -t ed25519 -f $(KEY_FILE) -N ""; \
	else \
		echo "SSH key already exists, skipping generation."; \
	fi

# 3. Deploy the pre-configured SSH alias settings
config_ssh:
	@sudo -u $(USER_LOCAL) cp $(SSH_CONFIG_SRC) /home/$(USER_LOCAL)/.ssh/config
	@sudo -u $(USER_LOCAL) chmod 600 /home/$(USER_LOCAL)/.ssh/config 

# 4. Install the systemd service file into the system directory
install_service:
	@sudo cp $(SERVICE_NAME) /etc/systemd/system/$(SERVICE_NAME)
	@sudo systemctl daemon-reload

# 5. Push the public key to the remote Anchor (Manual step required once)
# This uses the alias defined in the SSH config to locate the remote server.
deploy_key:
	@echo "Pushing public key to remote anchor via ssh-copy-id..."
	@echo "Note: You will be prompted for the 'sshlog' password on the remote server."
	sudo -u $(USER_LOCAL) ssh-copy-id -i $(KEY_FILE).pub $(REMOTE_ALIAS)

# 6. Enable and start the IPv6 monitoring service
start:
	@sudo systemctl enable $(SERVICE_NAME)
	@sudo systemctl start $(SERVICE_NAME)
	@echo "ipmon service is now active and monitoring IPv6 changes."

