import marimo

__generated_with = "0.11.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pycek_public as cek
    lab = cek.crystal_violet(make_plots=True)
    return cek, lab, mo


@app.cell
def _(mo):
    mo.md(
        """
        # Crystdal Violet Lab

        This notebook mimics a kinetics laboratory experiment, where a UV-Vis spectrophotometer is used to measure the absorbance as the reaction between crystal violet and hydroxide proceeds. 
        The absorbance versus time data can then be used to determine the rate of the reaction with respect to both crystal violet and hydroxide ions.

        ## Objectives
        1. Determine the reaction order with respect to CV
        2. Determine the reaction order with respect to hydroxide
        3. Determine the rate constant for the overall reaction
        4. Determine the activation energy


        ## Instructions
        1. Type your student ID
        2. Select the volumes of the CV solution, the hydroxide solution and DI water to use
        3. Select the temperature of the experiment
        4. Click "Run Experiment"
        5. Perform two sets of at least three experiments each:
           - constant [CV] while the [OH$^-$] is varied
           - constant [OH$^-$] while the [CV] is varied
        6. Obtain another set of data where the temperature is changed and compute the activation energy and pre-exponential factor
        ___
        """
    )
    return


@app.cell
def _(lab, mo):
    def set_ID(value):
        try:
            student_number = int(value)
            if student_number <= 0:
                print(mo.md(f"### Invalid Student ID: {student_ID.value}"))
            else:
                print(f"Valid Student ID: {student_number}")
                lab.set_student_ID(int(value))
        except ValueError:
            print(mo.md(f"### Invalid Student ID: {student_ID.value}"))

    student_ID = mo.ui.text(value="", label="Student ID:",on_change=set_ID)

    def set_fname(value):
        lab._set_filename(value)
    exp_ID = mo.ui.text(value="Automatic", label="Output file:", on_change=set_fname)

    cv_volume = mo.ui.number(start=0,stop=100,step=1,value=None,label="Volume of CV solution (mL)")
    oh_volume = mo.ui.number(start=0,stop=100,step=1,value=None,label="Volume of OH solution (mL)")
    h2o_volume = mo.ui.number(start=0,stop=100,step=1,value=None,label="Volume of DI water (mL)")
    temperature = mo.ui.number(start=0,stop=100,step=1,value=25,label="Temperature (C)")
    run_button = mo.ui.run_button(label="Run Experiment")
    reset_button = mo.ui.run_button(label="Reset Counter")

    # Create download button using marimo's download function

    mo.vstack([student_ID, 
               exp_ID, 
               cv_volume, 
               oh_volume, 
               h2o_volume, 
               temperature,
               run_button, 
               reset_button])
    return (
        cv_volume,
        exp_ID,
        h2o_volume,
        oh_volume,
        reset_button,
        run_button,
        set_ID,
        set_fname,
        student_ID,
        temperature,
    )


@app.cell
def _(
    cek,
    cv_volume,
    h2o_volume,
    lab,
    mo,
    oh_volume,
    reset_button,
    run_button,
    student_ID,
    temperature,
):
    if reset_button.value:
        lab.ID = 0
        lab._set_filename(None)

    image = ""
    message = ""
    download_button = ""
    if run_button.value:
        mo.stop(not student_ID.value.isdigit(), mo.md(f"### Invalid Student ID: {student_ID.value}"))

        cv_vol = cv_volume.value
        oh_vol = oh_volume.value
        h2o_vol = h2o_volume.value

        lab.set_parameters(
            volumes={'cv': cv_vol, 'oh': oh_vol, 'h2o': h2o_vol},
            temperature=temperature.value+273.15
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
        cv_vol,
        data,
        download_button,
        f,
        file_content,
        fname,
        h2o_vol,
        image,
        k,
        message,
        oh_vol,
        plot,
        v,
    )


if __name__ == "__main__":
    app.run()
