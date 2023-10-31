Developed by M.J. van der Zwart as MSc thesis project (c) 2023

Preparing data

```python
		from R2Ntab import transform_dataset, kfold_dataset
		
		name = 'adult'
		X, Y, X_headers, Y_headers = transform_dataset(name, method='onehot-compare', negations=False, labels='binary')
		datasets = kfold_dataset(X, Y, shuffle=1)
		X_train, X_test, Y_train, Y_test = datasets[0]
		train_set = torch.utils.data.TensorDataset(torch.Tensor(X_train.to_numpy()), torch.Tensor(Y_train))
		test_set = torch.utils.data.TensorDataset(torch.Tensor(X_test.to_numpy()), torch.Tensor(Y_test))
```

Creating and training the model

```python
		from r2ntab import R2NTab
		
		model = R2Ntab(len(X_headers), 20, 1)
		model.fit(train_set, epochs=1000, batch_size=400, cancel_lam=1e-2)
```

Extracting the results

```python
		Y_pred = r2ntab.predict(X_test)
		rules = r2ntab.extract_rules(X_headers, print_rules=True)
		print(f'AUC: {r2ntab.score(Y_pred, Y_test, metric="auc")}, num rules: {len(rules)}, num conditions: {sum(map(len, rules))}')
```
