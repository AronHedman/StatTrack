<script>
    let artist = $state("");
    let tracks = $state([]);

    async function fetchTracks() {
        const res = await fetch(
            "/api/fetch-tracks?artist=" + encodeURIComponent(artist),
        );
        tracks = await res.json();

        for (const track of tracks) {
            console.log(track);
        }
    }

    $effect(() => {
        if (artist.length > 3) {
            fetchTracks();
        }
    });
</script>

<section id="ranking">
    <input type="text" bind:value={artist} />

    {#if tracks}
        <ul>
            {#each tracks as title}
                <li>
                    <strong>{title}</strong>
                </li>
            {/each}
        </ul>
    {/if}
</section>

<style lang="scss">
    #ranking {
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
        }
    }
</style>
