<script>
    import { onMount } from "svelte";

    let tracks = [];

    onMount(async () => {
        // (kan behöva en rutt som kollar session["user"]["username"])
        const res = await fetch("/api/stats");
        tracks = await res.json();

        for (const track of tracks) {
            console.log(track);
        }
    });
</script>

<h2>Dina senaste låtar</h2>
<ul>
    {#each tracks as track}
        <li>
            <strong>{track.artist}</strong> - {track.title_cleaned} - {track.title_original}
        </li>
    {/each}
</ul>
