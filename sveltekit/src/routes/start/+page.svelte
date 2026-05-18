<script>
    import { onMount } from "svelte";

    import LatestStreams from "$lib/components/LatestStreams.svelte";
    import Card from "$lib/components/Card.svelte";

    let artists = $state([]);
    let songs = $state([]);
    let rankingGlobal = $state([]);

    function toRanking() {
        window.location.replace("/ranking");
    }

    async function fetchTopArtists() {
        const res = await fetch("/api/fetchtop/artists", {
            credentials: "include",
        });

        if (!res.ok) {
            window.location.replace("/login");
        }

        artists = await res.json();
    }

    async function fetchTopSongs() {
        const res = await fetch("/api/fetchtop/songs", {
            credentials: "include",
        });

        if (!res.ok) {
            window.location.replace("/login");
        }

        songs = await res.json();
    }

    async function fetchGlobalRanking() {
        const res = await fetch("/api/ranking/global", {
            credentials: "include",
        });

        if (!res.ok) {
            window.location.replace("/login");
        }

        rankingGlobal = await res.json();
    }

    onMount(async () => {
        const res = await fetch("/api/me", {
            credentials: "include",
        });

        if (!res.ok) {
            window.location.replace("/login");
        }

        await Promise.all([fetchTopArtists(), fetchTopSongs()]);
    });
</script>

<div class="full-page">
    <main class="main-content">
        <div class="main-container">
            <div class="left-column">
                <button
                    class="reset card ranking-card"
                    id="ranking-card"
                    onclick={toRanking}
                >
                    <h1 id="ranking-card-text">Rankings</h1>
                </button>

                <div class="card streams-card">
                    <LatestStreams />
                </div>
            </div>

            <div class="right-column">
                <div class="container">
                    <h2 class="section-title">Most streamed artists</h2>
                    <div class="sub-container">
                        {#each artists as artist}
                            <Card
                                title1={artist.artist_name}
                                title2={artist.stream_count}
                                backgroundImage={artist.artist_image}
                            />
                        {/each}
                    </div>
                </div>

                <div class="container">
                    <h2 class="section-title">Most streamed songs</h2>
                    <div class="sub-container">
                        {#each songs as song}
                            <Card
                                title1={song.title}
                                title2={song.artist_name}
                                backgroundImage={song.extralarge}
                                info={song.stream_count}
                            />
                        {/each}
                    </div>
                </div>

                <div class="container">
                    <h2 class="section-title">Global rankings</h2>
                    <div class="sub-container">
                        {#each rankingGlobal as song}
                            <Card
                                title1={song.title}
                                title2={song.artist_name}
                                backgroundImage={song.artist_image}
                                info={song.quality_score}
                            />
                        {/each}
                    </div>
                </div>
            </div>
        </div>
    </main>
</div>

<style lang="scss">
    .full-page {
        height: 92vh;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        background: var(--bg-base);
    }

    .main-content {
        width: 100%;
        flex: 1;
        min-height: 0;
        display: flex;
        overflow: hidden;
        padding: 24px 32px;
    }

    .main-container {
        flex: 1;
        min-height: 0;
        display: grid;
        grid-template-columns: 2fr 4fr;
        gap: 24px;
        width: 100%;

        margin: 0 auto;
    }

    .left-column,
    .right-column {
        min-height: 0;
        display: grid;
        grid-template-rows: repeat(3, minmax(0, 1fr));
        gap: 24px;
    }

    .card {
        min-height: 0;
        overflow: hidden;
        display: flex;
        background-color: var(--bg-elevated);
        border-radius: 12px;
    }

    .ranking-card {
        grid-row: 1;
        align-items: center;
        justify-content: center;
    }

    .streams-card {
        grid-row: 2 / span 2;
        padding: 0;
    }

    .right-column > :nth-child(1) {
        grid-row: 1;
    }

    .right-column > :nth-child(2) {
        grid-row: 2;
    }

    .right-column > :nth-child(3) {
        grid-row: 3;
    }

    .container {
        min-height: 0;
        display: flex;
        flex-direction: column;
        align-items: stretch;
        padding: 24px;
        border: 1px solid var(--border-subtle);
        border-radius: 20px;
        background-color: var(--bg-surface);
        box-shadow: var(--shadow-card);
        box-sizing: border-box;
        overflow: hidden;
    }

    .section-title {
        font-family: "Inter", system-ui, sans-serif;
        font-size: 20px;
        font-weight: 600;
        color: var(--text-primary);
        letter-spacing: -0.01em;
        line-height: 1.3;
        margin: 0 0 16px 0;
        flex-shrink: 0;
    }

    .sub-container {
        width: 100%;
        min-width: 0;
        min-height: 0;
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        grid-auto-rows: minmax(0, 1fr);
        gap: 16px;
        align-items: stretch;
        overflow: hidden;
        aspect-ratio: auto;
    }

    #ranking-card:hover {
        background-color: var(--bg-elevated-hover);
    }

    #ranking-card-text {
        font-family: "Inter", system-ui, sans-serif;
        font-size: 80px;
        margin: 0;
    }
</style>
