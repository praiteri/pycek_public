import marimo

__generated_with = "0.11.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pycek_public as cek
    lab = cek.bomb_calorimetry(make_plots=True)
    return cek, lab, mo


@app.cell
def _(mo):
    mo.md(
        """
        #Bomb calorimetry lab

        This notebook mimics a bomb calorimetry laboratory experiment.
        In each experiment a tablet of reactant is prepared and combusted in the calorimeter.
        During the experiment the temperature inside the calorimeter is monitored.

        ## Obejectives
        1. Calibration of the calorimeter
        2. Calculation of enthalpy of combustion of sucrose
        3. Calculation of enthalpy of combustion of napthalene

        ## Instructions
        1. Type your student ID
        2. Select a sample
        3. Click "Run Experiment"
        4. Perform at least 4 experiments per sample
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

    exp_ID = mo.ui.text(value="Automatic", label="Output file:", 
                        on_change=set_fname)

    sample_selector = mo.ui.dropdown(
        options=lab.available_samples, value=None, label="Select sample:"
    )

    run_button = mo.ui.run_button(label="Run Experiment")
    reset_button = mo.ui.run_button(label="Reset Counter")

    # Create download button using marimo's download function

    mo.vstack([student_ID, exp_ID, sample_selector, run_button, reset_button])
    return (
        exp_ID,
        reset_button,
        run_button,
        sample_selector,
        set_ID,
        set_fname,
        student_ID,
    )


@app.cell
def _(cek, lab, mo, reset_button, run_button, sample_selector, student_ID):
    if reset_button.value:
        lab.ID = 0
        lab._set_filename(None)

    image = ""
    message = ""
    download_button = ""
    if run_button.value:
        mo.stop(sample_selector.value is None, mo.md(f"### No sample selected !!"))

        lab.set_parameters(sample=sample_selector.value,precision=0.01)
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


@app.cell
def _():
    import numpy as np
    return (np,)


if __name__ == "__main__":
    app.run()
