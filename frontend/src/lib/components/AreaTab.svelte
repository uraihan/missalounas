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
          "font-bold rounded-full bg-green-400 px-3 py-2",
      )}
    >
      {area.area}
    </a>
  {/each}
</div>

<!-- {% macro area_tab(area_list, selected_area) %} -->
<!--   <div> -->
<!--     <nav class="flex gap-x-3"> -->
<!--       {% for area in area_list %}{% -->
<!--         if selected_area == -->
<!--         area.get('area') -->
<!--       %} -->
<!--         <a -->
<!--           class="p-2 inline-flex items-center bg-blue-600 text-sm -->
<!--           font-medium text-center text-white rounded-2xl focus:outline-hidden" -->
<!--           aria-current="page" -->
<!--           href="{{ url_for('index', **build_url(area=area.get('area'))) }}" -->
<!--         > -->
<!--           {{ area.get('area') }} -->
<!--         </a> -->
<!--       {% else %} -->
<!--         <a -->
<!--           class="-mb-px py-3 px-4 inline-flex items-center gap-2 -->
<!--           bg-gray-200 text-sm font-medium text-center border rounded-t-lg border-gray-200 text-gray-600 hover:text-gray-800 focus:outline-hidden focus:text-gray-600 dark:bg-neutral-700 dark:border-neutral-700 dark:text-neutral-400 dark:hover:text-neutral-200 dark:focus:text-neutral-400" -->
<!--           href="{{ url_for('index', **build_url(area=area.get('area'))) }}" -->
<!--         > -->
<!--           {{ area.get('area') }} -->
<!--         </a> -->
<!--       {% endif %}{% endfor %} -->
<!--     </nav> -->
<!--   </div> -->
<!-- {% endmacro %} -->
