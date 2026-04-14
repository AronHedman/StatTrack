<script>
    let { onSelect } = $props();

    let artist = $state("");
    let tracks = $state([]);

    async function fetchTracks() {
        const res = await fetch(
            "/api/fetch-tracks?artist=" + encodeURIComponent(artist),
        );
        tracks = await res.json();

        // for (const track of tracks) {
        // console.log("track: " + track);
        // }
    }

    $effect(() => {
        if (artist.length > 1) {
            fetchTracks();
        }
    });

    function clickArtist(artist) {
        // This updates 'selectedArtist' in the parent, triggering the UI switch
        onSelect(artist);
    }
</script>

<section id="ranking-artist">
    <input type="text" bind:value={artist} />

    {#if tracks}
        <div>
            <ul>
                {#each tracks as title}
                    <li>
                        <button
                            class="reset"
                            onclick={() => clickArtist(artist)}
                        >
                            <strong>{title}</strong>
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
