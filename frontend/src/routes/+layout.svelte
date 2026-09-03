<script lang="ts">
  import "./layout.css";
  import favicon from "$lib/assets/favicon.svg";
  import { ModeWatcher } from "mode-watcher";

  let { children } = $props();
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
  <title>Missä Lounas?</title>
</svelte:head>

<ModeWatcher />
<main>
  {@render children()}
</main>

<style>
  main {
    margin-inline: 5%;
    margin-block: 1.25rem;
  }
</style>
