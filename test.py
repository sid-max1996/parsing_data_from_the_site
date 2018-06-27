import os 

directory = 'union/' 
files = os.listdir(directory) 
outfile = open('res.sql', 'w', encoding='utf-8')

for file in files:
    file = open(directory+file, 'r', encoding='utf-8')
    outfile.write( file.read() )
