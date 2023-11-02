import json
import numpy as np
import spacy
import torch
import torch.nn as nn
import torch.optim as optim
from Janex import *

class SimpleRNN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(SimpleRNN, self).__init__()
        self.rnn = nn.RNN(input_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        out, _ = self.rnn(x)
        return out

def decompress(janex_model):
    with open(f"{janex_model}", "rb") as bin_file:
        json_data = bin_file.read()
        loaded_data = json.loads(json_data.decode('utf-8'))
        return loaded_data

class NLG:
    def __init__(self, spacy_model, janex_model):
        self.nlp = spacy.load(spacy_model)
        self.trends_dictionary = decompress(janex_model)
        self.max_tokens = 20
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.rnn_model = SimpleRNN(300, 128, len(self.trends_dictionary))

    def set_device(self, device_type):
        self.device = torch.device(device_type)

    def get_word_vector(self, word):
        return self.nlp(word).vector

    def predict_next_word(self, input_word):
        context_window_size = 3
        context_vectors = np.array([self.get_word_vector(word) for word in self.inputs.split()[-context_window_size:]])

        context_vectors = np.resize(context_vectors, 300)
        # Assuming you have already prepared context_vectors as input
        context_tensor = torch.Tensor(context_vectors).unsqueeze(0)  # Add batch dimension

        output = self.rnn_model(context_tensor)
        _, predicted_idx = torch.max(output, 1)
        best_next_word = list(self.trends_dictionary.keys())[predicted_idx.item()]

        if best_next_word and output[0, predicted_idx.item()] > 0.1:
            return best_next_word

    def generate_sentence(self, input):
        sentence = ""

        for _ in range(self.max_tokens):
            self.inputs = input
            input = sentence[:-1]
            next_word = self.predict_next_word(input)
            sentence = f"{sentence} {next_word}"

        return sentence

if __name__ == "__main__":
    Gen = NLG("en_core_web_sm", "janex.bin")
    input_sentence = input("You: ")
    ResponseOutput = Gen.generate_sentence(input_sentence)
    ResponseOutput = ResponseOutput.replace("\n", " ")
    ResponseOutput = ResponseOutput.replace("  ", " ")
    print(ResponseOutput)
