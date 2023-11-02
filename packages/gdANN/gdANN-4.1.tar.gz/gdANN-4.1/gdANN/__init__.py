from time import ctime
import os.path
from random import shuffle
from typing import List

from functions import *

__all__ = (
    "MLP_Network",
    "Linear_Regression",
    "Convolution_layer",
    "plot_net"
)


class Convolution_layer(object):
    __slots__ = ('kernel', 'size', 'pooling_method', 'pool_l')

    def __init__(self, kernel: List[List[float]], max_pooling: bool = True, pool_length: int = 2):
        self.kernel = kernel
        self.size = len(kernel)
        self.pooling_method = max_pooling
        self.pool_l = pool_length

    def __call__(self, image: List[List[float]]):
        range_ = range(len(image) - self.size + 1)
        temp = [[0 for _ in range_] for _ in range_]
        for i in range_:
            for j in range_:
                for x in range(self.size):
                    for y in range(self.size):
                        temp[i][j] += image[i + x][j + y] * self.kernel[x][y]
        range_ = range(0, len(image), self.pool_l)
        out = [[0 for _ in range_] for _ in range_]
        if self.pooling_method:
            for i in range_:
                for j in range_:
                    max = -1
                    for x in range(self.size):
                        for y in range(self.size):
                            if max == -1 or temp[i + x][j + y] > max:
                                max = temp[i + x][j + y]
                    out[i][j] = max
        else:
            for i in range_:
                for j in range_:
                    avg = 0
                    for x in range(self.size):
                        for y in range(self.size):
                            avg += temp[i + x][j + y]
                    out[i][j] = avg / (self.size * self.size)
        output = []

        for i in out:
            for j in i:
                output.append(j)
        return output


