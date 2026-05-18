<script>
    import { onMount } from "svelte";

    import Ranking from "$lib/components/Ranking.svelte";
    import Card from "$lib/components/Card.svelte";

    let rankingGlobal = $state([]);
    let userRankingsComplete = $state([]);

    async function fetchGlobalRanking() {
        const res = await fetch("/api/ranking/global", {
            credentials: "include",
        });

        if (!res.ok) return;

        rankingGlobal = await res.json();
    }

    async function fetchUserRankingsComplete() {
        const res = await fetch("/api/ranking/user/complete", {
            credentials: "include",
        });

        if (!res.ok) return;

        userRankingsComplete = await res.json();
    }

    async function updateRankingDisplay() {
        await Promise.all([fetchGlobalRanking(), fetchUserRankingsComplete()]);
    }

    onMount(async () => {
        const res = await fetch("/api/me", { credentials: "include" });

        if (!res.ok) {
            window.location.replace("/login");
            return;
        }

        await Promise.all([fetchGlobalRanking(), fetchUserRankingsComplete()]);
    });
</script>

<div class="full-page">
    <main class="main-content">
        <div class="main-container">
            <div class="left-column">
                <div class="container">
                    <Ranking {updateRankingDisplay} />
                </div>
            </div>
            <div class="right-column custom-scrollbar">
                <div class="container">
                    <h2 class="section-title">Global rankings</h2>
                    <div class="sub-container">
                        {#each rankingGlobal as song}
                            <Card
                                rank={parseFloat(song.quality_score)}
                                title1={song.title}
                                title2={song.artist_name}
                                backgroundImage={song.extralarge}
                            />
                        {/each}
                    </div>
                </div>

                {#if userRankingsComplete.length > 0}
                    {#each userRankingsComplete as artist}
                        <div class="container">
                            <h2 class="section-title">
                                {artist.artist_name}
                            </h2>
                            <div class="sub-container">
                                {#each artist.songs as song}
                                    <Card
                                        rank={"#" + song.rank}
                                        title1={song.title}
                                        title2={"Score: " +
                                            parseFloat(song.quality_score)}
                                        backgroundImage={song.extralarge}
                                    />
                                {/each}
                            </div>
                        </div>
                    {/each}
                {/if}
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
        grid-template-columns: 1fr 1fr;
        gap: 24px;
        width: 100%;

        margin: 0 auto;
    }

    .left-column {
        min-height: 0;
        min-width: 0;
        display: flex;
        flex-direction: column;
        gap: 24px;

        .container {
            flex: 1;
            min-height: 0;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            padding: 24px;
            overflow: hidden;
            border: 1px solid var(--border-subtle);
            border-radius: 20px;
            background-color: var(--bg-surface);
            box-shadow: var(--shadow-card);
        }
    }

    .right-column {
        min-height: 0;
        min-width: 0;
        display: flex;
        flex-direction: column;
        gap: 24px;
        overflow-y: auto;
        overflow-x: hidden;
        padding-right: 8px;

        .container {
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            padding: 24px;
            border: 1px solid var(--border-subtle);
            border-radius: 20px;
            background-color: var(--bg-surface);
            box-shadow: var(--shadow-card);
            flex-shrink: 0;
        }
    }

    .card {
        min-height: 0;
        overflow: hidden;
        display: flex;
        background-color: var(--bg-elevated);
        border-radius: 12px;
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
        margin: 0 0 16px 0;
    }

    .sub-container {
        flex: 1;
        min-height: 0;
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 16px;
        align-content: center;
        align-items: center;
        overflow: hidden;
    }
</style>
