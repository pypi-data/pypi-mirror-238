import torch
from .tensor import TextTensor


class TextToText(torch.nn.Module):
    """
    Wrapper that converts a TextTensor input to a TextTensor output using a specified model or function.

    Parameters:
    - model (callable): The model or function to be wrapped.
    - reshape (bool, optional): If True, reshapes the output TextTensor to the shape of the input. Default is True.
    - key (str, optional): Key to set for the output TextTensor. Default is None.
    - **model_kwargs: Keyword arguments for the wrapped model or function.
    """

    def __init__(self, model, reshape=True, key=None, **model_kwargs):
        super(TextToText, self).__init__()
        self.model = model
        self.reshape = reshape
        self.key = key
        self.model_kwargs = model_kwargs

    def forward(self, input_texttensor: TextTensor, **gen_kwargs) -> TextTensor:
        """
        Processes the given TextTensor input and returns a TextTensor output.

        Parameters:
        - input_texttensor (TextTensor): Input data in TextTensor format.
        - **gen_kwargs: Additional keyword arguments for the wrapped model or function.

        Returns:
        - TextTensor: Processed output in TextTensor format.
        """
        assert isinstance(input_texttensor, TextTensor)

        texts = [str(entry) for entry in input_texttensor.flat]
        decoded_texts = self.model(texts, **self.model_kwargs, **gen_kwargs)
        output = TextTensor([str(text) for text in decoded_texts]).reshape(
            input_texttensor.shape if self.reshape else (-1,))

        return output if self.key is None else output.set_key(self.key)


class TextToTensor(torch.nn.Module):
    """
    Wrapper that converts a TextTensor input to a torch.Tensor output using a specified model or function.

    Parameters:
    - model (callable): The model or function to be wrapped.
    - reshape (bool, optional): If True, reshapes the output torch.Tensor to the shape of the input. Default is True.
    - key (str, optional): Key to set for the output torch.Tensor. Default is None.
    - **model_kwargs: Keyword arguments for the wrapped model or function.
    """

    def __init__(self, model, reshape=True, key=None, **model_kwargs):
        super(TextToTensor, self).__init__()
        self.model = model
        self.reshape = reshape
        self.key = key
        self.model_kwargs = model_kwargs

    def forward(self, input_texttensor: TextTensor, **gen_kwargs) -> torch.Tensor:
        """
        Processes the given TextTensor input and returns a torch.Tensor output.

        Parameters:
        - input_texttensor (TextTensor): Input data in TextTensor format.
        - **gen_kwargs: Additional keyword arguments for the wrapped model or function.

        Returns:
        - torch.Tensor: Processed output in torch.Tensor format.
        """
        assert isinstance(input_texttensor, TextTensor)

        texts = [str(entry) for entry in input_texttensor.flat]
        outputs = self.model(texts, **self.model_kwargs, **gen_kwargs)
        tensor_outputs = torch.tensor(outputs).reshape(input_texttensor.shape if self.reshape else (-1,))

        return tensor_outputs
