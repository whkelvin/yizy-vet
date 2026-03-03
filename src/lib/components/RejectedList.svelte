<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import type { Entry } from '$lib/types';

	let { entries }: { entries: Entry[] } = $props();

	let rejected = $derived(entries.filter((e) => e.status === 'rejected'));

	async function restore(id: string) {
		try {
			await fetch(`/api/entries/${id}`, {
				method: 'PATCH',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ status: 'pending' })
			});
			await invalidateAll();
		} catch (err) {
			console.error('Failed to restore entry:', err);
		}
	}

	function domain(url: string): string {
		try {
			return new URL(url).hostname.replace('www.', '');
		} catch {
			return url;
		}
	}
</script>

<div class="flex flex-col gap-2 w-full max-w-sm">
	{#if rejected.length === 0}
		<div class="rounded-xl border border-dashed border-stone-300 p-8 text-center text-stone-400">
			<p class="text-sm font-mono">No rejected entries</p>
		</div>
	{:else}
		{#each rejected as entry}
			<div class="flex items-start gap-3 rounded-xl bg-white border border-stone-200 p-3">
				<div class="flex-1 min-w-0">
					<div class="flex items-center gap-1.5 mb-1">
						<span class="section-heading text-stone-400">{entry.kind}</span>
					</div>
					<p class="yizy-title text-sm line-clamp-2">{entry.title}</p>
					<p class="text-xs text-stone-400 font-mono mt-0.5">{domain(entry.url)}</p>
				</div>
				<button
					type="button"
					onclick={() => restore(entry._id)}
					class="shrink-0 rounded-lg border border-stone-300 px-2.5 py-1.5 text-xs font-mono font-semibold text-stone-600 hover:bg-stone-100 hover:border-stone-400 transition-colors"
				>
					Restore
				</button>
			</div>
		{/each}
	{/if}
</div>
