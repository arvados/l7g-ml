from subprocess import Popen, PIPE, STDOUT
import os, re

genomes_raw = """0001.00.2654.000+1,11c05127e69ad6815ad56f8715964973,ccctccaggccacgccatggccacagggtgagctgccaccttcatggagaaatggtctctgtgtccatccacttcctcggtctctggtgactcaggacattgcctaagtgtaggcttctgtcccatcaccaaaagtcatgcaggagcagaatgcaggggatgcccaggatctccagtgattctgccctgtggacatcttctgggagcacgtgcttggctgggacagttgactgcagagacacagaggaa
0001.00.2654.001+1,6324e2c3384ca9811f1184c9e3615c78,ccctccaggccacgccatggccacagggcgagctgccaccttcatggagaaatggtctctgtgtccatccacttcctcggtctctggtgactcaggacattgcctaagtgtaggcttctgtcccatcaccaaaagtcatgcaggagcagaatgcaggggatgcccaggatctccagtgattctgccctgtggacatcttctgggagcacgtgcttggctgggacagttgactgcagagacacagaggaa
0001.00.2654.002+1,65945bcd856b06cb0c87ccf4de41fb5d,ccctccaggccacgccatggccacagggcgagctgccaccttcatggagaaatggtctctgtgtccatccacttcctcggtctctggtgactcaggacattgcctaagtgtaggcttctgtcccatcaccaaaagtcatgcaggagcagaatgcaggggatgcccaggatctccagtgattctgccctgtggacatcttctgggagcacgtgcttggctggaacagttgactgcagagacacagaggaa
0001.00.2654.003+1,8c5f7a9e4f9984bac99818cebaf1c608,ccctccaggccacgccatggccacagggtgagctgccaccttcatggagaaatggtctctgtgtccatccacttcctcggtctctggtgactcaggacattgcctaagtgtaggcttctgtcccatcaccaaaagtcatgcaggagcagaatgcaggggatgcccaggatctccagtgattctgccctgtggacatcttctgggagcacgtgcttggctggaacagttgactgcagagacacagaggaa
"""

# convert list of sequences to fasta
def convert_list_to_fasta(sequences_list):
	fasta = "\n".join(sequences_list)
	#print(fasta)
	return fasta

def get_clustalo(sequence):
	# split genomes by line
	input_genomes = sequence.strip().split('\n')

	# create temporary FASTA file for alignment
	fasta = ""
	for genome in input_genomes:
		chunks = genome.split(',')
		fasta += ">{},{}\n{}\n".format(*chunks)
	fasta = fasta[:-1]

	input_filename = "fasta"
	output_filename = "aligned.tmp"

	with open(input_filename, 'w') as f:
		f.write(fasta)

	# run Clustal Omega alignment on FASTA
	proc = Popen(['clustalo', "-infile={}".format(input_filename), "-outfile={}".format(output_filename)], stdout=PIPE, stderr=STDOUT)

	# save output
	stdout = proc.communicate()

	# delete temporary files and save results
	os.remove(input_filename)

	aligned = ""
	with open(output_filename, 'r') as f:
		aligned = f.read()

	os.remove(output_filename)

	# parse string from output to calculate variant differences locations
	aligned = "\n".join(aligned.split('\n')[3:-1])

	entries = []
	for item in aligned.split('\n\n'):
		entries.append(item.split('\n'))

	diffs = []
	for entry in entries:
		diffs.append(entry[-1][57:])

	#print(entries)
	return entries, diffs

def get_diff_indices(sequence):
	
	clustal_entries = get_clustalo(sequence)[1]
	# find location of spaces in lines of asterisks
	diffs = []
	for j, string in enumerate(clustal_entries):
		spaces = [i + 60 * j + 1 for i, ltr in enumerate(string) if ltr == " "]
		diffs.extend(spaces)

	return diffs

if __name__ == "__main__":
	from sys import argv
	print(get_diffs(argv[1]))