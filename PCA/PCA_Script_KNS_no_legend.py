import os
os.environ.get('DISPLAY','')
import matplotlib as mpl
mpl.use('Agg')      # This line must come before importing pyplot
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerPatch
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
<<<<<<< HEAD
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("data_dir_1hot", default='/home/keldin/keep/by_id/su92l-4zz18-zkrq9qdscuhpqj4')
parser.add_argument("data_dir_ethn", default='/home/keldin/keep/by_id/su92l-4zz18-mcg5xarbwji8t58')
args = parser.parse_args()
data_dir_1hot = args.data_dir_1hot
data_dir_ethn = args.data_dir_ethn


# Assume we are on lightning-dev1. We begin by mounting keep
=======


# Assume we are on lightning-dev1. We beging by mounting keep
>>>>>>> 64dee6a847e025175a23a1c3a1bbf8899a3f1d73
# And as long as we're saving the output to keeprw, better mount that as well
    # Todo

# Here we ask user for inputs of files
# (In the future, encapsulate this in class)
<<<<<<< HEAD
#data_dir_1hot = '/home/keldin/keep/by_id/su92l-4zz18-zkrq9qdscuhpqj4'
#input("Please provide directory of 1hot data:\n")
#data_dir_ethn = '/home/keldin/keep/by_id/su92l-4zz18-mcg5xarbwji8t58'
#input("Please provide direcotry of ethnicity data:\n")

# As for directory which to save plot
#plot_save_dir = '/home/keldin/keeprw/by_id/su92l-4zz18-hhyjc7arp04d20t'
=======
data_dir_1hot = '/home/keldin/keep/by_id/su92l-4zz18-zkrq9qdscuhpqj4'
#input("Please provide directory of 1hot data:\n")
data_dir_ethn = '/home/keldin/keep/by_id/su92l-4zz18-mcg5xarbwji8t58'
#input("Please provide direcotry of ethnicity data:\n")

# As for directory which to save plot
plot_save_dir = '/home/keldin/keeprw/by_id/su92l-4zz18-hhyjc7arp04d20t'
>>>>>>> 64dee6a847e025175a23a1c3a1bbf8899a3f1d73
#input("Please provide directory into which to save plots:\n")


# Loading in one-hot-encoded data and names of subjects for each row

oh = np.load(data_dir_1hot + "/hiq-1hot-simple.npy")
ohinfo = np.load(data_dir_1hot + "/names.npy")
#var1 = np.load("/home/swz/PGP-work/Lightning_Work/PGP1000Genomes/hiq/hiq-collect.npy")
# ^ hiq-collect.npy not in the dataset that Sarah gave me, but fortunately it
# is unused in this script, so we can just comment it out.

oh.shape


# PCA 
#pca = NMF(n_components=3)

pca = PCA(n_components=2)

X = pca.fit_transform(oh)
#X = spca.fit_transform(oh)

# Copied from http://www.1000genomes.org/category/phenotype

pop_to_super_pop = {
  "CHB":"EAS",
  "JPT":"EAS",
  "CHS":"EAS",
  "CDX":"EAS",
  "KHV":"EAS",
  "CEU":"EUR",
  "TSI":"EUR",
  "FIN":"EUR",
  "GBR":"EUR",
  "IBS":"EUR",
  "YRI":"AFR",
  "LWK":"AFR",
  "MSI":"AFR",#added
  "GWD":"AFR",
  "MSL":"AFR",
  "ESN":"AFR",
  "ASW":"AFR",
  "ACB":"AFR",
  "MXL":"AMR",
  "PUR":"AMR",
  "CLM":"AMR",
  "PEL":"AMR",
  "GIH":"SAS",
  "PJL":"SAS",
  "BEB":"SAS",
  "STU":"SAS",
  "ITU":"SAS",
  "asian-pgp":"EAS",
  "white-pgp":"EUR",
  "ethiopian-pgp":"AFR",
  "columbian-pgp":"AMR"
}
pop_human_readable = {
  "CHB":["Han Chinese in Bejing, China",'yellowgreen'], #None in 433
  "JPT":["Japanese in Tokyo, Japan",'mediumspringgreen'], #None in 433
  "CHS":["Southern Han chinese",'forestgreen'], #93 in 433
  "CDX":["Chinese Dai in Xishuangbanna, China",'mediumseagreen'], #None in 433
  "KHV":["Kinh in Ho Chi Minh City, Vietnam", 'lawngreen'], #6 in 433
  "asian-pgp":["PGP participants of Asian ancestry", 'olive'],

  "CEU":["Utah Residents (CEPH) with Northern and Western European Ancestry",'darkviolet'], #96 in 433
  "TSI":["Toscani in Italia",'darkslateblue'], #None in 433
  "FIN":["Finnish in Finland",'blueviolet'], #None in 433
  "GBR":["British in England and Scotland",'darkmagenta'], #None in 433
  "IBS":["Iberian Population in Spain",'indigo'], #None in 433
  "white-pgp":["PGP participants of European ancestry",'magenta'],

  "YRI":["Yoruba in Ibadan, Nigeria",'maroon'], #80 in 433
  "LWK":["Luhya in Webuye, Kenya",'sandybrown'], #11 in 433
  "MSI":["Maasai from Kenya", 'peru'],#None in 433, added!
  "GWD":["Gambian in Western Divisions in the Gambia",'sienna'], #None in 433
  "MSL":["Mende in Sierra Leone",'goldenrod'], #None in 433
  "ESN":["Esan in Nigeria",'tan'], #None in 433
  "ASW":["Americans of African Ancestry in SW USA",'brown'], #None in 433
  "ACB":["African Caribbeans in Barbados",'burlywood'], #None in 433
  "ethiopian-pgp":["PGP Ethiopian participant", 'black'],

  "MXL":["Mexican Ancestry from Los Angeles USA",'tomato'], #None in 433
  "PUR":["Puerto Ricans from Puerto Rico",'orangered'], #6 in 433
  "CLM":["Colombians from Medellin, Colombia",'coral'], #None in 433
  "PEL":["Peruvians from Lima, Peru",'palevioletred'], #94 in 433
  "columbian-pgp":["PGP Columbian participant", 'darkorange'],

  "GIH":["Gujarati Indian from Houston, Texas",'cyan'], #None in 433
  "PJL":["Punjabi from Lahore, Pakistan",'darkturquoise'], #47 in 433
  "BEB":["Bengali from Bangladesh", 'darkcyan'], #None in 433
  "STU":["Sri Lankan Tamil from the UK",'aquamarine'], #None in 433
  "ITU":["Indian Telugu from the UK",'lightseagreen'], #None in 433
}
super_pop_human_readable = {
  "EAS":["East Asian", 'g'],
  "EUR":["European", 'darkviolet'],
  "AFR":["African", 'brown'],
  "AMR":["Ad Mixed American", 'darkorange'],
  "SAS":["South Asian", 'c']
}


