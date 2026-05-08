<script>
    import { onMount } from "svelte";

    onMount(async () => {
        const res = await fetch("/api/me", {
            credentials: "include",
        });

        if (res.ok) {
            window.location.replace("/start");
        } else {
            window.location.replace("/login");
        }
    });
</script>
