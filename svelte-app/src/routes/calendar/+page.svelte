<svelte:head>
	<title>Lab Calendar</title>
</svelte:head>

<div class="container">
	<h1>Lab Calendar - 2025</h1>

	<div class="markdown-content">
		<p>The lab schedule and deadlines calendar will be displayed here.</p>
		<p>Please check with your instructor for the most up-to-date schedule.</p>

		<p><a href="/">← Back to Home</a></p>
	</div>
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
	a {
		color: #3498db;
		text-decoration: none;
	}
	a:hover {
		text-decoration: underline;
	}
</style>
