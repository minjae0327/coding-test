import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

train_transform = transforms.Compose([
    transforms.RandomCrop(32, 4),
    transforms.RandomVerticalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

train_dataset = torchvision.datasets.CIFAR10("./data", True, train_transform, download=False)
test_dataset = torchvision.datasets.CIFAR10("./data", False, test_transform, download=False)

train_loader = torch.utils.data.DataLoader(train_dataset, 64, True, num_workers=2)
test_loader = torch.utils.data.DataLoader(test_dataset, 64, True, num_workers=2)

classes = train_dataset.classes


class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        self.flatten = nn.Flatten()
        
        self.fc1 = nn.Linear(64*8*8, 512)
        self.fc2 = nn.Linear(512, 10)
        
    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = self.pool(x)
        
        x = self.flatten(x)
        
        x = self.fc1(x)
        x = self.fc2(x)
        
        return x
    
model = SimpleCNN()
x = torch.randn(64, 3, 32, 32)
model(x).size()


# from torchvision.models import resnet18, ResNet18_Weights

# model = resnet18(ResNet18_Weights.DEFAULT)

# for param in model.parameters():
#     param.requires_grad() = False
    
# num_features = model.fc.in_features
# model.fc = nn.Linear(num_features, 10)




criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def train(model, train_loader, criterion, optimizer, epochs):
    model.train()
    
    for epoch in range(epochs):
        running_loss = 0.0
        for data in train_loader:
            X, y = data
            X, y = X.to(device), y.to(device)
            
            optimizer.zero_grad()
            
            output = model(X)
            
            loss = criterion(output, y)
            
            loss.backward()
            
            optimizer.step()
            
            running_loss += loss.item()
            
        print(f"epoch:{epoch+1}, loss : {running_loss / len(train_loader)}")
            
train(model, train_loader, criterion, optimizer, 5)
            
            

def evaluate(model, test_loader):
    model.eval() # 모델을 평가 모드로 설정
    all_preds = []
    all_labels = []

    # 평가 시에는 기울기 계산이 필요 없으므로 no_grad() 사용
    with torch.no_grad():
        for data in test_loader:
            X, y = data
            X, y = X.to(device), y.to(device)
            
            outputs = model(X)
            _, predicted = torch.max(outputs.data, 1)
            
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(y.cpu().numpy())
    
    # 1. 평가 지표 계산
    accuracy = accuracy_score(all_labels, all_preds)
    precision, recall, f1, _ = precision_recall_fscore_support(all_labels, all_preds, average='macro')
    
    
    print(f'Accuracy: {accuracy:.4f}')
    print(f'Precision: {precision:.4f}')
    print(f'Recall: {recall:.4f}')
    print(f'F1 Score: {f1:.4f}')
    
evaluate(model, test_loader)