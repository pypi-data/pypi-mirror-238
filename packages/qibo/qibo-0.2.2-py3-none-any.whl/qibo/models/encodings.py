"""Module with functions that encode classical data into quantum circuits."""

import math

import numpy as np

from qibo import gates
from qibo.config import raise_error
from qibo.models.circuit import Circuit


def unary_encoder(data):
    """Creates circuit that performs the unary encoding of ``data``.

    Given a classical ``data`` array :math:`\\mathbf{x} \\in \\mathbb{R}^{d}` such that

    .. math::
        \\mathbf{x} = (x_{1}, x_{2}, \\dots, x_{d}) \\, ,

    this function generate the circuit that prepares the following quantum state
    :math:`\\ket{\\psi} \\in \\mathcal{H}`:

    .. math::
        \\ket{\\psi} = \\frac{1}{\\|\\mathbf{x}\\|_{\\textup{HS}}} \\,
            \\sum_{k=1}^{d} \\, x_{k} \\, \\ket{k} \\, ,

    with :math:`\\mathcal{H} \\cong \\mathbb{C}^{d}` being a :math:`d`-qubit Hilbert space,
    and :math:`\\|\\cdot\\|_{\\textup{HS}}` being the Hilbert-Schmidt norm.
    Here, :math:`\\ket{k}` is a unary representation of the number :math:`1` through
    :math:`d`.

    Args:
        data (ndarray, optional): :math:`1`-dimensional array of data to be loaded.

    Returns:
        :class:`qibo.models.circuit.Circuit`: circuit that loads ``data`` in unary representation.

    References:
        1. S. Johri *et al.*, *Nearest Centroid Classiﬁcation on a Trapped Ion Quantum Computer*.
        `arXiv:2012.04145v2 [quant-ph] <https://arxiv.org/abs/2012.04145>`_.
    """
    if len(data.shape) != 1:
        raise_error(
            TypeError,
            f"``data`` must be a 1-dimensional array, but it has dimensions {data.shape}.",
        )
    elif not math.log2(data.shape[0]).is_integer():
        raise_error(
            ValueError, f"len(data) must be a power of 2, but it is {len(data)}."
        )

    nqubits = len(data)
    j_max = int(nqubits / 2)

    circuit, _ = _generate_rbs_pairs(nqubits)

    # calculating phases and setting circuit parameters
    r_array = np.zeros(nqubits - 1, dtype=float)
    phases = np.zeros(nqubits - 1, dtype=float)
    for j in range(1, j_max + 1):
        r_array[j_max + j - 2] = math.sqrt(data[2 * j - 1] ** 2 + data[2 * j - 2] ** 2)
        theta = math.acos(data[2 * j - 2] / r_array[j_max + j - 2])
        if data[2 * j - 1] < 0.0:
            theta = 2 * math.pi - theta
        phases[j_max + j - 2] = theta

    for j in range(j_max - 1, 0, -1):
        r_array[j - 1] = math.sqrt(r_array[2 * j] ** 2 + r_array[2 * j - 1] ** 2)
        phases[j - 1] = math.acos(r_array[2 * j - 1] / r_array[j - 1])

    circuit.set_parameters(phases)

    return circuit


def _generate_rbs_pairs(nqubits):
    """Generating list of indexes representing the RBS connections
    and creating circuit with all RBS initialised with 0.0 phase."""
    pairs_rbs = [[(0, int(nqubits / 2))]]
    indexes = list(np.array(pairs_rbs).flatten())
    for depth in range(2, int(math.log2(nqubits)) + 1):
        pairs_rbs_per_depth = [
            [(index, index + int(nqubits / 2**depth)) for index in indexes]
        ]
        pairs_rbs += pairs_rbs_per_depth
        indexes = list(np.array(pairs_rbs_per_depth).flatten())

    circuit = Circuit(nqubits)
    circuit.add(gates.X(0))
    for row in pairs_rbs:
        for pair in row:
            circuit.add(gates.RBS(*pair, 0.0, trainable=True))

    return circuit, pairs_rbs
