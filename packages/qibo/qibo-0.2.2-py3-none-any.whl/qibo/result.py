import collections
import warnings

import numpy as np

from qibo import __version__, backends, gates
from qibo.measurements import apply_bitflips, frequencies_to_binary


def load_result(filename):
    """Loads the results of a circuit execution saved to disk.

    Args:
        filename (str): Path to the file containing the results.

    Returns:
        A :class:`qibo.result.QuantumState`, :class:`qibo.result.MeasurementOutcomes` or :class:`qibo.result.CircuitResult` object, depending on the input file.
    """
    payload = np.load(filename, allow_pickle=True).item()
    return globals()[payload.pop("dtype")].from_dict(payload)


class QuantumState:
    """Data structure to represent the final state after circuit execution."""

    def __init__(self, state, backend):
        self.backend = backend
        self.density_matrix = len(state.shape) == 2
        self.nqubits = int(np.log2(state.shape[0]))
        self._state = state

    def symbolic(self, decimals=5, cutoff=1e-10, max_terms=20):
        """Dirac notation representation of the state in the computational basis.

        Args:
            decimals (int): Number of decimals for the amplitudes.
                Default is 5.
            cutoff (float): Amplitudes with absolute value smaller than the
                cutoff are ignored from the representation.
                Default is 1e-10.
            max_terms (int): Maximum number of terms to print. If the state
                contains more terms they will be ignored.
                Default is 20.

        Returns:
            A string representing the state in the computational basis.
        """
        if self.density_matrix:
            terms = self.backend.calculate_symbolic_density_matrix(
                self._state, self.nqubits, decimals, cutoff, max_terms
            )
        else:
            terms = self.backend.calculate_symbolic(
                self._state, self.nqubits, decimals, cutoff, max_terms
            )
        return " + ".join(terms)

    def state(self, numpy=False):
        """State's tensor representation as a backend tensor.

        Args:
            numpy (bool): If ``True`` the returned tensor will be a numpy array,
                otherwise it will follow the backend tensor type.
                Default is ``False``.

        Returns:
            The state in the computational basis.
        """
        if numpy:
            return self.backend.to_numpy(self._state)
        else:
            return self._state

    def probabilities(self, qubits=None):
        """Calculates measurement probabilities by tracing out qubits.
        When noisy model is applied to a circuit and `circuit.density_matrix=False`,
        this method returns the average probability resulting from
        repeated execution. This probability distribution approximates the
        exact probability distribution obtained when `circuit.density_matrix=True`.

        Args:
            qubits (list, set): Set of qubits that are measured.
        """

        if qubits is None:
            qubits = tuple(range(self.nqubits))

        if self.density_matrix:
            return self.backend.calculate_probabilities_density_matrix(
                self._state, qubits, self.nqubits
            )
        else:
            return self.backend.calculate_probabilities(
                self._state, qubits, self.nqubits
            )

    def __str__(self):
        return self.symbolic()

    def to_dict(self):
        """Returns a dictonary containinig all the information needed to rebuild the ``QuantumState``"""
        return {
            "state": self.state(numpy=True),
            "dtype": self.__class__.__name__,
            "qibo": __version__,
        }

    def dump(self, filename):
        """Writes to file the ``QuantumState`` for future reloading.

        Args:
            filename (str): Path to the file to write to.
        """
        with open(filename, "wb") as f:
            np.save(f, self.to_dict())

    @classmethod
    def from_dict(cls, payload):
        """Builds a ``QuantumState`` object starting from a dictionary.

        Args:
            payload (dict): Dictionary containing all the information to load the ``QuantumState`` object.

        Returns:
            A :class:`qibo.result.QuantumState` object.
        """
        backend = backends.construct_backend("numpy")
        return cls(payload.get("state"), backend)

    @classmethod
    def load(cls, filename):
        """Builds the ``QuantumState`` object stored in a file.

        Args:
            filename (str): Path to the file containing the ``QuantumState``.

        Returns:
            A :class:`qibo.result.QuantumState` object.
        """
        payload = np.load(filename, allow_pickle=True).item()
        return cls.from_dict(payload)


