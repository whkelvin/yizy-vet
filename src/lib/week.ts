/** Get the Sunday that starts the edition week containing the given date. */
export function getWeekOf(date: string): string {
  const d = new Date(date + 'T00:00:00Z');
  const day = d.getUTCDay(); // 0=Sun, 1=Mon, ...
  d.setUTCDate(d.getUTCDate() - day);
  return d.toISOString().slice(0, 10);
}

/** Get all 7 dates (Sun–Sat) for the week containing the given date. */
export function getWeekDates(anyDateInWeek: string): string[] {
  const sunday = getWeekOf(anyDateInWeek);
  const d = new Date(sunday + 'T00:00:00Z');
  return Array.from({ length: 7 }, (_, i) => {
    const day = new Date(d);
    day.setUTCDate(d.getUTCDate() + i);
    return day.toISOString().slice(0, 10);
  });
}

/** Get today's date as YYYY-MM-DD string. */
export function todayString(): string {
  return new Date().toISOString().slice(0, 10);
}

/** Get the weekOf for the current date. */
export function getCurrentWeekOf(): string {
  return getWeekOf(todayString());
}
