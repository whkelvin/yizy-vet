import type { PageServerLoad } from './$types';
import { getEntriesByWeek } from '$lib/server/entries';
import { getWeeklyMetaCollection } from '$lib/server/collections';
import { getCurrentWeekOf } from '$lib/week';
import type { WeeklyMeta } from '$lib/types';

export const load: PageServerLoad = async ({ url }) => {
  const weekOf = url.searchParams.get('weekOf') ?? getCurrentWeekOf();

  // Load all entries for the week (client filters by status)
  const [entries, metaCol] = await Promise.all([
    getEntriesByWeek(weekOf),
    getWeeklyMetaCollection()
  ]);

  const metaDoc = await metaCol.findOne({ weekOf });

  const meta: WeeklyMeta = {
    weekOf,
    kelvinsPick: metaDoc?.kelvinsPick ?? null
  };

  return { weekOf, entries, meta };
};
