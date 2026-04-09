<script>
    let username = "";
    let password = "";
    let error = "";

    //lägg till en onoload function för att kolla om det finns aktiv sesison.

    async function handleLogin() {
        const res = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
        });

        const data = await res.json();

        if (data.success) {
            window.location.href = "/start"; // Skicka användaren vidare
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
            window.location.href = "/start"; // Skicka användaren vidare
        } else {
            error = data.message;
        }
    }
</script>

<div class="login-container">
    <h1>StatTrack</h1>
    <p>Ange ditt Last.fm-användarnamn för att se din statistik</p>

    <input type="text" bind:value={username} placeholder="Username..." />

    <input type="password" bind:value={password} placeholder="Password..." />

    <button on:click={handleLogin}>Log in</button>
    <button on:click={handleSignup}>Sign up</button>

    {#if error}
        <p style="color: red;">{error}</p>
    {/if}
</div>
