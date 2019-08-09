import pandas as pd

data = pd.read_csv('gz-verify/src/gzverify.csv',
                   header=None, names=['filepath', 'status'])
supplemental = pd.read_csv('gz-verify/src/filenames.txt',
                           header=None, names=['vcf'])
s = supplemental.sort_values(by=['vcf'])

path_split = data['filepath'].str.split("/", expand=True)
status_split = data['status'].str.split("\n", expand=True)
data['src'] = path_split[6]
data['status'] = status_split[0]
sample_d = data['src'].str.split(".", expand=True)
data['sample'] = sample_d[0]
d = data.sort_values(by=['src'])

sample_s = s['vcf'].str.split(".", expand=True)
s['sample'] = sample_s[0]

df = pd.merge(left=d, right=s, how='inner', on='sample')
cols = ['vcf', 'sample', 'status', 'src']
df = df[cols]

output = df.to_csv('gz-verify/src/validated.csv', index=False)
