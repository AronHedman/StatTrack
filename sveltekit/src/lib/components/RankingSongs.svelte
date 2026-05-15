<script>
    import { onMount } from "svelte";
    import RankingDisplay from "$lib/components/RankingDisplay.svelte";

    let { artist, onBack } = $props();

    let tracks_input = $state("");
    let tracks = $state([]);
    let selectedTrack = $state(null);
    let rankedTracks = $state(Array(10).fill(null));
    let fetchedAll = $state(false);
    let isSubmitting = $state(false);

    async function fetchTracks() {
        const res = await fetch(
            "/api/fetch/tracks?title=" +
                encodeURIComponent(tracks_input) +
                "&artist_id=" +
                encodeURIComponent(artist.artist_id),
            {
                credentials: "include",
            },
        );
        tracks = await res.json();
    }

    async function fetchAllTracks() {
        const res = await fetch(
            "/api/fetch/tracks?artist_id=" +
                encodeURIComponent(artist.artist_id),
            {
                credentials: "include",
            },
        );
        tracks = await res.json();
    }

    async function loadExistingRanking() {
        const res1 = await fetch(
            "/api/fetch/artists?artist=" + encodeURIComponent(artist),
            {
                credentials: "include",
            },
        );

        if (!res1.ok) return;

        const artist_ids = await res1.json();
        const artist_id = artist_ids[0];

        if (!artist_id) return;

        const res2 = await fetch("/api/ranking/user?artist_id=" + artist_id, {
            credentials: "include",
        });

        if (!res2.ok) return;

        const data = await res2.json();

        rankedTracks = Array(10).fill(null);

        for (const track of data) {
            const index = track.rank - 1;
            if (index >= 0 && index < 10) {
                rankedTracks[index] = track;
            }
        }
    }

    function assignSlot(i) {
        if (selectedTrack) {
            rankedTracks = rankedTracks.map((track) =>
                track && track.song_id === selectedTrack.song_id ? null : track,
            );
            rankedTracks[i] = selectedTrack;
            selectedTrack = null;
        } else {
            rankedTracks[i] = null;
        }
    }

    function selectTrack(track) {
        if (selectedTrack && selectedTrack.song_id === track.song_id) {
            selectedTrack = null;
        } else {
            selectedTrack = track;
        }
    }

    async function sendRanking() {
        isSubmitting = true;
        const rankings = [];

        for (let i = 0; i < rankedTracks.length; i++) {
            if (rankedTracks[i]) {
                rankings.push({
                    song_id: rankedTracks[i].song_id,
                    rank: i + 1,
                });
            }
        }

        const res = await fetch(
            "/api/fetch/artists?artist=" +
                encodeURIComponent(artist.artist_name),
            {
                credentials: "include",
            },
        );
        const results = await res.json();
        const artist_id = results[0].artist_id;

        fetch("/api/ranking/user", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                artist_id: artist_id,
                rankings: rankings,
            }),
            credentials: "include",
        })
            .then((res) => res.json())
            .then((data) => {
                isSubmitting = false;
                alert("Ranking submitted successfully!");
            })
            .catch((err) => {
                isSubmitting = false;
                console.error(err);
            });
    }

    $effect(() => {
        if (tracks_input.trim() === "") {
            if (!fetchedAll) {
                fetchAllTracks();
                fetchedAll = true;
            }
            return;
        }
        const timer = setTimeout(() => {
            fetchTracks();
            fetchedAll = false;
        }, 200);
        return () => clearTimeout(timer);
    });

    onMount(() => {
        loadExistingRanking();
    });
</script>