class MLP_Network(object):
    __slots__ = (
        'name', 'sizes', 'weights', 'biases', 'accuracy', 'softmax', 'softmax_out', 's_weights', 's_biases', 'func',
        'func_prime', 'func_name', 'loss_func', 'loss_func_prime', 'loss_func_name', 'learning_rate', 'neurons',
        'num_layers', 'z', 'alpha', 'beta', 'epsilon', 'weight_hat', 'bias_hat', 'momentum_weight', 'RMSProp_weight',
        'momentum_bias', 'RMSProp_bias', 'grad_s_bias', 'grad_s_weight', 'softmax_outpt')

    def find_name(self, filename: str) -> str:
        if os.path.isfile(filename):
            if filename.split('New Network')[1] == '':
                self.find_name('New Network 1')
            else:
                self.find_name('New Network ' + str(int(filename.split('New Network')[1]) + 1))
        else:
            self.name = filename

    def __init__(self, sizes=None, act_func=None, softmax_layer=False, softmax_out=2, loss_func=None,
                 name=None, read=False, FileName="New Network", learning_rate=8e-6):  # tested
        if read:
            with open(FileName, 'r') as file:
                data = [file.readline().split(')  ')[1].replace("\n", "") for _ in range(14)]
                file.close()
            temp = data
            self.name = temp[0]
            temp[2] = temp[2].split('|')[:-1]
            self.sizes = [int(x) for x in temp[2]]
            temp[3], self.weights = temp[3].split('|')[:-1], []
            for x in zip(temp[3], range(len(temp[3]))):
                self.weights.append([])
                for j in zip(x[0].split(';'), range(len(x[0].split(';')))):
                    self.weights[x[1]].append([])
                    for m in j[0].split(','):
                        self.weights[x[1]][j[1]].append(float(m))
            temp[4], self.biases = temp[4].split('|')[:-1], []
            for x in zip(temp[4], range(len(temp[4]))):
                self.biases.append([])
                for j in x[0].split(','):
                    self.biases[x[1]].append(float(j))
            self.accuracy = temp[5]
            func_lst = activate_dict[temp[6]]
            self.softmax = temp[7] == 'True'
            if self.softmax:
                self.softmax_out = int(temp[8])
                temp[9], self.s_weights = temp[9].split('|')[:-1], []
                for x in zip(temp[9], range(len(temp[9]))):
                    self.s_weights.append([])
                    for j in x[0].split(','):
                        self.s_weights[x[1]].append(float(j))
                self.s_biases = [float(m) for m in temp[10].split('|')[:-1]]
            else:
                self.softmax_out, self.s_biases, self.s_weights = 'N/A', 'N/A', 'N/A'
            loss_func_lst = loss_dict[temp[11]]
            self.func = func_lst[0]
            self.func_prime = func_lst[1]
            self.func_name = func_lst[2]
            self.loss_func = loss_func_lst[0]
            self.loss_func_name = loss_func_lst[1]
            self.loss_func_prime = loss_func_lst[2]
            print("Network \"" + self.name + "\" from " + temp[1] + " loaded")
        else:
            if sizes is None:
                sizes = [1, 1]
            if loss_func is None:
                loss_func = QuadraticCost
            if act_func is None:
                act_func = ReLU
            if name is None:
                self.find_name('New Network')
            else:
                self.name = name
            self.learning_rate = learning_rate
            self.sizes = sizes
            self.biases = [[np.random.randn() for _ in range(y)] for y in sizes[1:]]
            self.weights = [[[np.random.randn() for _ in range(x)] for _ in range(y)] for x, y in
                            zip(sizes[:-1], sizes[1:])]
            self.softmax = softmax_layer
            if self.softmax:
                self.softmax_out = softmax_out
                self.s_weights = [[np.random.randn() for _ in range(sizes[-1])] for _ in range(softmax_out)]
                self.s_biases = [np.random.randn() for _ in range(softmax_out)]
            else:
                self.softmax_out, self.s_biases, self.s_weights = 'N/A', 'N/A', 'N/A'
            self.func = act_func[0]
            self.func_prime = act_func[1]
            self.func_name = act_func[2]
            self.loss_func = loss_func[0]
            self.loss_func_name = loss_func[1]
            self.loss_func_prime = loss_func[2]
            self.accuracy = 0
            print("New network \"" + self.name + "\" created!")
        self.neurons = [[0 for _ in range(x)] for x in sizes]
        self.num_layers = len(sizes)
        self.z = [[0 for _ in range(x)] for x in sizes]
        self.alpha = 0.9
        self.beta = 0.9
        self.epsilon = 1e-6
        self.weight_hat = self.weights
        self.bias_hat = self.biases
        self.momentum_weight = [[[0 for _ in range(x)] for _ in range(y)] for x, y in
                                zip(self.sizes[:-1], self.sizes[1:])]
        self.RMSProp_weight = [[[0 for _ in range(x)] for _ in range(y)] for x, y in
                               zip(self.sizes[:-1], self.sizes[1:])]
        self.momentum_bias = [[0 for _ in range(y)] for y in self.sizes[1:]]
        self.RMSProp_bias = [[0 for _ in range(y)] for y in self.sizes[1:]]
        if self.softmax:
            self.grad_s_bias = [0 for _ in range(self.softmax_out)]
            self.grad_s_weight = [[0 for _ in range(self.sizes[-1])] for _ in range(self.softmax_out)]
            self.softmax_outpt = []

    @staticmethod
    def calc(w, x, b):  # tested
        return b + sum(x[0] * x[1] for x in zip(w, x))

    def calc_neurons(self):  # tested
        for x in range(1, self.num_layers):
            for j in range(self.sizes[x]):
                z = self.calc(self.weights[x - 1][j], self.neurons[x - 1], self.biases[x - 1][j])
                self.z[x][j] = z
                self.neurons[x][j] = self.func(z)

    def train_feed_forward(self):
        for x in range(1, self.num_layers):
            for j in range(self.sizes[x]):
                z = self.calc(self.weight_hat[x - 1][j], self.neurons[x - 1], self.bias_hat[x - 1][j])
                self.z[x][j] = z
                self.neurons[x][j] = self.func(z)

    def softmax_layer(self):  # tested
        x = self.neurons[-1]
        ret = [np.exp(self.calc(self.s_weights[m], x, self.s_biases[m])) for m in range(self.softmax_out)]
        s = sum(ret)
        for m in ret:
            m /= s
        self.softmax_outpt = ret
        return ret

    def calc_loss(self, x, y) -> float:  # tested
        temp = 0.0
        for m in zip(x, y):
            temp += self.loss_func(m[0], m[1])
        return temp

    def __call__(self, input_, train: bool = False) -> list:  # tested
        if type(input_) != list:
            input_ = [input_]
        length = len(input_)
        if length == self.sizes[0]:
            self.neurons[0] = input_
            self.z[0] = input_
            if train:
                self.train_feed_forward()
            else:
                self.calc_neurons()
            if self.softmax:
                return self.softmax_layer()
            return self.neurons[-1]
        else:
            raise "Input Length Incorrect (desired:" + str(self.sizes[0]) + ", input:" + str(length) + ")"

    def gradient(self, x, w, z, fz, y):
        dc_db = [self.func_prime(a) * self.loss_func_prime(b, c) for a, b, c in zip(z, fz, y)]
        dc_dw = [[m * j for j in x] for m in dc_db]
        dc_da = [sum([a * j for a, j in zip(dc_db, m)]) for m in transpose(w)]
        return [dc_dw, dc_db, dc_da]

    def _backpropagation(self, y, layer=None):  # returns Del C Del Input
        if layer == -1:
            return y
        if layer is None:
            layer = self.num_layers - 2
        temp = self.gradient(self.neurons[layer], self.weights[layer], self.z[layer + 1], self.neurons[layer + 1], y)
        self.momentum_weight[layer] = array_operation(self.momentum_weight[layer], temp[0],
                                                      lambda a, b: a * self.alpha - self.learning_rate * b)
        self.RMSProp_weight[layer] = array_operation(self.RMSProp_weight[layer], temp[0],
                                                     lambda a, b: a * self.beta + self.learning_rate * b * b)
        self.momentum_bias[layer] = array_operation(self.momentum_bias[layer], temp[1],
                                                    lambda a, b: a * self.alpha - self.learning_rate * b)
        self.RMSProp_bias[layer] = array_operation(self.RMSProp_bias[layer], temp[1],
                                                   lambda a, b: a * self.beta + self.learning_rate * b * b)
        return self._backpropagation(temp[2], layer - 1)

    def Gradient_Descent(self):
        self.weights = array_operation(self.weights, array_operation(self.momentum_weight, self.RMSProp_weight,
                                                                     lambda a, b: a / (np.sqrt(b) + self.epsilon)),
                                       lambda a, b: a - b)
        self.biases = array_operation(self.biases, array_operation(self.momentum_bias, self.RMSProp_bias,
                                                                   lambda a, b: a / (np.sqrt(b) + self.epsilon)),
                                      lambda a, b: a - b)
        self.weight_hat = array_operation(self.weights, self.momentum_weight, lambda a, b: a + b * self.alpha)
        self.bias_hat = array_operation(self.biases, self.momentum_bias, lambda a, b: a + b * self.alpha)
        if self.softmax:
            self.s_weights = array_operation(self.s_weights, self.grad_s_weight,
                                             lambda a, b: a - self.learning_rate * b)
            self.s_biases = array_operation(self.s_biases, self.grad_s_bias, lambda a, b: a - self.learning_rate * b)
            self.grad_s_bias = [0 for _ in range(self.softmax_out)]
            self.grad_s_weight = [[0 for _ in range(self.sizes[-1])] for _ in range(self.softmax_out)]

    def backpropagation(self, y):
        if type(y) != list:
            y = [y]
        if self.softmax:
            dc_db = [a + 1 - 2 * b for a, b in zip(self.softmax_outpt, y)]
            dc_dw = [[m * j for j in self.neurons[-1]] for m in dc_db]
            dc_da = [sum([a * j for a, j in zip(dc_db, m)]) for m in transpose(self.s_weights)]
            self.grad_s_bias = array_operation(self.grad_s_bias, dc_db)
            self.grad_s_weight = array_operation(self.grad_s_weight, dc_dw)
            y = dc_da
        return self._backpropagation(y)

    def save_as(self, filename: str = None) -> None:  # tested
        if filename is None:
            filename = self.name
        with open(filename, 'w') as file:
            file.write("network)  " + filename + '\n')
            file.write("time)  " + str(ctime()) + '\n')
            file.write("sizes)  ")
            temp = ''
            for m in self.sizes:
                temp += str(m) + '|'
            temp += '\n'
            file.write(temp)
            file.write("weights)  ")
            temp = ''
            for layer in self.weights:
                for neuron in layer:
                    for weight in neuron:
                        temp += str(weight) + ','
                    temp += ';'
                temp += '|'
            temp += '\n'
            file.write(temp.replace(',;', ';').replace(';|', '|'))
            file.write("biases)  ")
            temp = ''
            for layer in self.biases:
                for bias in layer:
                    temp += str(bias) + ','
                temp += '|'
            temp += '\n'
            file.write(temp.replace(',|', '|'))
            if self.accuracy:
                file.write("accuracy)  " + str(self.accuracy) + '\n')
            else:
                file.write("accuracy)  ???\n")
            file.write("activation function)  " + self.func_name + '\n')
            file.write("softmax)  " + str(self.softmax) + '\n')
            if self.softmax:
                file.write("softmax output number)  " + str(self.softmax_out) + '\n')
                file.write("softmax weights)  ")
                temp = ''
                for neuron in self.s_weights:
                    for weight in neuron:
                        temp += str(weight) + ','
                    temp += '|'
                file.write(temp.replace(',|', '|') + '\n')
                file.write("softmax biases)  ")
                temp = ''
                for m in self.s_biases:
                    temp += str(m) + '|'
                file.write(temp + '\n')
            else:
                file.write("softmax output number)  N/A\nsoftmax weights)  N/A\nsoftmax biases)  N/A\n")
            file.write("loss function)  " + self.loss_func_name + '\n')
            file.write("learning rate)  " + str(self.learning_rate))
            file.close()
        print('Successfully saved network \"' + self.name + '\" as \"' + filename + '\"!')

    def train(self, inputs: list, outputs: list, iterations: int = 40) -> None:
        datasets = [j for j in zip(inputs, outputs)]
        for _ in range(iterations):
            '''
            self.momentum_weight = [[[0 for _ in range(x)] for _ in range(y)] for x, y in
                                    zip(self.sizes[:-1], self.sizes[1:])]
            self.RMSProp_weight = [[[0 for _ in range(x)] for _ in range(y)] for x, y in
                                   zip(self.sizes[:-1], self.sizes[1:])]
            self.momentum_bias = [[0 for _ in range(y)] for y in self.sizes[1:]]
            self.RMSProp_bias = [[0 for _ in range(y)] for y in self.sizes[1:]]
            '''
            shuffle(datasets)
            for m in datasets:
                self(m[0], train=False)
                self.backpropagation(m[1])
                self.Gradient_Descent()


