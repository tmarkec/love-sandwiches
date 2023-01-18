import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
        sales_data = data_str.split(",")
        # removes comas from the strings

        if validate_data(sales_data):
            print("Data is valid")
            break
    return sales_data


def validate_data(values):
    """ 
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )

    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


# def update_sales_worksheet(data):
#     """
#     Update sales worksheet, add new row with the list data provided.
#     """
#     print("Updating sales worksheet...\n")
#     # grab our spreadsheet and update it with our input on last row
#     sales_worksheet = SHEET.worksheet("sales")
#     sales_worksheet.append_row(data)
#     print("Sales worksheet updates successfully.\n")


def calculate_surplus(sales_row):
    """
    Compare sales with stock and calculate surplus for each item.
    Positive indicate waste.
    Negatice indicate extra made when stoc was sold out.
    """
    print("Surplus data calculation is starting.....")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    # creating loop to go through are sales and stock data
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data


# def update_surplus_worksheet(data):
#     """
#     Update surplus worksheet, add new row with the new surplus.
#     """
#     print("Updating surplus worksheet...\n")
#     surplus_worksheet = SHEET.worksheet("surplus")
#     surplus_worksheet.append_row(data)

#     print("Surplus worksheet has been updated")


def update_worksheet(data, worksheet):
    """
    Recives a list of integers to be inserted into workshee.
    Update the relevant worksheet with data provided.
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)

    print(f"Worksheet {worksheet} has been updated")


def get_last_5_entries():
    """
    Collect collumns of data from sales worksheet, collecting last 5 entries
    and returns the data as list of list.
    """
    sales = SHEET.worksheet('sales')
  
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns


def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...")

    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / 5
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data


def main():
    """
    Run all program function
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    # loop that goes through all numbers in 'data' and convert them to integers
    update_worksheet(sales_data, 'sales')
    # update_sales_worksheet(sales_data)
    new_surplus_date = calculate_surplus(sales_data)
    update_worksheet(new_surplus_date, 'surplus')
    sales_column = get_last_5_entries()
    stock_data = calculate_stock_data(sales_column)
    update_worksheet(stock_data, 'stock')
    

print("Welcome to Love Sandwiches Data Automation")


main()