<section class="ranking-song">
    <div class="header-row">
        <button class="back-button" onclick={onBack}>
            &larr; Back to Search
        </button>
        <h2 class="section-title">Rank your top 10 for {artist.artist_name}</h2>
    </div>

    <div class="track-search">
        <input
            type="text"
            bind:value={tracks_input}
            placeholder="Filter songs..."
            class="track-input"
        />

        {#if tracks && tracks.length > 0}
            <div class="track-list custom-scrollbar">
                <ul>
                    {#each tracks as track}
                        <li
                            class="track-item"
                            class:selected={selectedTrack &&
                                selectedTrack.song_id === track.song_id}
                        >
                            <button
                                class="reset track-button"
                                onclick={() => selectTrack(track)}
                            >
                                {#if track.small || track.medium}
                                    <img
                                        src={track.small || track.medium}
                                        alt=""
                                        class="track-thumb"
                                    />
                                {/if}
                                <span class="track-name">{track.title}</span>
                            </button>
                        </li>
                    {/each}
                </ul>
            </div>
        {/if}
    </div>

    <div class="ranking-grid">
        {#each rankedTracks as currentTrack, i}
            <div
                class="grid-slot animate-fade-in-up"
                style="animation-delay: {i * 50}ms"
            >
                <RankingDisplay
                    place={i + 1}
                    track={currentTrack}
                    onclick={() => assignSlot(i)}
                    isSelectedSlot={selectedTrack !== null &&
                        currentTrack === null}
                />
            </div>
        {/each}
    </div>

    <div class="submit-row">
        <button
            class="submit-button"
            onclick={() => sendRanking()}
            disabled={isSubmitting}
        >
            {isSubmitting ? "Submitting..." : "Send ranking"}
        </button>
    </div>
</section>

<style lang="scss">
    .ranking-song {
        flex: 1;
        min-height: 0;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }

    .header-row {
        margin-bottom: 16px;
    }

    .back-button {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-family: "Inter", system-ui, sans-serif;
        font-size: 12px;
        font-weight: 500;
        color: var(--text-secondary);
        background: transparent;
        border: 1px solid var(--border-subtle);
        border-radius: 9999px;
        padding: 8px 16px;
        cursor: pointer;
        transition: all 150ms ease;
        margin-bottom: 16px;

        &:hover {
            color: var(--text-accent);
            border-color: var(--border-highlight-dim);
            background: rgba(176, 228, 204, 0.05);
        }

        &:active {
            transform: scale(0.98);
        }
    }

    .section-title {
        font-family: "Inter", system-ui, sans-serif;
        font-size: 20px;
        font-weight: 600;
        color: var(--text-primary);
        letter-spacing: -0.01em;
        line-height: 1.3;
    }

    .track-search {
        flex-shrink: 0;
        margin-bottom: 16px;
    }

    .track-input {
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
        margin-bottom: 12px;

        &::placeholder {
            color: var(--text-secondary);
        }

        &:focus {
            border-color: var(--border-highlight);
            box-shadow: 0 0 0 3px rgba(176, 228, 204, 0.15);
        }
    }

    .track-list {
        max-height: 240px;
        overflow-y: auto;
        border-radius: 12px;
        background: var(--bg-elevated);
        border: 1px solid var(--border-subtle);

        ul {
            list-style: none;
            padding: 4px;
        }
    }

    .track-item {
        border-radius: 8px;
        overflow: hidden;
        transition: all 150ms ease;

        &:hover {
            background: var(--bg-surface-hover);
        }

        &.selected {
            background: rgba(176, 228, 204, 0.08);
            border-left: 2px solid var(--border-highlight);
        }
    }

    .track-button {
        display: flex;
        align-items: center;
        gap: 8px;
        width: 100%;
        padding: 10px 12px;
        cursor: pointer;
        border-radius: 8px;
        transition: all 150ms ease;
    }

    .track-thumb {
        width: 32px;
        height: 32px;
        border-radius: 4px;
        object-fit: cover;
        flex-shrink: 0;
    }

    .track-name {
        font-family: "Inter", system-ui, sans-serif;
        font-size: 14px;
        font-weight: 500;
        color: var(--text-primary);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .ranking-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        grid-template-rows: repeat(2, 1fr);
        gap: 12px;
        padding: 16px 0;
        margin-top: auto;
    }

    .grid-slot {
        opacity: 0;
        animation-fill-mode: forwards;
    }

    .submit-row {
        margin-top: 16px;
    }

    .submit-button {
        width: 100%;
        height: 48px;
        background: var(--border-highlight);
        color: var(--bg-base);
        font-family: "Inter", system-ui, sans-serif;
        font-size: 14px;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        cursor: pointer;
        transition: all 200ms ease;

        &:hover:not(:disabled) {
            background: #c5ebd8;
            box-shadow: var(--shadow-glow);
            transform: translateY(-1px);
        }

        &:active:not(:disabled) {
            transform: scale(0.98);
        }

        &:disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }
    }

    @media (max-width: 1023px) {
        .ranking-grid {
            grid-template-columns: repeat(3, 1fr);
            grid-template-rows: repeat(4, 1fr);
            flex: 1;
            min-height: 0;
        }
    }

    @media (max-width: 767px) {
        .ranking-grid {
            grid-template-columns: repeat(2, 1fr);
            grid-template-rows: repeat(5, 1fr);
            gap: 8px;
            flex: 1;
            min-height: 0;
        }

        .ranking-song {
            padding: 16px;
        }
    }
</style>
