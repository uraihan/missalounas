<script lang="ts">
  import { page } from "$app/state";
  import type { AreasGetAreas200Item } from "$lib/api/gen/model";
  import { cn } from "$lib/utils";

  const {
    areaList,
    initialSelectedArea,
  }: { areaList: AreasGetAreas200Item[]; initialSelectedArea: string } =
    $props();

  function selectArea(area: string): string {
    const params = new URLSearchParams(page.url.searchParams);
    params.set("area", area);
    return `/?${params}`;
  }
  let selectedArea = $derived(initialSelectedArea);
</script>

<div class="space-x-2">
  {#each areaList as area}
    <a
      href={selectArea(area.area)}
      class={cn(
        area.area === selectedArea &&
          "font-bold rounded-full bg-green-700 px-3 py-2",
      )}
    >
      {area.area}
    </a>
  {/each}
</div>
