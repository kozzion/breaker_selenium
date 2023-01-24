import time
import os
import sys
import json
import numpy as np
import pickle as pkl
from sklearn.decomposition import PCA

path_file_dict_symbol_history = 'dict_symbol_history.json'
path_file_list_symbol_selected = 'list_symbol_selected.json'
path_file_matrix_selected = 'matrix_selected.pkl'
if not os.path.isfile(path_file_matrix_selected):
    with open(path_file_dict_symbol_history, 'r') as file:
        dict_symbol_history = json.load(file)

    list_symbol_selected = []
    list_array_selected = []
    for symbol in dict_symbol_history:
        if 360 < len(dict_symbol_history[symbol]['list_candle']):
            list_close = []
            for candle in dict_symbol_history[symbol]['list_candle'][-360:-1]:
                if candle['Close'] is None:
                    list_close.append(list_close[-1])
                else:
                    list_close.append(float(candle['Close']))
            list_symbol_selected.append(symbol)
            list_array_selected.append(np.array(list_close))

    matrix_selected = np.vstack(list_array_selected)
    print(matrix_selected.shape)

    with open(path_file_list_symbol_selected, 'w') as file:
        json.dump(list_symbol_selected, file)

    with open(path_file_matrix_selected, 'wb') as file:
        pkl.dump(matrix_selected, file)
else:
    with open(path_file_list_symbol_selected, 'r') as file:
        list_symbol_selected = json.load(file)

    with open(path_file_matrix_selected, 'rb') as file:
        matrix_selected = pkl.load(file)

print(np.max(matrix_selected, axis=1).shape)
print(np.expand_dims(matrix_selected[:,0], axis=1).shape)
print(np.ones((1, matrix_selected.shape[0])).shape)


matrix_min = np.matmul(np.expand_dims(np.min(matrix_selected, axis=1), axis=1), np.ones((1, matrix_selected.shape[1])))
matrix_max = np.matmul(np.expand_dims(np.max(matrix_selected, axis=1), axis=1), np.ones((1, matrix_selected.shape[1])))
matrix_range = matrix_max - matrix_min 
matrix_range[matrix_range < 1] = 1
matrix_selected = (matrix_selected - matrix_min) / matrix_range
print(matrix_selected.shape)

count_component = 10

pca = PCA(n_components=count_component)
result = pca.fit_transform(matrix_selected)
print(pca.explained_variance_ratio_)
array_base = pca.inverse_transform(np.eye(count_component))
print(result.shape)
print(array_base.shape)



import matplotlib.pyplot as plt
plt.figure()
plt.scatter(result[:,1], result[:,2])

plt.figure()
plt.scatter(result[:,2], result[:,3])

print(array_base.shape)
plt.figure()
plt.plot(array_base[1,:])

plt.figure()
plt.plot(array_base[2,:])


plt.figure()
plt.plot(array_base[3,:])
plt.show()
# pca.inverse_transform(X)