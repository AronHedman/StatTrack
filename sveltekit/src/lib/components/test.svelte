<script>
    let user_input = $state("");

    let debounceTimer;

    let users = $state([]);

    async function userSearch() {
        if (!user_input.trim()) {
            artists = [];
            return;
        }
        try {
            const res = await fetch(
                "/api/userSearch?param=" + encodeURIComponent(user_input),
                {
                    credentials: "include",
                },
            );
            if (res.ok) {
                users = await res.json();
            }
        } catch (e) {
            console.error("Failed to fetch:", e);
        }
    }

    $effect(() => {
        if (user_input.length > 1) {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                userSearch();
            }, 200);
        } else {
            users = [];
        }
    });
</script>

<input type="text" bind:value={user_input} />

{#each users as user}
    <p>{user.username}</p>
    <p>{user.user_id}</p>
{/each}
