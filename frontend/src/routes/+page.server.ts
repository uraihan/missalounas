import { menuGetMenu } from "$lib/api/gen/default.ts";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params }) => {
  const menuData = await menuGetMenu({
    day: "monday",
    city: "Tampere",
    area: "Keskusta",
    lang: "fi",
  });

  return { data: menuData.data };
};
