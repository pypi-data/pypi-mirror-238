import torch.nn as nn
import torch.nn.functional as F
import torch

class ClassifierNet(nn.Module):
    
    def __init__(self, input_size, hidden_size, output_size,
                 batch_size, dropout_prop):
        super(ClassifierNet, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.batch1 = nn.BatchNorm1d(hidden_size)
        self.fc2 = nn.Linear(hidden_size, batch_size)
        self.batch2 = nn.BatchNorm1d(batch_size)
        self.fc3 = nn.Linear(batch_size, output_size)
        self.dropout = nn.Dropout(dropout_prop)

    def forward(self, x):
        x = self.batch1(self.dropout(F.relu(self.fc1(x))))
        x = self.batch2(self.dropout(F.relu(self.fc2(x))))
        x = F.softmax(self.fc3(x), dim=1)

        return x

class RegressorNet(nn.Module):

    def __init__(self, input_size, hidden_size, batch_size, dropout_prop):
        super(RegressorNet, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.batch1 = nn.BatchNorm1d(hidden_size)
        self.fc2 = nn.Linear(hidden_size, batch_size)
        self.batch2 = nn.BatchNorm1d(batch_size)
        self.fc3 = nn.Linear(batch_size, batch_size)
        self.fc4 = nn.Linear(batch_size, 2)
        self.fc5 = nn.Linear(2, 2)
        self.dropout = nn.Dropout(dropout_prop)

    def forward(self, x):
        x = self.batch1(self.dropout(F.elu(self.fc1(x))))
        x = self.batch2(self.dropout(F.elu(self.fc2(x))))
        x = F.elu(self.fc3(x))
        x = F.elu(self.fc3(x))
        x = self.fc5(self.fc4(x))

        return x