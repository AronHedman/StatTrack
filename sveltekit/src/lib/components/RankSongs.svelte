<script>
    let { artist, onBack } = $props();
</script>

<div>
    <button onclick={onBack}>&larr; Back to Search</button>

    <h2>Rank your top 10 for {artist.name}</h2>
</div>
