import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import type { IngestPayload } from '$lib/types';
import { getEntriesCollection } from '$lib/server/collections';
import { getWeekOf } from '$lib/week';

export const POST: RequestHandler = async ({ request }) => {
  let payload: IngestPayload;
  try {
    payload = await request.json();
  } catch {
    return json({ error: 'Invalid JSON' }, { status: 400 });
  }

  const { date, articles, repos, videos, podcasts } = payload;
  if (!date) {
    return json({ error: 'Missing date' }, { status: 400 });
  }

  const weekOf = getWeekOf(date);
  const col = await getEntriesCollection();
  const now = new Date();

  const ops: Promise<unknown>[] = [];

  for (const a of articles ?? []) {
    ops.push(
      col.updateOne(
        { kind: 'article', url: a.url },
        {
          $setOnInsert: {
            kind: 'article',
            title: a.title,
            url: a.url,
            date,
            weekOf,
            status: 'pending',
            createdAt: now,
            updatedAt: now
          }
        },
        { upsert: true }
      )
    );
  }

  for (const v of videos ?? []) {
    const url = `https://www.youtube.com/watch?v=${v.youtubeId}`;
    ops.push(
      col.updateOne(
        { kind: 'video', url },
        {
          $setOnInsert: {
            kind: 'video',
            title: v.title,
            url,
            youtubeId: v.youtubeId,
            date,
            weekOf,
            status: 'pending',
            createdAt: now,
            updatedAt: now
          }
        },
        { upsert: true }
      )
    );
  }

  for (const p of podcasts ?? []) {
    ops.push(
      col.updateOne(
        { kind: 'podcast', url: p.spotifyEmbedUrl },
        {
          $setOnInsert: {
            kind: 'podcast',
            title: p.title,
            url: p.spotifyEmbedUrl,
            spotifyEmbedUrl: p.spotifyEmbedUrl,
            date,
            weekOf,
            status: 'pending',
            createdAt: now,
            updatedAt: now
          }
        },
        { upsert: true }
      )
    );
  }

  for (const r of repos ?? []) {
    ops.push(
      col.updateOne(
        { kind: 'repo', url: r.url },
        {
          $set: {
            starsThisWeek: r.starsThisWeek,
            updatedAt: now
          },
          $setOnInsert: {
            kind: 'repo',
            title: r.name,
            repoName: r.name,
            url: r.url,
            date,
            weekOf,
            status: 'pending',
            createdAt: now
          }
        },
        { upsert: true }
      )
    );
  }

  await Promise.all(ops);

  return json({ ok: true, weekOf, ingested: ops.length });
};
