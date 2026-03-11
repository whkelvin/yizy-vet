<script lang="ts">
	let {
		entryId,
		value,
		fullWidth = false,
		onToggle
	}: {
		entryId: string;
		value: boolean;
		fullWidth?: boolean;
		onToggle?: (newVal: boolean) => void;
	} = $props();

	let optimistic = $state(value);
	let saving = $state(false);

	$effect(() => {
		optimistic = value;
	});

	async function toggle(e: MouseEvent | TouchEvent) {
		e.stopPropagation();
		if (saving) return;
		const next = !optimistic;
		optimistic = next;
		saving = true;
		try {
			await fetch(`/api/entries/${entryId}`, {
				method: 'PATCH',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ kelvinsPick: next })
			});
			onToggle?.(next);
		} catch {
			optimistic = !next;
		} finally {
			saving = false;
		}
	}
</script>

<button
	type="button"
	onmousedown={(e) => e.stopPropagation()}
	ontouchstart={(e) => e.stopPropagation()}
	onclick={toggle}
	class="rounded-lg transition-colors leading-none
		{fullWidth ? 'w-full py-3 text-2xl border' : 'shrink-0 px-2 py-1.5 text-base border'}
		{optimistic
			? 'text-red-500 hover:text-red-400 border-red-400 bg-red-50 hover:bg-red-100'
			: 'text-stone-300 hover:text-red-400 border-red-300 hover:bg-red-50'}
		{saving ? 'opacity-50 pointer-events-none' : ''}"
	title={optimistic ? "Remove Kelvin's Pick" : "Mark as Kelvin's Pick"}
>
	{optimistic ? '♥' : '♡'}
</button>
