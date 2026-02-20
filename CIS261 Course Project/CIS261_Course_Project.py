# Darius Bell - CIS261 - Course Project Phase 3 #

from datetime import datetime

DATA_FILE = "payroll_data.txt"

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def is_valid_date_mmddyyyy(date_str: str) -> bool:
    """Validate mm/dd/yyyy date format."""
    try:
        datetime.strptime(date_str, "%m/%d/%Y")
        return True
    except ValueError:
        return False


# ------------------------------------------------------------
# Input Functions
# ------------------------------------------------------------
def get_pay_period():
    while True:
        from_date = input("Enter from date (mm/dd/yyyy): ").strip()
        if is_valid_date_mmddyyyy(from_date):
            break
        print("Invalid from date. Use mm/dd/yyyy (example: 02/19/2026).")

    while True:
        to_date = input("Enter to date (mm/dd/yyyy): ").strip()
        if is_valid_date_mmddyyyy(to_date):
            break
        print("Invalid to date. Use mm/dd/yyyy (example: 02/25/2026).")

    return from_date, to_date


def get_employee_name():
    return input("Enter employee name (or type 'End' to finish): ").strip()


def get_total_hours():
    while True:
        try:
            hours = float(input("Enter total hours worked: "))
            if hours < 0:
                print("Hours cannot be negative.")
                continue
            return hours
        except ValueError:
            print("Please enter a valid number for hours.")


def get_hourly_rate():
    while True:
        try:
            rate = float(input("Enter hourly rate: "))
            if rate < 0:
                print("Hourly rate cannot be negative.")
                continue
            return rate
        except ValueError:
            print("Please enter a valid number for hourly rate.")


def get_tax_rate():
    while True:
        try:
            tax_rate = float(input("Enter income tax rate (e.g., 0.20 for 20%): "))
            if tax_rate < 0 or tax_rate > 1:
                print("Tax rate must be between 0 and 1 (example: 0.20).")
                continue
            return tax_rate
        except ValueError:
            print("Please enter a valid number for tax rate (example: 0.20).")


# ------------------------------------------------------------
# Payroll Calculations / Display
# ------------------------------------------------------------
def calculate_pay(hours, rate, tax_rate):
    gross_pay = hours * rate
    income_tax = gross_pay * tax_rate
    net_pay = gross_pay - income_tax
    return gross_pay, income_tax, net_pay


def display_employee_info(name, hours, rate, gross, tax_rate, tax, net, from_date, to_date):
    print("\n--- Employee Pay Information ---")
    print(f"Pay Period: {from_date} to {to_date}")
    print(f"Name: {name}")
    print(f"Hours Worked: {hours:.2f}")
    print(f"Hourly Rate: ${rate:.2f}")
    print(f"Gross Pay: ${gross:.2f}")
    print(f"Tax Rate: {tax_rate:.2%}")
    print(f"Income Tax: ${tax:.2f}")
    print(f"Net Pay: ${net:.2f}")
    print("--------------------------------\n")


def display_totals(emp_count, total_hours, total_gross, total_tax, total_net):
    print("\n=== Payroll Summary (This Run) ===")
    print(f"Total Employees: {emp_count}")
    print(f"Total Hours: {total_hours:.2f}")
    print(f"Total Gross Pay: ${total_gross:.2f}")
    print(f"Total Income Tax: ${total_tax:.2f}")
    print(f"Total Net Pay: ${total_net:.2f}")
    print("=================================")


# ------------------------------------------------------------
# File I/O (Step 8 requirements)
# ------------------------------------------------------------
def write_record_to_file(file_name, from_date, to_date, name, hours, rate, tax_rate):
    """
    Open the text file so entered data is added to existing data.
    Write one pipe-delimited record:
    from_date|to_date|name|hours|rate|tax_rate
    """
    with open(file_name, "a", encoding="utf-8") as f:
        f.write(f"{from_date}|{to_date}|{name}|{hours}|{rate}|{tax_rate}\n")


def run_report(file_name):
    """
    After the user terminates the data entry loop:
    - Ask for the From Date to run the report (mm/dd/yyyy) or 'All'
    - Read records from file and display matching results
    - Calculate income tax and net pay for each record
    - Store totals in a dictionary inside the loop
    - Display totals after loop terminates
    """
    while True:
        report_from = input("\nEnter from date for report (mm/dd/yyyy) or 'All': ").strip()
        if report_from.lower() == "all" or is_valid_date_mmddyyyy(report_from):
            break
        print("Invalid entry. Type 'All' or enter a valid date in mm/dd/yyyy.")

    totals = {
        "employee_count": 0,
        "total_hours": 0.0,
        "total_tax": 0.0,
        "total_net_pay": 0.0
    }

    print("\n=========== FILE REPORT ===========")

    try:
        with open(file_name, "r", encoding="utf-8") as f:
            found_any = False

            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split("|")
                if len(parts) != 6:
                    continue  # skip bad lines safely

                from_date, to_date, name, hours_s, rate_s, tax_rate_s = parts

                # Filter: show all OR only matching from_date
                if report_from.lower() != "all" and from_date != report_from:
                    continue

                try:
                    hours = float(hours_s)
                    rate = float(rate_s)
                    tax_rate = float(tax_rate_s)
                except ValueError:
                    continue

                gross, tax, net = calculate_pay(hours, rate, tax_rate)

                # Display record details
                display_employee_info(name, hours, rate, gross, tax_rate, tax, net, from_date, to_date)
                found_any = True

                # Update totals (dictionary) inside loop
                totals["employee_count"] += 1
                totals["total_hours"] += hours
                totals["total_tax"] += tax
                totals["total_net_pay"] += net

        if not found_any:
            print("No matching records found.")

    except FileNotFoundError:
        print("No data file found yet. Enter employee records first.")
        return

    print("\n--- Report Totals ---")
    print(f"Total Employees: {totals['employee_count']}")
    print(f"Total Hours:     {totals['total_hours']:.2f}")
    print(f"Total Tax:       ${totals['total_tax']:.2f}")
    print(f"Total Net Pay:   ${totals['total_net_pay']:.2f}")
    print("===================================\n")


# ------------------------------------------------------------
# Main Program
# ------------------------------------------------------------
def main():
    employee_count = 0
    total_hours = 0.0
    total_gross = 0.0
    total_tax = 0.0
    total_net = 0.0

    from_date, to_date = get_pay_period()

    while True:
        name = get_employee_name()

        if name.lower() == "end":
            break

        hours = get_total_hours()
        rate = get_hourly_rate()
        tax_rate = get_tax_rate()

        gross, tax, net = calculate_pay(hours, rate, tax_rate)

        # Display current entry
        display_employee_info(name, hours, rate, gross, tax_rate, tax, net, from_date, to_date)

        # Write record to file (append)
        write_record_to_file(DATA_FILE, from_date, to_date, name, hours, rate, tax_rate)

        # Totals for this run
        employee_count += 1
        total_hours += hours
        total_gross += gross
        total_tax += tax
        total_net += net

    # Display totals for the current run
    display_totals(employee_count, total_hours, total_gross, total_tax, total_net)

    # After loop ends, run the file report
    run_report(DATA_FILE)


if __name__ == "__main__":
    main()