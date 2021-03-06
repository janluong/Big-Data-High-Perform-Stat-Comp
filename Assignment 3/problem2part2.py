import problem2part1
import numpy as np
from sklearn.externals.joblib import Memory
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_svmlight_file
import sys

mem = Memory("./mycache3")

@mem.cache
def get_data(data):
    my_data = load_svmlight_file(data)
    return my_data[0], my_data[1]

X, y = get_data("news20.binary.bz2")
# X_train: 15996 x 1355191, y_train: 15996 x 1, X_test: 4000 x 1355191, y_test: 4000 x 1
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)

y_train =  np.matrix(y_train).transpose() # 15996 x 1
y_test = np.matrix(y_test).transpose() # 4000 x 1

# X_train = X_train[0:50]
# y_train = y_train[0:50]

Lamb = 1
epsilon = 0.001
step_size = float(sys.argv[1])

max_col = 1355191
w_0 = np.zeros(max_col) # 1 x 1355191
w_0 = np.matrix(w_0).transpose() # 1355191 x 1

grad_f_of_w = problem2part1.gradient_f_of_w(X_train, y_train, w_0, Lamb) # 1 x 1355191
# if w_0.shape != (62061, 1):
#     raise ValueError("w_0 is not 62061,1, but " + str(w_0.shape))
w_ep_g = w_0 - epsilon * np.transpose(grad_f_of_w) # 1355191 x 1
f_of_wepg = problem2part1.f_of_w(X_train, y_train, Lamb, w_ep_g) # 1 x 1

r_0 = np.sqrt(grad_f_of_w.dot(np.transpose(grad_f_of_w))) # 1 x 1

for i in range(50):
    g = problem2part1.gradient_f_of_w(X_train, y_train, w_0, Lamb) # 1 x 1355191
    if (np.sqrt(g.dot(np.transpose(g))) <= (epsilon * r_0))[0, 0] == True:  # 1 x 1 <= 1 x 1
        break
    g_times_step_size =  np.matrix(step_size * g).transpose() # 1355191 x 1
    w_0 = w_0 - g_times_step_size # 1355191 x 1
    # if w_0.shape != (1355191, 1):
    #     raise ValueError("Loop " + str(i + 1) + ": w_0 is not 1355191,1, but " + str(w_0.shape))

# Remove the last row so the dimensions matches with X_test
w_star = w_0 # [:-1, :] # 1355191 x 1
# print("w*:", w_star)

correct_pred = 0

for i in range(X_test.shape[0]):
    y_i = float(y_test[i])  # 1 x 1
    # print(y_i)
    x_i = X_test[i]  # 1 x 1355191
    pred = y_i * x_i * w_star  # y_i: 1 x 1, x_i: 1 x 1355191, w_star: 1355191 x 1 => result: 1 x 1
    pred = pred[0,0]
    # print("pred:",pred)
    if pred >= 0:
        correct_pred += 1

test_accuracy =  correct_pred/X_test.shape[0]

print("The accuracy rate for lambda = 1 at step size =", step_size, "is", test_accuracy)