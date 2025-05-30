import marimo

__generated_with = "0.11.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pycek_public as cek

    lab = cek.surface_adsorption(make_plots=True)
    return cek, lab, mo


@app.cell
def _(mo):
    mo.md(
        """
        # Surface Adsorption Lab

        In the virtual laboratory below, we will be looking at the adsorption of the dye Acid Blue 158 on chitin in water. 
        The simulated experiments mimic different conditions and will be used to determine the enthalpy of adsorption of the dye on the substrate.
        The output file contains the concentration of the dye left in solution, as a function of the amount that was added to the beaker with the kitin powder.

        ## Objectives
        1. Calculation of the Langmuir constant ($K_L$) and the monolayer coverage ($Q$) at different temperatures
        2. Compare the fitted values obtained from fitting both forms of the Langmuir isotherm (linear and non-linear)
        3. alculation of the adsorption enthalpy
        4. Comparison with the provided experimental value

        ## Instructions
        1. Type your student ID
        2. Select the temperature of the experiment
        3. Click "Run Experiment"
        4. Perform experiments at 5 different temperatures
        ___
        """
    )
    return


@app.cell
def _(cek, lab, mo):
    def set_ID(value):
        return cek.set_ID(mo, lab, value)

    student_ID = mo.ui.text(value="", label="Student ID:", on_change=set_ID)

    def set_fname(value):
        lab.output_file = value

    exp_ID = mo.ui.text(value="Automatic", label="Output file:", on_change=set_fname)

    temperature = mo.ui.number(
        start=0, stop=100, step=1, value=25, label="Temperature (C)"
    )

    run_button = mo.ui.run_button(label="Run Experiment")
    reset_button = mo.ui.run_button(label="Reset Counter")

    # Create download button using marimo's download function

    mo.vstack([student_ID, exp_ID, temperature, run_button, reset_button])
    return (
        exp_ID,
        reset_button,
        run_button,
        set_ID,
        set_fname,
        student_ID,
        temperature,
    )


@app.cell
def _(cek, lab, mo, reset_button, run_button, student_ID, temperature):
    if reset_button.value:
        lab.ID = 0
        lab.output_file = None

    image = ""
    message = ""
    download_button = ""
    if run_button.value:
        mo.stop(
            not student_ID.value.isdigit(),
            mo.md(f"### Invalid Student ID: {student_ID.value}"),
        )

        lab.set_parameters(temperature=temperature.value + 273.15)
        data = lab.create_data_for_lab()
        file_content = lab.write_data_to_string()

        fname = lab.output_file
        if not fname:
            fname = lab.filename_gen.random
        message = f"### Running Experiment\n"
        for k, v in lab.metadata.items():
            message += f"####{k} = {v}\n"
        message += f"#### File created = {fname}\n"

        download_button = mo.download(
            file_content,
            filename=fname,
            label=f"Download {fname}",
        )

        plot = cek.plotting()
        image = plot.quick_plot(scatter=data, output="marimo")

    mo.hstack([mo.vstack([mo.md(message), download_button]), image])
    return (
        data,
        download_button,
        file_content,
        fname,
        image,
        k,
        message,
        plot,
        v,
    )


if __name__ == "__main__":
    app.run()
