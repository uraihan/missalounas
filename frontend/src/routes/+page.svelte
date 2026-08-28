<script lang="ts">
  import { menuGetMenu } from "$lib/api/gen/default";
  import Navbar from "$lib/components/components/Navbar.svelte";
  import * as Card from "$lib/components/ui/card";

  let { data } = $props();

  console.log(data);
</script>

<header>
  <Navbar />
</header>
<main>
  <Card.Root>
    <Card.Header>
      <Card.Title>Restaurant Name</Card.Title>
    </Card.Header>
  </Card.Root>
</main>
