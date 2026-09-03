<script lang="ts">
  import type { WeeklyMenu } from "$lib/api/gen/model/weeklyMenu.js";
  import AreaTab from "$lib/components/AreaTab.svelte";
  import Navbar from "$lib/components/Navbar.svelte";
  import * as Card from "$lib/components/ui/card";

  let { data } = $props();
  let menuData: WeeklyMenu[] = $derived(data.weeklyMenu);

  // NOTE: reconsider how to deal with date and time consistently
  let selectedDate = $state(new Date().toLocaleDateString("sv-SE"));

  const dayMenu = $derived(
    menuData.find((day) => day.calendar_date === selectedDate) ?? menuData[0],
  );
</script>

<header>
  <Navbar
    cities={data.cities}
    {menuData}
    selectedCity={data.selectedCity}
    selectedLang={data.selectedLang}
    bind:selectedDate
  />
</header>

<main class="my-8 space-y-4">
  <AreaTab areaList={data.areas} initialSelectedArea={data.selectedArea} />
  <div class="grid grid-cols-4 gap-3 mt-2">
    {#if dayMenu}
      {#each dayMenu.restaurant_data as restaurant}
        <!-- each menu data is grouped per calendar day. has to be deconstructed in page.server.ts -->
        <Card.Root class="flex-1">
          <Card.Header>
            <Card.Title class="text-xl">{restaurant.restaurant_name}</Card.Title
            >
          </Card.Header>
          <Card.Content class="flex flex-col gap-4">
            {#each restaurant.menu_group_list as menu}
              <div>
                <h2 class="font-semibold">{menu.group_name}</h2>
                {#each menu.menu_item_list as menuItem}
                  <div class="flex justify-between gap-8 items-center my-1">
                    <p>{menuItem.name}</p>
                    <p class="text-end">{menuItem.diet}</p>
                  </div>
                {/each}
              </div>
            {:else}
              <p>No Menu found</p>
            {/each}
          </Card.Content>
        </Card.Root>
      {/each}
    {/if}
  </div>
</main>
