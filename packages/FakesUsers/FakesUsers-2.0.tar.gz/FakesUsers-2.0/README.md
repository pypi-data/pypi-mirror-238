# FakesUsers 1.1
FakesUsers - Python library that regenerates random names, phone numbers and addresses. For now, only the Russian generation is available, but over time we will add other generations.

## Content
- [NEW FAKESUSERS 1.1!](#NEW-FAKESUSERS-1.1!)
- [Import](#Import)
- [Basic Concepts](#Basic-Concept)
- [Example code](#Example-Code)
- [Information on creator](#Information-on-creator)

## NEW FAKESUSERS 1.1
On October 30, a new version of the FakesUsers library was released! What was added in version 1.1 ?
1) New command
```sh
fake_email()
```

2) Some bugs fixed

I hope you enjoy version 1.1 :)
P.s: Version 1.2 will be amazing!

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

Displaying a random male name
```sh
fakename_male()
```

Displaying a random female name
```sh
fakename_female()
```

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

print(fu.fakename_male())
print(fu.fakename_female())
print(fu.fake_number())
print(fu.fake_addres())
```
Result
```sh
Дмитрий Денисов
Елизавета Яркова      
+70033297583
ул. Грибоедова 90
```

## Information on creator
filcher2011 == I've been a Python programmer for about 2 years now. He does small projects :)
telegram-channel: https://t.me/filchercode