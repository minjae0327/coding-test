import torch
import matplotlib.pyplot as plt

device = "cude" if torch.cuda.is_available() else "cpu"

class EarlyStopping:
    def __init__(self, patience=7, min_delta=0, verbose=False):
        self.patience = patience
        self.min_delta = min_delta
        self.verbose = verbose
        self.counter = 0
        self.best_loss = None
        self.best_model_state = None  # 최적의 모델 상태를 저장
        self.early_stop = False

    def __call__(self, val_loss, model):
        if self.best_loss is None:
            self.best_loss = val_loss
            self.best_model_state = model.state_dict()  # 최초 상태 저장
        elif val_loss > self.best_loss - self.min_delta:
            self.counter += 1
            if self.verbose:
                print(f'EarlyStopping counter: {self.counter} out of {self.patience}')
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_loss = val_loss
            self.best_model_state = model.state_dict()  # 개선 시 모델 상태 업데이트
            self.counter = 0
            if self.verbose:
                print(f'Validation loss decreased ({self.best_loss:.6f} --> {val_loss:.6f})')

# 학습 함수
def train(_model, device, train_loader, optimizer, criterion, epoch):
    _model.train()
    running_loss = 0.0
    correct = 0
    total = len(train_loader.dataset)
    
    for data, label in train_loader:
        data, label = data.to(device), label.to(device)
        
        outputs = _model(data)
        if outputs.dim() == 3:
            outputs = outputs.mean(dim=0)
        loss = criterion(outputs, label)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item() * data.shape[0]
        predicted = outputs.argmax(dim=1)
        correct += torch.sum(predicted == label).item()
    
    epoch_loss = running_loss / total
    epoch_accuracy = 100 * correct / total
    print(f"Epoch[{epoch + 1}] loss: {epoch_loss:.4f}, train acc: {epoch_accuracy:.4f}")
    
    return epoch_loss

# 검증 함수
def validate(_model, device, val_loader, criterion):
    _model.eval()
    running_loss = 0.0
    correct = 0
    total = len(val_loader.dataset)
    
    with torch.no_grad():
        for data, label in val_loader:
            data, label = data.to(device), label.to(device)
            outputs = _model(data)
            if outputs.dim() == 3:
                outputs = outputs.mean(dim=0)
            loss = criterion(outputs, label)
            
            running_loss += loss.item() * data.shape[0]
            predicted = outputs.argmax(dim=1)
            correct += torch.sum(predicted == label).item()
    
    val_loss = running_loss / total
    val_accuracy = 100 * correct / total
    print(f"Validation loss: {val_loss:.4f}, val acc: {val_accuracy:.4f}")
    
    return val_loss

# 학습 루프
def train_model(_model, device, train_loader, val_loader, optimizer, criterion, num_epochs):
    # early_stopping = EarlyStopping(patience=5, min_delta = 0.001, verbose=True)
    
    for epoch in range(num_epochs):
        train(_model, device, train_loader, optimizer, criterion, epoch)
        val_loss = validate(_model, device, val_loader, criterion)
        
        # early_stopping(val_loss, _model)
        # if early_stopping.early_stop:
        #     print("Early stopping triggered!")
        #     return

    
def test(_model, device, train_loader, test_loader, criterion):
    _model.eval()
    running_loss = 0.0
    correct = 0
    total = len(train_loader.dataset)

    with torch.no_grad():  # 그래디언트 계산 비활성화
        for data, label in test_loader:
            data, label = data.to(device), label.to(device)
            
            outputs = _model(data) 
            if outputs.dim() == 3:
                outputs = outputs.mean(dim=0)
            loss = criterion(outputs, label)
            running_loss += loss.item() * data.shape[0]

            predicted = outputs.argmax(dim=1)
            correct += torch.sum(predicted == label)

    avg_loss = running_loss / total
    accuracy = 100 * correct / total
    print(f'Test Loss: {avg_loss:.4f}, Test Accuracy: {accuracy:.2f}%')


def plot_result(model, test_loader):
    model.eval()
    
    with torch.no_grad():
        data, label = next(iter(test_loader))
        data = data.to(device)
        output = model(data)
        predicted = output.argmax(dim=1)
        
    data = data.to("cpu")
    
    plt.figure(figsize=(8, 4))
    for idx in range(6):
        plt.subplot(2,3, idx+1, xticks=[], yticks=[])
        image = data[idx].permute(1, 2, 0).numpy().squeeze()
        plt.imshow(image, cmap='gray')
        
        pred_class = test_loader.dataset.classes[predicted[idx]]
        true_class = test_loader.dataset.classes[label[idx]]
        
        plt.title(f"{pred_class} ({true_class})", color="g" if pred_class == true_class else "r")
        plt.axis('off')  # 축 제거 (선택 사항)
    plt.tight_layout()
    plt.show()
    

def count_parameters(model):
    num = sum([p.numel() for p in model.parameters() if p.requires_grad])
    return num