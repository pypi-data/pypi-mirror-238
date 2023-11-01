########################
Circuit Knitting Toolbox
########################

.. image:: https://img.shields.io/github/stars/Qiskit-Extensions/circuit-knitting-toolbox?style=social
   :alt: GitHub repository star counter badge
   :target: https://github.com/Qiskit-Extensions/circuit-knitting-toolbox

Circuit Knitting is the process of decomposing a quantum circuit into smaller circuits, executing those smaller circuits on a quantum processor(s), and then knitting their results into a reconstruction of the original circuit's outcome. Circuit knitting includes techniques such as entanglement forging, circuit cutting, and classical embedding. The Circuit Knitting Toolbox (CKT) is a collection of such tools.

Each tool in the CKT partitions a user's problem into quantum and classical components to enable efficient use of resources constrained by scaling limits, i.e. size of quantum processors and classical compute capability. It is designed to work seamlessly with the `Quantum Serverless <https://qiskit-extensions.github.io/quantum-serverless/>`_ framework, which enables users to run parallelized and hybrid (quantum + classical) workloads without worrying about allocating and managing underlying infrastructure.

The toolbox currently contains the following tools:

- Circuit Cutting
- Entanglement Forging

.. note::

   The `Quantum Serverless <https://qiskit-extensions.github.io/quantum-serverless/>`_ framework is documented separately, as it lives in its own repository.  Check out `Entanglement Forging Tutorial 2: Forging with Quantum Serverless <./entanglement_forging/tutorials/tutorial_2_forging_with_quantum_serverless.ipynb>`_  and `CutQC Tutorial 3: Circuit Cutting with Quantum Serverless <./circuit_cutting/tutorials/cutqc/tutorial_3_cutting_with_quantum_serverless.ipynb>`_ for examples on how to integrate Quantum Serverless into circuit knitting workflows.

This project is meant to evolve rapidly and, as such, does not follow `Qiskit's deprecation policy <https://qiskit.org/documentation/contributing_to_qiskit.html#deprecation-policy>`_.  We may occasionally make breaking changes in order to improve the user experience.  When possible, we will keep old interfaces and mark them as deprecated, as long as they can co-exist with the new ones.  Each substantial improvement, breaking change, or deprecation will be documented in the :ref:`release notes`.

Citing this project
-------------------

If you use the Circuit Knitting Toolbox in your research, please cite it according to ``CITATON.bib`` file included in this repository:

.. literalinclude:: ../CITATION.bib
   :language: bibtex

Developer guide
---------------

The source code to the toolbox is available `on GitHub <https://github.com/Qiskit-Extensions/circuit-knitting-toolbox>`__.

The developer guide is located at `CONTRIBUTING.md <https://github.com/Qiskit-Extensions/circuit-knitting-toolbox/blob/main/CONTRIBUTING.md>`__ in the root of this project's repository.

Contents
--------

.. toctree::
  :maxdepth: 2

  About Circuit Knitting Toolbox <self>
  Installation Instructions <install>

.. toctree::
  :maxdepth: 2
  :caption: Circuit Cutting

  Cutting Tutorials <circuit_cutting/tutorials/index>
  Cutting Explanatory Material <circuit_cutting/explanation/index>
  Cutting How-To Guides <circuit_cutting/how-tos/index>
  CutQC (legacy circuit cutting implementation) <circuit_cutting/cutqc/index>

.. toctree::
  :maxdepth: 2
  :caption: Entanglement Forging

  Forging Tutorials <entanglement_forging/tutorials/index>
  Forging Explanatory Material <entanglement_forging/explanation/index>
  Forging How-To Guides <entanglement_forging/how-tos/index>

.. toctree::
  :maxdepth: 2
  :caption: References

  API References <apidocs/index>
  Release Notes <release-notes>

.. Hiding - Indices and tables
   :ref:`genindex`
   :ref:`modindex`
   :ref:`search`
