import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from pymongo import MongoClient

#--Connect to Mongodb--
client=MongoClient('mongodb://localhost:27017/')
db = client["expense_tracker"]
collection = db["expenses"]
# --- Data Handling ---
def load_expenses():
    return list(collection.find({},{"_id":0}))

def add_expense():
    category = category_entry.get()
    amount = amount_entry.get()
    date = date_entry.get()

    if category and amount and date:
        expense={"category":category,"amount":amount,"date":date}
        collection.insert_one(expense)
        refresh_table()
        messagebox.showinfo("Success,Expense added successfully!")
    else:
        messagebox.showerror("Error","Please fill in all fields.")
def delete_expense():
    selected_expense=table.selection()
    if selected_expense:
        values=table.item(selected_expense,"values")
        collection.delete_one({"category":values[0],"amount":values[1],"date":values[2]})
        refresh_table()
        messagebox.showinfo("Success","Expense deleted successfully!")
    else:
        messagebox.showerror("Error","Please select an expense to delete.")

def refresh_table():
    for row in table.get_children():
        table.delete(row)
    for expense in load_expenses():
        table.insert("",tk.END,values=(expense["category"],expense["amount"],expense["date"]))


# def save_expenses():
#     with open("expenses.txt", "w") as file:
#         for expense in expenses:
#             file.write(f"{expense['category']},{expense['amount']},{expense['date']}\n")

# def load_expenses():
#     try:
#         with open("expenses.txt", "r") as file:
#             for line in file:
#                 category, amount, date = line.strip().split(",")
#                 expenses.append({"category": category, "amount": amount, "date": date})
#     except FileNotFoundError:
#         pass

# --- UI Functions ---
# def add_expense():
#     category = category_entry.get()
#     amount = amount_entry.get()
#     date = date_entry.get()

#     if category and amount and date:
#         expense = {"category": category, "amount": amount, "date": date}
#         expenses.append(expense)
#         category_entry.delete(0, tk.END)
#         amount_entry.delete(0, tk.END)
#         date_entry.delete(0, tk.END)
#         messagebox.showinfo("Success", "Expense added successfully!")
#         save_expenses()  # Save after adding
#     else:
#         messagebox.showerror("Error", "Please fill in all fields.")

# --- Visualization ---
def show_chart():
    expenses =load_expenses()
    if not expenses:
        messagebox.showwarning("No Data","No expenses to display.")
        return 
    
    categories = [expense["category"] for expense in expenses]
    amounts = [float(expense["amount"]) for expense in expenses] 
    plt.figure(figsize=(6,4))
    plt.bar(categories, amounts,color='skyblue')
    plt.xlabel("Categories")
    plt.ylabel("Amount")
    plt.title("Expense Summary")
    plt.xticks(rotation=45)
    plt.show() 

# --- Main Window ---
root = tk.Tk()
root.title("Expense Tracker")

# --- UI Elements ---
category_label = tk.Label(root, text="Category:")
amount_label = tk.Label(root, text="Amount:")
date_label = tk.Label(root, text="Date:")

category_entry = tk.Entry(root)
amount_entry = tk.Entry(root)
date_entry = tk.Entry(root)

add_button = tk.Button(root, text="Add Expense", command=add_expense)
delete_button = tk.Button(root, text="Delete Expense", command=delete_expense) #  Delete buttons if needed) 
chart_button = tk.Button(root, text="Show Chart", command=show_chart)


# --- Table to Display Expenses ---
table = ttk.Treeview(root, columns=("Category", "Amount", "Date"), show="headings")
table.heading("Category", text="Category")
table.heading("Amount", text="Amount")
table.heading("Date", text="Date")
# --- Layout Using Grid ---
category_label.grid(row=0, column=0, padx=5, pady=5)
category_entry.grid(row=0, column=1, padx=5, pady=5)
amount_label.grid(row=1, column=0, padx=5, pady=5)
amount_entry.grid(row=1, column=1, padx=5, pady=5)
date_label.grid(row=2, column=0, padx=5, pady=5)
date_entry.grid(row=2, column=1, padx=5, pady=5)
add_button.grid(row=3, column=0, padx=5, pady=5)
delete_button.grid(row=3, column=1, padx=5, pady=5)
chart_button.grid(row=4, column=0, columnspan=2, pady=10)
table.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# --- Load Data When App Starts ---
refresh_table()

# --- Run Application ---
root.mainloop()