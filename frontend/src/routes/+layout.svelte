<script lang="ts">
  import "./layout.css";
  import favicon from "$lib/assets/favicon.svg";

  let { children } = $props();
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
  <title>Missä Lounas?</title>
</svelte:head>

<main>
  {@render children()}
</main>

<style>
  main {
    margin-inline: 10%;
  }
</style>
