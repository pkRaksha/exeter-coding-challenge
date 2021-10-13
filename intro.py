import re
import csv
import time
import psutil
import os

french_dict = {}
frequency = {}
start = time.monotonic()

# open and read the shakespeare file

orginal_doc = open("t8.shakespeare.txt", "r")
inputFile = orginal_doc.read()

# open and read the find_words file
x = open("find_words.txt", "r")
unique_words = x.read()
words_to_find = list(unique_words.split("\n"))

# open the CSV file
with open('french_dictionary.csv', mode='r') as file:

    # reading the CSV file
    dict_file = csv.reader(file)
    # adding the french words to a list
    for english, french in dict_file:
        french_dict[english] = french


fields = ["English", "French", "Frequency"]


with open("frequency.csv", 'w') as csvfile:
    csv_file = csv.writer(csvfile)
    csv_file.writerow(fields)
    f = open("t8.shakespeare.translated.txt", "w")
    # splits at new line to iterate through each line
    for line in inputFile.split('\n'):
        # splits at a space to iterate through each word
        for word in line.split():
            translated_word = ''
            # splits the punctuated word and stores as list
            for punc_splitted_words in re.findall(r'\w+|[^\s\w]+', word):
                # checks for each value in the list is present in the word list
                if punc_splitted_words in words_to_find:
                    # checks if the word is present in the dictionary for translation
                    if french_dict[punc_splitted_words]:
                        # checks if the word is present in frequency  if yes increments and assign the count as value
                        if punc_splitted_words in frequency:
                            frequency[punc_splitted_words] += 1
                        else:
                            frequency[punc_splitted_words] = 1
                        # Assigns the french word to the corresponding english word
                        punc_splitted_words = french_dict[punc_splitted_words]
                        # append the french word
                translated_word += punc_splitted_words

            f.write(translated_word+" ")
        f.write("\n")
    for x in frequency:
        csv_file.writerow([x, french_dict[x], frequency[x]])


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
