#include <iostream>
#include <fstream>
#include <chrono>
#include <ctime>
#include <string>
#include <cstdlib>

int main(int argc, char* argv[]) {
    auto now = std::chrono::system_clock::now();
    auto time = std::chrono::system_clock::to_time_t(now);
    std::string timestamp = std::ctime(&time);
    if (!timestamp.empty()) timestamp.pop_back();

    std::string passed_data;
    if (argc > 2) {
        passed_data = argv[1];
    } else {
        passed_data = "No Parameter";
    }

    std::ofstream log_file("/var/log/remote_ip.log", std::ios_base::app);
    
    if (log_file.is_open()) {
        log_file << "[" << timestamp << "] " << passed_data << std::endl;
        log_file.close();
    } else {
        std::cerr << "File error: Could not open log file. (Check permissions)" << std::endl;
        return 1;
    }
    return 0;
}

