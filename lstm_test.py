# -*- coding: utf-8 -*-
"""LSTM_Test

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bkvD7cvB7GlkhkPMAL0hBtli6Ous8pLM
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import math
import random

torch.manual_seed(1)

lstm = nn.LSTM(3, 3)  # Input dim is 3, output dim is 3
inputs = [torch.randn(1, 3) for _ in range(5)]  # make a sequence of length 5

# initialize the hidden state.
hidden = (torch.randn(1, 1, 3),
          torch.randn(1, 1, 3))
for i in inputs:
    # Step through the sequence one element at a time.
    # after each step, hidden contains the hidden state.
    out, hidden = lstm(i.view(1, 1, -1), hidden)

# alternatively, we can do the entire sequence all at once.
# the first value returned by LSTM is all of the hidden states throughout
# the sequence. the second is just the most recent hidden state
# (compare the last slice of "out" with "hidden" below, they are the same)
# The reason for this is that:
# "out" will give you access to all hidden states in the sequence
# "hidden" will allow you to continue the sequence and backpropagate,
# by passing it as an argument  to the lstm at a later time
# Add the extra 2nd dimension
inputs = torch.cat(inputs).view(len(inputs), 1, -1)
hidden = (torch.randn(1, 1, 3), torch.randn(1, 1, 3))  # clean out hidden state
out, hidden = lstm(inputs, hidden)
print(out)
print(hidden)

def prepare_sequence(seq, to_ix):
    #print(seq)
    #print("to_ix: " + str(to_ix))
    idxs = [to_ix[seq]]
    return torch.tensor(idxs, dtype=torch.long)


  
training_data = []
for i in range(1000):
  x = random.uniform(-1.5, 1.5)
  y = random.uniform(-1.5, 1.5)
  max_val = max(math.sin(x), math.cos(x))
  min_val = min(math.sin(x), math.cos(x))
  if y < max_val and y > min_val:
    training_data.append(((x, y), 1))
  else:
    training_data.append(((x, y), 0))
point_to_ix = {}
for point, on_funct in training_data:
    if point not in point_to_ix:
        point_to_ix[point] = len(point_to_ix)
print(point_to_ix)
#tag_to_ix = {"TRUE": 1, "FALSE": 0}
# print(training_data)
# These will usually be more like 32 or 64 dimensional.
# We will keep them small, so we can see how the weights change as we train.
EMBEDDING_DIM = 32
HIDDEN_DIM = 32

class LSTMTagger(nn.Module):

    def __init__(self, embedding_dim, hidden_dim, vocab_size, tagset_size):
        super(LSTMTagger, self).__init__()
        self.hidden_dim = hidden_dim
        self.word_embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim)
        self.hidden2tag = nn.Linear(hidden_dim, tagset_size)

    def forward(self, sentence):
        embeds = self.word_embeddings(sentence)
        lstm_out, _ = self.lstm(embeds.view(len(sentence), 1, -1))
        tag_space = self.hidden2tag(lstm_out.view(len(sentence), -1))
        tag_scores = F.log_softmax(tag_space, dim=1)
        return tag_scores

model = LSTMTagger(EMBEDDING_DIM, HIDDEN_DIM, len(point_to_ix), 2)
loss_function = nn.NLLLoss()
optimizer = optim.SGD(model.parameters(), lr=0.1)

# See what the scores are before training
# Note that element i,j of the output is the score for tag j for word i.
# Here we don't need to train, so the code is wrapped in torch.no_grad()
with torch.no_grad():
    inputs = prepare_sequence(training_data[0][0], point_to_ix)
    tag_scores = model(inputs)
    print(tag_scores)

for epoch in range(30):  # again, normally you would NOT do 300 epochs, it is toy data
    for point, on_funct in training_data:
        # Step 1. Remember that Pytorch accumulates gradients.
        # We need to clear them out before each instance
        model.zero_grad()

        # Step 2. Get our inputs ready for the network, that is, turn them into
        # Tensors of word indices.
        sentence_in = prepare_sequence(point, point_to_ix)
        targets = torch.tensor([on_funct], dtype=torch.long)

        # Step 3. Run our forward pass.
        tag_scores = model(sentence_in)

        # Step 4. Compute the loss, gradients, and update the parameters by
        #  calling optimizer.step()
        loss = loss_function(tag_scores, targets)
        loss.backward()
        optimizer.step()

# See what the scores are after training
test_point = (4,-0.7568024953)
with torch.no_grad():
    inputs = prepare_sequence(test_point, point_to_ix)
    tag_scores = model(inputs)

    # The sentence is "the dog ate the apple".  i,j corresponds to score for tag j
    # for word i. The predicted tag is the maximum scoring tag.
    # Here, we can see the predicted sequence below is 0 1 2 0 1
    # since 0 is index of the maximum value of row 1,
    # 1 is the index of maximum value of row 2, etc.
    # Which is DET NOUN VERB DET NOUN, the correct sequence!
    print(tag_scores)

parts = ['on the curve', 'not on the curve']
for i in tag_scores:
  a = np.argmax(i)
  print(str(test_point) + 'is ' + str(parts[a]), end = " ")