import { areasGetAreas, menuGetMenu } from "$lib/api/gen/default.ts";
import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
import type { City } from "$lib/api/gen/model/city.ts";

export const load: PageServerLoad = async ({ url, parent }) => {
  // TODO: change these to be aware of client's geolocation
  const city = url.searchParams.get("city") ?? "Tampere";
  const lang = url.searchParams.get("lang") ?? "en";

  const areaData = await areasGetAreas({ city });
  if (areaData.status !== 200) {
    throw error(areaData.status, "Failed to load areas");
  }

  const { cities }: { cities: City[] } = await parent();
  const cityInfo = cities.find((c) => c.name === city);
  const area = url.searchParams.get("area") ?? cityInfo?.default_area;

  const menuResp = await menuGetMenu({ city, area, lang });
  if (menuResp.status !== 200) {
    throw error(menuResp.status, "Failed to load menu");
  }

  const menuData = menuResp.data.map((day) => ({
    ...day,
    calendar_date: day.calendar_date.slice(0, 10),
  }));

  return {
    areas: areaData.data,
    weeklyMenu: menuData,
    selectedCity: city,
    selectedArea: area,
    selectedLang: lang,
  };
};
