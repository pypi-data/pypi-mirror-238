# This code is a Qiskit project.

# (C) Copyright IBM 2022.

# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""File containing the EntanglementForgingGroundStateSolver class and associated functions."""

from __future__ import annotations

import copy
from typing import Sequence

import numpy as np

from qiskit.quantum_info import Pauli
from qiskit.quantum_info import SparsePauliOp
from qiskit_nature.second_q.problems import ElectronicStructureProblem
from qiskit_nature.second_q.mappers import JordanWignerMapper
from qiskit_nature.second_q.operators import (
    FermionicOp,
    PolynomialTensor,
)
from qiskit_nature.second_q.operators.tensor_ordering import (
    to_chemist_ordering,
    to_physicist_ordering,
)

from .entanglement_forging_ansatz import EntanglementForgingAnsatz
from .entanglement_forging_operator import EntanglementForgingOperator


def get_cholesky_op(
    l_op: np.ndarray, g: int, converter: JordanWignerMapper, opname: str
) -> SparsePauliOp:
    """
    Convert a two-body term into a cholesky operator.

    Args:
        l_op: Two body integrals
        g: Integral index
        converter: Qubit converter to be used
        opname: Prefix for output cholesky operator name

    Returns:
        The converted Cholesky operator
    """
    pt = PolynomialTensor({"+-": l_op[:, :, g]})
    fer_op = FermionicOp.from_polynomial_tensor(pt)
    cholesky_op = converter.map(fer_op)
    cholesky_op._name = opname + "_chol" + str(g)

    return cholesky_op


def cholesky_decomposition(
    problem: ElectronicStructureProblem,
    mo_coeff: np.ndarray | None = None,
    orbitals_to_reduce: Sequence[int] | None = None,
) -> tuple[list[SparsePauliOp], float]:
    """
    Construct the decomposed Hamiltonian from an input ``ElectronicStructureProblem``.

    Args:
        problem: An ``ElectronicStructureProblem`` from which the decomposed Hamiltonian
            will be calculated
        mo_coeff: The coefficients for mapping to the MO basis. If ``None``, the input
            integrals will be assumed to be in the MO basis
        orbitals_to_reduce: A list of orbital indices to remove from the problem
            before decomposition

    Returns:
        Tuple containing the cholesky operator and the energy shift resulting from decomposition

    Raises:
        ValueError: The input ElectronicStructureProblem contains no particle number information.
    """
    hcore = np.array(problem.hamiltonian.electronic_integrals.one_body.alpha["+-"])
    eri = to_chemist_ordering(
        problem.hamiltonian.electronic_integrals.two_body.alpha["++--"]
    )
    num_alpha = problem.num_alpha
    if num_alpha is None:
        raise ValueError(
            "The input ElectronicStructureProblem contains no particle number information."
        )

    # If no mo coeffs are passed, we assume the integrals are with respect to MO basis
    if mo_coeff is None:
        mo_coeff = np.eye(eri.shape[0], eri.shape[0])

    # Store the reduced orbitals as virtual and occupied lists
    if orbitals_to_reduce is None:
        orbitals_to_reduce = []
    orbitals_to_reduce_dict: dict[str, np.ndarray] = _get_orbitals_to_reduce(
        orbitals_to_reduce, num_alpha
    )

    # Hold fields used to calculate the final energy shift
    # Freeze shift will be calculated during decomposition
    nuclear_repulsion_energy = problem.nuclear_repulsion_energy
    if nuclear_repulsion_energy is None:
        nuclear_repulsion_energy = 0.0

    h_1_op, h_chol_ops, freeze_shift, _, _ = _get_fermionic_ops_with_cholesky(
        mo_coeff,
        hcore,
        eri,
        opname="H",
        halve_transformed_h2=True,
        occupied_orbitals_to_reduce=orbitals_to_reduce_dict["occupied"],
        virtual_orbitals_to_reduce=orbitals_to_reduce_dict["virtual"],
    )

    op_list = [h_1_op] + h_chol_ops
    operator = op_list

    return operator, nuclear_repulsion_energy + freeze_shift


