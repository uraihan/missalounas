import { areasGetAreas, menuGetMenu } from "$lib/api/gen/default.ts";
import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ url }) => {
  // TODO: change these to be aware of client's geolocation
  const city = url.searchParams.get("city") ?? "Tampere";
  const area = url.searchParams.get("area") ?? "Hervanta";
  const lang = url.searchParams.get("lang") ?? "en";

  const menuResp = await menuGetMenu({ city, area, lang });
  if (menuResp.status !== 200) {
    throw error(menuResp.status, "Failed to load menu");
  }
  const areaData = await areasGetAreas({ city });
  if (areaData.status !== 200) {
    throw error(areaData.status, "Failed to load areas");
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
