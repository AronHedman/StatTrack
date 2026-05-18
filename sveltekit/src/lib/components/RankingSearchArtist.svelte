<script>
    let { onSelect } = $props();

    let artist_input = $state("");
    let artists = $state([]);
    let debounceTimer;
    let isLoading = $state(false);

    async function fetchArtists() {
        if (!artist_input.trim()) {
            artists = [];
            return;
        }
        isLoading = true;
        try {
            const res = await fetch(
                "/api/fetch/artists?artist=" + encodeURIComponent(artist_input),
                {
                    credentials: "include",
                },
            );
            if (res.ok) {
                artists = await res.json();
            }
        } catch (e) {
            console.error("Failed to fetch artists:", e);
        } finally {
            isLoading = false;
        }
    }

    $effect(() => {
        if (artist_input.length > 1) {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                fetchArtists();
            }, 200);
        } else {
            artists = [];
        }
    });

    function clickArtist(artist) {
        onSelect(artist);
    }
</script>

<section class="ranking-artist">
    <div class="search-wrapper">
        <input
            type="text"
            bind:value={artist_input}
            placeholder="Search for an artist"
            class="search-input"
        />
    </div>

    <div class="results-container custom-scrollbar">
        {#if isLoading}
            <div class="loading-state">Searching...</div>
        {:else if artists.length > 0}
            <ul class="artist-list">
                {#each artists as artist}
                    <li class="artist-item">
                        <button
                            class="reset artist-button"
                            onclick={() => clickArtist(artist)}
                        >
                            <span class="artist-name"
                                >{artist.artist_name}
                            </span>
                            <span class="arrow">&rarr;</span>
                        </button>
                    </li>
                {/each}
            </ul>
        {:else if artist_input.length > 1}
            <div class="empty-state">No artists found</div>
        {:else}
            <div class="empty-state">Start typing to search for artists</div>
        {/if}
    </div>
</section>

<style lang="scss">
    .ranking-artist {
        width: 100%;
        height: 100%;
        min-height: 0;
        min-width: 0;
        display: flex;
        flex-direction: column;
        gap: 16px;
    }

    .search-wrapper {
        flex-shrink: 0;
    }

    .search-input {
        width: 100%;
        height: 48px;
        background: var(--bg-elevated);
        border: 1px solid var(--border-subtle);
        border-radius: 12px;
        padding: 0 16px;
        font-family: "Inter", system-ui, sans-serif;
        font-size: 14px;
        color: var(--text-primary);
        outline: none;
        transition: all 200ms ease;
        box-sizing: border-box;

        &::placeholder {
            color: var(--text-secondary);
        }

        &:focus {
            border-color: var(--border-highlight);
            box-shadow: 0 0 0 3px rgba(176, 228, 204, 0.15);
        }
    }

    .results-container {
        flex: 1;
        min-height: 0;
        min-width: 0;
        overflow-y: auto;
        overflow-x: hidden;
    }

    .artist-list {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin: 0;
        padding: 0;
        list-style: none;
    }

    .artist-item {
        min-width: 0;
    }

    .artist-button {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;

        width: 100%;
        padding: 10px 12px;
        border-radius: 8px;
        background: transparent;
        border: none;
        border-left: 2px solid transparent;
        transition: all 150ms ease;
        cursor: pointer;

        font-family: "Inter", system-ui, sans-serif;
        font-size: 14px;
        line-height: 1.4;
        box-sizing: border-box;
        text-align: left;

        &:hover {
            background: var(--bg-elevated);
            border-left-color: var(--border-highlight);
            padding-left: 10px;

            .arrow {
                color: var(--text-primary);
                transform: translateX(4px);
            }
        }
    }

    .artist-name {
        font-weight: 700;
        color: var(--text-primary);

        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .arrow {
        color: var(--text-secondary);
        font-size: 16px;
        transition: all 150ms ease;
        flex-shrink: 0;
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
