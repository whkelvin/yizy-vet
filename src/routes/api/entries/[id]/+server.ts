import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { updateEntryStatus } from '$lib/server/entries';

export const PATCH: RequestHandler = async ({ params, request }) => {
  const { id } = params;

  let body: { status?: string };
  try {
    body = await request.json();
  } catch {
    return json({ error: 'Invalid JSON' }, { status: 400 });
  }

  const { status } = body;
  if (!status || !['pending', 'kept', 'rejected'].includes(status)) {
    return json({ error: 'Invalid status' }, { status: 400 });
  }

  const updated = await updateEntryStatus(id, status as 'pending' | 'kept' | 'rejected');
  if (!updated) {
    return json({ error: 'Entry not found' }, { status: 404 });
  }

  return json({ ok: true });
};
