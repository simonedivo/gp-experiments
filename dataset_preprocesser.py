import pandas as pd
from sklearn.model_selection import train_test_split
import os

print('Preprocessing datasets...')

pbc_dataset = pd.read_csv('./datasets/1191_BNG_pbc.tsv', sep='\t')
pharynx_dataset = pd.read_csv('./datasets/1196_BNG_pharynx.tsv', sep='\t')
poker_dataset = pd.read_csv('./datasets/1595_poker.tsv', sep='\t')

pbc_dataset.dropna(inplace=True)
pharynx_dataset.dropna(inplace=True)
poker_dataset.dropna(inplace=True)


X_pbc = pbc_dataset.drop(columns=['target'])
#y_pbc = pd.DataFrame(pbc_dataset['target'])
y_pbc = pbc_dataset['target']

X_pharynx = pharynx_dataset.drop(columns=['target'])
#y_pharynx = pd.DataFrame(pharynx_dataset['target'])
y_pharynx = pharynx_dataset['target']

X_poker = poker_dataset.drop(columns=['target'])
#y_poker = pd.DataFrame(poker_dataset['target'])
y_poker = poker_dataset['target']


X_pbc_train, X_pbc_test, y_pbc_train, y_pbc_test = train_test_split(X_pbc, y_pbc, test_size=0.5, random_state=42, shuffle=True)
X_pharynx_train, X_pharynx_test, y_pharynx_train, y_pharynx_test = train_test_split(X_pharynx, y_pharynx, test_size=0.5, random_state=42, shuffle=True)
X_poker_train, X_poker_test, y_poker_train, y_poker_test = train_test_split(X_poker, y_poker, test_size=0.5, random_state=42, shuffle=True)

preprocessed_datasets_dir = './preprocessed_datasets'
if not os.path.exists(preprocessed_datasets_dir):
    os.makedirs(preprocessed_datasets_dir)


X_pbc_train.to_csv('./preprocessed_datasets/X_pbc_train.csv', index=False)
y_pbc_train.to_csv('./preprocessed_datasets/y_pbc_train.csv', index=False)
X_pbc_test.to_csv('./preprocessed_datasets/X_pbc_test.csv', index=False)
y_pbc_test.to_csv('./preprocessed_datasets/y_pbc_test.csv', index=False)

X_pharynx_train.to_csv('./preprocessed_datasets/X_pharynx_train.csv', index=False)
y_pharynx_train.to_csv('./preprocessed_datasets/y_pharynx_train.csv', index=False)
X_pharynx_test.to_csv('./preprocessed_datasets/X_pharynx_test.csv', index=False)
y_pharynx_test.to_csv('./preprocessed_datasets/y_pharynx_test.csv', index=False)

X_poker_train.to_csv('./preprocessed_datasets/X_poker_train.csv', index=False)
y_poker_train.to_csv('./preprocessed_datasets/y_poker_train.csv', index=False)
X_poker_test.to_csv('./preprocessed_datasets/X_poker_test.csv', index=False)
y_poker_test.to_csv('./preprocessed_datasets/y_poker_test.csv', index=False)

print('Datasets preprocessed and saved in ./preprocessed_datasets directory')