def convert_cholesky_operator(
    operator: list[SparsePauliOp],
    ansatz: EntanglementForgingAnsatz,
) -> EntanglementForgingOperator:
    """
    Convert the Cholesky operator (List[SparsePauliOp]) into the entanglement forging format.

    Args:
        operator: A `List[SparsePauliOp]` containing the single-body Hamiltonian followed
            by the Cholesky operators
            shape: [single-body hamiltonian, cholesky_0, ..., cholesky_{N-1}]
        ansatz: The ansatz for which to compute expectation values of operator. The
            `EntanglementForgingAnsatz` also contains the bitstrings for each subsystem

    Returns:
        An `EntanglementForgingOperator` object describing the
        decomposed operator
    """
    calculate_hybrid_cross_terms = len(set(ansatz.bitstrings_u)) < len(
        ansatz.bitstrings_u
    ) or len(set(ansatz.bitstrings_v)) < len(ansatz.bitstrings_v)

    op1 = operator[0]
    cholesky_ops = operator[1:]

    # The block below calculate the Pauli-pair prefactors w_ij and returns
    # them as a dictionary
    tensor_paulis = set()
    superpos_paulis = set()
    paulis_each_op = [
        {label: weight for label, weight in op.to_list() if np.abs(weight) > 0}
        for op in [op1] + list(cholesky_ops)
    ]

    # Gather the elements in the Pauli basis for tensor and superpos terms
    paulis_each_op = [paulis_each_op[0]] + [p for p in paulis_each_op[1:] if p]
    for op_idx, paulis_this_op in enumerate(paulis_each_op):
        pnames = list(paulis_this_op.keys())
        tensor_paulis.update(pnames)

        # If hybrid terms are needed, the superposition basis includes
        # terms from the single body Hamiltonian.
        if calculate_hybrid_cross_terms or op_idx > 0:
            superpos_paulis.update(pnames)

    # ensure Identity string is represented since we will need it
    identity_string = "I" * len(pnames[0])
    tensor_paulis.add(identity_string)
    superpos_paulis.add(identity_string)

    # Sort the Pauli bases
    tensor_pauli_names = list(sorted(tensor_paulis))
    superpos_pauli_names = list(sorted(superpos_paulis))

    # Map the tensor Pauli terms to their place in the tensor index
    pauli_ordering_for_tensor_states = {
        pname: idx for idx, pname in enumerate(tensor_pauli_names)
    }
    # Map the superpos Pauli basis terms to their place in the superpos index
    pauli_ordering_for_superpos_states = {
        pname: idx for idx, pname in enumerate(superpos_pauli_names)
    }

    # Create arrays for the tensor and superpos weights, respectively
    w_ij = np.zeros((len(tensor_pauli_names), len(tensor_pauli_names)))
    w_ab = np.zeros((len(superpos_pauli_names), len(superpos_pauli_names)))

    # Processes the non-Cholesky operator
    identity_idx = pauli_ordering_for_tensor_states[identity_string]
    identity_idx_superpos = pauli_ordering_for_tensor_states[identity_string]
    for pname_i, w_i in paulis_each_op[0].items():
        i = pauli_ordering_for_tensor_states[pname_i]
        w_ij[i, identity_idx] += np.real(w_i)  # H_spin-up
        w_ij[identity_idx, i] += np.real(w_i)  # H_spin-down

        # In the special case where bn=bm, we need terms from the
        # single body system represented in the cross terms
        if calculate_hybrid_cross_terms:
            w_ab[i, identity_idx_superpos] += np.real(w_i)
            w_ab[identity_idx_superpos, i] += np.real(w_i)

    # Processes the Cholesky operators (indexed by gamma)
    for paulis_this_gamma in paulis_each_op[1:]:
        for pname_1, w_1 in paulis_this_gamma.items():
            i = pauli_ordering_for_tensor_states[pname_1]
            superpos_ordering1 = pauli_ordering_for_superpos_states[pname_1]
            for pname_2, w_2 in paulis_this_gamma.items():
                j = pauli_ordering_for_tensor_states[pname_2]
                superpos_ordering2 = pauli_ordering_for_superpos_states[pname_2]
                w_ij[i, j] += np.real(w_1 * w_2)
                w_ab[superpos_ordering1, superpos_ordering2] += np.real(w_1 * w_2)

    # Convert from string representation to Pauli objects
    tensor_pauli_list = [Pauli(name) for name in tensor_pauli_names]
    superpos_pauli_list = [Pauli(name) for name in superpos_pauli_names]

    forged_operator = EntanglementForgingOperator(
        tensor_paulis=tensor_pauli_list,
        superposition_paulis=superpos_pauli_list,
        w_ij=w_ij,
        w_ab=w_ab,
    )

    return forged_operator


