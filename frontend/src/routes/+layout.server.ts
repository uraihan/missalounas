import { citiesGetCities } from "$lib/api/gen/default.ts";
import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async () => {
  const { data: cities } = await citiesGetCities();
  return { cities };
};
