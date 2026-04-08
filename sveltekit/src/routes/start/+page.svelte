
<script>
    import LatestStreams from "$lib/components/LatestStreams.svelte";
    import Ranking from "$lib/components/Ranking.svelte";

    // (kan behöva en rutt som kollar session["user"]["username"])
</script>

<section id="main">
    <div class="wrapper ranking-wrapper"><Ranking /></div>
    <div class="wrapper latestStreams-wrapper"><LatestStreams /></div>
</section>

<style>
    #main {
        display: grid;
        gap: 10vw;
        padding: 2rem;
        grid: "ranking latestStreams" 70vh / 1fr 1fr;
    }

    .ranking-wrapper {
        grid-area: "ranking";
    }

    .latestStreams-wrapper {
        grid-area: "latestStreams";
    }
</style>

