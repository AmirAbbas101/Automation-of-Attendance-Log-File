import csv
import os
from datetime import datetime, timedelta

def info():
    os.system("cls")
    row()
    print("\n\n\t\t\tAmir Abbas is the creator of this script.")
    print("\t\t\t\t\t002-BSCS-21\n")
    row()

def row():
    for i in range(1,90,1):
        print("*",end = "")


def process_attendance_log(current_index, file_path="AF4C211360651_attlog.dat"):
    filtered_data = []

    with open(file_path) as attendance_log:
        attendance_data = [line.replace("\t", " ").replace("\n", " ").strip() for line in attendance_log]

    filtered = [line for line in attendance_data if line.startswith(str(current_index))]

    for i in range(len(filtered)):
        current_timestamp = filtered[i][12:17]  # Extract timestamp (assuming timestamps are at positions 12:17)

        if i < len(filtered) - 1 and current_timestamp == filtered[i + 1][12:17]:
            # Check if the next element has the same timestamp
            if not filtered_data or filtered_data[-1][12:17] != current_timestamp:
                filtered_data.append(filtered[i])
        elif not filtered_data or filtered_data[-1][12:17] != current_timestamp:
            # If filtered_data is empty or the timestamps don"t match, add the current element to filtered_data
            filtered_data.append(filtered[i])
            
    return filtered_data

def extract_data(current_index, data_list):
    result_dict = {}
    user_id = str(current_index)

    for item in data_list:
        parts = item.split()

        # Check if parts has at least three elements before trying to access its elements
        if len(parts) >= 3:
            user_id = parts[0]
            date = parts[1]
            time = int(parts[2].split(":")[0])

            if user_id not in result_dict:
                result_dict[user_id] = {}

            if time <= 12:
                result_dict[user_id][date] = {"checkIn": parts[2], "checkOut": ""}
            else:
                if date not in result_dict[user_id]:
                    result_dict[user_id][date] = {"checkIn": "", "checkOut": parts[2]}
                else:
                    result_dict[user_id][date]["checkOut"] = parts[2]
        else:
            if user_id not in result_dict:
                result_dict[user_id] = {}
            result_dict[user_id][date] = {"checkIn": "", "checkOut": ""}
    return result_dict

def fill_missing_dates(result_dict, date_ranges):
    for user_id, dates in date_ranges.items():
        if len(dates) >= 1:      
            earliest_date, latest_date = dates[0], dates[-1]
            all_dates = [str((datetime.strptime(earliest_date, "%Y-%m-%d") + timedelta(days=i)).date()) for i in range((datetime.strptime(latest_date, "%Y-%m-%d") - datetime.strptime(earliest_date, "%Y-%m-%d")).days + 1)]
    
            for date in all_dates:
                if date not in result_dict[user_id]:
                    result_dict[user_id][date] = {"checkIn": "", "checkOut": ""}

def get_csv_data(user_data, start_date, end_date):
    data_row = ["checkIn", "checkOut"] * ((end_date - start_date).days + 1)
    for date, times in user_data.items():
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        if start_date <= date_obj <= end_date:
            index = (date_obj - start_date).days * 2
            data_row[index] = times["checkIn"]
            data_row[index + 1] = times["checkOut"]
    return data_row

def get_csv_header(start_date, end_date):
    header_row = [start_date.strftime("%Y-%m-%d")]
    while start_date < end_date:
        start_date += timedelta(days=1)
        header_row.append(start_date.strftime("%Y-%m-%d"))
    return header_row

def find_date_ranges(result_dict):
    return {user_id: sorted(result_dict[user_id].keys()) for user_id in result_dict}

def create_csv(index, result_dict, month_input):    
    start_date = datetime(datetime.now().year, month_input, 1)
    end_date = datetime(datetime.now().year, month_input % 12 + 1, 1) - timedelta(days=1) if month_input < 12 else datetime(datetime.now().year + 1, 1, 1) - timedelta(days=1)

    output_file_path = "output_all_records.csv"

    with open(output_file_path, "a", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        # if index == 205 or index == 101:
        #     csv_writer.writerow(["checkIn", "checkOut"] * ((end_date - start_date).days + 1))
        for user_id, user_data in result_dict.items():
            # Write each user"s data on a new row
            csv_writer.writerow(get_csv_data(user_data, start_date, end_date))


def main():
    info()
    file_path = input("\nEnter the attendance log file name without extension: ")+".dat"
    current_index = int(input("Enter the current index: "))
    end_index = 0
    month_input = int(input("Enter the month (1-12): "))
    
    if current_index == 101:
        end_index = 174
    else:
        end_index = 290
    
    while current_index <= end_index:
        data_list = process_attendance_log(current_index, file_path)
        result_dict = extract_data(current_index, data_list)
        # Check if the key exists in result_dict before accessing it
        if str(current_index) in result_dict:
            date_ranges = find_date_ranges(result_dict)
            fill_missing_dates(result_dict, date_ranges)
            sorted_data = {k: dict(sorted(v.items(), key=lambda x: x[0])) for k, v in result_dict[str(current_index)].items()}
            sorted_data = dict(sorted(sorted_data.items(), key=lambda x: x[0]))
            create_csv(current_index, result_dict, month_input)
        else:
            print(f"No data found for index {current_index}")
        current_index += 1
    
    print(f"CSV file created successfully.")
    current_index = input()


if __name__ == "__main__":
    main()