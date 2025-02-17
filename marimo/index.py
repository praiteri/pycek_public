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
        #Labs

        1. [Statistics](/stats)
        2. [Bomb Calorimetry](/bc)
        3. [Crystal Violet](/cv)
        4. [Surface Adsorption](/surface)
        """
    )
    return
