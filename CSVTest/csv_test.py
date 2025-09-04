import csv

def avr_transaction_amount_csv(filename: str) -> float:
    with open(filename, 'r', encoding='utf-8') as csvfile:
        lines = csvfile.readlines()

    transactions = []

    for i in lines[1::]:
        _, amout = i.strip().split(',')
        transactions.append(float(amout))

    return sum(transactions) / len(transactions)


def avr_transaction_amount_csv2(filename: str) -> float:
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        amount = [float(row['transaction']) for row in reader]

    return sum(amount) / len(amount)


print(avr_transaction_amount_csv2('transaction.csv'))
