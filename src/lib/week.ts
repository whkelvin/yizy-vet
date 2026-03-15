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

/** Get the weekOf for the previous week. */
export function getPrevWeekOf(weekOf: string): string {
  const d = new Date(weekOf + 'T00:00:00Z');
  d.setUTCDate(d.getUTCDate() - 7);
  return d.toISOString().slice(0, 10);
}

/** Get the weekOf for the next week. */
export function getNextWeekOf(weekOf: string): string {
  const d = new Date(weekOf + 'T00:00:00Z');
  d.setUTCDate(d.getUTCDate() + 7);
  return d.toISOString().slice(0, 10);
}

/** Format a week range as "Mar 8 – Mar 14". */
export function formatWeekRange(weekOf: string): string {
  const start = new Date(weekOf + 'T00:00:00Z');
  const end = new Date(weekOf + 'T00:00:00Z');
  end.setUTCDate(end.getUTCDate() + 6);
  const fmt = (d: Date) =>
    d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', timeZone: 'UTC' });
  return `${fmt(start)} – ${fmt(end)}`;
}
