# Variables
TARGET_W = logargv
TARGET_R = rdiplog
TARGETS = $(TARGET_W) $(TARGET_R)

# User accounts
USER_W = sshlog
USER_R = rdiplog
# Shared log file
LOG_FILE = /var/log/remote_ip.log

.PHONY: all install clean

# 1. Build binaries
all: $(TARGETS)

$(TARGET_W): $(TARGET_W).cc
	$(CXX) $(TARGET_W).cc -O2 -o $(TARGET_W)
	@strip -s $(TARGET_W)

$(TARGET_R): $(TARGET_R).cc
	$(CXX) $(TARGET_R).cc -O2 -o $(TARGET_R)
	@strip -s $(TARGET_R)

# 2. Installation (Run with sudo permissions)
install: $(TARGETS)
	@echo "--- Starting Anchor Installation ---"
	
	@if id "$(USER_W)" >/dev/null 2>&1; then \
		echo "User [$(USER_W)] already exists."; \
	else \
		echo "Creating user [$(USER_W)] in 'adm' group..."; \
		sudo useradd -m -s /bin/bash -G adm $(USER_W); \
		sudo passwd $(USER_W); \
	fi

	@if id "$(USER_R)" >/dev/null 2>&1; then \
		echo "User [$(USER_R)] already exists."; \
		sudo usermod -aG adm $(USER_R); \
	else \
		echo "Creating user [$(USER_R)] and adding to 'adm' group..."; \
		sudo useradd -m -s /bin/bash -G adm $(USER_R); \
		sudo passwd $(USER_R); \
	fi

	sudo touch $(LOG_FILE)
	sudo chown $(USER_W):adm $(LOG_FILE)
	sudo chmod 640 $(LOG_FILE)

	
	sudo cp $(TARGET_W) /home/$(USER_W)/
	sudo chown $(USER_W):$(USER_W) /home/$(USER_W)/$(TARGET_W)
	
	sudo cp $(TARGET_R) /home/$(USER_R)/
	sudo chown $(USER_R):$(USER_R) /home/$(USER_R)/$(TARGET_R)
	
clean:
	rm -f $(TARGETS)

