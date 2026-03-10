<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import type { Entry } from '$lib/types';
	import SwipeCard from './SwipeCard.svelte';

	let { entries }: { entries: Entry[] } = $props();

	// Only show pending entries
	let pending = $derived(entries.filter((e) => e.status === 'pending'));
	let swiped = $state(new Set<string>());
	let skippedIds = $state<string[]>([]);
	let queue = $derived.by(() => {
		const remaining = pending.filter((e) => !swiped.has(e._id));
		const notSkipped = remaining.filter((e) => !skippedIds.includes(e._id));
		const skipped = skippedIds
			.filter((id) => remaining.some((e) => e._id === id))
			.map((id) => remaining.find((e) => e._id === id)!);
		return [...notSkipped, ...skipped];
	});

	// Show top 3 cards for stacking effect
	let visibleCards = $derived(queue.slice(0, 3));

	function handleSkip(id: string) {
		// Remove from current position if already skipped, then add to end
		skippedIds = [...skippedIds.filter((s) => s !== id), id];
	}

	async function handleSwipe(id: string, status: 'kept' | 'rejected') {
		// Remove from local queue immediately
		swiped.add(id);
		swiped = swiped;

		try {
			await fetch(`/api/entries/${id}`, {
				method: 'PATCH',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ status })
			});
			await invalidateAll();
		} catch (err) {
			console.error('Failed to update entry:', err);
		}
	}
</script>

<div class="flex flex-col items-center gap-4 w-full">
	<!-- Card stack -->
	<div class="relative w-full max-w-sm" style="height: 320px;">
		{#if queue.length === 0}
			<div class="flex h-full items-center justify-center rounded-2xl border border-dashed border-stone-300 text-stone-400">
				<div class="text-center">
					<div class="text-2xl mb-2">✓</div>
					<p class="text-sm font-mono">All done for today</p>
				</div>
			</div>
		{:else}
			{#each visibleCards.slice().reverse() as entry, revIdx (entry._id)}
				{@const idx = visibleCards.length - 1 - revIdx}
				{@const isTop = idx === 0}
				<div
					class="absolute inset-0"
					style="
						transform: translateY({idx * 8}px) scale({1 - idx * 0.03});
						z-index: {visibleCards.length - idx};
						pointer-events: {isTop ? 'auto' : 'none'};
					"
				>
					{#if isTop}
						<SwipeCard {entry} onswipe={handleSwipe} onskip={handleSkip} />
					{:else}
						<div class="h-full rounded-2xl bg-white border border-stone-200 shadow"></div>
					{/if}
				</div>
			{/each}
		{/if}
	</div>

	<!-- Progress bar -->
	<div class="w-full max-w-sm flex items-center gap-3">
		<div class="flex-1 h-1.5 rounded-full bg-stone-300 overflow-hidden">
			<div
				class="h-full rounded-full bg-stone-800 transition-all duration-300"
				style="width: {entries.length > 0 ? ((entries.length - pending.length) / entries.length) * 100 : 0}%"
			></div>
		</div>
		<p class="text-xs text-stone-400 font-mono shrink-0">{pending.length}/{entries.length}</p>
	</div>

	<!-- Stats row -->
	<div class="w-full max-w-sm flex gap-2">
		<div class="flex-1 rounded-xl bg-white border border-stone-200 px-3 py-2 text-center">
			<div class="text-lg font-bold text-stone-800">{pending.length}</div>
			<div class="section-heading text-stone-400">pending</div>
		</div>
		<div class="flex-1 rounded-xl bg-white border border-stone-200 px-3 py-2 text-center">
			<div class="text-lg font-bold text-green-700">{entries.filter((e) => e.status === 'kept').length}</div>
			<div class="section-heading text-stone-400">kept</div>
		</div>
		<div class="flex-1 rounded-xl bg-white border border-stone-200 px-3 py-2 text-center">
			<div class="text-lg font-bold text-red-600">{entries.filter((e) => e.status === 'rejected').length}</div>
			<div class="section-heading text-stone-400">skipped</div>
		</div>
	</div>
</div>
