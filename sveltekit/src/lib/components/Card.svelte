<script>
    let { title1, title2, backgroundImage = "", info = "" } = $props();

    function getBackgroundImage() {
        return backgroundImage || "";
    }
</script>

<div class="card">
    {#if getBackgroundImage()}
        <div
            class="card-bg"
            style={`background-image: url("${getBackgroundImage()}")`}
        ></div>
    {/if}

    <div class="gradient-overlay"></div>

    <div class="card-content">
        <h1 class="card-title">{title1}</h1>
        <h2 class="card-subtitle">
            {#if info !== ""}
                {title2 + " - " + info}
            {:else}
                {title2}
            {/if}
        </h2>
    </div>
</div>

<style lang="scss">
    .card {
        position: relative;
        min-height: 0;
        width: 100%;
        height: 100%;
        aspect-ratio: 1 / 1;
        overflow: hidden;
        border-radius: 16px;
        border: 1px solid var(--border-subtle);
        background: var(--bg-elevated);
    }

    .card-bg {
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
        z-index: 2;
        background: linear-gradient(
            to top,
            rgba(10, 10, 10, 0.95) 0%,
            rgba(10, 10, 10, 0.8) 30%,
            rgba(10, 10, 10, 0.5) 55%,
            rgba(10, 10, 10, 0.2) 75%,
            transparent 100%
        );
    }

    .card-content {
        position: relative;
        z-index: 3;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        padding: 16px;
        box-sizing: border-box;
    }

    .card-title {
        margin: 0;
        font-family: "Inter", system-ui, sans-serif;
        font-size: 18px;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1.2;
        text-shadow:
            0 2px 8px rgba(0, 0, 0, 0.9),
            0 0 4px rgba(0, 0, 0, 0.7);
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        word-break: break-word;
    }

    .card-subtitle {
        margin: 6px 0 0;
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
</style>
