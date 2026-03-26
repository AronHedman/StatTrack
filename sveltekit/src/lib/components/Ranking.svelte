<script>
    let artist = "";
</script>

<section id="ranking">
    <input type="text" bind:value={artist} />
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
