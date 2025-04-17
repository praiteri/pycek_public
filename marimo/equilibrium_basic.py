import marimo

__generated_with = "0.12.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    from typing import Dict
    from numpy.typing import NDArray

    conc_a = mo.ui.text(value="0.2",label="$[\mathrm{A}]_0$")
    conc_b = mo.ui.text(value="0.1",label="$[\mathrm{B}]_0$")
    keq = mo.ui.text(value="12",label="$K_{eq}$")

    step = mo.ui.slider(steps=np.logspace(-8,0,90),label="$\delta c$",show_value=True)
    tol = mo.ui.slider(steps=np.logspace(-8,0,90),label="Convergence Threshold",show_value=True)

    mo.md(
        f"""
        ##**Initial conditions**

        {conc_a} {conc_b} {keq}\n

        ##**Chemical Equilibrium Solver Parameters**

        {step} {tol}
        """
    )
    return Dict, NDArray, conc_a, conc_b, keq, mo, np, plt, step, tol


@app.cell
def _(np):
    def compute_Q(conc,stoich):
        Q = 1
        for c in conc:
            Q *= conc[c]**stoich[c]
        return Q

    def compute_force(conc,stoich,pkeq):
        Q = compute_Q(conc,stoich)
        return -np.log10(Q) - pkeq

    def update_concentrations(conc,stoich,force,dc):
        for c in conc:
            conc[c] += dc*stoich[c]*force
        return conc

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
    NDArray,
    compute_Q,
    compute_force,
    conc_a,
    conc_b,
    keq,
    mo,
    np,
    plt,
    solve_analytic,
    step,
    tol,
    update_concentrations,
):
    conc = {
        "A": float(conc_a.value),
        "B": float(conc_b.value),
    }

    stoich = {
        "A":-2,
        "B":1,
    }

    pkeq = -np.log10(float(keq.value))
    dc = float(step.value)
    rtol = float(tol.value)

    # print(conc,np.log10(compute_Q(conc,stoich)),pkeq)

    initial = mo.md(
        f"""
        ##**Initial conditions**
        $Q$ = {compute_Q(conc,stoich):.4e} &nbsp; &nbsp; 
        Initial force = {compute_force(conc, stoich, pkeq):.4e}
        """
    )

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
        iterations = np.zeros(max_iterations + 1)
        conc_A = np.zeros(max_iterations + 1)
        conc_B = np.zeros(max_iterations + 1)
        forces = np.zeros(max_iterations + 1)

        # Set initial values
        conc = initial_conc.copy()
        force_0 = compute_force(conc, stoichiometry, pK_eq)
        conc_A[0] = conc['A']
        conc_B[0] = conc['B']
        forces[0] = force_0

        # Iterate until convergence or max iterations
        for i in range(max_iterations):
            # Update values
            conc = update_concentrations(conc, stoichiometry, forces[i], dc)
            force = compute_force(conc, stoichiometry, pK_eq)
            # if force*forces[i] < 0:
            #     dc /=2
            pQ = -np.log10(compute_Q(conc, stoichiometry))

            # Store results
            iterations[i + 1] = i + 1
            conc_A[i + 1] = conc['A']
            conc_B[i + 1] = conc['B']
            forces[i + 1] = force

            # Check convergence
            # if np.isclose(pQ, pK_eq, rtol=rtol):
            if np.abs(force) < rtol:
                # Trim unused array space if converged early
                return np.column_stack([
                    iterations[:i + 2],
                    conc_A[:i + 2],
                    conc_B[:i + 2],
                    forces[:i + 2]
                ])

        # Return all iterations if no convergence
        return np.column_stack([iterations, conc_A, conc_B, forces])

    def plot(data,labels=None,refs=None,log=False,axes=None):
        ncols = data.shape[1]
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        plt.figure(figsize=(4,4))
        for i in range(0,ncols-1):
            plt.plot(data[:,0],data[:,i+1],label=labels[i],color=colors[i])

        if refs is not None:
            for i in range(len(refs)):
                plt.axhline(refs[i],linestyle='dashed',label=labels[i]+"$_{exact}$",color=colors[i])

        if axes is not None:
            plt.xlabel(axes[0])
            plt.ylabel(axes[1])
        if log:
            plt.yscale("log")
        plt.legend()
        return plt.gca()


    data = solve_equilibrium(conc,stoich,pkeq,dc,rtol,max_iterations=1000)
    final_conc = {"A":data[-1,1] , "B":data[-1,2]}

    roots = solve_analytic(conc,float(keq.value))
    analytic_solution = [ data[0,1] + stoich["A"]*roots[0] , data[0,2] + stoich["B"]*roots[0] ]


    plot_c = plot(data[:,0:3],labels=["[A]","[B]"],refs=analytic_solution,axes=["Cycles","Concentration"])
    plot_f = plot(
        np.column_stack([data[:,0],np.abs(data[:,3])]),
        labels=["Force"],refs=[rtol],log=True,axes=["Cycles","Force"])
    final = mo.md(
        f"""
        ##**Final conditions**

        $[A]_f$ = {final_conc["A"]:.4e} &nbsp; &nbsp;
        $[B]_f$ = {final_conc["B"]:.4e} &nbsp; &nbsp;
        $Q$ = {compute_Q(final_conc,stoich):.4e} &nbsp; &nbsp;
        $K_{{eq}}$ = {float(keq.value):.4e} \n
        Final force = {compute_force(final_conc,stoich,pkeq):.4e} &nbsp; &nbsp;
        Force threshold = {float(tol.value):.4e}

        """
    )

    mo.vstack([initial,final,
        mo.hstack([plot_c,plot_f])
        ])
    return (
        analytic_solution,
        conc,
        data,
        dc,
        final,
        final_conc,
        initial,
        pkeq,
        plot,
        plot_c,
        plot_f,
        roots,
        rtol,
        solve_equilibrium,
        stoich,
    )


if __name__ == "__main__":
    app.run()
