import marimo

__generated_with = "0.18.2"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from io import BytesIO, StringIO
    from scipy.optimize import curve_fit
    from scipy.signal import find_peaks

    import pycek_public as cek

    import altair as alt
    return cek, StringIO, alt, mo, np, pd


@app.cell
def _(mo):
    get_files, set_files = mo.state([])
    # file_button = mo.ui.file(kind="button",on_change=set_files)
    file_area = mo.ui.file(kind="area",on_change=set_files)
    # mo.vstack([file_button, file_area])
    _text = """
    # Raman Spectrum Fitting 
    ## Upload a **.txt** file with the Raman spectrum and fit its peaks using Lorentzian functions.
    """
    mo.vstack([mo.md(_text), file_area])
    return (file_area,)


@app.cell
def _(file_area):
    filename = None
    # if file_button.value:
    #     filename = file_button
    if file_area.value:
        filename = file_area
    return (filename,)


@app.cell
def _(StringIO, alt, filename, mo, pd):
    if filename is None:
        mo.stop(mo.md("Upload a file"))

    _file_contents = filename.contents()
    df = pd.read_csv(StringIO(_file_contents.decode('utf-8')), sep=r"\s+")
    df.columns = ("X","Y","Z")
    # print(df)

    # Create an interval selection for box zoom
    brush = alt.selection_interval(encodings=['x'])

    # Base chart with selection
    base_chart = alt.Chart(df).mark_line().encode(
        x='X:Q',
        y=alt.Y('Y:Q', scale=alt.Scale(zero=False)),
    ).properties(height=300)

    # Chart with brush selection
    selection_chart = base_chart.add_params(brush)

    # Zoomed chart that filters based on selection and autoscales Y
    zoomed_chart = base_chart.transform_filter(
        brush
    ).properties(
        title='Zoomed View (Y autoscaled)'
    )

    # Combine both charts vertically
    _chart = alt.vconcat(selection_chart, zoomed_chart)
    # Make it reactive ⚡
    chart = mo.ui.altair_chart(selection_chart)
    # chart = mo.ui.altair_chart(_chart)
    return chart, df


@app.cell
def _(chart, mo):
    # Access the selected/zoomed data
    # selected_data = chart.value

    mo.vstack([
        chart,
    ])
    return


@app.cell
def _(chart, df, mo):
    selected_df = chart.value if len(chart.value) > 0 else df
    # Use it however you want
    # mo.vstack([
    # mo.md(f"Selected {len(selected_df)} rows"),
    # mo.ui.table(selected_df)
    # ])

    wavenumbers = selected_df.iloc[:, 0]
    intensities = selected_df.iloc[:, 1]

    get_npeaks, set_npeaks = mo.state(0)
    get_xmin, set_xmin = mo.state(min(wavenumbers))
    get_xmax, set_xmax = mo.state(max(wavenumbers))

    get_fit, set_fit = mo.state(False)

    # Create a state to hold peak positions as a list
    get_peak_positions, set_peak_positions = mo.state([])

    # Create a state to hold fit results
    get_fit_results, set_fit_results = mo.state(None)
    return (
        get_fit_results,
        get_npeaks,
        get_peak_positions,
        get_xmax,
        get_xmin,
        intensities,
        set_fit_results,
        set_npeaks,
        set_peak_positions,
        set_xmax,
        set_xmin,
        wavenumbers,
    )


@app.cell
def _(get_npeaks, get_xmax, get_xmin):
    fitting_parameters = {
        "range" : [get_xmin(),get_xmax()],
        "npeaks" : get_npeaks(),
    }
    return (fitting_parameters,)


@app.cell
def _(get_npeaks, get_xmax, get_xmin, mo, set_npeaks, set_xmax, set_xmin):
    x_min = mo.ui.text(
        value=str(get_xmin()),
        label="Minimum Raman shift",
        on_change = lambda value: set_xmin(value))
    x_max = mo.ui.text(
        value=str(get_xmax()),
        label="Maximum Raman shift",
        on_change = lambda value: set_xmax(value))

    n_input = mo.ui.number(
        start=-1,
        value=get_npeaks(),
        label="Number of peaks for fitting (N):",
        on_change=lambda value: set_npeaks(value)
    )
    # n_inpxut  # This displays the input box

    # mo.hstack([mo.vstack([x_min,x_max,n_input]),chart])
    # mo.vstack([chart,mo.hstack([x_min,x_max,n_input])])
    return n_input, x_max, x_min


