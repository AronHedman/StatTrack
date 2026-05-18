<script>
    import RankingSearchArtist from "$lib/components/RankingSearchArtist.svelte";
    import RankingSongs from "$lib/components/RankingSongs.svelte";

    let { updateRankingDisplay } = $props();

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
        <RankingSongs
            artist={selectedArtist}
            onBack={handleBack}
            {updateRankingDisplay}
        />
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
