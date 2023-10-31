alpaqa
======

``alpaqa`` is an efficient implementation of an augmented Lagrangian method for
general nonlinear programming problems, which uses the first-order, matrix-free
PANOC algorithm as an inner solver.
The numerical algorithms themselves are implemented in C++ for optimal
performance, and they are exposed as an easy-to-use Python package.

The solvers in this library solve minimization problems of the following form:

.. math::

    \begin{aligned}
        & \underset{x}{\textbf{minimize}}
        & & f(x) &&&& f : {{\rm I\mathchoice{\hspace{-2pt}}{\hspace{-2pt}}{\hspace{-1.75pt}}{\hspace{-1.7pt}}R}}^n \rightarrow {{\rm I\mathchoice{\hspace{-2pt}}{\hspace{-2pt}}{\hspace{-1.75pt}}{\hspace{-1.7pt}}R}} \\
        & \textbf{subject to}
        & & \underline{x} \le x \le \overline{x} \\
        &&& \underline{z} \le g(x) \le \overline{z} &&&& g : {{\rm I\mathchoice{\hspace{-2pt}}{\hspace{-2pt}}{\hspace{-1.75pt}}{\hspace{-1.7pt}}R}}^n \rightarrow {{\rm I\mathchoice{\hspace{-2pt}}{\hspace{-2pt}}{\hspace{-1.75pt}}{\hspace{-1.7pt}}R}}^m
    \end{aligned}

Documentation
-------------

- `Sphinx documentation <https://kul-optec.github.io/alpaqa/develop/Sphinx/index.html>`_
- `Python examples <https://kul-optec.github.io/alpaqa/develop/Sphinx/examples/index.html>`_
- `Doxygen documentation <https://kul-optec.github.io/alpaqa/develop/Doxygen/index.html>`_
- `C++ examples <https://kul-optec.github.io/alpaqa/develop/Doxygen/examples.html>`_

Installation
------------

The Python interface can be installed directly from PyPI:

.. code-block:: sh

    python3 -m pip install --upgrade --pre alpaqa

For more information, please see the full
`installation instructions <https://kul-optec.github.io/alpaqa/develop/Sphinx/install/installation.html>`_.

Publications
------------

- `P. Pas, M. Schuurmans, and P. Patrinos, “Alpaqa: A matrix-free solver for nonlinear MPC and large-scale nonconvex optimization,” 20th European Control Conference (ECC), Jul. 2022 (arXiv) <https://arxiv.org/abs/2112.02370>`_
