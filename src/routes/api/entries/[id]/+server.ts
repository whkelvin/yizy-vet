import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { updateEntryStatus, updateEntryKelvinsPick } from '$lib/server/entries';

export const PATCH: RequestHandler = async ({ params, request }) => {
  const { id } = params;

  let body: { status?: string; kelvinsPick?: boolean };
  try {
    body = await request.json();
  } catch {
    return json({ error: 'Invalid JSON' }, { status: 400 });
  }

  const { status, kelvinsPick } = body;

  if (status !== undefined) {
    if (!['pending', 'kept', 'rejected'].includes(status)) {
      return json({ error: 'Invalid status' }, { status: 400 });
    }
    const updated = await updateEntryStatus(id, status as 'pending' | 'kept' | 'rejected');
    if (!updated) return json({ error: 'Entry not found' }, { status: 404 });
  }

  if (kelvinsPick !== undefined) {
    if (typeof kelvinsPick !== 'boolean') {
      return json({ error: 'kelvinsPick must be a boolean' }, { status: 400 });
    }
    const updated = await updateEntryKelvinsPick(id, kelvinsPick);
    if (!updated) return json({ error: 'Entry not found' }, { status: 404 });
  }

  return json({ ok: true });
};
