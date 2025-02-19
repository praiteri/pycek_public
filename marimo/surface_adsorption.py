import marimo

__generated_with = "0.11.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pycek_public as cek
    lab = cek.cek.surface_adsorption(make_plots=True)
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
        2. Select the volumes of the CV solution, the hydroxide solution and DI water to use
        3. Select the temperature of the experiment
        4. Click "Run Experiment"
        5. Perform at least 5 experiments at different temperatures
        ___
        """
    )
    return


@app.cell
def _(lab, mo):
    def set_ID(value):
    try:
        student_number = int(value.strip())
        if student_number <= 0:
            print(mo.md(f"### Invalid Student ID: {student_ID.value}"))
        else:
            print(f"Valid Student ID: {student_number}")
            lab.set_student_ID(int(value))
    except ValueError:
        mo.stop(not student_ID.value.isdigit(), mo.md(f"### Invalid Student ID: {student_ID.value}"))
        print(mo.md(f"### Invalid Student ID: {student_ID.value}"))


    student_ID = mo.ui.text(value="", label="Student ID:",on_change=set_ID)

    def set_fname(value):
        lab._set_filename(value)
    exp_ID = mo.ui.text(value="Automatic", label="Output file:", on_change=set_fname)

    temperature = mo.ui.number(start=0,stop=100,step=1,value=25,label="Temperature (C)")

    run_button = mo.ui.run_button(label="Run Experiment")
    reset_button = mo.ui.run_button(label="Reset Counter")

    # Create download button using marimo's download function

    mo.vstack([student_ID, 
               exp_ID, 
               temperature,
               run_button, 
               reset_button])
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
        lab._set_filename(None)

    image = ""
    message = ""
    download_button = ""
    if run_button.value:
        lab.set_parameters(
            temperature = temperature.value+273.15
        )
        _ = lab.create_data()
        fname = lab.write_data_to_file()
        
        with open(fname, "r") as f:
            file_content = f.read()
        message = f"### Running Experiment\n"
        for k,v in lab.metadata.items():
            message += f"####{k} = {v}\n"
        message += f"#### File created = {fname}\n"

        download_button = mo.download(
            file_content,
            filename=fname,
            label=f"Download {fname}",
        )

        plot = cek.plotting()
        data,_,_ = lab.read_data_file(fname)
        plot.quick_plot(data,output=fname.replace(".csv",".png"))
        image = mo.image(fname.replace(".csv",".png"),width=500)
        
    mo.vstack([mo.md(message),download_button,image])
    return (
        data,
        download_button,
        f,
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
