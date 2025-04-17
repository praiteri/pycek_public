import marimo

__generated_with = "0.12.5"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import copy
    from typing import Dict
    from numpy.typing import NDArray

    nspecies = mo.ui.number(2,10,value=2,label="Number of species")
    mo.vstack([
        mo.md("#**Numerical Solution of Equilibrium Problems**").center(),
        nspecies],gap=2)
    return Dict, NDArray, copy, mo, np, nspecies, plt


@app.cell
def _(mo, nspecies):
    species = [chr(i) for i in range(65, 65 + nspecies.value)]
    def_nu = { s:1 for s in species }
    def_cc = { s:0.1 for s in species }
    def_nu["A"] = -1
    ss = [ mo.ui.text(value=s) for s in species]
    compounds = mo.ui.array([ *ss ],label=f"Species Names")

    nn = [ mo.ui.number(-5,5,value=def_nu[s],label=f"{s}") for s in species]
    stoichiometry = mo.ui.array([
           *nn,
    ],label=f"Stiochiometric coefficients")

    cc = [ mo.ui.text(value=str(def_cc[s]),label=f"{s}") for s in species]
    concentrations = mo.ui.array([
           *cc,
    ],label=f"Initial concentrations")

    mo.hstack([
        compounds,stoichiometry,concentrations
    ],align="start",justify="space-around")
    return (
        cc,
        compounds,
        concentrations,
        def_cc,
        def_nu,
        nn,
        species,
        ss,
        stoichiometry,
    )


@app.cell
def _(compounds, mo, stoichiometry):
    nu = stoichiometry.value
    _tex = ""

    def format_tex(s):
        for c in ["3+", "2+", "+", "-", "2-", "3-"]:
            s = s.replace(c, f"^{{{c}}}")
        return s

    for i, xs in enumerate(compounds.value):
        formatted_xs = format_tex(xs)
        if nu[i] < 0:
            _tex += f"\\mathrm{{{abs(nu[i])}{formatted_xs}}} + " if nu[i] < -1 else f"\\mathrm{{{formatted_xs}}} + "

    _tex = _tex.strip().rstrip('+')
    _tex += " \\rightleftharpoons "

    for i, xs in enumerate(compounds.value):
        formatted_xs = format_tex(xs)
        if nu[i] > 0:
            _tex += f"\\mathrm{{{nu[i]}{formatted_xs}}} + " if nu[i] > 1 else f"\\mathrm{{{formatted_xs}}} + "

    _tex = _tex.strip().rstrip('+')


    keq = mo.ui.text(value="12",label="$K_{eq}$")

    a = mo.md(
            f"""
            ##**Chemical Reaction**\n
            $$\\begin{{align*}}
            {_tex} &
            \\end{{align*}}$$
            """
        )
    b = mo.md(
            f"""
            ##**Equilibrium constant**\n
            {keq}
            """
        )

    mo.hstack([a,b],align="start",justify="space-around")
    return a, b, format_tex, formatted_xs, i, keq, nu, xs


@app.cell
def _(mo, np):
    step = mo.ui.slider(steps=np.logspace(-8,0,90),label="$\delta c$",show_value=True)
    tol = mo.ui.slider(steps=np.logspace(-8,0,90),label="Convergence Threshold",show_value=True)
    max_iterations = mo.ui.slider(steps=np.logspace(2,6,90),label="Max Iterations",show_value=True)

    check_0 = mo.ui.checkbox(label= "opt 0",)
    check_1 = mo.ui.checkbox(label= f"Decrease $\delta c$",)
    check_2 = mo.ui.checkbox(label= f"Increase $\delta c$",)
    check_3 = mo.ui.checkbox(label= f"Positive [C]",)
    mo.vstack([
        mo.md("##**Optimisation parameters**").center(),
        mo.hstack([check_1,check_2,check_3],align="start",justify="space-around"),
        mo.hstack([
            step, 
            max_iterations,
            tol,]
        ,align="start",justify="space-around")
    ])
    return check_0, check_1, check_2, check_3, max_iterations, step, tol


@app.cell
def _(check_3, np):
    def compute_Q(conc,stoich):
        Q = 1
        for c, s in zip(conc, stoich):
            if c == 0 and s < 0: 
                return None
            Q *= c**s
        return Q

    def compute_force(conc,stoich,pkeq):
        Q = compute_Q(conc,stoich)
        if Q is None: # Conc of at least one reactant is zero
            return -1
        elif Q == 0: # Conc of at least one product is zero
            return 1
        else:
            return -np.log10(Q) - pkeq 

    def update_concentrations(conc,stoich,force,dc):
        if check_3.value:
            for i in range(5):
                ctmp = conc +dc*stoich*force
                if all(ctmp > 0):
                    return ctmp, dc
                dc /= 2
        else:
            ctmp = conc +dc*stoich*force
        return ctmp, dc
    return compute_Q, compute_force, update_concentrations