def Linear_Regression(data: list = None, inpt: list = None, outpt: list = None, cdata: str = 'blue', cline: str = 'red',
                      save_data: bool = False, filename: str = 'Linear Regression'):
    if data is None:
        data = []
    if inpt is None:
        inpt = []
    if outpt is None:
        outpt = []
    if data:
        for inout in data:
            inpt.append(inout[0])
            outpt.append(inout[1])
    a = MLP_Network(act_func=linear, sizes=[1, 3, 6, 3, 1])
    while True:
        iteration = int(input('Iterations(0 to reset optimiser, -1 to end):'))
        if iteration == -1:
            break
        if iteration == 0:
            a.momentum_weight = [[[0 for _ in range(x)] for _ in range(y)] for x, y in
                                    zip(a.sizes[:-1], a.sizes[1:])]
            a.RMSProp_weight = [[[0 for _ in range(x)] for _ in range(y)] for x, y in
                                   zip(a.sizes[:-1], a.sizes[1:])]
            a.momentum_bias = [[0 for _ in range(y)] for y in a.sizes[1:]]
            a.RMSProp_bias = [[0 for _ in range(y)] for y in a.sizes[1:]]
        a.train(inpt, outpt, iterations=iteration)
        plt.scatter(inpt, outpt, color=cdata, label='Data')
        j = [a(k)[0] for k in inpt]
        plt.plot(inpt, j, color=cline, label='Regression Line')
        plt.legend()
        plt.show()
        plt.close()
    if save_data:
        a.save_as(filename=filename)


def plot_net(network_name: str) -> None:
    if not os.path.isfile(network_name):
        raise "file not found"
    a = MLP_Network(read=True, FileName=network_name)
    plot_func([a], [a.name])


if __name__ == '__main__':
    Linear_Regression(inpt=[[i] for i in range(100)], outpt=[[2 * i + 10 * np.random.randn() + 30] for i in range(100)])
