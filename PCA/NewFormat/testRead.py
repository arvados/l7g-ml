import pandas as pd

ancestry1k = pd.read_csv('igsr_samples.tsv',sep='\t')
print(ancestry1k)
#ancestryMap = ancestry1k[['Sample','Population']]
#ancestryMap['DataSource'] = '1K'
#ancestryMap['ID'] = ancestry1k.Sample
#ancestryMap['Region'] = ancestry1k.Population
#ancestries = ancestryMap[['ID','Region','DataSource']]

