import re
import csv
import time
import psutil
import os

french_dict = {}
start = time.monotonic()

# open and read the shakespeare file

orginal_doc = open("t8.shakespeare.txt", "r")
inputFile = orginal_doc.read()

# open and read the find_words file
x = open("find_words.txt", "r")
unique_words = x.read()
words_to_find = list(unique_words.split("\n"))

# open the CSV file
with open('french_dictionary.csv', mode='r')as file:

    # reading the CSV file
    dict_file = csv.reader(file)
    # adding the french words to a list
    for english, french in dict_file:
        french_dict[english] = french


fields = ["English", "French", "Frequency"]


with open("frequency.csv", 'w') as csvfile:
    csv_file = csv.writer(csvfile)
    csv_file.writerow(fields)

    for x in range(len(words_to_find)):
        if french_dict[words_to_find[x]]:
            # to calculate the occurances of each word from the find_words file in the shakespeare file
            a = len([*re.finditer("\\b"+words_to_find[x]+"\\b", inputFile)])
        # to store the result as a CSV file
            csv_file.writerow(
                [words_to_find[x], french_dict[words_to_find[x]], a])
        # to translate the words found from the find_words file
            inputFile = re.sub(
                "\\b"+words_to_find[x]+"\\b", french_dict[words_to_find[x]], inputFile)


# to store the translated file
f = open("t8.shakespeare.translated.txt", "a")
f.write(inputFile)
f.close()


# to calculte the time
end = time.monotonic()
execTime = end - start
execution_time = time.strftime(
    "Time to process: %#M minutes %#S seconds", time.gmtime(execTime))


# to calculate the memory
memory = "Memory used: " + \
    str(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2) + " MB"

# to store the time and memory
a = open("performance.txt", 'a')
a.write(execution_time + "\n" + memory)
a.close()
