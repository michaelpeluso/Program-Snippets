
import numpy as np

np.random.seed(1)
debug = False

# =======
# initial variables and data
# =======

# correctness sensitivity
alpha = 0.35

# test data used for training 
test_data = np.array([[0, 0, 0],
                      [1, 0, 0],
                      [0, 1, 0],
                      [0, 0, 1],
                      [1, 1, 0],
                      [1, 0, 1],
                      [0, 1, 1],
                      [1, 1, 1],])

# correct test answers
training = np.array([[0, 0, 0, 0, 0, 1, 0, 1]]).T # 1 when [1, ?, 1]

# layer weights
layer_0_size = len(test_data[0])
layer_1_size = 4
layer_2_size = 1
layer_0_to_1_weights = 2 * np.random.random((layer_0_size, layer_1_size)) - 1
layer_1_to_2_weights = 2 * np.random.random((layer_1_size, layer_2_size)) - 1


# =======
# rectified linear activation function: minimizes small & negative values, while boosting larger ones
# =======
def relu(x):
    return (x > 0) * x

# first derivative of relu
def dir_relu(x):
    return x > 0


# =======
# main prediction function
# =======
for iteration in range(60):
    pred_error = 0
    for case in range(len(test_data)):
        
        # predict each layer
        layer_0 = test_data[case:case+1]
        layer_1 = relu(np.dot(layer_0, layer_0_to_1_weights))
        layer_2 = np.dot(layer_1, layer_1_to_2_weights)
        
        # find error
        pred = layer_2
        error = pred - training[case:case+1]
        pred_error += np.sum((error) ** 2) # sum and square values to assign positive value and focus on larger (>1) errors
        
        # backpropagation
        layer_2_delta = error
        layer_1_delta = error.dot(layer_1_to_2_weights.T) * dir_relu(layer_1) # turn off layer 1 nodes with error < 0
        
        # adjust weights
        layer_1_to_2_weights -= alpha * layer_1.T.dot(layer_2_delta) # weights = weights - (alpha * input * delta)
        layer_0_to_1_weights -= alpha * layer_0.T.dot(layer_1_delta)
        
        # debug
        if debug:
            print("input:", test_data[case:case+1][0], "\t",
                  "output:", f"{layer_2[0][0]:.9f}", "\t", 
                  "answer:", training[case:case+1][0][0], "\t", 
                  "error:", pred_error)

    # print every 10th error
    if (iteration % 10 == 9):
        print("Error:", pred_error)