import math
import spacy
import random
import numpy as np

nlp = spacy.load("en_core_web_md")

def initialize_random_weights(num_weights):
    return [random.uniform(-1, 1) for _ in range(num_weights)]

def initialize_random_bias():
    return random.uniform(-1, 1)

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def simple_neuron(inputs, weights, bias):
    weighted_sum = sum(input_i * weight_i for input_i, weight_i in zip(inputs, weights))
    return sigmoid(weighted_sum + bias)


if __name__ == "__main__":
    input_sentence = input("You: ")
    inputs = nlp(input_sentence).vector

    inputs = np.resize(inputs, 300)

    weights = initialize_random_weights(300)
    bias = initialize_random_bias()

    output = simple_neuron(inputs, weights, bias)
    print(output)
