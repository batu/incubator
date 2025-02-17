import torch
import numpy as np

from rogue_net.head_creator import CategoricalActionHead
from rogue_net.ragged_tensor import RaggedTensor
from ragged_buffer import RaggedBufferI64
from entity_gym.environment import CategoricalActionMaskBatch


def test_empty_actors() -> None:
    head = CategoricalActionHead(d_model=4, n_choice=2)
    x = RaggedTensor(
        data=torch.zeros(12, 4),
        batch_index=torch.tensor([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 3, 3]),
        lengths=torch.tensor([4, 4, 2, 2]),
    )

    action, lengths, logprob, entropy, logits = head.forward(
        x,
        index_offsets=RaggedBufferI64.from_array(
            np.array([[[0]], [[4]], [[6]], [[8]]])
        ),
        mask=CategoricalActionMaskBatch(
            actors=RaggedBufferI64.from_flattened(
                np.zeros((0, 1), dtype=np.int64),
                lengths=np.array([0, 0, 0, 0], dtype=np.int64),
            ),
            masks=None,
        ),
        prev_actions=None,
    )
    assert action.shape == (0, 1)
    assert np.array_equal(lengths, np.array([0, 0, 0, 0]))
    assert logprob.shape == (0, 1)
    assert entropy.shape == (0, 1)
    assert logits.shape == (0, 2)
