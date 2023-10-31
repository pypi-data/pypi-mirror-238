from collections.abc import Callable
from typing import Literal, Optional, Union, Tuple
import jax
import jax.random as random
from jaxtyping import Array, PRNGKeyArray
import equinox as eqx
import jax.numpy as jnp
import generax.util as util


class InputConvexNN(eqx.Module):
  """
  """

  hidden_dim: int = eqx.field(static=True)
  aug_dim: int = eqx.field(static=True)
  total_dim: int = eqx.field(static=True)
  n_hidden_layers: int = eqx.field(static=True)


  def __init__(self,
               input_shape: Tuple[int],
               out_size: int,
               key: PRNGKeyArray,
               **kwargs):
    super().__init__(**kwargs)
