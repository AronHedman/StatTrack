<script>
    import { onMount } from "svelte";

    let tracks = $state([]);
    let isLoading = $state(true);

    onMount(async () => {
        try {
            const res = await fetch("/api/fetch-recent");
            if (res.ok) {
                tracks = await res.json();
            }
            await fetch("api/update-db");
        } catch (e) {
            console.error("Failed to load recent tracks:", e);
        } finally {
            isLoading = false;
        }
    });
</script>

<section class="latest-streams">
    <h2 class="section-title">Dina senaste låtar</h2>

    {#if isLoading}
        <div class="loading-state">Loading...</div>
    {:else if tracks.length > 0}
        <ul class="track-list">
            {#each tracks as track}
                <li class="track-item">
                    <span class="track-artist">{track.artist}</span>
                    <span class="track-separator"> - </span>
                    <span class="track-title">{track.title_cleaned}</span>
                    {#if track.title_original !== track.title_cleaned}
                        <span class="track-original">
                            ({track.title_original})</span
                        >
                    {/if}
                </li>
            {/each}
        </ul>
    {:else}
        <div class="empty-state">No recent tracks found</div>
    {/if}
</section>

<style lang="scss">
    .latest-streams {
        height: 100%;
        min-height: 0;

        display: flex;
        flex-direction: column;

        padding: 24px;
        border: 1px solid var(--border-subtle);
        border-radius: 20px;
        background-color: var(--bg-surface);
        box-shadow: var(--shadow-card);
    }

    .section-title {
        font-family: "Inter", system-ui, sans-serif;
        font-size: 20px;
        font-weight: 600;
        color: var(--text-primary);
        letter-spacing: -0.01em;
        line-height: 1.3;
        margin-bottom: 16px;
        flex-shrink: 0;
    }

    .track-list {
        flex: 1;
        min-height: 0;
        overflow-y: auto;
    }

    .track-item {
        padding: 10px 12px;
        border-radius: 6px;
        background: transparent;
        border-left: 2px solid transparent;
        transition: all 150ms ease;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        font-family: "Inter", system-ui, sans-serif;
        font-size: 14px;
        line-height: 1.5;

        &:hover {
            background: var(--bg-elevated);
            border-left-color: var(--border-highlight);
            padding-left: 10px;
        }
    }

    .track-artist {
        font-weight: 700;
        color: var(--text-primary);
    }

    .track-separator {
        color: var(--text-secondary);
    }

    .track-title {
        color: var(--text-primary);
    }

    .track-original {
        color: var(--text-secondary);
    }

    .loading-state,
    .empty-state {
        font-family: "Inter", system-ui, sans-serif;
        font-size: 14px;
        color: var(--text-secondary);
        text-align: center;
        padding: 32px 0;
    }
</style>
