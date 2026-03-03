import type { PageServerLoad } from './$types';
import { getEntriesByDate, getEntriesByWeek } from '$lib/server/entries';
import { getWeekDates, getWeekOf, todayString } from '$lib/week';

export const load: PageServerLoad = async ({ url }) => {
  const date = url.searchParams.get('date') ?? todayString();
  const weekOf = getWeekOf(date);
  const weekDates = getWeekDates(date);

  const [entriesByDate, allWeekEntries] = await Promise.all([
    getEntriesByDate(date),
    getEntriesByWeek(weekOf)
  ]);

  return {
    date,
    weekOf,
    weekDates,
    entries: entriesByDate,
    allWeekEntries
  };
};
