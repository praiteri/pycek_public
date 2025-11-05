<script>
	import { CrystalViolet } from '$lib/labs/CrystalViolet.js';
	import { downloadCSV } from '$lib/utils/csv.js';
	import Plot from '$lib/components/Plot.svelte';

	let lab = new CrystalViolet({ makePlots: true });

	let studentID = '';
	let outputFile = 'Automatic';
	let cvVolume = null;
	let ohVolume = null;
	let h2oVolume = null;
	let temperature = 25;
	let data = [];
	let message = '';
	let fileContent = '';
	let filename = '';
	let showResults = false;
	let error = '';

	function runExperiment() {
		error = '';
		if (!studentID || !/^\d+$/.test(studentID)) {
			error = 'Invalid Student ID: must be a number';
			return;
		}

		lab.setStudentID(parseInt(studentID));
		lab.outputFile = outputFile === 'Automatic' ? null : outputFile;
		lab.setParameters({
			volumes: { cv: cvVolume, oh: ohVolume, h2o: h2oVolume },
			temperature: temperature + 273.15
		});

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
	<title>Crystal Violet Lab</title>
</svelte:head>

<div class="container">
	<h1>Crystal Violet Lab</h1>

	<div class="markdown-content">
		<p>
			This notebook mimics a kinetics laboratory experiment, where a UV-Vis spectrophotometer is
			used to measure the absorbance as the reaction between crystal violet and hydroxide proceeds.
			The absorbance versus time data can then be used to determine the rate of the reaction with
			respect to both crystal violet and hydroxide ions.
		</p>

		<h2>Objectives</h2>
		<ol>
			<li>Determine the reaction order with respect to CV</li>
			<li>Determine the reaction order with respect to hydroxide</li>
			<li>Determine the rate constant for the overall reaction</li>
			<li>Determine the activation energy</li>
		</ol>

		<h2>Instructions</h2>
		<ol>
			<li>Type your student ID</li>
			<li>Select the volumes of the CV solution, the hydroxide solution and DI water to use</li>
			<li>Select the temperature of the experiment</li>
			<li>Click "Run Experiment"</li>
			<li>
				Perform two sets of at least three experiments each:
				<ul>
					<li>constant [CV] while the [OH<sup>-</sup>] is varied</li>
					<li>constant [OH<sup>-</sup>] while the [CV] is varied</li>
				</ul>
			</li>
			<li>
				Obtain another set of data where the temperature is changed and compute the activation
				energy and pre-exponential factor
			</li>
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
				placeholder="Enter student ID"
			/>
		</div>

		<div class="form-group">
			<label for="outputFile">Output file:</label>
			<input
				id="outputFile"
				type="text"
				bind:value={outputFile}
				placeholder="Automatic"
			/>
		</div>

		<div class="form-group">
			<label for="cvVolume">Volume of CV solution (mL):</label>
			<input id="cvVolume" type="number" bind:value={cvVolume} min="0" max="100" step="1" />
		</div>

		<div class="form-group">
			<label for="ohVolume">Volume of OH solution (mL):</label>
			<input id="ohVolume" type="number" bind:value={ohVolume} min="0" max="100" step="1" />
		</div>

		<div class="form-group">
			<label for="h2oVolume">Volume of DI water (mL):</label>
			<input id="h2oVolume" type="number" bind:value={h2oVolume} min="0" max="100" step="1" />
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
				<Plot {data} xLabel="Time (s)" yLabel="Absorbance" />
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
