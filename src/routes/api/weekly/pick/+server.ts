import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { getWeeklyMetaCollection } from '$lib/server/collections';

export const PATCH: RequestHandler = async ({ request }) => {
  let body: { weekOf?: string; title?: string; url?: string; description?: string };
  try {
    body = await request.json();
  } catch {
    return json({ error: 'Invalid JSON' }, { status: 400 });
  }

  const { weekOf, title, url, description } = body;
  if (!weekOf || !title || !url || description === undefined) {
    return json({ error: 'Missing required fields: weekOf, title, url, description' }, { status: 400 });
  }

  const col = await getWeeklyMetaCollection();
  await col.updateOne(
    { weekOf },
    {
      $set: {
        kelvinsPick: { title, url, description }
      },
      $setOnInsert: { weekOf }
    },
    { upsert: true }
  );

  return json({ ok: true });
};