@app.cell
def _(
    get_peak_positions,
    mo,
    n_input,
    set_fit_results,
    set_npeaks,
    set_peak_positions,
):
    # Create a state to track when to guess peaks
    get_should_guess, set_should_guess = mo.state(0)

    guess_peaks = mo.ui.button(
        label="Guess Peaks",
        on_click=lambda _: (
            set_should_guess(get_should_guess() + 1),
            set_fit_results(None)
        )
    )

    # Create a state to track when fit button is clicked
    get_fit_trigger, set_fit_trigger = mo.state(0)

    fit_spectrum = mo.ui.button(
        label="Fit Spectrum",
        on_click=lambda _: set_fit_trigger(get_fit_trigger() + 1)
    )

    # Create a reset button
    reset_button = mo.ui.button(
        label="Reset Fit",
        on_click=lambda _: (
            set_npeaks(0),
            set_peak_positions([]),
            set_fit_results(None)
        )
    )

    n = n_input.value

    # Get current peak positions from state
    current_positions = get_peak_positions()

    # Initialize peak positions if needed
    if len(current_positions) != n:
        current_positions = [0] * n
        set_peak_positions(current_positions)

    if n > 0:
        # Create the float_inputs array using current positions
        float_inputs = mo.ui.array(
            [
                mo.ui.number(
                    label=f"Peak position {i+1}:",
                    value=current_positions[i],
                    step=1,
                    on_change=lambda value, idx=i: (
                        lambda v, i: (
                            new_positions := get_peak_positions().copy(),
                            new_positions.__setitem__(i, v),
                            set_peak_positions(new_positions),
                            set_fit_results(None)
                        )[-1]
                    )(value, idx)
                )
                for i in range(n)
            ]
        )
    else:
        float_inputs = ""

    # mo.vstack([
    #     mo.hstack([x_min,x_max,n_input]),
    #     mo.hstack(float_inputs),
    #     mo.hstack([guess_peaks, fit_spectrum, reset_button]),
    # ])
    
    return (
        fit_spectrum,
        float_inputs,
        get_fit_trigger,
        get_should_guess,
        guess_peaks,
        reset_button,
    )


