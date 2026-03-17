#include <iostream>
#include <fstream>
#include <string>
#include <algorithm>
#include <iterator>

/**
 * Program: Log Parser (C++14)
 * Purpose: Extract the timestamp and the latest IPv6 from the log file.
 * Format: [Timestamp] IPv6
 */
int main() {
    const std::string filePath = "/var/log/remote_ip.log";

    std::ifstream file(filePath, std::ios::in | std::ios::binary);
    if (!file) {
        std::cerr << "Error: Could not open " << filePath << std::endl;
        return 1;
    }

    // Load file into memory for efficient backward scanning
    std::string content((std::istreambuf_iterator<char>(file)), 
                         std::istreambuf_iterator<char>());

    if (content.empty()) {
        std::cout << "The log file is empty." << std::endl;
        return 0;
    }

    size_t endPos = content.size();
    bool found = false;

    // Scan backwards line by line
    while (endPos > 0) {
        size_t newlinePos = content.find_last_of('\n', endPos - 1);
        size_t lineStart = (newlinePos == std::string::npos) ? 0 : newlinePos + 1;
        std::string line = content.substr(lineStart, endPos - lineStart);

        // Remove carriage return for cross-platform compatibility
        if (!line.empty() && line.back() == '\r') line.pop_back();

        // Check if line contains IPv6 marker and is not a Renew log
        if (!line.empty() && 
            line.find(':') != std::string::npos && 
            line.find("Renew") == std::string::npos) {

            // 1. Extract Timestamp: Find content between '[' and ']'
            size_t openBracket = line.find('[');
            size_t closeBracket = line.find(']');
            
            // 2. Extract IP: Get the part after the last space
            size_t lastSpace = line.find_last_of(' ');

            if (openBracket != std::string::npos && closeBracket != std::string::npos && lastSpace != std::string::npos) {
                std::string timestamp = line.substr(openBracket, closeBracket - openBracket + 1);
                std::string ip = line.substr(lastSpace + 1);

                // Output combined result
                std::cout << timestamp << " " << ip << std::endl;
                found = true;
                break; 
            }
        }

        if (newlinePos == std::string::npos) break;
        endPos = newlinePos;
    }

    if (!found) {
        std::cout << "No valid IPv6 entry found." << std::endl;
    }

    return 0;
}

