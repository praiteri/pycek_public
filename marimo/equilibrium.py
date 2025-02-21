import marimo

__generated_with = "0.11.7"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import copy

    nspecies = mo.ui.number(2,10,value=2,label="Number of species")
    mo.vstack([
        mo.md("#**Numerical Solution of Equilibrium Problems**").center(),
        nspecies],gap=2)
    return copy, mo, np, nspecies, plt


@app.cell
def _(nspecies):
    species = [chr(i) for i in range(65, 65 + nspecies.value)]
    return (species,)


@app.cell
def _(mo, species):
    ss = [ mo.ui.text(value=s) for s in species]
    compounds = mo.ui.array([ *ss ],label=f"Species Names")

    nn = [ mo.ui.number(-5,5,value=1,label=f"{s}") for s in species]
    stoichiometry = mo.ui.array([
           *nn,
    ],label=f"Stiochiometric coefficients")

    cc = [ mo.ui.number(-5,5,0.01,value=1,label=f"{s}") for s in species]
    concentrations = mo.ui.array([
           *cc,
    ],label=f"Initial concentrations")

    mo.hstack([
        compounds,stoichiometry,concentrations
    ],align="start",justify="space-around")

    return cc, compounds, concentrations, nn, ss, stoichiometry


@app.cell
def _(compounds, mo, stoichiometry):
    nu = stoichiometry.value
    _tex = ""
    for i,xs in enumerate(compounds.value):
        if nu[i] < 0:
            _tex += f"\\mathrm{{{abs(nu[i])}{xs}}} + " if nu[i] < -1 else f"\\mathrm{{{xs}}} + "
    _tex = _tex.strip().rstrip('+')
    _tex += "\\rightleftharpoons"
    for i,xs in enumerate(compounds.value):
        if nu[i] > 0:
            _tex += f"\\mathrm{{{nu[i]}{xs}}} + " if nu[i] > 1 else f"\\mathrm{{{xs}}} + "
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

    return a, b, i, keq, nu, xs


@app.cell
def _(mo, np):
    step = mo.ui.slider(steps=np.logspace(-8,0,90),label="$\delta c$",show_value=True)
    tol = mo.ui.slider(steps=np.logspace(-8,0,90),label="Convergence Threshold",show_value=True)

    mo.vstack([
        mo.md("##**Optimisation parameters**").center(),
        mo.hstack([
        step, 
        tol,]
        ,align="start",justify="space-around")
    ])
    
    return step, tol


@app.cell
def _(np):
    def compute_Q(conc,stoich):
        Q = 1
        for i in range(len(conc)):
            Q *= conc[i]**stoich[i]
        return Q

    def compute_force(conc,stoich,pkeq):
        Q = compute_Q(conc,stoich)
        return -np.log10(Q) - pkeq

    def update_concentrations(conc,stoich,force,dc):
        ctmp = np.zeros(len(conc))
        for i in range(len(conc)):
            ctmp[i] = conc[i] +dc*stoich[i]*force
        return ctmp

    def solve_analytic(conc,keq):
        """
        (b+x) / (a-2x)**2 = c
        """
        a = conc["A"]
        b = conc["B"]
        c = keq
        x0 = (-np.sqrt(8*a*c + 16*b*c + 1) + 4*a*c + 1)/(8*c)
        x1 = (np.sqrt(8*a*c + 16*b*c + 1) + 4*a*c + 1)/(8*c)
        return x0,x1
    return compute_Q, compute_force, solve_analytic, update_concentrations


@app.cell
def _(
    Dict,
    List,
    NDArray,
    compute_Q,
    compute_force,
    np,
    plt,
    update_concentrations,
):
    def solve_equilibrium(
        species: List,
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
        ns = len(species)

        conc = np.zeros(shape=(max_iterations + 1, ns))
        forces = np.zeros(shape=(max_iterations + 1,1))

        # Set initial values
        conc[0,:] = np.array(initial_conc)
        forces[0] = compute_force(conc[0,:], stoichiometry, pK_eq)

        # Iterate until convergence or max iterations
        for i in range(max_iterations):
            # Update values
            conc[i+1,:] = update_concentrations(conc[i,:], stoichiometry, forces[i,0], dc)
            forces[i+1] = compute_force(conc[i+1,:], stoichiometry, pK_eq)
            if forces[i+1]*forces[i] < 0:
                dc /=2
            pQ = -np.log10(compute_Q(conc[i+1,:], stoichiometry))

            # Check convergence
            # if np.isclose(pQ, pK_eq, rtol=rtol):
            if np.abs(forces[i+1]) < rtol:
                # Trim unused array space if converged early
                return conc[:i+2,:], forces[:i + 2]

        # Return all iterations if no convergence
        return conc[:i+2,:], forces[:i + 2]

    def plot(x,data,labels=None,refs=None,log=False,axes=None):
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        ncols = data.shape[1]
        plt.figure(figsize=(4,4))
        for i in range(ncols):
            plt.plot(x,data[:,i],label=labels[i],color=colors[i])

        if refs is not None:
            for i in range(len(refs)):
                plt.axhline(refs[i],linestyle='dashed',color=colors[i])

        if axes is not None:
            plt.xlabel(axes[0])
            plt.ylabel(axes[1])
        if log:
            plt.yscale("log")
        plt.legend()
        return plt.gca()
    return plot, solve_equilibrium


@app.cell
def _(compounds, keq, np, plot, solve_equilibrium, species, step, tol):
    # conc = { s: float(conc_all[s].value) for s in species }
    # stoich = { s: nu_all[s].value for s in species }
    def execute(conc_list,stoich_list):
        # conc_list = np.array([float(conc_all[s].value) for s in species])
        # stoich_list = np.array([nu_all[s].value for s in species])

        pkeq = -np.log10(float(keq.value))
        dc = float(step.value)
        rtol = float(tol.value)

        final_conc_list, forces = solve_equilibrium(
            species,
            conc_list,
            stoich_list,
            pkeq,dc,rtol,max_iterations=10000)

        cycles = np.linspace(0,len(forces),len(forces))
        # roots = solve_analytic(conc,float(keq.value))
        # analytic_solution = [ data[0,1] + stoich["A"]*roots[0] , data[0,2] + stoich["B"]*roots[0] ]

        plot_c = plot(cycles,final_conc_list,labels=compounds.value,axes=["Cycles","Concentration"])
        plot_f = plot(
            cycles, np.abs(forces),
            labels=["Force"],refs=[rtol],log=True,axes=["Cycles","Force"])

        return final_conc_list, forces, plot_c, plot_f
    return (execute,)


@app.cell
def _(concentrations, execute, mo, np, stoichiometry):
    final_conc_list, forces, plot_c, plot_f = execute(
        np.array(concentrations.value, dtype=float),
        np.array(stoichiometry.value,dtype=int)
    )

    mo.vstack([
            mo.md("##**Optimisation Results**").center(),
            mo.hstack([plot_c,plot_f],
    align="start", justify="space-around")])
    return final_conc_list, forces, plot_c, plot_f


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
