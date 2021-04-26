import os
import pathlib

# using os methods
print('-'*10 + 'OS methods' + '-'*10)
# getting the absolute file path of this file
print(os.path.abspath(__file__))
# getting the parent directory of this file
print(os.path.dirname(os.path.abspath(__file__)))
# getting the current working directory
print(os.getcwd())

print()
# using pathlib methods
print('-'*10 + 'Pathlib methods' + '-'*10)
# getting the absolute file path of this file
print(pathlib.Path(__file__).absolute())
# getting the parent directory of this file
print(pathlib.Path(__file__).parent.absolute().parent)
# getting the current working directory
print(pathlib.Path().cwd())
# changing the name and extension of a file while not changing the directory
print(pathlib.Path(__file__).absolute().with_name('file_name_change1.txt'))
# extract the file name without extension
print(pathlib.Path(__file__).absolute().stem)