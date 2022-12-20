# elastomech.py 🛠
[Run on Streamlit Cloud](https://l-mech-elastomech-home-dinx3b.streamlit.app/)

## Support forces and working radius using a substitute model 

### Resources
- [Theoretical background](https://github.com/l-mech/elastomech/blob/main/resources/Elastostatic%20model%20for%20platform%20supports%20Rev%20A.pdf)
- [Github Repo](https://github.com/l-mech/elastomech)

### How to use
**Make sure to use a consistent unit system!** The script does not know about units, you can choose the unit system as you like, but everything has to fit together.

Useful consistent unit systems are:
- ``SI system: m, kg, N``
- ``mm-t-s: (mm, t, N)``
- ``mm-kg-ms: (mm, kg, kN)``

#### Support Force Distribution Tool
Using the **Support Force Distribution** tool the support forces and other values can be determined for a specific load condition.

To do this, specify all the required parameters in the sidebar, the diagrams update continuously.

The results include the following quantities:
- ``f1...f4``: Support forces of the four supports
- ``t14x, t23x``: Torques induced in the two virtual torsion springs of the frame
- ``s1...s4``: Deflection of the four supports. Negative values mean that one support lifts off.
- ``f12...f14``: Residual loads of the four tilt edges, where the residual load is the sum of two neighboring support forces

When a support lifts off, the calculation in the background switches from the statically overdetermined model (four feet on the floor) to the statically determined model (three feet on the floor).

Mathematically, the corresponding support force is set to $F_i=0$ and the spring equation $F_i=s_i\cdot D_i$ of the respective support is removed from the equation system.

#### Working Radius Tool
With the **Working Radius** tool we can create a working range limit curve that is limited by different boundaries.

These boundaries include:
- Working radius ``ro`` itself (e.g. limited by boom length)
- Residual load ``rl`` (with ``rl = min(f12, f23, f34, f14)``)
- Support forces ``f1...f4``
- Torsional moments ``t14x``, ``t23x`` in the virtual torsion springs of the frame
For each of the quantities a lower bound and an upper bound can be defined.

For each step $0°\leq \phi_i \leq 360°$ the script tries to maximize the working radius ``ro`` within the given bounds using the ``SLSQP`` method ([Sequential Least Squares Programming](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html#optimize-minimize-slsqp)).
If no solution can be found the algorithm stops after a defined number of iterations.

The actual load moment ``ml`` as input for the calculation is calculated as $M_L = r_o \cdot F_{ro}$. This means that only one load on the boom is considered, namely the force at the tip of the boom ``f_ro``. No dead weight of the boom or other additional forces are included in this calculation, because the position of these forces cannot be determined with certainty as a function of the working radius ``ro`` (the same outreach can be achieved with different positions of the boom).                                                                                                                      

**Please be aware that it's easily possible to set the constraints in such a way that there are no more admissible solutions.** In this case the script skips the calculation and steps to next angle $\phi_i$ (an error log is shown after the loop finishes).
However, the calculation can take very long in this case, because the optimization algorithm tries to determine a solution until the maximum allowed iterations are reached. Check the diagrams next to the polar plot to get an idea of which boundaries might cause problems.

After setting all parameters, the calculation is started with the button.

Results and input values can be downloaded as csv files using the corresponding download buttons.
