<script>
    let menuState = $state(false);

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
    <button
        class="reset header-title"
        onclick={() => window.location.replace("/start")}
    >
        StatTrack
    </button>

    <div class="burger-container">
        <a href="/" class="home-link" title="Home">Home</a>

        <div
            class="dropdown-wrapper"
            onmouseenter={() => (menuState = true)}
            onmouseleave={() => (menuState = false)}
            role="navigation"
        >
            {#if menuState}
                <div class="burger-content">
                    <a href="#top" class="menu-item" title="Top">Top</a>
                    <a href="/start" class="menu-item" title="Home">Home</a>
                    <a href="/ranking" class="menu-item" title="Rankings"
                        >Rankings</a
                    >

                    <button
                        id="logout"
                        class="menu-item reset"
                        onclick={logout}
                        title="Log out"
                    >
                        Log out
                    </button>
                </div>
            {/if}

            <button class="burger-toggle reset" title="Menu">
                <i class="fa fa-bars"></i>
            </button>
        </div>
    </div>
</header>

<style lang="scss">
    .reset {
        background: none;
        border: none;
        padding: 0;
        font: inherit;
        cursor: pointer;
        outline: inherit;
    }

    .header {
        width: 100%;
        height: 8vh;
        background: var(--bg-surface, #fff);
        border-bottom: 1px solid var(--border-subtle, #ccc);
        padding: 0 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-sizing: border-box;
    }

    .header-title {
        font-family: "Inter", system-ui, sans-serif;
        font-size: 20px;
        font-weight: 600;
        color: var(--text-primary, #333);
        text-shadow: 0 0 20px rgba(176, 228, 204, 0.3);
        letter-spacing: -0.01em;
        margin: 0;
    }

    .burger-container {
        display: flex;
        align-items: center;
        gap: 16px;

        .home-link {
            font-family: "Inter", system-ui, sans-serif;
            font-size: 14px;
            font-weight: 600;
            color: var(--text-primary);
            text-decoration: none;
            padding: 8px 12px;
            border-radius: 8px;
            transition: background-color 150ms ease;

            &:hover {
                background-color: var(--bg-elevated);
            }
        }

        .dropdown-wrapper {
            position: relative;
            display: flex;
            align-items: center;
        }

        .burger-toggle {
            color: var(--text-primary);
            font-size: 20px;
            padding: 8px;
            border-radius: 8px;
            transition: background-color 150ms ease;
            display: flex;
            align-items: center;
            justify-content: center;

            &:hover {
                background-color: var(--bg-elevated);
            }
        }

        .burger-content {
            position: absolute;
            top: calc(100% + 10px);
            right: 0;
            background-color: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            box-shadow: var(--shadow-card);
            min-width: 140px;
            padding: 8px;
            display: flex;
            flex-direction: column;
            gap: 4px;
            z-index: 50;

            &::before {
                content: "";
                position: absolute;
                top: -10px;
                left: 0;
                right: 0;
                height: 10px;
                background: transparent;
            }
        }
    }

    .menu-item {
        display: flex;
        align-items: center;
        width: 100%;
        padding: 10px 12px;
        border-radius: 8px;
        background: transparent;
        border-left: 2px solid transparent;
        transition: all 150ms ease;

        font-family: "Inter", system-ui, sans-serif;
        font-size: 14px;
        color: var(--text-primary);
        text-decoration: none;
        text-align: left;
        box-sizing: border-box;

        &:hover {
            background: var(--bg-elevated);
            border-left-color: var(--border-highlight);
            padding-left: 14px;
        }
    }

    #logout:hover {
        background-color: var(--alert-color, #ffebee);
        border-left-color: var(--alert-color, #f44336);
        color: var(--text-primary, #333);
    }
</style>
