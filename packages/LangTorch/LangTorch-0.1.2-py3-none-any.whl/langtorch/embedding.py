import torch
from typing import Optional, Union, List
from .api.call import get_embedding

class EmbeddingModule(torch.nn.Module):
    def __init__(self, api_key=None):
        super(EmbeddingModule, self).__init__()
        self.api_key = api_key

    def forward(self, x: Union[str, 'TextTensor']) -> torch.Tensor:
        # Collect all the texts from the TextTensor into a list
        # if not isinstance(x, TextTensor): x = TextTensor(x)
        shape = x.shape
        texts = [str(m) for m in x.content.flat if str(m)]
        with open("embed_temp.txt",'w') as f:
          f = ''
        with open("embed_temp_log.txt",'w') as f:
          f = ''
        # Get the embeddings for these texts
        embeddings = get_embedding(texts, "embed_temp.txt", as_np = True, api_key=self.api_key)

        # Convert the embeddings into a PyTorch tensor
        embedding_tensor = torch.from_numpy(np.array(embeddings))

        # # Reshape the tensor to match the shape of the input TextTensor
        # embedding_tensor = embedding_tensor.view(*x.content.shape, embedding_tensor.shape[-1])
        x.embedding = embedding_tensor
        return x
