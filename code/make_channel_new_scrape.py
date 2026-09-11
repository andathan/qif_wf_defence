
import random
import csv
import pandas as pd
import os




def read_and_sort_csv():

	csv_filename = "channel_output.csv"
	df = pd.read_csv(csv_filename, header = 0)
	df.columns = df.columns.astype(int)

	print(df.columns)
	print(df.head(10))

	df_sorted = df.sort_index( axis=1)
	print(df_sorted.head(10))
	df_sorted.rename(columns={-100:''}, inplace=True)
	df_sorted.to_csv("channel_output_sorted.csv", index=False)






def write_to_csv(file_name, header, first_column, data):

	with open(file_name, mode='w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(header)
		for col_value, row_data in zip(first_column, data):
			writer.writerow([col_value] + row_data)

	#now sort it
	read_and_sort_csv()


def check_channel (channel):
	for row in channel:
		if (abs(sum(row) - 1) > 0.0001):
			print("Error, row")
			print(row)
			print("does not sum to 1. Exiting...")
			exit()


def make_channel(available_file_sizes,site_filesize):

	#index.html gets 0.5 probability

	#the rest uniformly random 

	channel = []
	header = available_file_sizes

	header.insert(0,-100)

	#print("AVAILABLE FILESIZES:", header)
	#first find all the observable file sizes
	
	if (len(header) != len(set(header))):
		print("Error, header contains non unique elements!")
		exit()

	#quick for timing experiments
	print("Warning, uniform channel just for timing experiments")
	for site in range((200)):
		row = [1/len(header) for i in range (len(header))]
		row.insert(0,"this is a site.org")
		channel.append(row)

	'''
	#Normal operation:

	for site in site_filesize:
		print("RUNNING FOR SITE", site)
		row = []
		num_of_unif_elements = 0 
		new_site = 1
		for item in site:
			print("SERACHING FOR", item)
			found = 0 
			for possible_file_size in header:
				if possible_file_size == item:
					#is it index.html?
					if (new_site == 1):
						row.append(0.5)
						new_site = 0
						found =1
					else:
						num_of_unif_elements +=1
						row.append(0.1)
						found = 1
						break
			if found == 0:
				print("not found... ", item)
				row.append(0)
			#no scaling needed
		if num_of_unif_elements==0:
			row[row.index(0.5)] = 1
			continue


			#need to normalize: we will turn all the "0.1" to normalized uniformly random floats
		random_numbers = [random.uniform(0.0001, 0.5) for _ in range(num_of_unif_elements)]
		scaling_factor = 0.5 / sum(random_numbers)
		scaled_numbers = [num * scaling_factor for num in random_numbers]
		j=0
		for i in range(len(row)):
			if row[i] == 0.1:
   				row[i] = scaled_numbers[j]
   				j+=1
		channel.append(row)
		print("My row", row)
	'''
	#check_channel(channel)
	#print(header)
	#print("elements of channel are:", len(channel))
	return channel, header




websites = []
available_file_sizes = []
site_filesize = []


#Timing exp
file = open("scraped_data.csv", "r")
data = list(csv.reader(file, delimiter=","))
file.close()
for i in range (1,1000000):
	if i not in available_file_sizes:
		available_file_sizes.append(i)


available_file_sizes.sort()
channel,header = make_channel(available_file_sizes,site_filesize)

print(len(channel))
with open('huge_channel.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(channel)
print(channel[0])
exit()


'''
#Normal operation
for item in data:
	site_name = item[0]
	index_size = int(item[1])
	rest_sizes = item[2][1:-1].split(',')
	rest_sizes = [int(i) for i in rest_sizes]


	#remove duplicates from rest_sizes
	rest_sizes = list(set(rest_sizes))
	if index_size in rest_sizes:
		rest_sizes.remove(index_size)
	rest_sizes.insert(0,index_size)	
	websites.append(site_name)
	site_filesize.append(rest_sizes)

	
	for item in rest_sizes:
		if item not in available_file_sizes:
			available_file_sizes.append(item)

channel,header = make_channel(available_file_sizes,site_filesize)
'''


#print("----------------")
#print(channel)
#print("----------------")
write_to_csv ("channel_output.csv", header,websites, channel)


with open('output', 'w') as fp:
	fp.write('[')
	for row in channel:
		fp.write(str(row))
		fp.write(',')
	fp.write(']')


with open('header', 'w') as fp:
	fp.write('[')
	fp.write(str(header))
	fp.write(',')
	fp.write(']')


