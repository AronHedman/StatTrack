<script>
    let menuState = $state(false);

    function toggleMenu() {
        menuState = !menuState;
    }

    async function logout() {
        await fetch("/api/logout", {
            method: "POST",
            credentials: "include",
        });

        window.location.replace("/login");
    }
</script>

<svelte:head>
    <link
        rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
    />
</svelte:head>

<header class="header">
    <h1 class="header-title">StatTrack</h1>

    <div class="burger-container">
        <a href="/" class="active" title="Home">Hem</a>

        {#if menuState}
            <div class="burger-content">
                <a href="#top" title="New Start">Top</a>
                <a
                    id="logout"
                    href="javascript:void(0);"
                    onclick={logout}
                    title="Log out">Log out</a
                >
            </div>
        {/if}

        <a
            href="javascript:void(0);"
            class="icon"
            onclick={toggleMenu}
            title="Burger?"
        >
            <!-- javascript:void() prevents default href action-->
            <i class="fa fa-bars"></i>
        </a>
    </div>
</header>

<style lang="scss">
    .header {
        width: 100%;
        height: 64px;
        background: var(--bg-surface, #fff);
        border-bottom: 1px solid var(--border-subtle, #ccc);
        padding: 0 32px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .header-title {
        font-family: "Inter", system-ui, sans-serif;
        font-size: 20px;
        font-weight: 700;
        color: var(--text-accent, #333);
        text-shadow: 0 0 20px rgba(176, 228, 204, 0.3);
        letter-spacing: -0.01em;
        margin: 0;
    }

    .burger-container {
        background-color: var(--bg-surface);
        position: relative;
        display: flex;

        .burger-content {
            position: absolute;
            top: 100%;
            right: 0;
            background-color: var(--bg-base);
            min-width: 120px;
        }

        a {
            color: white;
            padding: 14px 16px;
            text-decoration: none;
            font-size: 17px;
            display: block;

            &.icon {
                background: var(--bg-base);
                display: block;
            }

            &:hover {
                background-color: var(--bg-surface-hover);
                color: var(--text-primary);
            }
        }
    }

    #logout:hover {
        background-color: var(--alert-color);
    }

    .active {
        background-color: var(--bg-base);
        color: var(--text-accent);
    }
</style>
