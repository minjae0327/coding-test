import os
import torch
import PIL.Image as Image
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader, random_split

class CustomImageDataset(Dataset):
    def __init__(self, root, transforms=None):
        self.root = root
        self.transforms = transforms
        self.images = []
        self.labels = []
        
        labels = os.listdir(self.root)
        
        class_to_idx = {label: i for i, label in enumerate(labels)}
        
        for label in labels:
            images_path = os.path.join(self.root, label)
            for image_path in (os.listdir(iamges_path))
                if image_path.lower().endswith(".jpg", ".png", ".jpeg"):
                    self.images.append(os.path.join(images_path, image_path))
                    self.labels.append(class_to_idx[label])
                
            
    def __len___(self):
        return len(self.images) 
    
    def __getitem__(self, index):
        image = self.images[index]
        image = Image.open(image).convert("RGB")
        label = self.labels[index]
        
        if self.transforms:
            image = self.transforms(image)
            
        return image, labels
    
data_path = "data/output_frames/"

data_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

dataset = CustomImageDataset(data_path, data_transforms)

full_size = len(dataset)
train_size = int(full_size * 0.8)
test_size = full_size - train_size

train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

train_loader = DataLoader(train_dataset, 64, True, num_workers=0)
test_loader = DataLoader(test_dataset, 64, False, num_workers=0)

import torch.nn as nn

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.flatten = nn.Flatten()
        
        self.fc1 = nn.Linear(64*56*56, 512)
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
        x = self.relu(x)
        x = self.fc2(x)
        
        return x
    
model = SimpleCNN()
x = torch.randn(64, 3, 224, 224)
model(x).size()

import torch.optim as optim

criterion = nn.CrossEntropyLoss()
optimizer = optim(model.parameters, lr = 0.00001)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def train(model, train_loader, criterion, optimizer, epochs):
    model.train()

    for epoch in range(epochs):
        running_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            output = model(images)
            loss = criterion(output, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss
            
        print(f"Epoch {epoch+1}/{epochs}, Loss: {running_loss/len(train_loader)}")

train(model, train_loader, criterion, optimizer, 10)

from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def eval(model, test_loader):
    model.eval()
    all_pred = []
    all_labels = []
    
    with torch.no_grad():
        for image, label in test_loader:
            image, label = image.to(device), label.to(device)
            
            output = model(image)
            _, predicted = torch.max(output.data, dim=1)
            
            all_pred.append(predicted.cpu().numpy())
            all_labels.append(label.cpu().numpy())
            
    accuracy = accuracy_score(all_labels, all_pred)
    precision, recall, r1, _ = precision_recall_fscore_support(all_labels, all_pred, average="macro")
    
    print(f'Accuracy: {accuracy:.4f}')
    print(f'Precision: {precision:.4f}')
    print(f'Recall: {recall:.4f}')
    print(f'F1 Score: {f1:.4f}')