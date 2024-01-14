#!/bin/bash

# --------- Functions

# Function to print colored messages
print_colored_message() {
    local color="$1"
    local message="$2"
    
    case "$color" in
        "red")    echo -e "\e[91m$message\e[0m" ;;
        "green")  echo -e "\e[92m$message\e[0m" ;;
        "yellow") echo -e "\e[93m$message\e[0m" ;;
        "blue")   echo -e "\e[94m$message\e[0m" ;;
        "purple") echo -e "\e[95m$message\e[0m" ;;
        "cyan")   echo -e "\e[96m$message\e[0m" ;;
        "white")  echo -e "\e[97m$message\e[0m" ;;
        *)
            echo "Invalid color specified"
            return 1
            ;;
    esac
}

# Function to prompt user to press Enter
press_enter() {
    print_colored_message "cyan" "Press Enter to continue..."
    read -r
}

# Function to display and execute a command
run_command() {
    echo "Running command:"
    print_colored_message "blue" "$1"
    press_enter
    eval "$1"
    echo ""
    press_enter
}


# --------- Main

# Variables declaration
SESSION_ID=""
CSRF_TOKEN=""
SESSION=""
ORIGIN="expected_origin"

# Clear terminal
clear


# --------- CSRF
print_colored_message "green" "Test - CSRF"

# Get all data
run_command "curl -i -X GET http://localhost:8000/data/all"

# Login 
run_command "login_response=\$(curl -i -X POST http://localhost:8000/login -H \"Content-Type: application/json\" -d '{\"username\": \"username\", \"password\": \"password\"}')"

# Extract cookies from the login response
SESSION_ID=$(echo "$login_response" | grep -oP 'session_id=\K[^;]+')
CSRF_TOKEN=$(echo "$login_response" | grep -oP 'csrf_token=\K[^;]+')
SESSION=$(echo "$login_response" | grep -oP 'session=\K[^;]+')

# Get all data with cookies
run_command "curl -i -X GET -H \"Cookie: csrf_token=$CSRF_TOKEN; session=$SESSION; session_id=$SESSION_ID\" http://localhost:8000/data/all"

# Create CSRF Headers variable
CSRF_HEADERS="\"Origin: expected_origin\" -H \"Cookie: csrf_token=$CSRF_TOKEN; session=$SESSION; session_id=$SESSION_ID\""
CSRF_HEADERS_XSS="\"Origin: expected_origin\" -H \"Cookie: my_cookie=<script>alert(\"XSSAttack\")</script>; csrf_token=$CSRF_TOKEN; session=$SESSION; session_id=$SESSION_ID\""

# Get all data with origin header and insert new information
run_command "curl -i -X GET -H $CSRF_HEADERS http://localhost:8000/data/all"
run_command "curl -i -X POST -H $CSRF_HEADERS -H \"Content-Type: application/json\" -d '[{\"driver\": \"Paul\", \"temperature\": 18, \"speed\": 50}, {\"driver\": \"John\", \"temperature\": 20, \"speed\": 80}]' http://localhost:8000/data/add/many"
run_command "curl -i -X GET -H $CSRF_HEADERS http://localhost:8000/data/all"


# --------- File inclusion
print_colored_message "green" "Test - File Inclusion Vulnerability"
run_command "curl -i -X GET -H $CSRF_HEADERS http://localhost:8000/data/all?file=/safe_directory/somefile.txt"
run_command "curl -i -X GET -H $CSRF_HEADERS http://localhost:8000/data/all?file=/unsafe_directory/somefile.txt"
run_command "curl -i -X GET -H $CSRF_HEADERS http://localhost:8000/data/all?file=/safe_directory/../somefile.txt"
run_command "curl -i -X GET -H $CSRF_HEADERS http://localhost:8000/data/all?file=/safe_directory/somefile"


# --------- SQL Injection and Origin Blacklist
print_colored_message "green" "Test - SQL Injection and Origin Blacklist"
run_command "curl -i -X GET -H $CSRF_HEADERS http://localhost:8000/data/id/select%20*%20from%20users%20where%20id%20=%201%20or%201%20=%201%20--%201"
run_command "curl -i -X GET -H $CSRF_HEADERS http://localhost:8000/data/id/0"
print_colored_message "yellow" "Delete banned IP from 'waf/app/validators/black_list_files/list.csv'"
press_enter
run_command "curl -i -X GET -H $CSRF_HEADERS http://localhost:8000/data/id/0"


# --------- XSS
print_colored_message "green" "Test - XSS"
run_command "curl -i -X GET -H $CSRF_HEADERS 'http://localhost:8000/data/all?query_param=<script>alert(\"XSSAttack\")</script>'"
run_command "curl -i -X GET -H $CSRF_HEADERS -H \"X-My-Header: <script>alert(\"XSSAttack\")</script>\" http://localhost:8000/data/all"
run_command "curl -i -X GET -H $CSRF_HEADERS_XSS http://localhost:8000/data/all"

# End
print_colored_message "green" "Test flow completed successfully"
