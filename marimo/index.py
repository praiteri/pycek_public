import marimo

__generated_with = "0.11.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

@app.cell
def _(mo):
    mo.md(
        """
        # Chemical Energetics and Kinetics Virtual Notebook,
        This web page and those linked below have been created with Python using Jupyter Notebooks and will be used to develop important skills in data analysis, data processing, and computing using simulated experimental results and computational chemistry software. 
        ALthough we would encourage you to use Python notebooks for processing the laboratory data, as this is a sought-after skill by many employers, all the numerical labs can also be solved using simple Excel spreadsheets or even by hand with some algebra and a pocket calculator. 
        The assesment of the reports does not focus on the programming skills, but rather on the data analysis and data presentation, so you can choose your preferred method to analyse the data. 
        All the data will be available in CSV files, which can be readily imported into Excel or read by Python. 
        During the numerical labs, your lab demonstrator will show you how Python notebooks can be used to solve these problems, which you may have already used in the first year, or help you with the excel functions. 

        The links below will take you to a series of experiences that will be done in the corresponding week. 
        All the labs focus on physical chemistry concepts that you have already seen in the first year (*e.g.*, calorimetry, equilibrium, kinetics) or will be covered during the semester.
        We will start with one labs to refresh sam basic statistics concepts and familiarize ourselves with Python, if you choose to do the laboratories activities in that way.
        We will then have one thermodynamics lab, one kinetics lab and one lab about chemical equilibrium.
        In the chemical equilibriun lab, no data need to be generated, but you would have to implement a minimisation algorithm either in Python or in in Excel.

        Although these numerical labs cover a variety of different topics in Thermodynamics and Kinetics, the problems proposed here share some common features:

        1. They have been designed to mimic real experiments, to a certain extent. This means that you often have the choice of setting the conditions of the experiment (*i.e.*, the temperature) and then perform the measurement by clicking a button.
        2. The results of all measurements come with some random noise, designed to mimic the experimental uncertainty of the instruments and user errors. This means that if you perform the same measurement 10 times under the same conditions, you will obtain 10 different values.
        3. Often the initial conditions can be set using sliding bars, designed to be difficult to set to nice round numbers, and the measurements will give results with lots of decimal places. It will be left to you to decide how many digits are significant and worth reporting.
        4. At the end of the virtual experiments, all the data collected can be exported as a Comma Separated Values (CSV) file that can be directly imported into Excel or read by Python and R.
        5. In most cases, the data obtained during the virtual experiment should be comparable to real experimental data.

        You don't need to solve the entire lab during the lab time, this web page will remain active for the entire semester, and you can easily access it from home.

        ##**Check the unit outline for when the reports are due**

        #Labs

        1. [Statistics](/stats)
        2. [Bomb Calorimetry](/bc)
        3. [Crystal Violet](/cv)
        4. [Surface Adsorption](/surface)
        """
    )
    return