def _get_fermionic_ops_with_cholesky(
    mo_coeff: np.ndarray,
    h1: np.ndarray,
    h2: np.ndarray,
    opname: str,
    halve_transformed_h2: bool = False,
    occupied_orbitals_to_reduce: np.ndarray | None = None,
    virtual_orbitals_to_reduce: np.ndarray | None = None,
    epsilon_cholesky: float = 1e-10,
) -> tuple[SparsePauliOp, list[SparsePauliOp], float, np.ndarray, np.ndarray,]:
    r"""
    Decompose the Hamiltonian operators into a form appropriate for entanglement forging.

    Args:
        mo_coeff: 2D array representing coefficients for converting from AO to MO basis
        h1: 2D array representing operator
            coefficients of one-body integrals in the AO basis
        h2: 4D array representing operator coefficients
            of two-body integrals in the AO basis
        halve_transformed_h2: Should be set to True for Hamiltonian
            operator to agree with Qiskit conventions
        occupied_orbitals_to_reduce: A list of occupied orbitals that will be removed
        virtual_orbitals_to_reduce: A list of virtual orbitals that will be removed
        epsilon_cholesky: The threshold for the decomposition (typically a number close to 0)

    Returns:
        A tuple containing the single and two-body integrals, the energy shift, and the
        one and two body integrals in the MO basis
    """
    if virtual_orbitals_to_reduce is None:
        virtual_orbitals_to_reduce = np.array([])
    if occupied_orbitals_to_reduce is None:
        occupied_orbitals_to_reduce = np.array([])

    coeff_mo = copy.copy(mo_coeff)

    h1 = np.einsum("pi,pr->ir", coeff_mo, h1)
    h1 = np.einsum("rj,ir->ij", coeff_mo, h1)  # h_{pq} in MO basis

    # Do the cholesky decomposition
    if h2 is not None:
        _, l_op = _get_modified_cholesky(h2, epsilon_cholesky)

        # Obtain L_{pr,g} in the MO basis
        l_op = np.einsum("prg,pi,rj->ijg", l_op, coeff_mo, coeff_mo)
    else:
        size = len(h1)
        l_op = np.zeros(shape=(size, size, 0))

    if len(occupied_orbitals_to_reduce) > 0:
        orbitals_not_to_reduce_array = np.array(
            sorted(set(range(len(h1))) - set(occupied_orbitals_to_reduce))
        )

        h1_frozenpart = h1[
            np.ix_(occupied_orbitals_to_reduce, occupied_orbitals_to_reduce)
        ]
        h1_activepart = h1[
            np.ix_(orbitals_not_to_reduce_array, orbitals_not_to_reduce_array)
        ]
        l_frozenpart = l_op[
            np.ix_(occupied_orbitals_to_reduce, occupied_orbitals_to_reduce)
        ]
        l_activepart = l_op[
            np.ix_(orbitals_not_to_reduce_array, orbitals_not_to_reduce_array)
        ]

        freeze_shift = (
            2 * np.einsum("pp", h1_frozenpart)
            + 2 * np.einsum("ppg,qqg", l_frozenpart, l_frozenpart)
            - np.einsum("pqg,qpg", l_frozenpart, l_frozenpart)
        )

        h1 = (
            h1_activepart
            + 2 * np.einsum("ppg,qsg->qs", l_frozenpart, l_activepart)
            - np.einsum(
                "psg,qpg->qs",
                l_op[np.ix_(occupied_orbitals_to_reduce, orbitals_not_to_reduce_array)],
                l_op[np.ix_(orbitals_not_to_reduce_array, occupied_orbitals_to_reduce)],
            )
        )
        l_op = l_activepart

    else:
        freeze_shift = 0

    if virtual_orbitals_to_reduce.shape[0]:
        virtual_orbitals_to_reduce -= len(occupied_orbitals_to_reduce)  # type: ignore
        orbitals_not_to_reduce = list(
            sorted(set(range(len(h1))) - set(virtual_orbitals_to_reduce))  # type: ignore
        )
        h1 = h1[np.ix_(orbitals_not_to_reduce, orbitals_not_to_reduce)]
        l_op = l_op[np.ix_(orbitals_not_to_reduce, orbitals_not_to_reduce)]
    else:
        pass

    h2 = np.einsum("prg,qsg->prqs", l_op, l_op)

    if halve_transformed_h2:
        h2 /= 2  # type: ignore

    converter = JordanWignerMapper()
    pt = PolynomialTensor({"+-": h1, "++--": to_physicist_ordering(h2)})
    fer_op = FermionicOp.from_polynomial_tensor(pt)
    qubit_op = converter.map(fer_op)
    qubit_op._name = opname + "_onebodyop"

    cholesky_ops = [
        get_cholesky_op(l_op, g, converter, opname) for g in range(l_op.shape[2])
    ]

    return qubit_op, cholesky_ops, freeze_shift, h1, h2