# Loading subject phenotype information

filePGP = data_dir_ethn + '/PGP_assigned_ethnicities.csv'
file1000G = data_dir_ethn + '/1000G_ethnicities_20130606_sample_info.csv'
#file3 = '/home/swz/Downloads/1000G_ethnicities_69_hashed_together.csv'

PGPeth = pd.read_csv(filePGP) 
G1000 = pd.read_csv(file1000G) 

# Converting Population to Superpopulation, and getting colors for population and superpopulation for plotting

G1000['SuperPopulation'] = G1000['Population'].apply(lambda x: pop_to_super_pop[x])
G1000['ColorSuper'] = G1000['SuperPopulation'].apply(lambda x: super_pop_human_readable[x][1])
G1000['SuperPopHumanRead']=  G1000['SuperPopulation'].apply(lambda x: super_pop_human_readable[x][0])
G1000['Color'] = G1000['Population'].apply(lambda x: pop_human_readable[x][1])
G1000['PopHumRead'] = G1000['Population'].apply(lambda x: pop_human_readable[x][1])

g2 = lambda x:x[0:x.find(b"-")]
results = [g2(i).decode("utf-8") for i in ohinfo]

df = pd.DataFrame(results,columns={'Sample'})

df2 =  df.merge(G1000,on = 'Sample', how='left')
df2['Color'] = df2.Color.fillna('w')
df2['ColorSuper'] = df2.ColorSuper.fillna('w')


colors = df2['Color'].values.tolist()
clabels = df2['PopHumRead'].values.tolist()

# Plotting data against first two principle components

xlabel="Principal Component 1"
ylabel="Principal Component 2"

plt.figure()
plt.scatter(X[:,0], X[:,1], c = colors, alpha=0.2)

plt.xlabel(xlabel)
plt.ylabel(ylabel)

plt.gca().set_xlim([-20,60])
plt.gca().set_ylim([-20,30])

# Add custom legend
vals = list(pop_human_readable.values())
legcolors = [v[1] for v in vals]
labels = [v[0] for v in vals]

leghandle = []

#for ix,cc in enumerate(legcolors):
#    leghandle.append(mpatches.Rectangle((0,0),0.2,0.2, facecolor=cc,
#                            edgecolor=cc, linewidth=3,label='test'))


#plt.legend(handles=leghandle, bbox_to_anchor=(0, 2.), loc=2, borderaxespad=0,ncol = 3)

#leg = plt.gca().get_legend()
#print(type(leg))
#ltext  = leg.get_texts()  
#llines = leg.get_lines()  
#frame  = leg.get_frame()  

#plt.setp(ltext, fontsize='x-small')    # the legend text fontsize
#plt.setp(llines, linewidth=1.5)  

#plt.gcf().subplots_adjust(right=0.7, top=0.8)
<<<<<<< HEAD
plt.savefig('PCA12-Pop_cwl.png',format='png',dpi=300)
=======
plt.savefig(plot_save_dir + '/PCA12-Pop.png',format='png',dpi=300)
>>>>>>> 64dee6a847e025175a23a1c3a1bbf8899a3f1d73


