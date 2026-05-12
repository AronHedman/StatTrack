<script>
    import RankingSearchArtist from "$lib/components/RankingSearchArtist.svelte";
    import RankingSongs from "$lib/components/RankingSongs.svelte";

    let selectedArtist = $state(null);

    function handleSelectArtist(artist) {
        selectedArtist = artist;
    }

    function handleBack() {
        selectedArtist = null;
    }
</script>

<section class="ranking-main">
    {#if !selectedArtist}
        <RankingSearchArtist onSelect={handleSelectArtist} />
    {:else}
        <RankingSongs artist={selectedArtist} onBack={handleBack} />
    {/if}
</section>

<style lang="scss">
    .ranking-main {
        flex: 1;
        min-height: 0;
        overflow: hidden;
        display: flex;
    }
</style>
