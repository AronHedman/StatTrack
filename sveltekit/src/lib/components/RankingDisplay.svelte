<script>
    let { place, track, onclick, isSelectedSlot = false } = $props();

    function getBackgroundImage(t) {
        if (!t) return "";
        return t.extralarge || t.large || t.medium || t.small || "";
    }
</script>

<button
    id="ranking-display-card"
    class="reset"
    class:has-track={track}
    class:empty={!track}
    class:selected-slot={isSelectedSlot}
    {onclick}
>
    {#if getBackgroundImage(track)}
        <div
            class="album-bg"
            style="background-image: url({getBackgroundImage(track)});"
        ></div>
    {/if}
    <div class="gradient-overlay"></div>
    <div class="content">
        <h3 class="rank">#{place}</h3>
        {#if track}
            <p class="track-title">{track.title}</p>
        {:else}
            <p class="track-title empty-title">No track</p>
        {/if}
    </div>
</button>

<style lang="scss">
    #ranking-display-card {
        position: relative;
        aspect-ratio: 1 / 1;
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid var(--border-subtle);
        cursor: pointer;
        background: var(--bg-elevated);
        transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
        padding: 0;
        display: block;
        width: 100%;

        &:hover {
            border-color: var(--border-highlight);
            box-shadow: var(--shadow-glow);
            transform: scale(1.02);
        }

        &:active {
            transform: scale(0.98);
        }

        &.empty:hover {
            border-color: var(--border-highlight-dim);
            box-shadow: none;
        }

        &.selected-slot {
            border: 2px solid var(--border-highlight);
            box-shadow: 0 0 0 4px rgba(176, 228, 204, 0.2);
            animation: pulse-highlight 2s ease-in-out infinite;
        }
    }

    .album-bg {
        position: absolute;
        inset: 0;
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        z-index: 1;
    }

    .gradient-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(
            to top,
            rgba(10, 10, 10, 0.95) 0%,
            rgba(10, 10, 10, 0.8) 30%,
            rgba(10, 10, 10, 0.5) 55%,
            rgba(10, 10, 10, 0.2) 75%,
            transparent 100%
        );
        z-index: 2;
    }

    .content {
        position: relative;
        z-index: 3;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        height: 100%;
        padding: 16px;
    }

    .rank {
        position: absolute;
        top: 12px;
        left: 12px;
        font-family: "Inter", system-ui, sans-serif;
        font-size: 32px;
        font-weight: 800;
        color: var(--text-primary);
        text-shadow:
            0 2px 8px rgba(0, 0, 0, 0.9),
            0 0 4px rgba(0, 0, 0, 0.7);
        line-height: 1;
        letter-spacing: -0.03em;
    }

    .track-title {
        font-family: "Inter", system-ui, sans-serif;
        font-size: 14px;
        font-weight: 600;
        color: var(--text-primary);
        line-height: 1.3;
        text-shadow:
            0 1px 4px rgba(0, 0, 0, 1),
            0 2px 8px rgba(0, 0, 0, 0.8);
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        word-break: break-word;
    }

    .empty-title {
        color: var(--text-secondary);
        font-style: italic;
        font-weight: 400;
    }
</style>
