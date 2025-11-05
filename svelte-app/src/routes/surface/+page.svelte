<script>
	import { SurfaceAdsorption } from '$lib/labs/SurfaceAdsorption.js';
	import { downloadCSV } from '$lib/utils/csv.js';
	import Plot from '$lib/components/Plot.svelte';

	let lab = new SurfaceAdsorption({ makePlots: true });

	let studentID = '';
	let outputFile = 'Automatic';
	let temperature = 25;
	let data = [];
	let message = '';
	let fileContent = '';
	let filename = '';
	let showResults = false;
	let error = '';

	function setID() {
		if (studentID && /^\d+$/.test(studentID)) {
			lab.setStudentID(parseInt(studentID));
			error = '';
		} else if (studentID) {
			error = 'Invalid Student ID: must be a number';
		}
	}

	function setFilename() {
		lab.outputFile = outputFile === 'Automatic' ? null : outputFile;
	}

	function runExperiment() {
		error = '';
		if (!studentID || !/^\d+$/.test(studentID)) {
			error = 'Invalid Student ID: must be a number';
			return;
		}

		lab.setParameters({ temperature: temperature + 273.15 });
		data = lab.createDataForLab();
		fileContent = lab.writeDataToString();

		filename = lab.outputFile || lab.filenameGen.random;

		message = `### Running Experiment\n`;
		for (const [k, v] of Object.entries(lab.metadata)) {
			message += `#### ${k} = ${v}\n`;
		}
		message += `#### File created = ${filename}\n`;

		showResults = true;
	}

	function resetCounter() {
		lab.filenameGen.reset();
		lab.outputFile = null;
		showResults = false;
		message = '';
	}

	function handleDownload() {
		downloadCSV(fileContent, filename);
	}
</script>

<svelte:head>
	<title>Surface Adsorption Lab</title>
</svelte:head>

<div class="container">
	<h1>Surface Adsorption Lab</h1>

	<div class="markdown-content">
		<p>
			In the virtual laboratory below, we will be looking at the adsorption of the dye Acid Blue
			158 on chitin in water. The simulated experiments mimic different conditions and will be used
			to determine the enthalpy of adsorption of the dye on the substrate. The output file contains
			the concentration of the dye left in solution, as a function of the amount that was added to
			the beaker with the kitin powder.
		</p>

		<h2>Objectives</h2>
		<ol>
			<li>Calculation of the Langmuir constant (K<sub>L</sub>) and the monolayer coverage (Q) at different temperatures</li>
			<li>
				Compare the fitted values obtained from fitting both forms of the Langmuir isotherm
				(linear and non-linear)
			</li>
			<li>Calculation of the adsorption enthalpy</li>
			<li>Comparison with the provided experimental value</li>
		</ol>

		<h2>Instructions</h2>
		<ol>
			<li>Type your student ID</li>
			<li>Select the temperature of the experiment</li>
			<li>Click "Run Experiment"</li>
			<li>Perform experiments at 5 different temperatures</li>
		</ol>
		<hr />
	</div>

	<div class="controls">
		<div class="form-group">
			<label for="studentID">Student ID:</label>
			<input
				id="studentID"
				type="text"
				bind:value={studentID}
				on:input={setID}
				placeholder="Enter student ID"
			/>
		</div>

		<div class="form-group">
			<label for="outputFile">Output file:</label>
			<input
				id="outputFile"
				type="text"
				bind:value={outputFile}
				on:input={setFilename}
				placeholder="Automatic"
			/>
		</div>

		<div class="form-group">
			<label for="temperature">Temperature (°C):</label>
			<input id="temperature" type="number" bind:value={temperature} min="0" max="100" step="1" />
		</div>

		{#if error}
			<div class="error">{error}</div>
		{/if}

		<div class="button-group">
			<button on:click={runExperiment}>Run Experiment</button>
			<button on:click={resetCounter}>Reset Counter</button>
		</div>
	</div>

	{#if showResults}
		<div class="results">
			<div class="info-panel">
				<div class="metadata">
					{@html message.replace(/###/g, '<h3>').replace(/####/g, '<p>')}
				</div>
				<button on:click={handleDownload} class="download-btn">Download {filename}</button>
			</div>

			{#if data.length > 0}
				<Plot {data} xLabel="Dye added (mg)" yLabel="Dye in solution (mol/L)" />
			{/if}
		</div>
	{/if}
</div>

<style>
	.container {
		max-width: 900px;
		margin: 0 auto;
		padding: 20px;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
			sans-serif;
	}

	h1 {
		color: #2c3e50;
		border-bottom: 2px solid #eee;
		padding-bottom: 10px;
	}

	.markdown-content {
		margin: 20px 0;
	}

	.markdown-content h2 {
		color: #34495e;
		margin-top: 20px;
	}

	.controls {
		background: #f8f9fa;
		padding: 20px;
		border-radius: 8px;
		margin: 20px 0;
	}

	.form-group {
		margin-bottom: 15px;
	}

	.form-group label {
		display: block;
		margin-bottom: 5px;
		font-weight: 500;
		color: #333;
	}

	.form-group input {
		width: 100%;
		padding: 8px 12px;
		border: 1px solid #ddd;
		border-radius: 4px;
		font-size: 14px;
		box-sizing: border-box;
	}

	.button-group {
		display: flex;
		gap: 10px;
		margin-top: 20px;
	}

	button {
		padding: 10px 20px;
		background: #3498db;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
		font-size: 14px;
		font-weight: 500;
		transition: background 0.2s;
	}

	button:hover {
		background: #2980b9;
	}

	.error {
		color: #e74c3c;
		padding: 10px;
		background: #fadbd8;
		border-radius: 4px;
		margin-top: 10px;
	}

	.results {
		margin-top: 30px;
	}

	.info-panel {
		background: #f8f9fa;
		padding: 20px;
		border-radius: 8px;
		margin-bottom: 20px;
	}

	.metadata {
		margin-bottom: 15px;
	}

	.metadata :global(h3) {
		color: #34495e;
		margin: 10px 0 5px 0;
		font-size: 18px;
	}

	.metadata :global(p) {
		color: #555;
		margin: 5px 0;
		font-size: 14px;
	}

	.download-btn {
		background: #27ae60;
	}

	.download-btn:hover {
		background: #229954;
	}

	hr {
		border: none;
		border-top: 1px solid #ddd;
		margin: 20px 0;
	}
</style>