@app.cell
def _(
    cek,
    filename,
    fitting_parameters,
    get_fit_results,
    get_fit_trigger,
    get_npeaks,
    get_peak_positions,
    get_should_guess,
    intensities,
    mo,
    n_input,
    np,
    set_fit_results,
    set_peak_positions,
    wavenumbers,
):
    fitter = cek.RamanFitter(wavenumbers, intensities)

    freq_range = fitting_parameters['range']
    if freq_range[0] in [None, ""]:
        freq_range[0] = min(wavenumbers)
    else:
        freq_range[0] = float(freq_range[0])

    if freq_range[1] in [None, ""]:
        freq_range[1] = max(wavenumbers)
    else:
        freq_range[1] = float(freq_range[1])

    text = ''

    # Check if guess button was clicked
    if get_should_guess() > 0:
        print(n_input.value)
        p0 = fitter.get_peaks_guess(
            n_peaks=n_input.value,
            freq_range=freq_range,
        )
        # Extract peak positions and update state
        new_positions = [p0[i*3] for i in range(min(len(p0)//3, n_input.value))]
        set_peak_positions(new_positions)

    # Check if fit button was clicked
    if get_fit_trigger() > 0 and get_npeaks() > 0:
        current_fit_results = get_fit_results()
        # Only fit if we don't have results or the trigger is new
        if current_fit_results is None or current_fit_results.get('trigger') != get_fit_trigger():
            pp = get_peak_positions()
            print("Running fit with positions:", pp)
            popt = fitter.fit(
                n_peaks=fitting_parameters['npeaks'],
                freq_range=freq_range,
                peak_positions=pp,
                remove_background=True
            )

            # Extract fitted peak positions and update state
            fitted_positions = [popt[i*3] for i in range(fitting_parameters['npeaks'])]
            set_peak_positions(fitted_positions)

            # Store fit results
            set_fit_results({
                'trigger': get_fit_trigger(),
                'popt': popt,
                'fitted': True
            })

    if filename is None:
        mo.stop(mo.md("Upload a file"))

    # Display results
    fit_results = get_fit_results()

    text_h = ""
    text_b = ""
    text_p = ""

    if get_npeaks() > 0:
        text_h = "## Displaying fit result"
        pp = get_peak_positions()

        if fit_results is not None and fit_results.get('fitted'):
            # # Need to re-run the fit to populate the fitter object for plotting
            popt = fitter.fit(
                n_peaks=fitting_parameters['npeaks'],
                freq_range=freq_range,
                peak_positions=pp,
                remove_background=True
            )

            n_peaks = len(popt) // 3 if (len(popt) % 3 == 0) else (len(popt) - 2) // 3

            has_background = len(popt) % 3 == 2
        
            # Background table (if present)
            text_lines = []
            if has_background:
                bg_a, bg_b = popt[-2:]
                text_lines.append("### Background (linear)\n")
                text_lines.append("| Parameter | Value |")
                text_lines.append("| --- | --- |")
                text_lines.append(f"| **Offset** | {bg_a:.4f} |")
                text_lines.append(f"| **Slope** | {bg_b:.6f} |")
                text_lines.append("")
            text_b = "\n".join(text_lines)
        
            # Peaks table
            text_lines = [f"## Fitting Results ({n_peaks} peaks)\n"]
          
            # Group peaks into rows of max 10 columns
            max_cols = 10
            for row_start in range(0, n_peaks, max_cols):
                row_end = min(row_start + max_cols, n_peaks)
                n_cols = row_end - row_start
            
                # Create header row
                header = "| | " + " | ".join([f"**Peak {i+1}**" for i in range(row_start, row_end)]) + " |"
                separator = "| --- |" + "|".join([" --- " for _ in range(n_cols)]) + "|"            
                text_lines.append(header)
                text_lines.append(separator)
            
                # Create data rows
                rows_data = [[] for _ in range(4)]  # Position, Height, Width, Integral
            
                for i in range(row_start, row_end):
                    pos, height, width = popt[i*3:(i*3)+3]
                    integral = height * width * np.pi
                    rows_data[0].append(f"{pos:.2f} cm⁻¹")
                    rows_data[1].append(f"{height:.4f}")
                    rows_data[2].append(f"{width:.4f} cm⁻¹")
                    rows_data[3].append(f"{integral:.4f}")
            
                text_lines.append("| **Position** | " + " | ".join(rows_data[0]) + " |")
                text_lines.append("| **Height** | " + " | ".join(rows_data[1]) + " |")
                text_lines.append("| **Width** | " + " | ".join(rows_data[2]) + " |")
                text_lines.append("| **Integral** | " + " | ".join(rows_data[3]) + " |")
                text_lines.append("")  # Empty line between row groups
        
            text_p = "\n".join(text_lines)
        
            image = fitter.plot(show_components=True)
        else:
            text_h = "## Displaying initial guess"
            image = fitter.plot_data_with_initial_guess(
                freq_range=freq_range,
                peak_positions=pp
            )
    else:
        text_h = "## Displaying raw data"
        image = fitter.plot_data(freq_range=freq_range)
    return image, text_b, text_h, text_p


@app.cell
def _(image, mo):
    import io
    import base64

    def download_plot():
        buf = io.BytesIO()
        image.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        buf.seek(0)
        return buf.getvalue()

    download_button = mo.download(
        data=download_plot,
        filename="plot.png",
        label="Download PNG",
    )
    return (download_button,)


@app.cell
def _(
    download_button,
    fit_spectrum,
    float_inputs,
    guess_peaks,
    image,
    mo,
    n_input,
    reset_button,
    text_h,
    x_max,
    x_min,
):
    mo.vstack([
        mo.md(text_h),
        mo.hstack([x_min,x_max,n_input]),
        mo.hstack(float_inputs),
        mo.hstack([guess_peaks, fit_spectrum, reset_button], align="center"),
        download_button,
        image, 
    ])
    
    return


@app.cell
def _(mo, text_b, text_p):
    mo.vstack([
        mo.md(text_p) , mo.md(text_b)
    ])
    return


if __name__ == "__main__":
    app.run()
