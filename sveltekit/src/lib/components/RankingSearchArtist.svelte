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
                "/api/fetch/artists/names?artist=" +
                    encodeURIComponent(artist_input),
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
            placeholder="Search for an artist..."
            class="search-input"
        />
    </div>

    {#if isLoading}
        <div class="empty-state">
            <span class="loading-text">Searching...</span>
        </div>
    {:else if artists.length > 0}
        <div class="results-container">
            <ul class="artist-list">
                {#each artists as artist_name}
                    <li class="artist-item">
                        <button
                            class="reset artist-button"
                            onclick={() => clickArtist(artist_name)}
                        >
                            <span class="artist-name">{artist_name}</span>
                            <span class="arrow">&rarr;</span>
                        </button>
                    </li>
                {/each}
            </ul>
        </div>
    {:else if artist_input.length > 1}
        <div class="empty-state">
            <span>No artists found</span>
        </div>
    {:else}
        <div class="empty-state">
            <span>Start typing to search for artists</span>
        </div>
    {/if}
</section>

<style lang="scss">
    .ranking-artist {
        height: 100%;
        min-height: 0;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }

    .search-wrapper {
        margin-bottom: 16px;
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

        &::placeholder {
            color: var(--text-secondary);
        }

        &:focus {
            border-color: var(--border-highlight);
            box-shadow: 0 0 0 3px rgba(176, 228, 204, 0.15);
        }
    }

    .results-container {
        margin-top: 8px;
    }

    .artist-list {
        list-style: none;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }

    .artist-item {
        border-radius: 12px;
        overflow: hidden;
    }

    .artist-button {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        padding: 14px 16px;
        background: transparent;
        border: 1px solid transparent;
        border-radius: 12px;
        transition: all 150ms ease;
        cursor: pointer;

        &:hover {
            background: var(--bg-surface-hover);
            border-color: var(--border-subtle);
            transform: translateX(4px);

            .arrow {
                color: var(--text-accent);
            }
        }
    }

    .artist-name {
        font-family: "Inter", system-ui, sans-serif;
        font-size: 14px;
        font-weight: 600;
        color: var(--text-primary);
    }

    .arrow {
        font-family: "Inter", system-ui, sans-serif;
        font-size: 14px;
        color: var(--text-secondary);
        transition: color 150ms ease;
    }

    .empty-state {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 48px;
        font-family: "Inter", system-ui, sans-serif;
        font-size: 14px;
        color: var(--text-secondary);
    }

    .loading-text {
        color: var(--text-accent);
    }
</style>
