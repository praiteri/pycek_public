<svelte:head>
	<title>Chemical Energetics and Kinetics Virtual Notebook</title>
</svelte:head>

<div class="container">
	<h1>Chemical Energetics and Kinetics Virtual Notebook</h1>

	<div class="lab-grid">
		<a href="/calendar" class="lab-card">
			<h3>Calendar</h3>
			<p>Lab schedule and deadlines<br />(2025)</p>
		</a>
		<a href="/download-file/LabManualCHEM2000-1.pdf" class="lab-card">
			<h3>Lab Manual<br />(Download PDF)</h3>
			<p>Version 1 - 20/02/2025</p>
		</a>
		<a href="/download-file/LabReportTemplate.docx" class="lab-card">
			<h3>Lab Report Template<br />(Download DOCX)</h3>
			<p>Version 1 - 28/02/2025</p>
		</a>
		<a href="/download-file/NotesOfStatistics-1.pdf" class="lab-card">
			<h3>Notes of Statistics<br />(Download PDF)</h3>
			<p>Version 1 - 20/02/2025</p>
		</a>
		<a href="/download-file/python_primer.pdf" class="lab-card">
			<h3>A Python Primer<br />(Download PDF)</h3>
			<p>Version 1 - 20/02/2025</p>
		</a>
	</div>

	<hr />

	<div class="lab-grid">
		<a href="/stats" class="lab-card">
			<h3>Statistics Lab</h3>
			<p>Basic statistical concepts and Python introduction<br />(Week 2)</p>
		</a>
		<a href="/bc" class="lab-card">
			<h3>Bomb Calorimetry Lab</h3>
			<p>Thermodynamics and heat measurements<br />(Week 4)</p>
		</a>
		<a href="/cv" class="lab-card">
			<h3>Crystal Violet Lab</h3>
			<p>Chemical kinetics and reaction rates<br />(Week 8)</p>
		</a>
		<a href="/eq" class="lab-card">
			<h3>Chemical Equilibrium Lab</h3>
			<p>Numerical solution of equilibrium problems<br />(Week 10)</p>
		</a>
		<a href="/surface" class="lab-card">
			<h3>Surface Adsorption Lab</h3>
			<p>Equilibrium and surface chemistry<br />(Week 12)</p>
		</a>
	</div>

	<h2><strong>Check the calendar for when the reports are due</strong></h2>

	<hr />

	<h2>Introduction</h2>

	<p>
		This web page and those linked below have been created with Python using Jupyter Notebooks and
		will be used to develop important skills in data analysis, data processing, and computing using
		simulated experimental results and computational chemistry software.
	</p>

	<p>
		Although we would encourage you to use Python notebooks for processing the laboratory data, as
		this is a sought-after skill by many employers, all the numerical labs can also be solved using
		simple Excel spreadsheets or even by hand with some algebra and a pocket calculator.
	</p>

	<p>
		The assessment of the reports does not focus on the programming skills, but rather on the data
		analysis and data presentation, so you can choose your preferred method to analyse the data.
	</p>

	<p>
		All the data will be available in CSV files, which can be readily imported into Excel or read
		by Python.
	</p>

	<p>
		During the numerical labs, your lab demonstrator will show you how Python notebooks can be used
		to solve these problems, which you may have already used in the first year, or help you with
		the excel functions.
	</p>

	<p>
		The links below will take you to a series of experiences that will be done in the corresponding
		week.
	</p>

	<p>
		All the labs focus on physical chemistry concepts that you have already seen in the first year
		(<em>e.g.</em>, calorimetry, equilibrium, kinetics) or will be covered during the semester.
	</p>

	<p>
		We will start with one labs to refresh some basic statistics concepts and familiarize ourselves
		with Python, if you choose to do the laboratories activities in that way.
	</p>

	<p>
		We will then have one thermodynamics lab, one kinetics lab and one lab about chemical
		equilibrium.
	</p>

	<p>
		In the chemical equilibrium lab, no data need to be generated, but you would have to implement
		a minimisation algorithm either in Python or in Excel.
	</p>

	<p>
		Although these numerical labs cover a variety of different topics in Thermodynamics and
		Kinetics, the problems proposed here share some common features:
	</p>

	<ol>
		<li>
			They have been designed to mimic real experiments, to a certain extent. This means that you
			often have the choice of setting the conditions of the experiment (<em>i.e.</em>, the
			temperature) and then perform the measurement by clicking a button.
		</li>
		<li>
			The results of all measurements come with some random noise, designed to mimic the
			experimental uncertainty of the instruments and user errors. This means that if you perform
			the same measurement 10 times under the same conditions, you will obtain 10 different values.
		</li>
		<li>
			Often the initial conditions can be set using sliding bars, designed to be difficult to set
			to nice round numbers, and the measurements will give results with lots of decimal places. It
			will be left to you to decide how many digits are significant and worth reporting.
		</li>
		<li>
			At the end of the virtual experiments, all the data collected can be exported as a Comma
			Separated Values (CSV) file that can be directly imported into Excel or read by Python and R.
		</li>
		<li>
			In most cases, the data obtained during the virtual experiment should be comparable to real
			experimental data.
		</li>
	</ol>

	<p>
		You don't need to solve the entire lab during the lab time, this web page will remain active
		for the entire semester, and you can easily access it from home.
	</p>
</div>

<style>
	.container {
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
			sans-serif;
		line-height: 1.6;
		max-width: 1200px;
		margin: 0 auto;
		padding: 10px;
		color: #333;
	}

	h1 {
		color: #2c3e50;
		border-bottom: 2px solid #eee;
		padding-bottom: 10px;
		margin-top: 30px;
	}

	h2 {
		color: #34495e;
		margin-top: 25px;
		text-align: center;
	}

	p {
		margin: 16px 0;
	}

	a {
		color: #3498db;
		text-decoration: none;
	}

	a:hover {
		text-decoration: underline;
	}

	ol {
		padding-left: 20px;
	}

	li {
		margin: 8px 0;
	}

	strong {
		color: #e74c3c;
	}

	.lab-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
		gap: 20px;
		margin: 20px 0;
	}

	.lab-card {
		background: #fff;
		border: 1px solid #e1e1e1;
		border-radius: 8px;
		padding: 20px;
		text-decoration: none;
		transition:
			transform 0.2s,
			box-shadow 0.2s;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	.lab-card:hover {
		transform: translateY(-3px);
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
		text-decoration: none;
	}

	.lab-card h3 {
		color: #2c3e50;
		margin: 0 0 10px 0;
		text-align: center;
	}

	.lab-card p {
		color: #666;
		margin: 0;
		font-size: 0.9em;
		text-align: center;
	}

	hr {
		width: 80%;
		height: 2px;
		background-color: #333;
		border: none;
		margin: 40px auto;
	}
</style>
