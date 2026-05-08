<script>
	import "$lib/global.scss";

	let { children } = $props();
</script>

<svelte:head>
	<title>StatTrack</title>
	<meta name="description" content="Rank your favorite songs" />
</svelte:head>

{@render children()}
