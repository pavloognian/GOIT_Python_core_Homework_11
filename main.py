from collections import UserDict
from collections.abc import Iterator
from datetime import datetime, timedelta
import re



class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value
        

    @property
    def value(self):
        return self.__value
        
    @value.setter
    def value(self, value):
        self.__value = value




class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
    
    @Field.value.setter
    def value(self, value):
        if type(value) == str:
            if len(value) > 10:
                return "Wrong format for birthday. Should be: 'year-month-day'"
            else:
                res = re.findall("\d{0,4}-\d{1,2}-\d{1,2}", value)
                if res == []:
                    return "Wrong format for birthday. Should be: 'year-month-day'"
                else:
                    Field.value.fset(self, value)
        else:
            return "Wrong format for birthday. Should be string format."

    

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
    
    @Field.value.setter
    def value(self, value):
        if len(value) > 17:
            return "You wrote wrong phone. Example for correct phone: '+380 96 xxx-xx-xx' | '+380 63 xxx-xx-xx'"
        else:
            res = re.findall("\+\d{3} \d{2} \d{3}-\d{2}-\d{2}", value)
            if res == []:
                return "You wrote wrong phone. Example for correct phone: '+380 96 xxx-xx-xx' | '+380 63 xxx-xx-xx'"
            else:
                Field.value.fset(self, value)
    
class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        Field.value.fset(self, value)
        

class Record:
    def __init__(self, name: Name, phone=None, birthday = Birthday):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday #"2011-07-26"

    def add_phone(self, phone):
        phone_number = Phone(phone)
        if phone_number not in self.phones:
            self.phones.append(phone_number)

    def delete_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone

    def find_phone(self, value):
        pass

    def days_to_birthday(self):
        # self.birthday = '2023-08-29'
        if self.birthday != None:
            date_of_birth = datetime.strptime(self.birthday, '%Y-%m-%d').date()

            current_data = datetime.now().date()
            diff = (date_of_birth - current_data).days
            return diff
        else:
            return "You didn't write birthday."


class Iterator():
    def __init__(self, value_to_show, length_of_AddressBook, data):
        self.value_to_show = value_to_show
        self.length_of_AddressBook = length_of_AddressBook
        self.end = value_to_show
        self.data = data
        # print(data)
        self.dict = {}
        self.count = 0
        count = 0
        for key in self.data.keys():
            self.dict[count] = key
            count+=1
        #print(self.dict)
        self.flag = True
        self.first_itteration = True




    def __next__(self):
        list_to_show_1 = []
        list_to_show_2 = []
        
        if self.flag:
            if self.end <= self.length_of_AddressBook:
                #print("@@@@")
                for _ in range(0, self.value_to_show):
                    key = self.dict.get(self.count)
                    temp_dict = {}
                    temp_dict['Name'] = key
                    temp_dict['Contact'] = self.data[key]
                    list_to_show_1.append(temp_dict)
                    # print(key, self.data[key])
                    self.count+=1
                if self.end == self.length_of_AddressBook:
                    self.flag = False
                self.end += self.value_to_show
                self.first_itteration = False
                return list_to_show_1
            else:
                #print("$$$")
                #print(self.end)
                if self.first_itteration:
                    self.end = self.end - (self.end - self.length_of_AddressBook) #for first
                else:
                    self.end = self.end - self.value_to_show
                    self.end = self.length_of_AddressBook - self.end
                #print(self.end)
                for f in range(0, self.end):
                    key = self.dict.get(self.count)
                    temp_dict = {}
                    temp_dict['Name'] = key
                    #print(key)
                    #print(self.data[key])
                    temp_dict['Contact'] = self.data[key]
                    list_to_show_2.append(temp_dict)
                    # print("Name:",key,"| Contact:", self.data[key])
                    self.count+=1
                self.flag = False
                return list_to_show_2
        else:
            raise StopIteration



        # if self.end < self.length_of_AddressBook:
        #     count = self.start
        #     for _ in range(self.start, self.end):
        #         key = self.dict.get(count)
        #         print(key, self.data[key])
        #         count+=1
        #     self.start = self.end
        #     self.end += 6

        # else:
        #     self.end = self.length_of_AddressBook - self.end
        #     count = self.start
        #     for _ in range(self.start, self.end):
        #         key = self.dict.get(count)
        #         print(key, self.data[key])
        #         count+=1
        #     self.start = self.end
        #     self.end += 6
        # else:
        #     raise StopIteration

        


class AddressBook(UserDict):
    def __iter__(self) -> Iterator:
        return Iterator(self.value_to_show, len(self.data), self.data)


    def how_many_to_show(self, value):
        self.value_to_show = value

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find_record(self, value):
        return self.data.get(value)

if __name__ == "__main__":
    name = Name('Bill')
    # print(name.value)
    phone = Phone('+380 96 345-54-76')
    birthday = Birthday('2011-9-26')
    rec = Record(name, phone, birthday)
    rec.add_phone('+380 96 111-22-33')
    ab = AddressBook()
    ab.add_record(rec)

    name = Name('John')
    # print(name.value)
    phone = Phone('+380 96 574-87-21')
    birthday = Birthday('2023-04-12')
    rec = Record(name, phone, birthday)
    rec.add_phone('+380 63 333-32-23')
    ab.add_record(rec)

    name = Name('Anna')
    # print(name.value)
    phone = Phone('+380 63 453-54-22')
    birthday = Birthday('2022-03-01')
    rec = Record(name, phone, birthday)
    rec.add_phone('+380 96 331-32-21')
    ab.add_record(rec)

    name = Name('Rolandos')
    # print(name.value)
    phone = Phone('+380 63 453-54-22')
    birthday = Birthday('2022-03-01')
    rec = Record(name, phone, birthday)
    rec.add_phone('+380 96 331-32-21')
    ab.add_record(rec)

    # print(ab['Bill'])
    # assert isinstance(ab['Bill'], Record)
    # assert isinstance(ab['Bill'].name, Name)
    # assert isinstance(ab['Bill'].phones, list)
    # assert isinstance(ab['Bill'].phones[0], Phone)
    # assert ab['Bill'].phones[0].value == '+380 96 345-54-76'
    # print('All Ok)')
    # print("-"*50)

    # for phone in map(lambda x: x.value, ab['Bill'].phones[:]):
    #     print(phone)
    # print(ab['Bill'].birthday.value)
    ab.how_many_to_show(3)
    for i in ab:
        if i == []:
            print(i)
            break
        print(i,'\n')

