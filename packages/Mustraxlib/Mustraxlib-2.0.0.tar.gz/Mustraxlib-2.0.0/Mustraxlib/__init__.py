import requests
from bs4 import BeautifulSoup
import time
import os
import sys
import random
import string
from argon2 import PasswordHasher

if os.name == 'nt':
    try:
          import msvcrt
    except ImportError:
        print("Failed to import msvcrt on Windows.")
        exit(1)
else:
		try:
				import termios
				import tty
		except ImportError:
				print("Failed to import termios/tty on Linux.")
				exit(1)

def hash(text):
    ph = PasswordHasher()
    hashed_password = ph.hash(text)
    return hashed_password

def verify_hash(hashed_text, text):
	ph = PasswordHasher()
	try:
		is_valid = ph.verify(hashed_text, text)
		return is_valid
	except:
		return False
    
def code(code_length):
		characters = string.ascii_letters + string.digits
		code = ''.join(random.choice(characters) for _ in range(code_length))
		return code
  
def detect_input():
		if os.name == 'nt':  # Windows
				try:
						import msvcrt
						key = msvcrt.getch()
						if key == b'\xe0':
								key = msvcrt.getch()
								if key == b'H':
										return 'up'
								elif key == b'P':
										return 'down'
						elif key == b'\r':
								return 'enter'
						return key.decode('utf-8')
				except ImportError:
						print("Failed to import msvcrt on Windows.")
						exit(1)
		else:  # Linux
				try:
						import termios
						import tty
						fd = sys.stdin.fileno()
						old_settings = termios.tcgetattr(fd)
						try:
								tty.setraw(fd)
								key = sys.stdin.read(1)
								if key == '\x1b':
										key = sys.stdin.read(2)
										if key == '[A':
												return 'up'
										elif key == '[B':
												return 'down'
								elif key == '\r':
										return 'enter'
								return key
						finally:
								termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
				except ImportError:
						print("Failed to import termios/tty on Linux.")
						exit(1)

def background(text, color):
		color_code = {
				'white': '97;40',
				'black': '30;47',
				'red': '41',  # Set the background color
				'green': '42',
				'blue': '44',
				'yellow': '43',
				'cyan': '46',
				'magenta': '45',
				# Add more colors as needed
		}

		if color.lower() in color_code:
				return f"\033[{color_code[color.lower()]}m{text}\033[0m"
		else:
				return text  # Return the text as is if the color is not found in the dictionary

def clear_last_x_lines(lines_to_clear):
		if os.name == 'posix':
				for _ in range(lines_to_clear):
						print("\033[F\033[K", end="")  # Move up and clear line
		elif os.name == 'nt':
				for _ in range(lines_to_clear):
						os.system('cls')
		else:
				for _ in range(lines_to_clear):
						print('\033[A\033[K', end='')

def radio_choice(choice):
		i = 0
		a = 0
		while True:
				for x in choice:
						if i == a:
								print(background(x, 'white'))
						else:
								print(x)
						a += 1
						if a == len(choice):  # Reset 'a' to 0 when it reaches the end of the list
								a = 0
				user_input = detect_input()
				if user_input == 'up' and i > 0:
						i -= 1
				elif user_input == 'down' and i < len(choice) - 1:
						i += 1
				elif user_input == 'enter':
						return choice[i]
				clear_last_x_lines(len(choice))

def password(min_length=3, max_length=20, warning_message=True):
	password = ""
	while True:
			clear_last_x_lines(1)  # Clear the last line

			if len(password) > max_length:
					display_password = '*' * (max_length - 3) + "..."
			else:
					display_password = '*' * len(password)

			print("Password : ", display_password)
			a = detect_input()

			if a == 'enter':
					if len(password) >= min_length and len(password) <= max_length:
							return password
					elif warning_message:
							clear_last_x_lines(1)
							temp = f"Password must be between {min_length} and {max_length} characters."
							print(background(temp, 'white'))
							time.sleep(3)
							clear_last_x_lines(0)
							password = ""
					else:
							password = ""
			elif (a != 'up') and (a != 'down'):
					password = password + a
			clear_last_x_lines(1)

def matrixify(columns, rows, filler):
		xyz = [[filler] * columns for _ in range(rows)]
		return xyz

def display(matrix):
		for row in matrix:
				print(" ".join(map(str, row)))

def replace_index(matrix, x, y, filler):
		matrix[x][y] = filler
		return matrix

def contains(matrix, string):
		for row in matrix:
				if string in row:
						return True
		return False

def replace(matrix, string, filler):
		for x in range(len(matrix)):
				for y in range(len(matrix[x])):
						if matrix[x][y] == string:
								matrix[x][y] = filler
		return matrix

def webscrape(url):
		try:
				response = requests.get(url)
				if response.status_code == 200:
						html = response.text
						soup = BeautifulSoup(html, 'html.parser')
						return soup
				else:
						return response.status_code
		except:
				return "Error while scraping:" + url
