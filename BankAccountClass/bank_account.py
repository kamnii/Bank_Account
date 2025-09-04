from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
import csv


class BankAccount:   # Комиссия, взимается за переводы между счетами.
    exchange_rate = Decimal('87.36')

    def __init__(self, account_number):
        self.account_number = account_number
        self.is_blocked = False
        self.balance_usd = Decimal('0.00')
        self.balance_kgs = Decimal('0.00')
        self.history_file = f'TransactionsHistory/history_{self.account_number}.csv'

        try:        # Создание csv файла с историями транзакций.
            with open(self.history_file, 'x', newline="", encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['date', 'operation', 'amount', 'target_account'])
        except (FileExistsError, PermissionError, IOError) as e:
            pass

    
    def _add_history(self, operation, amount, target_account=""):        # Добавление данных о транзакциях в csv файлы.
        with open(self.history_file, 'a', newline="", encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), operation, amount, target_account])


    def _round_decimal(self, value: Decimal) -> Decimal:
        return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


    def check_history(self):         # Просмотр истории транзакций.
        try:
            with open(self.history_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                reader_lst = []

                for row in reader:
                    reader_lst.append(row)

                return reader_lst

        except FileNotFoundError:
            return 'История операций не найдена.'
        

    def set_exchange_rate(self, new_rate: Decimal):
        self.exchange_rate = Decimal(str(new_rate))

        return f'Курс обновлен: 1 USD = {self._round_decimal(self.exchange_rate)} KGS.'


    def deposit(self, amount: Decimal, currency='KGS'):       # Пополнение баланса.
        if self.is_blocked is True:
            return 'Ошибка пополнения. Ваш аккаунт заблокирован!'
        
        if amount < 0:
            return 'Ошибка! Сумма пополнения не может быть отрицательной.'
        
        amount = Decimal(str(amount))

        if currency == 'KGS':
            self.balance_kgs += amount
        elif currency == 'USD':
            self.balance_usd += amount
        else:
            return 'Счета для такой валюты нет.'

        self._add_history('deposit', self._round_decimal(amount))
        self._add_history('currency', currency)
        return f'На счет {self.account_number} {currency} внесена сумма: {self._round_decimal(amount)}. Текущий баланс: KGS - {self._round_decimal(self.balance_kgs)}, USD - {self._round_decimal(self.balance_usd)}.'

    
    def withdraw(self, amount: Decimal, currency='KGS'):        # Снятие денег с баланса.
        if self.is_blocked is True:
            return 'Ошибка снятия денег. Ваш аккаунт заблокирован!'
        
        if amount < 0:
            return 'Ошибка! Сумма снятия не может быть отрицательной.'
        
        amount = Decimal(str(amount))

        if currency == 'KGS':
            if amount > 100000:
                return 'Нельзя снять больше 100 000 KGS за одну операцию.'

            if self.balance_kgs >= amount:
                self.balance_kgs -= amount
                self._add_history('withdraw', self._round_decimal(amount))
                self._add_history('currency', currency)
                return f'Со счета {self.account_number} KGS снята сумма: {self._round_decimal(amount)}. Текущий баланс: {self._round_decimal(self.balance_kgs)}.'
            else:
                return f'Ошибка! На счету {self.account_number} - KGS недостаточно средств для снятия суммы: {self._round_decimal(self.balance_kgs)}.'

        elif currency == 'USD':
            if amount > 3500:
                return 'Нельзя снять больше 3 500 USD за одну операцию.'
            
            if self.balance_usd >= amount:
                self.balance_usd -= amount
                self._add_history('withdraw', self._round_decimal(amount))
                self._add_history('currency', currency)
                return f'Со счета {self.account_number} - USD снята сумма: {self._round_decimal(amount)}. Текущий баланс: {self._round_decimal(self.balance_usd)}.'
            else:
                return f'Ошибка! На счету {self.account_number} - USD недостаточно средств для снятия суммы: {self._round_decimal(self.balance_usd)}.'
            
        else:
            return 'Счетов с другой валютой нет.'

        
    def check_balance(self):       # Проверка баланса.
        if self.is_blocked is True:
            return 'Ошибка проверки. Ваш аккаунт заблокирован!'

        self._add_history('chek_balance', f'USD-{self._round_decimal(self.balance_usd)}/KGS-{self._round_decimal(self.balance_kgs)}')
        return f'Текущий баланс: KGS - {self._round_decimal(self.balance_kgs)}; USD - {self._round_decimal(self.balance_usd)}.'
    

    def transfer(self, target_account, amount: Decimal, currency='KGS', target_currency='KGS'):       # Переводы между счетами, где взимается комиссия 1% за перевод.
        if self.is_blocked is True:
            return 'Ошибка перевода. Ваш аккаунт заблокирован!'
        
        if amount < 0:
            return 'Ошибка! Сумма перевода должна быть положительной.'
        
        amount = Decimal(str(amount))

        if currency == 'KGS':
            comission = amount / Decimal('100')
            total_debit = comission + amount
            if self.balance_kgs >= total_debit:
                self.balance_kgs -= total_debit
                if target_currency == 'KGS':
                    target_account.balance_kgs += amount
                    self._add_history('transfer_KGS/KGS', self._round_decimal(amount), target_account.account_number)
                    self._add_history('comission', self._round_decimal(comission), target_account.account_number)
                    return f'Перевод: со счета {self.account_number} KGS в счет {target_account.account_number} KGS. Сумма перевода: {self._round_decimal(amount)}. Комиссия составила: {self._round_decimal(comission)}.'
                elif target_currency == 'USD':
                    target_account.balance_usd += amount / self.exchange_rate
                    self._add_history('transfer_KGS/USD', f'KGS-{self._round_decimal(amount)}/USD-{self._round_decimal(amount/self.exchange_rate)}', target_account.account_number)
                    self._add_history('comission', self._round_decimal(comission), target_account.account_number)
                    return f'Перевод: со счета {self.account_number} KGS в счет {target_account.account_number} USD. Сумма перевода: KGS {self._round_decimal(amount)} -> USD {self._round_decimal(amount/self.exchange_rate)}. Комиссия составила: {self._round_decimal(comission)}.'
                else: 
                    return 'Счета с такой валютой нет.'
            else:
                return f'Ошибка! Недостаточно средств на счете: {self._round_decimal(self.balance_kgs)}'
            
        elif currency == 'USD':
            comission = amount / Decimal('100')
            total_debit = comission + amount
            if self.balance_usd >= total_debit:
                self.balance_usd -= total_debit
                if target_currency == 'KGS':
                    target_account.balance_kgs += amount * self.exchange_rate
                    self._add_history('transfer_USD/KGS', f'USD-{self._round_decimal(amount)}/KGS-{self._round_decimal(amount*self.exchange_rate)}', target_account.account_number)
                    self._add_history('comission', self._round_decimal(comission), target_account.account_number)
                    return f'Перевод: со счета {self.account_number} USD в счет {target_account.account_number} KGS. Сумма перевода: USD {self._round_decimal(amount)} -> KGS {self._round_decimal(amount)*self.exchange_rate}. Комиссия составила: {self._round_decimal(comission)}.'
                elif target_currency == 'USD':
                    target_account.balance_usd += amount
                    self._add_history('transfer_USD/USD', self._round_decimal(amount), target_account.account_number)
                    self._add_history('comission', self._round_decimal(comission), target_account.account_number)
                    return f'Перевод: со счета {self.account_number} KGS в счет {target_account.account_number} USD. Сумма перевода: {self._round_decimal(amount)}. Комиссия составила: {self._round_decimal(comission)}.'
                else: 
                    return 'Счета с такой валютой нет.'

            else:
                return f'Ошибка! Недостаточно средств на счете {self._round_decimal(self.balance_usd)}'
        

    def accrual_interest(self, percent, currency='KGS'):      # Начисление процента на счет.
        percent = Decimal(str(percent))
        if currency == 'KGS':
            if self.balance_kgs > 0:
                amount = self.balance_kgs * percent / Decimal('100')
                self.balance_kgs += amount
                self._add_history('interest_accrual', amount)
                return f'На баланс {self.account_number} начислен процент {self._round_decimal(percent)}% на остаток. Сумма начисления: {self._round_decimal(amount)}'
            else:
                return f'Ошибка. Баланс счета {self.account_number} KGS пуст.'

        elif currency == 'USD':
            if self.balance_usd > 0:
                amount = self.balance_usd * percent / Decimal('100')
                self.balance_usd += amount
                self._add_history('interest_accrual', amount)
                return f'На баланс {self.account_number} начислен процент {self._round_decimal(percent)}% на остаток. Сумма начисления: {self._round_decimal(amount)}'
            else:
                return f'Ошибка. Баланс счета {self.account_number} USD пуст.'
            
        else:
            return 'Счета с такой валютой нет.'
        

    def account_status(self):
        if self.is_blocked is False:
            self.is_blocked = True
            self._add_history('account_blocked', self.is_blocked)
            return f'Счета {self.account_number} заблокированы.'
        else:
            self.is_blocked = False
            self._add_history('account_unblocked', self.is_blocked)
            return f'Счета {self.account_number} разблокированы.'
        

    def deposite_interest(self, amount, percent, month):           # Сколько получит клиент при взносе депозита под годовой процент
        return self._round_decimal(Decimal(str(amount)) * Decimal(str(percent)) / Decimal('100') / Decimal('12') * Decimal(str(month)))
