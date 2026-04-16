<script>
    let { artist, onBack } = $props();

    let tracks_input = $state("");
    let tracks = $state([]);

    let debounceTimer;

    async function fetchTracks() {
        const res = await fetch(
            "/api/fetch/tracks?title=" +
                encodeURIComponent(tracks_input) +
                "&artist=" +
                encodeURIComponent(artist),
        );
        tracks = await res.json();
    }

    $effect(() => {
        if (tracks_input.length > 1) {
            clearTimeout(debounceTimer);

            debounceTimer = setTimeout(() => {
                fetchTracks();
            }, 200);
        }
    });
</script>

<section id="ranking-song">
    <div>
        <button onclick={onBack}>&larr; Back to Search</button>

        <h2>Rank your top 10 for {artist}</h2>
    </div>
    <div>
        <input type="text" bind:value={tracks_input} />

        {#if tracks}
            <div>
                <ul>
                    {#each tracks as track}
                        <li>
                            <button class="reset">
                                <strong>{track}</strong>
                            </button>
                        </li>
                    {/each}
                </ul>
            </div>
        {/if}
    </div>
</section>

<style lang="scss">
    #ranking-song {
        height: 100%;
        overflow: auto;
        padding: 2rem;
        margin: 2rem;
        border: 0.2rem solid var(--highlight-color);
        border-radius: 2rem;
        background-color: var(--prim-color);
        h2 {
            padding: 2rem;
        }
        li {
            margin: 0.5rem;
            list-style: none;

            width: fit-content;
        }
        li:hover {
            filter: brightness(1.2);
            box-shadow: inset 0 0 100px 100px rgba(255, 255, 255, 0.1);
        }
    }
</style>
