<script>
    import RankingSearchArtist from "$lib/components/RankingSearchArtist.svelte";
    import RankSongs from "$lib/components/RankSongs.svelte";

    let selectedArtist = $state(null);

    function handleSelectArtist(artist) {
        selectedArtist = artist;
    }

    function handleBack() {
        selectedArtist = null;
    }
</script>

<section id="ranking-main">
    {#if !selectedArtist}
        <RankingSearchArtist onSelect={handleSelectArtist} />
    {:else}
        <RankSongs artist={selectedArtist} onBack={handleBack} />
    {/if}
</section>

<style>
    /* Add any layout styles for the container here */
    #ranking-main {
        height: 100%;
    }
</style>
