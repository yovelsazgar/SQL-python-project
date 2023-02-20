from persistence import *

def main():
    print("Activities")
    ordered = repo.activities.getRecordsByDate()
    for row in ordered:
        to_print = (row.product_id, row.quantity, row.activator_id, row.date)
        print(to_print)

    print("Branches")
    ordered = repo.branches.getRecordsById()
    for row in ordered:
        to_print = (row.id, row.location, row.number_of_employees)
        print(to_print)

    print("Employees")
    ordered = repo.employees.getRecordsById()
    for row in ordered:
        to_print = (row.id, row.name, row.salary, row.branche)
        print(to_print)

    print("Products")
    ordered = repo.products.getRecordsById()
    for row in ordered:
        to_print = (row.id, row.description, row.price, row.quantity)
        print(to_print)

    print("Suppliers")
    ordered = repo.suppliers.getRecordsById()
    for row in ordered:
        to_print = (row.id, row.name, row.contact_information)
        print(to_print)

    print()
    print("Employees report")

    c = repo._conn.cursor()
    c.execute("""SELECT employees.name, employees.salary, branches.location, SUM(activities.quantity * -1*products.price) 
                    FROM employees 
                    LEFT JOIN branches ON employees.branche = branches.id
                    LEFT JOIN activities ON activities.activator_id = employees.id
                    LEFT JOIN products ON products.id = activities.product_id
                    GROUP BY employees.id
                    ORDER BY employees.name """)

    all = c.fetchall()
    for worker in all:
        if worker[3] == None:
            details = (worker[0], worker[1], worker[2], 0)
            print(*details)
        else:
            details = (worker[0], worker[1], worker[2], worker[3])
            print(*details)

    print()
    print("Activities report")
    c = repo._conn.cursor()
    c.execute("""SELECT activities.date, products.description, activities.quantity, employees.name, suppliers.name 
                    FROM activities
                    LEFT JOIN products ON products.id = activities.product_id
                    LEFT JOIN employees ON employees.id = activities.activator_id
                    LEFT JOIN suppliers ON suppliers.id = activities.activator_id
                    ORDER BY activities.date""")

    all = c.fetchall()
    for worker in all:
        date = worker[0]
        description = worker[1]
        quantity = worker[2]
        employee = worker[3]
        supplier = worker[4]
        if quantity < 0:
            supplierName = None
        details = (date, description, quantity, employee, supplier)
        if (date != None):
            print(details)


if __name__ == '__main__':
    main()