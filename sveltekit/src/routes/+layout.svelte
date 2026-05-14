<script>
	import "$lib/global.scss";

	import Header from "$lib/components/Header.svelte";

	let { children } = $props();
</script>

<svelte:head>
	<title>StatTrack</title>
	<meta name="description" content="Rank your favorite songs" />
</svelte:head>

<Header />

{@render children()}
