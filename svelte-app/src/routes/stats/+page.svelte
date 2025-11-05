<script>
	import { StatisticsLab } from '$lib/labs/StatisticsLab.js';
	import { downloadCSV } from '$lib/utils/csv.js';
	import Plot from '$lib/components/Plot.svelte';

	let lab = new StatisticsLab({ makePlots: true });

	let studentID = '';
	let outputFile = 'Automatic';
	let sample = null;
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
		if (!sample) {
			error = 'No sample selected!';
			return;
		}

		lab.setStudentID(parseInt(studentID));
		lab.outputFile = outputFile === 'Automatic' ? null : outputFile;
		lab.setParameters({ sample });

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
		showResults = false;
		message = '';
	}

	function handleDownload() {
		downloadCSV(fileContent, filename);
	}
</script>

<svelte:head>
	<title>Statistics Lab</title>
</svelte:head>

<div class="container">
	<h1>Statistics Lab</h1>

	<div class="markdown-content">
		<p>
			This numerical lab consists a few small tasks, which cover the key statistics topics that
			were introduced in the previous chapter. They are also preparatory for the following labs,
			where you would have to use the same concepts in more complicated situations. In particular,
			if you are using python, it would be beneficial to solve some of this exercises by creating
			specific functions that can the be reused (maybe with small modifications) in the following
			labs.
		</p>

		<h2>Tasks</h2>
		<ol>
			<li>Average and standard error</li>
			<li>Propagation of uncertainty</li>
			<li>Comparison of averages</li>
			<li>Linear Fit</li>
			<li>Non linear fit</li>
			<li>Outlier detection</li>
		</ol>

		<h2>Instructions</h2>
		<ol>
			<li>Type your student ID</li>
			<li>Select a task</li>
			<li>Click "Run Experiment"</li>
			<li>Analyse the data</li>
		</ol>
		<hr />
	</div>

	<div class="controls">
		<div class="form-group">
			<label for="studentID">Student ID:</label>
			<input id="studentID" type="text" bind:value={studentID} placeholder="Enter student ID" />
		</div>

		<div class="form-group">
			<label for="outputFile">Output file:</label>
			<input id="outputFile" type="text" bind:value={outputFile} placeholder="Automatic" />
		</div>

		<div class="form-group">
			<label for="sample">Select task:</label>
			<select id="sample" bind:value={sample}>
				<option value={null}>--Select--</option>
				{#each lab.availableSamples as sampleOption}
					<option value={sampleOption}>{sampleOption}</option>
				{/each}
			</select>
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
				<Plot {data} xLabel="X" yLabel="Y" />
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
	.form-group input,
	.form-group select {
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
