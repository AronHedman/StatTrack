<script>
    let { onSelect } = $props();

    let artist_input = $state("");
    let artists = $state([]);

    let debounceTimer;

    async function fetchArtists() {
        const res = await fetch(
            "/api/fetch/artists?artist=" + encodeURIComponent(artist_input),
        );
        artists = await res.json();
    }

    $effect(() => {
        if (artist_input.length > 1) {
            clearTimeout(debounceTimer);

            debounceTimer = setTimeout(() => {
                fetchArtists();
            }, 200);
        }
    });

    function clickArtist(artist) {
        onSelect(artist);
    }
</script>

<section id="ranking-artist">
    <input type="text" bind:value={artist_input} />

    {#if artists}
        <div>
            <ul>
                {#each artists as artist_name}
                    <li>
                        <button
                            class="reset"
                            onclick={() => clickArtist(artist_name)}
                        >
                            <strong>{artist_name}</strong>
                        </button>
                    </li>
                {/each}
            </ul>
        </div>
    {/if}
</section>

<style lang="scss">
    #ranking-artist {
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
