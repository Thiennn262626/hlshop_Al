from tqdm import tqdm
import torch
from torch.autograd import Variable


class Model:
    def __init__(self, model):
        self.model = model
        self.item_factors = model.item_factors
        self.user_factors = model.user_factors

    def fit(self, train_loader, num_epochs, loss_fn, optimizer, cuda=False):
        if cuda:
            self.model = self.model.cuda()

        for it in tqdm(range(num_epochs)):
            self.model.train()
            losses = []
            for x, y in train_loader:
                if cuda:
                    x, y = x.cuda(), y.cuda()
                else:
                    x, y = Variable(x), Variable(y)

                optimizer.zero_grad()
                outputs = self.model(x)
                loss = loss_fn(outputs.squeeze(), y.type(torch.float32))
                losses.append(loss.item())
                loss.backward()
                optimizer.step()

            print("iter #{}".format(it), "Loss:", sum(losses) / len(losses))

    def predict(self, X):
        return self.model(X)

    def score(self, X, y):
        # Tính toán score của mô hình, ví dụ: accuracy, R^2 score, ...
        pass

    def save(self, path):
        # Lưu trữ mô hình vào đường dẫn được chỉ định
        torch.save(self.model.state_dict(), path)

    def load(self, path):
        # Tải mô hình từ đường dẫn được chỉ định
        self.model.load_state_dict(torch.load(path))

    def get_params(self):
        return self.model.parameters()

    def set_params(self, **params):
        for param_name, value in params.items():
            setattr(self.model, param_name, value)


