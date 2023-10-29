import math

import torch
import torch.nn as nn
import lightning.pytorch as pl
from torch.optim import Adam


class AmazingEncoder(pl.LightningModule):
    """
    The AmazingEncoder class is a PyTorch module, inheriting from LightningModule, for encoding data.

    Attributes
    ----------
    input_shape : tuple
        The shape of the input tensor.
    embedding_shape : tuple
        The shape of the embedded output tensor.
    linear_expander : torch.nn.Module
        Expands the last dimension of the input tensor.
    linear_encoder : torch.nn.Module
        Encodes the second dimension of the input tensor to a scalar.
    encoder : torch.nn.Module
        The main encoder module which uses a TransformerEncoder layer.
    """

    def __init__(self, input_shape, embedding_shape, num_layers=3, num_heads=8, dropout=0.1):
        """
        Construct a new AmazingEncoder object.

        Parameters
        ----------
        input_shape : tuple
            The shape of the input tensor.
        embedding_shape : tuple
            The shape of the embedded output tensor.
        num_layers : int, optional
            Number of layers in the transformer encoder. Defaults to 3.
        num_heads : int, optional
            Number of heads in the transformer encoder. Defaults to 8.
        """

        super(AmazingEncoder, self).__init__()

        self.save_hyperparameters()

        self.hparams.input_shape = input_shape
        self.hparams.embedding_shape = embedding_shape

        self.linear_expander = nn.Linear(input_shape[2], embedding_shape[1])

        self.linear_encoder = nn.Linear(input_shape[1], 1)

        encoder_layer = nn.TransformerEncoderLayer(d_model=embedding_shape[1],
                                                   nhead=num_heads, dim_feedforward=input_shape[1],
                                                   batch_first=True)

        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor):
        """
        Defines the computation performed at every call.

        Parameters
        ----------
        x : torch.Tensor
            The input tensor to encode.

        Returns
        -------
        torch.Tensor
            The encoded tensor.
        """

        x = self.linear_expander(x)

        x = self.encoder(x)

        x = self.dropout(x)

        x = x.reshape((x.shape[0], x.shape[2], x.shape[1]))

        x = self.linear_encoder(x)

        x = x.squeeze(2)

        return x


class AmazingDecoder(pl.LightningModule):
    """
    The AmazingDecoder class is a PyTorch module, inheriting from LightningModule, for decoding data.

    Attributes
    ----------
    input_shape : tuple
        The shape of the input tensor.
    embedding_shape : tuple
        The shape of the embedded input tensor.
    decoder : torch.nn.Module
        The main decoder module which uses a TransformerDecoder layer.
    linear_decoder : torch.nn.Module
        Decodes the input tensor to match the second dimension of the output tensor.
    linear_expander : torch.nn.Module
        Expands the last dimension of the decoded tensor to match the last dimension of the output tensor.
    """

    def __init__(self, input_shape, embedding_shape, num_layers=3, num_heads=8, dropout=0.1):
        """
        Construct a new AmazingDecoder object.

        Parameters
        ----------
        input_shape : tuple
            The shape of the input tensor.
        embedding_shape : tuple
            The shape of the embedded input tensor.
        num_layers : int, optional
            Number of layers in the transformer decoder. Defaults to 3.
        num_heads : int, optional
            Number of heads in the transformer decoder. Defaults to 8.
        """

        super(AmazingDecoder, self).__init__()

        self.hparams.input_shape = input_shape
        self.hparams.embedding_shape = embedding_shape

        decoder_layer = nn.TransformerDecoderLayer(d_model=embedding_shape[1],
                                                   nhead=num_heads,
                                                   dim_feedforward=input_shape[1],
                                                   batch_first=True)

        self.decoder = nn.TransformerDecoder(decoder_layer, num_layers=num_layers)

        self.linear_decoder = nn.Linear(1, input_shape[1])

        self.linear_expander = nn.Linear(embedding_shape[1], input_shape[2])

        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor):
        """
        Defines the computation performed at every call.

        Parameters
        ----------
        x : torch.Tensor
            The input tensor to decode.

        Returns
        -------
        torch.Tensor
            The decoded tensor.
        """

        x = x.unsqueeze(2)

        x = self.linear_decoder(x)

        x = x.reshape((x.shape[0], x.shape[2], x.shape[1]))

        x = self.decoder(x, x)

        x = self.dropout(x)

        x = self.linear_expander(x)

        return x


class AmazingAutoEncoder(pl.LightningModule):
    """
    The AmazingAutoEncoder class is a PyTorch module, inheriting from LightningModule, that utilizes
    the AmazingEncoder and AmazingDecoder for an autoencoding task.

    Attributes
    ----------
    encoder : AmazingEncoder
        The encoder module.
    decoder : AmazingDecoder
        The decoder module.
    learning_rate : float
        The learning rate for the optimizer.
    """

    def __init__(self, input_shape, embedding_shape, learning_rate, num_layers=3, num_heads=8, dropout=0.1):
        """
        Construct a new AmazingAutoEncoder object.

        Parameters
        ----------
        input_shape : tuple
            The shape of the input tensor.
        embedding_shape : tuple
            The shape of the embedded tensor.
        learning_rate : float
            The learning rate for the optimizer.
        num_layers : int, optional
            Number of layers in the transformer encoder and decoder. Defaults to 3.
        num_heads : int, optional
            Number of heads in the transformer encoder and decoder. Defaults to 8.
        """

        super(AmazingAutoEncoder, self).__init__()
        self.save_hyperparameters()

        self.encoder = AmazingEncoder(input_shape, embedding_shape, num_layers, num_heads, dropout)

        self.decoder = AmazingDecoder(input_shape, embedding_shape, num_layers, num_heads, dropout)

    def forward(self, x: torch.Tensor):
        """
        Defines the computation performed at every call.

        Parameters
        ----------
        x : torch.Tensor
            The input tensor to autoencode.

        Returns
        -------
        torch.Tensor
            The autoencoded tensor.
        """

        x = self.encoder(x)

        x = self.decoder(x)

        return x

    def training_step(self, batch, batch_idx):
        """
        The training step for the model.

        Parameters
        ----------
        batch : torch.Tensor
            The batch of input data.
        batch_idx : int
            The index of the current batch.

        Returns
        -------
        torch.Tensor
            The loss of the current batch.
        """

        x = batch

        x_hat = self(x)

        loss = nn.MSELoss()(x_hat, x)

        self.log('train_loss', loss)
        return loss

    def validation_step(self, batch, batch_idx):
        """
        The validation step for the model.

        Parameters
        ----------
        batch : torch.Tensor
            The batch of input data.
        batch_idx : int
            The index of the current batch.

        Returns
        -------
        torch.Tensor
            The loss of the current batch.
        """

        x = batch

        x_hat = self(x)

        loss = nn.MSELoss()(x_hat, x)

        self.log('val_loss', loss)
        return loss

    def test_step(self, batch, batch_idx):
        """
        The test step for the model.

        Parameters
        ----------
        batch : torch.Tensor
            The batch of input data.
        batch_idx : int
            The index of the current batch.

        Returns
        -------
        torch.Tensor
            The loss of the current batch.
        """

        x = batch

        x_hat = self(x)

        loss = nn.MSELoss()(x_hat, x)

        self.log('test_loss', loss)
        return loss

    def configure_optimizers(self):
        """
        Configures the optimizer for the model.

        Returns
        -------
        Adam
            The Adam optimizer with the configured learning rate.
        """

        return Adam(self.parameters(), lr=self.hparams.learning_rate)
