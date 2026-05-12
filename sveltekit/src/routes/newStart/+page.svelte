<script>
    import { onMount } from "svelte";

    import Header from "$lib/components/Header.svelte";
    import Ranking from "$lib/components/Ranking.svelte";
    import LatestStreams from "$lib/components/LatestStreams.svelte";

    onMount(async () => {
        const res = await fetch("/api/me", {
            credentials: "include",
        });

        if (!res.ok) {
            window.location.replace("/login");
        }
    });
</script>

<div class="full-page">
    <Header />
    <main class="main-content">
        <div class="container">
            <!-- Main Content, add bars with artist streams, add stats for the player, like most streamed artists and songs etc -->
            <div class="content">Testdiv</div>
        </div>
    </main>
</div>

<style lang="scss">
    .full-page {
        height: 100vh;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        background: var(--bg-base);
    }

    .main-content {
        flex: 1;
        min-height: 0;
        display: flex;
        overflow: hidden;
        padding: 24px 32px;
    }

    .container {
        flex: 1;
        min-height: 0;
        display: flex;
        flex-direction: column;
        width: 100%;
        max-width: 1400px;
        margin: 0 auto;
    }

    .content {
        min-height: 0;
        overflow: hidden;
        display: flex;
        background-color: var(--bg-elevated);
    }
</style>
