<script>
    let username = "";
    let password = "";
    let error = "";

    async function handleLogin() {
        const res = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
        });

        const data = await res.json();

        if (data.success) {
            window.location.href = "/start";
        } else {
            error = data.message;
        }
    }

    async function handleSignup() {
        const res = await fetch("/api/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
        });

        const data = await res.json();

        if (data.success) {
            window.location.href = "/start";
        } else {
            error = data.message;
        }
    }
</script>

<section class="login-wrapper">
    <div class="login-card">
        <h1 class="title">StatTrack</h1>
        <p class="subtitle">
            Ange ditt Last.fm-användarnamn för att se din statistik
        </p>

        <div class="form">
            <input
                type="text"
                bind:value={username}
                placeholder="Username..."
                class="input"
            />

            <input
                type="password"
                bind:value={password}
                placeholder="Password..."
                class="input"
            />

            <div class="button-group">
                <button class="btn primary" onclick={handleLogin}>
                    Log in
                </button>
                <button class="btn secondary" onclick={handleSignup}>
                    Sign up
                </button>
            </div>

            {#if error}
                <p class="error">{error}</p>
            {/if}
        </div>
    </div>
</section>

<style lang="scss">
    .login-wrapper {
        height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--bg-base);
        padding: 24px;
    }

    .login-card {
        width: 100%;
        max-width: 400px;
        padding: 32px;
        border: 1px solid var(--border-subtle);
        border-radius: 20px;
        background-color: var(--bg-surface);
        box-shadow: var(--shadow-card);
        display: flex;
        flex-direction: column;
        gap: 16px;
    }

    .title {
        font-family: "Inter", system-ui, sans-serif;
        font-size: 24px;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.02em;
    }

    .subtitle {
        font-family: "Inter", system-ui, sans-serif;
        font-size: 14px;
        color: var(--text-secondary);
        line-height: 1.5;
        margin-bottom: 8px;
    }

    .form {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }

    .input {
        width: 100%;
        height: 44px;
        background: var(--bg-elevated);
        border: 1px solid var(--border-subtle);
        border-radius: 10px;
        padding: 0 12px;
        font-family: "Inter", system-ui, sans-serif;
        font-size: 14px;
        color: var(--text-primary);
        outline: none;
        transition: all 150ms ease;

        &::placeholder {
            color: var(--text-secondary);
        }

        &:focus {
            border-color: var(--border-highlight);
            box-shadow: 0 0 0 3px rgba(176, 228, 204, 0.15);
        }
    }

    .button-group {
        display: flex;
        gap: 8px;
        margin-top: 8px;
    }

    .btn {
        flex: 1;
        height: 42px;
        border-radius: 10px;
        font-family: "Inter", system-ui, sans-serif;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        transition: all 150ms ease;
        border: 1px solid transparent;
    }

    .btn.primary {
        background: var(--bg-elevated);
        color: var(--text-primary);

        &:hover {
            background: var(--bg-surface-hover);
            border-color: var(--border-subtle);
        }
    }

    .btn.secondary {
        background: transparent;
        color: var(--text-secondary);
        border: 1px solid var(--border-subtle);

        &:hover {
            background: var(--bg-surface-hover);
            color: var(--text-primary);
        }
    }

    .error {
        font-family: "Inter", system-ui, sans-serif;
        font-size: 13px;
        color: #ff6b6b;
        text-align: center;
        margin-top: 4px;
    }
</style>