class MeasurementOutcomes:
    """Object to store the outcomes of measurements after circuit execution."""

    def __init__(
        self, measurements, backend, probabilities=None, samples=None, nshots=1000
    ):
        self.backend = backend
        self.measurements = measurements
        self.nshots = nshots

        self._measurement_gate = None
        self._probs = probabilities
        self._samples = samples
        self._frequencies = None
        self._repeated_execution_frequencies = None

    def frequencies(self, binary=True, registers=False):
        """Returns the frequencies of measured samples.

        Args:
            binary (bool): Return frequency keys in binary or decimal form.
            registers (bool): Group frequencies according to registers.

        Returns:
            A `collections.Counter` where the keys are the observed values
            and the values the corresponding frequencies, that is the number
            of times each measured value/bitstring appears.

            If `binary` is `True`
                the keys of the `Counter` are in binary form, as strings of
                0s and 1s.
            If `binary` is `False`
                the keys of the `Counter` are integers.
            If `registers` is `True`
                a `dict` of `Counter` s is returned where keys are the name of
                each register.
            If `registers` is `False`
                a single `Counter` is returned which contains samples from all
                the measured qubits, independently of their registers.
        """
        if self._repeated_execution_frequencies is not None:
            return self._repeated_execution_frequencies

        qubits = self.measurement_gate.qubits
        if self._frequencies is None:
            if self.measurement_gate.has_bitflip_noise() and not self.has_samples():
                self._samples = self.samples()
            if not self.has_samples():
                # generate new frequencies
                self._frequencies = self.backend.sample_frequencies(
                    self._probs, self.nshots
                )
                # register frequencies to individual gate ``MeasurementResult``
                qubit_map = {q: i for i, q in enumerate(qubits)}
                reg_frequencies = {}
                binary_frequencies = frequencies_to_binary(
                    self._frequencies, len(qubits)
                )
                for gate in self.measurements:
                    rfreqs = collections.Counter()
                    for bitstring, freq in binary_frequencies.items():
                        idx = 0
                        rqubits = gate.target_qubits
                        for i, q in enumerate(rqubits):
                            if int(bitstring[qubit_map.get(q)]):
                                idx += 2 ** (len(rqubits) - i - 1)
                        rfreqs[idx] += freq
                    gate.result.register_frequencies(rfreqs, self.backend)
            else:
                self._frequencies = self.backend.calculate_frequencies(
                    self.samples(binary=False)
                )

        if registers:
            return {
                gate.register_name: gate.result.frequencies(binary)
                for gate in self.measurements
            }

        if binary:
            return frequencies_to_binary(self._frequencies, len(qubits))

        return self._frequencies

    def has_samples(self):
        return self.measurements[0].result.has_samples() or self._samples is not None

    def samples(self, binary=True, registers=False):
        """Returns raw measurement samples.

        Args:
            binary (bool): Return samples in binary or decimal form.
            registers (bool): Group samples according to registers.

        Returns:
            If `binary` is `True`
                samples are returned in binary form as a tensor
                of shape `(nshots, n_measured_qubits)`.
            If `binary` is `False`
                samples are returned in decimal form as a tensor
                of shape `(nshots,)`.
            If `registers` is `True`
                samples are returned in a `dict` where the keys are the register
                names and the values are the samples tensors for each register.
            If `registers` is `False`
                a single tensor is returned which contains samples from all the
                measured qubits, independently of their registers.
        """
        qubits = self.measurement_gate.target_qubits
        if self._samples is None:
            if self.measurements[0].result.has_samples():
                self._samples = np.concatenate(
                    [gate.result.samples() for gate in self.measurements], axis=1
                )
            else:
                if self._frequencies is not None:
                    # generate samples that respect the existing frequencies
                    frequencies = self.frequencies(binary=False)
                    samples = np.concatenate(
                        [np.repeat(x, f) for x, f in frequencies.items()]
                    )
                    np.random.shuffle(samples)
                else:
                    # generate new samples
                    samples = self.backend.sample_shots(self._probs, self.nshots)
                samples = self.backend.samples_to_binary(samples, len(qubits))
                if self.measurement_gate.has_bitflip_noise():
                    p0, p1 = self.measurement_gate.bitflip_map
                    bitflip_probabilities = [
                        [p0.get(q) for q in qubits],
                        [p1.get(q) for q in qubits],
                    ]
                    samples = self.backend.apply_bitflips(
                        samples, bitflip_probabilities
                    )
                # register samples to individual gate ``MeasurementResult``
                qubit_map = {
                    q: i for i, q in enumerate(self.measurement_gate.target_qubits)
                }
                self._samples = np.array(samples, dtype="int32")
                for gate in self.measurements:
                    rqubits = tuple(qubit_map.get(q) for q in gate.target_qubits)
                    gate.result.register_samples(
                        self._samples[:, rqubits], self.backend
                    )

        if registers:
            return {
                gate.register_name: gate.result.samples(binary)
                for gate in self.measurements
            }

        if binary:
            return self._samples
        else:
            return self.backend.samples_to_decimal(self._samples, len(qubits))

    @property
    def measurement_gate(self):
        """Single measurement gate containing all measured qubits.

        Useful for sampling all measured qubits at once when simulating.
        """
        if self._measurement_gate is None:
            for gate in self.measurements:
                if self._measurement_gate is None:
                    self._measurement_gate = gates.M(
                        *gate.init_args, **gate.init_kwargs
                    )
                else:
                    self._measurement_gate.add(gate)

        return self._measurement_gate

    def apply_bitflips(self, p0, p1=None):
        return apply_bitflips(self, p0, p1)

    def expectation_from_samples(self, observable):
        """Computes the real expectation value of a diagonal observable from frequencies.

        Args:
            observable (Hamiltonian/SymbolicHamiltonian): diagonal observable in the
            computational basis.

        Returns:
            Real number corresponding to the expectation value.
        """
        freq = self.frequencies(binary=True)
        qubit_map = self.measurement_gate.qubits
        return observable.expectation_from_samples(freq, qubit_map)

    def to_dict(self):
        """Returns a dictonary containinig all the information needed to rebuild the ``MeasurementOutcomes``."""
        args = {
            "measurements": [m.to_json() for m in self.measurements],
            "probabilities": self._probs,
            "samples": self._samples,
            "nshots": self.nshots,
            "dtype": self.__class__.__name__,
            "qibo": __version__,
        }
        return args

    def dump(self, filename):
        """Writes to file the ``MeasurementOutcomes`` for future reloading.

        Args:
            filename (str): Path to the file to write to.
        """
        with open(filename, "wb") as f:
            np.save(f, self.to_dict())

    @classmethod
    def from_dict(cls, payload):
        """Builds a ``MeasurementOutcomes`` object starting from a dictionary.

        Args:
            payload (dict): Dictionary containing all the information to load the ``MeasurementOutcomes`` object.

        Returns:
            A :class:`qibo.result.MeasurementOutcomes` object.
        """
        from qibo.backends import construct_backend

        if payload["probabilities"] is not None and payload["samples"] is not None:
            warnings.warn(
                "Both `probabilities` and `samples` found, discarding the `probabilities` and building out of the `samples`."
            )
            payload.pop("probabilities")
        backend = construct_backend("numpy")
        measurements = [gates.M.load(m) for m in payload.get("measurements")]
        return cls(
            measurements,
            backend,
            probabilities=payload.get("probabilities"),
            samples=payload.get("samples"),
            nshots=payload.get("nshots"),
        )

    @classmethod
    def load(cls, filename):
        """Builds the ``MeasurementOutcomes`` object stored in a file.

        Args:
            filename (str): Path to the file containing the ``MeasurementOutcomes``.

        Returns:
            A :class:`qibo.result.MeasurementOutcomes` object.
        """
        payload = np.load(filename, allow_pickle=True).item()
        return cls.from_dict(payload)


