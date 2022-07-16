import random
# import pyperclip

PASSWORD_LENGTH = 10
SPECIAL_CHARACTERS = 3
PASSWORD_NUMBERS = 5
PASSWORD_CHARACTERS = PASSWORD_LENGTH - SPECIAL_CHARACTERS - PASSWORD_NUMBERS
alphabet = 'q,w,e,r,t,y,u,i,o,p,a,s,d,f,g,h,j,k,l,z,x,c,v,b,n,m'.split(',')
specialChar = "!,@,#,$,%,^,&,*,(,),{,},:,?,|,<,>,.,`,".split(',')
numbers = '1,2,3,4,5,6,7,8,9,0'.split(',')


class Generator:
    def __init__(self):
        self.password_length = PASSWORD_LENGTH
        self.special_char = SPECIAL_CHARACTERS
        self.password_numbers = PASSWORD_NUMBERS
        self.password_char = PASSWORD_CHARACTERS

    def upper_transform(self):
        t_alphabet = []
        for char in alphabet:
            t_alphabet.append(random.choice([char.upper(), char.lower()]))
        return t_alphabet

    def generate(self):
        password = []
        if self.password_char < 0:
            return 'Invalid entry.The sum of special characters  or letters cannot exceed to Password length'
        else:
            t_alphabet = self.upper_transform()
            for count in range(1, self.password_length):
                if count <= self.password_char:
                    password += random.choice(t_alphabet)
                if count <= self.special_char:
                    password += random.choice(specialChar)
                if count <= self.password_numbers:
                    password += random.choice(numbers)

        generated_password = ''.join(random.sample(password, len(password)))
        # pyperclip.copy(generated_password)
        return generated_password

    def update_generator(self, password_len, special_char, password_num):

        self.password_length = password_len
        self.special_char = special_char
        self.password_numbers = password_num
        self.password_char = password_len - special_char - password_num

    def get_numeric(self):
        return self.password_numbers

    def get_lenth(self):
        return self.password_length

    def get_special_char(self):
        return self.special_char
