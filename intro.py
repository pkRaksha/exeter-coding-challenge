import re
import csv
import time
import psutil
import os


start = time.monotonic()

orginal_doc = open("t8.shakespeare.txt", "r")
inputFile = orginal_doc.read()

x = open("find_words.txt", "r")

search = x.read()

words_to_find = list(search.split("\n"))


fields = ["English", "French", "Frequency"]


# To calculate number of words replaced for each english word


with open("frequency.csv", 'w') as csvfile:
    csv_file = csv.writer(csvfile)
    csv_file.writerow(fields)
    with open('french_dictionary.csv', mode='r')as file:

        # reading the CSV file
        dict_file = csv.reader(file)
        for english, french in dict_file:
            a = len([*re.finditer("\\b"+english+"\\b", inputFile)])
            csv_file.writerow([english, french, a])

with open('french_dictionary.csv', mode='r')as file:

    # reading the CSV file
    dict_file = csv.reader(file)
    for english, french in dict_file:
        inputFile = re.sub("\\b"+english+"\\b", french, inputFile)


f = open("t8.shakespeare.translated.txt", "a")
f.write(inputFile)
f.close()


# To calculte the time
end = time.monotonic()
execTime = end - start
execution_time = time.strftime(
    "Time to process: %#M minutes %#S seconds", time.gmtime(execTime))


# To calculate the memory
memory = "Memory used: " + \
    str(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2) + " MB"

a = open("performance.txt", 'a')
a.write(execution_time + "\n" + memory)
a.close()