@app.cell
def _(
    Dict,
    NDArray,
    check_1,
    check_2,
    compute_force,
    np,
    plt,
    update_concentrations,
):
    def solve_equilibrium(
        initial_conc: Dict[str, float],
        stoichiometry: Dict[str, float],
        pK_eq: float,
        dc: float,
        rtol: float = 1e-5,
        max_iterations: int = 10
    ) -> NDArray:
        """
        Solves chemical equilibrium equations using an iterative approach.

        Args:
            initial_conc: Dictionary of initial concentrations for each species
            stoichiometry: Dictionary of stoichiometric coefficients
            pK_eq: Negative log of equilibrium constant
            dc: Concentration step size for iterations
            rtol: Relative tolerance for convergence
            max_iterations: Maximum number of iterations before stopping

        Returns:
            NDArray: Array with columns [iteration, conc_A, conc_B, force]
        """
        # Initialize arrays to store results
        ns = len(initial_conc)

        conc = np.zeros(shape=(max_iterations + 1, ns))
        forces = np.zeros(shape=(max_iterations + 1,1))
        delta = np.zeros(shape=(max_iterations + 1,1))

        # Set initial values
        conc[0,:] = np.array(initial_conc)
        forces[0] = compute_force(conc[0,:], stoichiometry, pK_eq)
        delta[0] = dc

        # Iterate until convergence or max iterations
        for i in range(max_iterations):
            # Update values
            conc[i+1,:] , dc = update_concentrations(conc[i,:], stoichiometry, forces[i,0], dc)
            forces[i+1] = compute_force(conc[i+1,:], stoichiometry, pK_eq)

            if check_1.value and forces[i+1]*forces[i] < 0:
                    dc /=2

            if check_2.value and forces[i+1]*forces[i] > 0:
                    dc *= 1.5

            delta[i+1] = dc

            # Check convergence
            if np.abs(forces[i+1]) < rtol:
                # Trim unused array space if converged early
                return conc[:i+2,:], forces[:i + 2], delta[:i + 2]

        # Return all iterations if no convergence
        return conc[:i+2,:], forces[:i + 2], delta[:i + 2]

    def plot(x,data,labels=None,refs=None,log=False,axes=None):
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        ncols = data.shape[1]
        nrows = data.shape[0]
        plt.figure(figsize=(4,4))
        for i in range(ncols):
            plt.plot(x,data[:,i],label=labels[i],color=colors[i])
            if nrows < 50:
                plt.scatter(x,data[:,i],color=colors[i],s=20)

        if refs is not None:
            for i in range(len(refs)):
                plt.axhline(refs[i],linestyle='dashed',color=colors[i])

        if axes is not None:
            plt.xlabel(axes[0])
            plt.ylabel(axes[1])
        if log:
            plt.yscale("log")

        ax = plt.gca()
        ax.text(0.5, 0.5, 'TEMPLATE', transform=ax.transAxes,
            fontsize=40, color='gray', alpha=0.5,
            ha='center', va='center', rotation=30)
        plt.legend()
        return plt.gca()
    return plot, solve_equilibrium


@app.cell
def _(compounds, keq, max_iterations, np, plot, solve_equilibrium, step, tol):
    def execute(conc_list,stoich_list):
        pkeq = -np.log10(float(keq.value))
        dc = float(step.value)
        rtol = float(tol.value)

        final_conc_list, forces, deltas = \
            solve_equilibrium(
                conc_list,
                stoich_list,
                pkeq,
                dc,
                rtol,
                max_iterations=int(max_iterations.value))

        cycles = np.linspace(0,len(forces),len(forces))

        logscale = False
        if any(final_conc_list[-1,:] < 1e-2):
            logscale = True
        plot_c = plot(cycles,final_conc_list,labels=compounds.value,
                      log=logscale,axes=["Cycles","Concentration"])
        plot_f = plot(
            cycles, np.abs(forces),
            labels=["Force"],refs=[rtol],log=True,axes=["Cycles","Force"])
        plot_d = plot(
            cycles, np.abs(deltas),
            labels=[f"dc"],log=True,axes=["Cycles",f"dc"])

        return final_conc_list, forces, plot_c, plot_f ,plot_d
    return (execute,)


@app.cell
def _(compute_Q, concentrations, execute, keq, mo, np, stoichiometry):
    final_conc_list, forces, plot_c, plot_f, plot_d = execute(
        np.array(concentrations.value, dtype=float),
        np.array(stoichiometry.value,dtype=int)
    )

    Q = compute_Q(final_conc_list[-1,:],np.array(stoichiometry.value,dtype=int))
    K = float(keq.value)
    if np.isclose(Q,K,rtol=1e-6):
        mm = mo.md("##**Optimisation Achieved**")
    else:
        mm = mo.md("##**Optimisation Failed**")

    mo.vstack([
            mm.center(),
            mo.hstack([plot_c,plot_f,plot_d],
    align="start", justify="space-around")])
    return K, Q, final_conc_list, forces, mm, plot_c, plot_d, plot_f


@app.cell
def _(
    compounds,
    compute_Q,
    final_conc_list,
    forces,
    keq,
    mo,
    np,
    stoichiometry,
):
    stoich_list = np.array(stoichiometry.value,dtype=int)
    # initial = mo.md(f"""
    #     ###**Initial conditions**
    #     ####Force = {forces[0,0]:.4e}
    #     ####Q  = {compute_Q(final_conc_list[0,:],stoich_list):.4e}
    #     ####Concentrations:<br> {" ".join([f"* [{xx}] = {final_conc_list[0,i]:.4e}<br>" for i,xx in enumerate(compounds.value)])}
    #     """)

    final_0 = mo.md(f"""
        Force = {forces[-1,0]:.4e}<br>
        Q  = {compute_Q(final_conc_list[-1,:],stoich_list):.4e}<br>
        Keq = {float(keq.value):.4e}
        """)
    final_1 = mo.md(f"""
        Concentrations:
        {" ".join([f"<br>[{xx}] = {final_conc_list[-1,i]:.4e}" for i,xx in enumerate(compounds.value)])}
        """)

    mo.vstack([
        mo.md('##**Final conditions**').center(),
        mo.hstack([final_0,final_1],align="start",justify="space-between")
    ],justify="space-around")
    return final_0, final_1, stoich_list


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
