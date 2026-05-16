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
            await fetch("/api/update-db");
        } catch (e) {
            console.error("Failed to load recent tracks:", e);
        } finally {
            isLoading = false;
        }
    });
</script>

<section class="latest-streams">
    <h2 class="section-title">Your recent tracks</h2>

    <div class="content custom-scrollbar">
        {#if isLoading}
            <div class="loading-state">Loading...</div>
        {:else if tracks.length > 0}
            <ul class="track-list">
                {#each tracks as track}
                    <li class="track-item">
                        <div class="track-info">
                            <span class="track-title"
                                >{track.title_cleaned}</span
                            >

                            {#if track.title_original !== track.title_cleaned}
                                <span class="track-original">
                                    {track.title_original}
                                </span>
                            {/if}

                            <span class="track-artist">{track.artist}</span>
                        </div>

                        {#if track.extralarge}
                            <div
                                class="track-img"
                                style={`background-image: url('${track.extralarge}')`}
                            ></div>
                        {/if}
                    </li>
                {/each}
            </ul>
        {:else}
            <div class="empty-state">No recent tracks found</div>
        {/if}
    </div>
</section>

<style lang="scss">
    .latest-streams {
        width: 100%;
        height: 100%;
        min-height: 0;
        min-width: 0;

        display: flex;
        flex-direction: column;
        gap: 16px;

        padding: 24px 24px 5px 24px;
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
        margin: 0;
        flex-shrink: 0;
    }

    .content {
        flex: 1;
        min-height: 0;
        min-width: 0;
        overflow-y: auto;
        overflow-x: hidden;
    }

    .track-list {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin: 0;
        padding: 0;
        list-style: none;
    }

    .track-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;

        padding: 10px 12px;
        border-radius: 8px;
        background: transparent;
        border-left: 2px solid transparent;
        transition: all 150ms ease;

        min-width: 0;

        font-family: "Inter", system-ui, sans-serif;
        font-size: 14px;
        line-height: 1.4;

        &:hover {
            background: var(--bg-elevated);
            border-left-color: var(--border-highlight);
            padding-left: 10px;
        }
    }

    .track-info {
        display: flex;
        flex-direction: column;
        gap: 2px;

        flex: 1;
        min-width: 0;
    }

    .track-title {
        font-weight: 700;
        color: var(--text-primary);

        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .track-original {
        color: var(--text-secondary);
        font-size: 13px;

        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .track-artist {
        color: var(--text-secondary);

        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .track-img {
        flex-shrink: 0;
        width: 48px;
        height: 48px;

        border-radius: 6px;

        background-position: center;
        background-size: cover;
        background-repeat: no-repeat;
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
