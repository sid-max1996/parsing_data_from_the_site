fileName = "Renault.sql"

file1 = open(fileName, 'r', encoding='utf-8')

file2 = open('new'+fileName, 'w', encoding='utf-8')

contents = file1.readlines()

startLine = 2925

for i in range(startLine, len(contents)):
    file2.write(contents[i]);