class CircuitResult(QuantumState, MeasurementOutcomes):
    """Object to store both the outcomes of measurements and the final state after circuit execution."""

    def __init__(self, final_state, measurements, backend, samples=None, nshots=1000):
        QuantumState.__init__(self, final_state, backend)
        qubits = [q for m in measurements for q in m.target_qubits]
        if len(qubits) == 0:
            raise ValueError(
                "Circuit does not contain measurements. Use a `QuantumState` instead."
            )
        probs = self.probabilities(qubits) if samples is None else None
        MeasurementOutcomes.__init__(
            self,
            measurements,
            backend,
            probabilities=probs,
            samples=samples,
            nshots=nshots,
        )

    def to_dict(self):
        """Returns a dictonary containinig all the information needed to rebuild the ``CircuitResult``."""
        args = MeasurementOutcomes.to_dict(self)
        args.update(QuantumState.to_dict(self))
        args.update({"dtype": self.__class__.__name__})
        return args

    @classmethod
    def from_dict(cls, payload):
        """Builds a ``CircuitResult`` object starting from a dictionary.

        Args:
            payload (dict): Dictionary containing all the information to load the ``CircuitResult`` object.

        Returns:
            A :class:`qibo.result.CircuitResult` object.
        """
        state_load = {"state": payload.pop("state")}
        state = QuantumState.from_dict(state_load)
        measurements = MeasurementOutcomes.from_dict(payload)
        return cls(
            state.state(),
            measurements.measurements,
            state.backend,
            samples=measurements.samples(),
            nshots=measurements.nshots,
        )
