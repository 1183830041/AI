import torch
import torch.nn as nn
from torch.autograd import Variable
import torchvision.datasets as dset
import torchvision.transforms as transforms
import torch.nn.functional as F
import torch.optim as optim
import os.path as IO
import numpy as np
from PIL import Image

def ImageProcessing(data):
    x = np.array([[0.0947416, 0.118318, 0.0947416], [0.118318, 0.147761, 0.118318], [0.0947416, 0.118318, 0.0947416]])
    x_reshape = np.reshape(x, 9, order='C')
    for k in range(50):
        p = np.zeros((28, 28))
        for i in range(27):
            for j in range(27):
                for a in range(0, 3):
                    for b in range(0, 3):
                        p[i][j] += data[k, 0, i+a-1, j+b-1] * x[a][b]
        data[k, 0, 0:28, 0:28] = torch.from_numpy(p)
    for k in range(0,50):
        data_tmp = np.zeros((28,28))
        data_tmp[0:28,0:28] = data[k,0,0:28,0:28]
        im_data = np.array(data_tmp * 255, dtype=np.int8)
        img = Image.fromarray(im_data, 'L')
        img.save('test' + str(k) + '.png')
        img.show()


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        # 1 input image channel, 6 output channels, 5x5 square convolution
        # kernel
        self.conv1 = nn.Conv2d(1, 5, 5)
        self.conv2 = nn.Conv2d(5, 10, 5)
        self.conv3 = nn.Conv2d(10, 20, 5)
        self.conv4 = nn.Conv2d(20, 10, 5)
        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(10 * 12 * 12, 64)
        self.fc2 = nn.Linear(64, 10)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        #conv1.append(x)
        x = F.relu(self.conv2(x))
        #conv2.append(x)
        x = F.relu(self.conv3(x))
        #conv3.append(x)
        x = F.relu(self.conv4(x))
        #conv4.append(x)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features

net = Net()
for layer in list(net._modules.items()):
    print(layer[1])

"""
def for_hook(module, input, output):
    print(module)
    for val in input:
        print("input val:",val.size())
    for out_val in output:
        print("output val:", out_val.size())
"""
# net.conv2.register_forward_hook(for_hook)
# net.conv3.register_forward_hook(for_hook)
batchSize = 50
trans = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (1.0,))])
# print(IO.exists('../MNIST_DATA/train-labels-idx1-ubyte'))
train_set = dset.MNIST('F:\python\PyCharm 2019.3.3\MNIST', train=True, transform=trans, download=True)
test_set = dset.MNIST('F:\python\PyCharm 2019.3.3\MNIST', train=False, transform=trans, download=True)
# img, label = train_set[0]

train_loader = torch.utils.data.DataLoader(dataset=train_set,
                                           batch_size=batchSize,
                                           shuffle=True)

test_loader = torch.utils.data.DataLoader(dataset=test_set,
                                          batch_size=batchSize,
                                          shuffle=False)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(),lr=1e-3)
savePath = 'F:\python\PyCharm 2019.3.3\MNIST'
appendix = '.t7'
#   print(IO.exists(savePath))
loss_bound = 0.01








def train(epoch): # epoch -- ensemble number
    for i in range(epoch):
        for batch_idx, (data, target) in enumerate(train_loader):
        #   target = target.float()
            data, target = Variable(data), Variable(target)
            #if i == 0:
                #for k in range(0, 40):
                    #data_tmp = np.zeros((28, 28))
                    #data_tmp[0:28, 0:28] = data[k, 0, 0:28, 0:28]
                    #im_data = np.array(data_tmp * 255, dtype=np.int8)
                    #img = Image.fromarray(im_data, 'L')
                    #img.save('test' + str(k) + '.jpg')
                    #img.show()
            if i == 0:
                ImageProcessing(data)
            optimizer.zero_grad()
            output = net(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            if loss.item() < loss_bound:
                print("Epoch {0}:  Batch idx: {1}  Loss: {2} -- IO".format(i,batch_idx,loss.item()))
                break
            if batch_idx % 500 == 0:
                print("Epoch {0}:  Batch idx: {1}  Loss: {2}".format(i,batch_idx,loss.item()))
        path = savePath + str(i) + appendix
        torch.save(net.state_dict(),path)
Ensemble_num = 50
train(2)
net.eval()  # eval mode (batchnorm uses moving mean/variance instead of mini-batch mean/variance)
with torch.no_grad():
    correct = 0
    total = 0
    for images, labels in test_loader:
        outputs = net(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
    print('Test Accurac y of the model on the 10000 test images: {} %'.format(100 * correct / total))