<script lang="ts">
	import type { Entry } from '$lib/types';
	import DayCarousel from '$lib/components/DayCarousel.svelte';
	import RadioGroup from '$lib/components/RadioGroup.svelte';
	import SwipeStack from '$lib/components/SwipeStack.svelte';
	import RejectedList from '$lib/components/RejectedList.svelte';
	import { invalidateAll } from '$app/navigation';
	import KelvinsPickBtn from '$lib/components/KelvinsPickBtn.svelte';

	let {
		data
	}: {
		data: { date: string; entries: Entry[]; weekDates: string[] };
	} = $props();

	const VIEW_OPTIONS = [
		{ value: 'pending', label: 'Pending' },
		{ value: 'kept', label: 'Kept' },
		{ value: 'rejected', label: 'Rejected' }
	];

	let view = $state('pending');

	let keptEntries = $derived(data.entries.filter((e) => e.status === 'kept'));
	let pendingEntries = $derived(data.entries.filter((e) => e.status === 'pending'));
	let rejectedEntries = $derived(data.entries.filter((e) => e.status === 'rejected'));

	async function rejectEntry(id: string) {
		try {
			await fetch(`/api/entries/${id}`, {
				method: 'PATCH',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ status: 'rejected' })
			});
			await invalidateAll();
		} catch (err) {
			console.error('Failed to reject entry:', err);
		}
	}
</script>

<div class="min-h-screen bg-stone-200 px-4 py-6 flex flex-col items-center gap-6">
	<!-- Header -->
	<header class="w-full max-w-sm flex items-center justify-between">
		<a href="/" class="text-xs font-mono text-stone-400 hover:text-stone-600 transition-colors">← Back</a>
		<h1 class="section-heading text-stone-600">Week View</h1>
		<span class="text-xs font-mono text-stone-400">{data.date}</span>
	</header>

	<!-- Day Carousel -->
	<div class="w-full max-w-sm">
		<DayCarousel weekDates={data.weekDates} selectedDate={data.date} />
	</div>

	<!-- View toggle -->
	<div class="w-full max-w-sm">
		<RadioGroup options={VIEW_OPTIONS} bind:selected={view} />
	</div>

	<!-- Main content area -->
	{#if view === 'pending'}
		<SwipeStack entries={data.entries} />
	{:else if view === 'kept'}
		<div class="flex flex-col gap-2 w-full max-w-sm">
			{#if keptEntries.length === 0}
				<div class="rounded-xl border border-dashed border-stone-300 p-8 text-center text-stone-400">
					<p class="text-sm font-mono">No kept entries yet</p>
				</div>
			{:else}
				{#each keptEntries as entry}
					<div class="flex items-start gap-3 rounded-xl bg-white border border-stone-200 p-3 hover:border-stone-400 transition-colors">
						<a
							href={entry.url}
							target="_blank"
							rel="noopener noreferrer"
							class="flex-1 min-w-0"
						>
							<div class="flex items-center gap-1.5 mb-1">
								<span class="section-heading text-stone-400">{entry.kind}</span>
							</div>
							<p class="yizy-title text-sm line-clamp-2">{entry.title}</p>
							{#if entry.description}
								<p class="yizy-description text-xs mt-1 line-clamp-2">{entry.description}</p>
							{/if}
						</a>
						<KelvinsPickBtn entryId={entry._id} value={entry.kelvinsPick} onToggle={() => invalidateAll()} />
						<button
							type="button"
							class="shrink-0 rounded-lg border border-red-300 px-2.5 py-1.5 text-xs font-mono font-semibold text-red-500 hover:bg-red-50 hover:border-red-400 transition-colors"
							onclick={() => rejectEntry(entry._id)}
						>
							Reject
						</button>
					</div>
				{/each}
			{/if}
		</div>
	{:else if view === 'rejected'}
		<RejectedList entries={data.entries} />
	{/if}
</div>
