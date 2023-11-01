# FakesUsers
FakesUsers - Python library that regenerates random names, phone numbers, addresses and email.

## Content
- [About the project](#About-the-project)
- [Import](#Import)
- [Basic Concepts](#Basic-Concept)
- [Example code](#Example-Code)
- [Information on creator](#Information-on-creator)

## About the project
FakesUsers -- is a project designed to generate random information from its database. It can be used for any purpose, as well as modified and improved in some way. filcher2011 is working on the project. He works hard on the project and tries to release updates more often.

## Import
In order to import the library, you need to install it :)
Enter the cmd command to install this library
```sh
pip install FakesUsers
```
After that, in your file with the .py extension, write . . .
```sh
from FakesUsers import Fu
fu = Fu()
```

## Basic Concept
What commands are there in this library? This library has commands such as:
Changing the region for generation
```sh
genRegion('ru/en')
```
PS:If you put genRegion('ru'), then all names, numbers and addresses will be regenerated relevant for Russia. Well, if you put genRegion('en'), then all names, phone numbers and addresses will be regenerated relevant for the USA (default is 'ru')

Displaying a random male name
```sh
fake_name('gender')
```
PS:If you write 'male' in brackets, then only male names will be generated, the opposite if you put 'female' in brackets

Displaying a random phone number
```sh
fake_number()
```

Displaying a random addres
```sh
fake_addres()
```

And displaying a random email
```sh
fake_email()
```

## Example Code
Let's look at a simple code that will output a random man's and woman's name, phone number and address
Code
```sh
from FakesUsers import Fu

fu = Fu()
fu.genRegion('ru')

print(fu.fake_name('male'))
print(fu.fake_name('female'))
print(fu.fake_number())
print(fu.fake_addres())
```
Result (Translated from Russian)
```sh
Dmitry Denisov
Elizaveta Yarkova
+70033297583
st. Griboyedova 90
```

## Information on creator
filcher2011 == I've been a Python programmer for about 2 years now. He does small projects :)
Telegram-channel: https://t.me/filchercode