def _get_modified_cholesky(two_body_overlap_integrals: np.ndarray, eps: float):
    """Perform modified Cholesky decomposition on the two-body integrals given an epsilon value."""
    n_basis_states = two_body_overlap_integrals.shape[0]  # number of basis states
    # Max (chmax) and current (n_gammas) number of Cholesky vectors
    ch_max, n_gammas = 10 * n_basis_states, 0

    w_op = two_body_overlap_integrals.reshape(n_basis_states**2, n_basis_states**2)
    l_op = np.zeros((n_basis_states**2, ch_max))
    d_max = np.diagonal(w_op).copy()
    nu_max = np.argmax(d_max)
    v_max = d_max[nu_max]

    while v_max > eps:
        l_op[:, n_gammas] = w_op[:, nu_max]
        if n_gammas > 0:
            l_op[:, n_gammas] -= np.dot(l_op[:, 0:n_gammas], l_op.T[0:n_gammas, nu_max])
        l_op[:, n_gammas] /= np.sqrt(v_max)
        d_max[: n_basis_states**2] -= l_op[: n_basis_states**2, n_gammas] ** 2
        n_gammas += 1
        nu_max = np.argmax(d_max)
        v_max = d_max[nu_max]

    l_op = l_op[:, :n_gammas].reshape((n_basis_states, n_basis_states, n_gammas))

    return n_gammas, l_op


def _get_orbitals_to_reduce(
    orbitals_to_reduce: Sequence[int],
    num_alpha: int,
) -> dict[str, np.ndarray]:
    orb_to_reduce_dict = {
        "occupied": np.asarray(orbitals_to_reduce),
        "virtual": np.asarray(orbitals_to_reduce),
        "all": np.asarray(orbitals_to_reduce),
    }

    # Populate the occupied list within the dict
    orb_to_reduce_dict["occupied"] = orb_to_reduce_dict["occupied"][
        orb_to_reduce_dict["occupied"] < num_alpha
    ]

    # Populate the virtual list within the dict
    orb_to_reduce_dict["virtual"] = orb_to_reduce_dict["virtual"][
        orb_to_reduce_dict["virtual"] >= num_alpha
    ]

    return orb_to_reduce_dict
