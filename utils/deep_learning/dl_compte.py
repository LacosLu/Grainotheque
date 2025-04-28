# ----- IMPORTS -----
# --- Bibliothèques externes ---
import torch
import torch.nn as nn
import torch.nn.functional as F

# ----- CLASSE -----
class Compte(nn.Module):
    def __init__(self):
        super().__init__()
        self.__conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.__conv2 = nn.Conv2d(16, 8, kernel_size=3, padding=1)
        self.__fc1 = nn.Linear(8 * 8 * 8, 32)
        self.__fc2 = nn.Linear(32, 74)

    def forward(self, x):
        out = F.max_pool2d(torch.tanh(self.__conv1(x)), 2)
        out = F.max_pool2d(torch.tanh(self.__conv2(out)), 2)
        out = out.view(-1, 8 * 8 * 8)
        out = torch.tanh(self.__fc1(out))
        out = self.__fc2(out)
        return out
    
# ----- PROGRAMME -----
if __name__ == "__main__":
    print("--- TEST DE FONCTIONNEMENT ---")
    random_tensor : torch.Tensor = torch.rand((1, 3, 32, 32))

    nn_test : Compte = Compte()
    result : torch.Tensor = nn_test(random_tensor)

    print(result.shape)