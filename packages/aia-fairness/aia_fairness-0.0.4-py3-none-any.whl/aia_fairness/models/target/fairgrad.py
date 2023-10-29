import  numpy as np
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR
from torch.utils.data import Dataset, DataLoader

from fairgrad import CrossEntropyLoss

class Net(nn.Module):
    def __init__(self, input_size):
        self.arch = "full"
        super(Net, self).__init__()
        if self.arch == "conv":
            self.conv1 = nn.Conv2d(3,32,kernel_size=3, stride=1, padding=1)
            self.relu1 = nn.ReLU()
            self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
            self.conv2 = nn.Conv2d(32,64,kernel_size=3,stride=1,padding=1)
            self.relu2 = nn.ReLU()
            self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)

            self.fc1 = nn.Linear(64 * 15 * 11, 128)
            self.relu3 = nn.ReLU()
            self.fc2 = nn.Linear(128, 10)
            self.relu4 = nn.ReLU()
            self.fc3 = nn.Linear(10, 2)
            self.sigmoid = nn.Sigmoid()


        elif self.arch == "full":
            self.fc1 = nn.Linear(input_size, 2914)
            #self.fc1 = nn.Linear(3*2914, 2914)
            self.fc2 = nn.Linear(2914, 128)
            self.fc3 = nn.Linear(128, 10)
            self.fc4 = nn.Linear(10, 2)
            self.sigmoid = nn.Sigmoid()


    def forward(self, x):
        if self.arch == "conv":
            x = self.conv1(x)
            x = self.relu1(x)
            x = self.pool1(x)

            x = self.conv2(x)
            x = self.relu2(x)
            x = self.pool2(x)

            x = x.view(x.size(0), -1)

            x = self.fc1(x)
            x = self.relu3(x)
            x = self.fc2(x)
            x = self.relu4(x)
            x=self.fc3(x)
            output = self.sigmoid(x)

        elif self.arch == "full":
            #x = torch.flatten(x,1)
            x = self.fc1(x)
            x = F.relu(x)
            x = self.fc2(x)
            x = F.relu(x)
            x = self.fc3(x)
            x = F.relu(x)
            x = self.fc4(x)
            output = self.sigmoid(x)


        return output

def onehot(y):
    n = np.shape(y)[0]
    onehot = np.zeros([n,2])
    onehot[y==1,1] = 1
    onehot[y==0,0] = 1
    return onehot.astype(np.float32)

class LFWdset(Dataset):

    def __init__(self,x,y,z=np.array([None])):
        self.x = x.astype(np.float32)
        #self.y = onehot(y)
        #self.y = y.astype(np.float32)
        self.y = y
        self.z = z

    def __len__(self):
        return np.shape(self.y)[0]

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        if (self.z!=None).any():
            return self.x[idx],self.y[idx],self.z[idx]
        else:
            return self.x[idx],self.y[idx]

class target_model:
    def __init__(self, input_size):
        self.model = Net(input_size)
        self.fair=False

    def set_fair(self, fair):
        self.fair=fair

    def fit(self,x,y,z=np.array([None])): 

        #GPU
        use_cuda = torch.cuda.is_available()
        use_mps = torch.backends.mps.is_available()

        #torch.manual_seed(args.seed)

        if use_cuda:
            device = torch.device("cuda")
        elif use_mps:
            device = torch.device("mps")
        else:
            device = torch.device("cpu")

        train_kwargs = {'batch_size': 50}
        if use_cuda:
            cuda_kwargs = {'num_workers': 1,
                           'pin_memory': True,
                           'shuffle': True}
            train_kwargs.update(cuda_kwargs)

        #Data
        dataset = LFWdset(x,y,z)
        train_loader = torch.utils.data.DataLoader(dataset, **train_kwargs)
        
        #Optimization
        self.model = self.model.to(device)

        if self.fair:
            criterion = CrossEntropyLoss(y_train=torch.tensor(y),
                                         s_train=torch.tensor(z),
                                         fairness_measure="demographic_parity")
        else:
            criterion = nn.CrossEntropyLoss()

        optimizer = optim.Adam(self.model.parameters(), lr=0.001)

        num_epochs = 10
        #Training
        for epoch in range(num_epochs):
            self.model.train()
            running_loss = 0.0
            correct=0
            total=0
            for batch in train_loader:
                if self.fair:
                    xb,yb,zb = batch
                    xb, yb, zb = xb.to(device), yb.to(device), zb.to(device)
                else:
                    xb,yb = batch
                    xb, yb= xb.to(device), yb.to(device)
                optimizer.zero_grad()
                output = self.model(xb)

                if self.fair:
                    loss = criterion(output,yb.long(), zb, mode="train")
                else:
                    loss = criterion(output,yb.long())

                loss.backward()
                optimizer.step()
                running_loss += loss.item()
                predicted = np.argmax(output.cpu().detach().numpy(),axis=1)
                correct += (predicted == yb.cpu().detach().numpy()).sum().item()
                total += yb.size(0)


            epoch_loss = running_loss / len(train_loader)
            epoch_acc = correct / total
        
            #print(f"Epoch {epoch+1}/{num_epochs} - Loss: {epoch_loss:.4f} - Accuracy: {epoch_acc*100:.2f}%")



    def predict_proba(self, x):
        #GPU
        use_cuda = torch.cuda.is_available()
        use_mps = torch.backends.mps.is_available()

        #torch.manual_seed(args.seed)

        if use_cuda:
            device = torch.device("cuda")
        elif use_mps:
            device = torch.device("mps")
        else:
            device = torch.device("cpu")

        x = torch.from_numpy(x).float()
        x = x.to(device)

        with torch.no_grad():
            predictions = self.model(x).cpu().detach().numpy()

        return predictions

    def predict(self, x):
        prediction = self.predict_proba(x)
        yhat = np.argmax(prediction, axis=1)
        return yhat
