import type { EntryDocument, WeeklyMetaDocument } from '$lib/types';
import { getDb } from './db';

export async function getEntriesCollection() {
  const db = await getDb();
  return db.collection<EntryDocument>('entries');
}

export async function getWeeklyMetaCollection() {
  const db = await getDb();
  return db.collection<WeeklyMetaDocument>('weekly_meta');
}

/** Ensure indexes exist. Call once on startup. */
export async function ensureIndexes() {
  const entries = await getEntriesCollection();
  await entries.createIndex({ kind: 1, url: 1 }, { unique: true });
  await entries.createIndex({ weekOf: 1, status: 1 });
  await entries.createIndex({ date: 1, status: 1 });

  const meta = await getWeeklyMetaCollection();
  await meta.createIndex({ weekOf: 1 }, { unique: true });
}
