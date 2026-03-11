import { ObjectId } from 'mongodb';
import type { Entry, EntryDocument } from '$lib/types';
import { getEntriesCollection } from './collections';

/** Serialize a MongoDB document to a client-safe Entry. */
function serialize(doc: EntryDocument): Entry {
  return {
    _id: doc._id.toHexString(),
    kind: doc.kind,
    title: doc.title,
    url: doc.url,
    date: doc.date,
    weekOf: doc.weekOf,
    status: doc.status,
    kelvinsPick: doc.kelvinsPick ?? false,
    why: '',
    description: '',
    youtubeId: doc.youtubeId,
    spotifyEmbedUrl: doc.spotifyEmbedUrl,
    repoName: doc.repoName,
    starsThisWeek: doc.starsThisWeek
  };
}

export async function getEntriesByDate(date: string): Promise<Entry[]> {
  const col = await getEntriesCollection();
  const docs = await col.find({ date }).sort({ kind: 1, title: 1 }).toArray();
  return docs.map(serialize);
}

export async function getEntriesByWeek(
  weekOf: string,
  status?: string
): Promise<Entry[]> {
  const col = await getEntriesCollection();
  const filter: Record<string, unknown> = { weekOf };
  if (status && status !== 'all') {
    filter.status = status;
  }
  const docs = await col.find(filter).sort({ kind: 1, title: 1 }).toArray();
  return docs.map(serialize);
}

export async function updateEntryStatus(
  id: string,
  status: 'pending' | 'kept' | 'rejected'
): Promise<boolean> {
  const col = await getEntriesCollection();
  const result = await col.updateOne(
    { _id: new ObjectId(id) },
    { $set: { status, updatedAt: new Date() } }
  );
  return result.modifiedCount === 1;
}

export async function updateEntryKelvinsPick(
  id: string,
  kelvinsPick: boolean
): Promise<boolean> {
  const col = await getEntriesCollection();
  const result = await col.updateOne(
    { _id: new ObjectId(id) },
    { $set: { kelvinsPick, updatedAt: new Date() } }
  );
  return result.modifiedCount === 1;
}
