
<script>
    import { onMount } from "svelte";

    let tracks = [];

    onMount(async () => {
        const res = await fetch("/api/fetch-recent");
        tracks = await res.json();

        for (const track of tracks) {
            console.log(track);
        }
        await fetch("api/update-db");
    });
</script>

<section id="latestStreams">
    <h2>Dina senaste låtar</h2>
    <ul>
        {#each tracks as track}
            <li>
                <strong>{track.artist}</strong> - {track.title_cleaned} - {track.title_original}
            </li>
        {/each}
    </ul>
</section>

<style lang="scss">
    #latestStreams {
        height: 100%;
        overflow: auto;
        padding: 1rem;
        margin: 1rem;
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

