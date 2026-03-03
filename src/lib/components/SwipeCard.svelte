<script lang="ts">
	import type { Entry } from '$lib/types';
	import EntryCard from './EntryCard.svelte';

	let {
		entry,
		onswipe
	}: {
		entry: Entry;
		onswipe: (id: string, status: 'kept' | 'rejected') => void;
	} = $props();

	const THRESHOLD = 80;

	let startX = $state(0);
	let dx = $state(0);
	let dragging = $state(false);
	let dismissed = $state(false);
	let dismissDir = $state<'kept' | 'rejected' | null>(null);

	let rotation = $derived(dx * 0.08);
	let opacity = $derived(dismissed ? 0 : 1);

	function onpointerdown(e: PointerEvent) {
		if (dismissed) return;
		dragging = true;
		startX = e.clientX;
		(e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
	}

	function onpointermove(e: PointerEvent) {
		if (!dragging || dismissed) return;
		dx = e.clientX - startX;
	}

	function onpointerup() {
		if (!dragging) return;
		dragging = false;

		if (Math.abs(dx) >= THRESHOLD) {
			dismissDir = dx > 0 ? 'kept' : 'rejected';
			dismissed = true;
			// After animation, notify parent
			setTimeout(() => {
				onswipe(entry._id, dismissDir!);
			}, 300);
		} else {
			dx = 0;
		}
	}

	let translateX = $derived(dismissed ? (dismissDir === 'kept' ? 500 : -500) : dx);

	let indicatorKept = $derived(dx > 30);
	let indicatorReject = $derived(dx < -30);
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<div
	class="absolute inset-0 select-none touch-none cursor-grab active:cursor-grabbing"
	style="
		transform: translateX({translateX}px) rotate({rotation}deg);
		transition: {dismissed ? 'transform 0.3s ease, opacity 0.3s ease' : dragging ? 'none' : 'transform 0.2s ease'};
		opacity: {opacity};
	"
	onpointerdown={onpointerdown}
	onpointermove={onpointermove}
	onpointerup={onpointerup}
	onpointercancel={onpointerup}
>
	<!-- Card body -->
	<div class="h-full rounded-2xl bg-white border border-stone-200 shadow-lg overflow-auto">
		<!-- Keep / Reject indicators -->
		{#if indicatorKept}
			<div class="absolute top-4 left-4 z-10 rounded-full border-2 border-green-500 px-3 py-1 text-xs font-bold text-green-500 uppercase tracking-wider rotate-[-15deg] opacity-{Math.min(100, Math.round((dx / THRESHOLD) * 100))}">
				Keep
			</div>
		{/if}
		{#if indicatorReject}
			<div class="absolute top-4 right-4 z-10 rounded-full border-2 border-red-500 px-3 py-1 text-xs font-bold text-red-500 uppercase tracking-wider rotate-[15deg] opacity-{Math.min(100, Math.round((Math.abs(dx) / THRESHOLD) * 100))}">
				Skip
			</div>
		{/if}

		<EntryCard {entry} />
	</div>
</div>
