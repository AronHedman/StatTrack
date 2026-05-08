<script>
    import Header from "$lib/components/Header.svelte";
    import Ranking from "$lib/components/Ranking.svelte";
    import LatestStreams from "$lib/components/LatestStreams.svelte";
</script>

<div class="page">
    <Header />
    <main class="main-content">
        <div class="container">
            <div class="left-column">
                <Ranking />
            </div>
            <div class="right-column">
                <LatestStreams />
            </div>
        </div>
    </main>
</div>

<style lang="scss">
    .page {
        min-height: 100vh;
        background: var(--bg-base);
    }

    .main-content {
        padding: 24px 32px;
    }

    .container {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 24px;
        max-width: 1400px;
        margin: 0 auto;
    }

    .left-column,
    .right-column {
        min-height: calc(100vh - 64px - 48px);
    }

    @media (max-width: 1023px) {
        .container {
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }

        .main-content {
            padding: 16px;
        }
    }

    @media (max-width: 767px) {
        .container {
            grid-template-columns: 1fr;
            gap: 16px;
        }

        .main-content {
            padding: 12px;
        }
    }
</style>
