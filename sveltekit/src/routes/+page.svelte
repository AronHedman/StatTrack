<script>
    let username = "";
    let error = "";

    async function handleLogin() {
        const res = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username }),
        });

        const data = await res.json();

        if (data.success) {
            window.location.href = "/start"; // Skicka användaren vidare
        } else {
            error = data.message;
        }
    }
</script>

<div class="login-container">
    <h1>StatTrack</h1>
    <p>Ange ditt Last.fm-användarnamn för att se din statistik</p>

    <input
        bind:value={username}
        placeholder="Användarnamn..."
        on:keydown={(e) => e.key === "Enter" && handleLogin()}
    />

    <button on:click={handleLogin}>Logga in</button>

    {#if error}
        <p style="color: red;">{error}</p>
    {/if}
</div>
