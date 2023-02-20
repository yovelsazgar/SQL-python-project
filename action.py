from persistence import *

import sys

def main(args : list[str]):
    inputfilename : str = args[1]
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list[str] = line.strip().split(", ")
            #TODO: apply the action (and insert to the table) if possible
            productId = splittedline[0]
            quantity = int(splittedline[1])
            date = splittedline[3]
            currQuantity = repo.products.find(id=productId)[0].quantity

            if quantity != 0:
                # supplier
                if quantity > 0:
                    supplierId = splittedline[2]
                    repo.products.updateQuantity(quantity + currQuantity, productId)
                    repo.activities.insert(Activitie(productId, quantity, supplierId, date))
                # sale
                else:
                    employeeId = splittedline[2]
                    if quantity + currQuantity > 0:
                        repo.products.updateQuantity(quantity + currQuantity, productId)
                        repo.activities.insert(Activitie(productId, quantity, employeeId, date))

if __name__ == '__main__':
    main(sys.argv)