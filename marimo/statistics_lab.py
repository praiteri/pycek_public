import marimo

__generated_with = "0.11.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pycek_public as cek

    lab = cek.stats_lab(make_plots=True)
    return cek, lab, mo


@app.cell
def _(mo):
    mo.md(
        """
        # Statistics lab
        This numerical lab consists a few small tasks, which cover the key statistics topics that were introduced in the previous chapter.
        They are also preparatory for the following labs, where you would have to use the same concepts in more complicated situations.
        In particular, if you are using python, it would be beneficial to solve some of this exercises by creating specific functions that can the be reused (maybe with small modifications) in the following labs.

        ## Tasks
        1. Average and standard error
        2. Propagation of uncertainty
        3. Comparison of averages
        4. Linear Fit
        5. Non linear fit
        6. Outlier detection


        ## Instructions
        1. Type your student ID
        2. Select a task
        3. Click "Run Experiment"
        4. Analysed the data
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

    sample_selector = mo.ui.dropdown(
        options=lab.available_samples, value=None, label="Select task:"
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
        lab.output_file = None

    image = ""
    message = ""
    download_button = ""
    data = None
    file_content = None
    fname = None
    plot = None
    # print(run_button.value)
    if run_button.value:
        mo.stop(
            not student_ID.value.isdigit(),
            mo.md(f"### Invalid Student ID: {student_ID.value}"),
        )
        mo.stop(sample_selector.value is None, mo.md("### No sample selected !!"))

        lab.set_parameters(number_of_values=12, sample=sample_selector.value)
        data = lab.create_data_for_lab()
        file_content = lab.write_data_to_string()

        fname = lab.output_file
        if not fname:
            fname = lab.filename_gen.random
        if not fname.endswith('.csv'):
            fname += '.csv'
        message = "### Running Experiment\n"
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


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
