<script lang="ts">
  import { goto } from "$app/navigation";
  import { page } from "$app/state";
  import type { CitiesGetCities200Item, WeeklyMenu } from "$lib/api/gen/model";
  import * as Select from "$lib/components/ui/select/index";
  import { cn } from "$lib/utils";
  import DarkModeSwitcher from "./DarkModeSwitcher.svelte";

  let {
    cities,
    menuData,
    selectedLang,
    selectedCity,
    selectedDate = $bindable(),
  }: {
    cities: CitiesGetCities200Item[];
    menuData: WeeklyMenu[];
    selectedLang: string;
    selectedCity: string;
    selectedDate: string;
  } = $props();
  const triggerCity = $derived(
    cities.find((c) => c.name === selectedCity)?.name ?? "Select a city",
  );

  // available languages
  const lang = ["EN", "FI"];
  const triggerLang = $derived(
    // TODO: replace this with system language
    lang.find((c) => c === selectedLang.toUpperCase()),
  );

  function selectQuery(query: "city" | "lang", newValue: string) {
    const params = new URLSearchParams(page.url.searchParams);
    params.set(query, query === "lang" ? newValue.toLowerCase() : newValue);

    if (query === "city") {
      params.delete("area");
    }
    goto(`?${params}`, { keepFocus: true, noScroll: true, replaceState: true });
  }
</script>

<nav class="flex justify-center lg:justify-between">
  <div class="flex flex-col sm:flex-row gap-6">
    <div class="flex items-center">
      <div class="items-center">
        <a class="text-xl sm:text-2xl xl:text-3xl" href="#">
          <strong>Missä Lounas??</strong>
        </a>
        <!-- <p class="text-center">{date}</p> -->
      </div>
    </div>

    <div class="gap-3 items-center lg:flex">
      {#each menuData as { calendar_date } (calendar_date)}
        <button
          class={cn(
            "lg:text-lg",
            calendar_date === selectedDate &&
              "font-bold rounded-full bg-green-700 px-3 py-1",
          )}
          onclick={() => (selectedDate = calendar_date)}
        >
          {new Date(calendar_date).toLocaleDateString("en-US", {
            weekday: "long",
          })}
        </button>
      {/each}
    </div>
  </div>

  <div class="flex items-center gap-6">
    <DarkModeSwitcher />
    <Select.Root
      type="single"
      name="selectedCity"
      bind:value={selectedCity}
      onValueChange={(value) => selectQuery("city", value)}
    >
      <Select.Trigger class="w-[180px]">{triggerCity}</Select.Trigger>
      <Select.Content>
        <Select.Group>
          <Select.Label>Cities</Select.Label>
          {#each cities as city}
            <Select.Item value={city.name} label={city.name}>
              {city.name}
            </Select.Item>
          {/each}
        </Select.Group>
      </Select.Content>
    </Select.Root>

    <Select.Root
      type="single"
      name="selectedLang"
      bind:value={selectedLang}
      onValueChange={(value) => selectQuery("lang", value)}
    >
      <Select.Trigger class="w-[180px]">{triggerLang}</Select.Trigger>
      <Select.Content>
        <Select.Group>
          <Select.Label>Language</Select.Label>
          {#each lang as langs}
            <Select.Item value={langs} label={langs}>
              {langs}
            </Select.Item>
          {/each}
        </Select.Group>
      </Select.Content>
    </Select.Root>
  </div>
</nav>
