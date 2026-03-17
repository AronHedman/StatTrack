<script>
    import { onMount } from "svelte";

    let tracks = [];

    onMount(async () => {
        // Vi hämtar statistik för den inloggade användaren
        // (Du kan behöva en rutt som kollar session["user"]["username"])
        const res = await fetch("/api/stats");
        tracks = await res.json();

        console.log(tracks);
    });
</script>

<h2>Dina senaste låtar</h2>
<ul>
    {#each tracks as track}
        <li>
            <strong>{track.artist["#text"]}</strong> - {track.name}
        </li>
    {/each}
</ul>
