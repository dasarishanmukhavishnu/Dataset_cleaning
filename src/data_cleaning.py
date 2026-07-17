import csv
from datetime import datetime

schema = {
    "Age": {"type": "int", "min": 22, "max": 50, "required": True},
    "Status": {"allowed": ["active", "inactive", "pending"], "required": True},
    "Salary": {"type": "float", "min": 1, "required": True},
    "Join_Date": {"type": "date", "required": True},
    "Performance_Score": {
        "allowed": ["average", "excellent", "good", "poor"],
        "required": True
    },
    "Phone": {"type": "phone", "required": False}
}

def validate_age(value, min_val=None, max_val=None):
    try:
        value = int(value)
        if min_val is not None and value < min_val:
            return None
        if max_val is not None and value > max_val:
            return None
        return value
    except:
        return None


def validate_salary(value, min_val=None):
    try:
        value = float(value)
        if min_val is not None and value < min_val:
            return None
        return value
    except:
        return None


def validate_date(date_str):
    formats = ("%d-%m-%Y", "%d/%m/%Y", "%m-%d-%Y", "%Y-%m-%d")
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime("%Y-%m-%d")
        except:
            continue
    return None


def validate_phone(value):
    try:
        value = str(abs(int(float(value))))
        return value
    except:
        return None

def validate_employee(emp):
    errors = []

    for field, rules in schema.items():
        if rules.get("required") and not emp.get(field):
            errors.append(f"{field} is required")

    if "Department_Region" in emp and "-" in emp["Department_Region"]:
        dept, region = emp["Department_Region"].split("-", 1)
        emp["Department"] = dept.strip()
        emp["Region"] = region.strip()
    else:
        errors.append("Invalid Department_Region")
        
    age = validate_age(emp.get("Age", ""), schema["Age"]["min"], schema["Age"]["max"])
    if age is None:
        errors.append("Invalid Age")
    else:
        emp["Age"] = age

    salary = validate_salary(emp.get("Salary", ""), schema["Salary"]["min"])
    if salary is None:
        errors.append("Invalid Salary")
    else:
        emp["Salary"] = salary

    status = emp.get("Status", "").strip().lower()
    if status not in schema["Status"]["allowed"]:
        errors.append("Invalid Status")
    else:
        emp["Status"] = status

    score = emp.get("Performance_Score", "").strip().lower()
    if score not in schema["Performance_Score"]["allowed"]:
        errors.append("Invalid Performance Score")
    else:
        emp["Performance_Score"] = score

    date = validate_date(emp.get("Join_Date", ""))
    if date is None:
        errors.append("Invalid Join_Date")
    else:
        emp["Join_Date"] = date

    phone = validate_phone(emp.get("Phone", ""))
    if emp.get("Phone") and phone is None:
        errors.append("Not Valid Phone.")
    else:
        emp["Phone"] = phone

    return errors

def process(file):
    valid_rows = []
    invalid_rows = []
    seen = set()  

    with open(file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            errors = validate_employee(row)
            row_tuple = tuple(sorted(row.items()))
            if row_tuple in seen:
                errors.append("Duplicate Record")
            else:
                seen.add(row_tuple)

            if not errors:
                valid_rows.append(row)
            else:
                row["Errors"] = "; ".join(errors)
                invalid_rows.append(row)

    return valid_rows, invalid_rows

def write_csv(filename, data):
    if not data:
        print(f"No data to write in {filename}")
        return

    fieldnames = data[0].keys()

    with open(filename, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def main():
    input_file = input("Enter employee CSV file path: ")

    print("Processing...")

    valid, invalid = process(input_file)

    write_csv("valid_employee.csv", valid)
    write_csv("invalid_employee.csv", invalid)

    print("\nCleaning Completed.")
    print(f"Valid Records: {len(valid)}")
    print(f"Invalid Records: {len(invalid)}")


if __name__ == "__main__":
    main()
