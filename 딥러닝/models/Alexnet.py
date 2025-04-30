import torch
import torch.nn as nn

class AlexNet(nn.Module): # input : 227*227*3
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 48, kernel_size=11, stride=4),
            nn.ReLU(),
            nn.Conv2d(48, 48, kernel_size=3, stride=2),
            nn.LocalResponseNorm(5),
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(48, 128, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, stride=2),
            nn.LocalResponseNorm(5),
        )
        self.conv3 = nn.Sequential(
            nn.Conv2d(128, 192, kernel_size=3, padding=1),
            nn.ReLU()
        )
        self.conv4 = nn.Sequential(
            nn.Conv2d(192, 192, kernel_size=3, padding=1),
            nn.ReLU()
        )
        self.conv5 = nn.Sequential(
            nn.Conv2d(192, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3, stride=2)
        )
        
        self.fc1 = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 6 * 6, 2048),
            nn.ReLU(),
            nn.Dropout(0.5)
        )
        self.fc2 = nn.Sequential(
            nn.Linear(2048, 2048),
            nn.ReLU(),
            nn.Dropout(0.5)
        )
        self.fc3 = nn.Sequential(
            nn.Linear(4096, 1000)
        )
        
    def forward(self, x):
        a = x
        b = x
        
        a = self.conv1(a)
        a = self.conv2(a)
        a = self.conv3(a)
        a = self.conv4(a)
        a = self.conv5(a)
        a = self.fc1(a)
        a = self.fc2(a)
        
        b = self.conv1(b)
        b = self.conv2(b)
        b = self.conv3(b)
        b = self.conv4(b)
        b = self.conv5(b)
        b = self.fc1(b)
        b = self.fc2(b)
        
        out = torch.cat((a, b), dim=1)
        out = self.fc3(out)
        
        return out
    

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = AlexNet().to(device)
BATCH = 32

x = torch.rand(BATCH, 3,227,227)
model(x).size()