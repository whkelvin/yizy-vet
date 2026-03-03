<script lang="ts">
	interface Option {
		value: string;
		label: string;
	}

	let {
		options,
		selected = $bindable()
	}: {
		options: Option[];
		selected: string;
	} = $props();
</script>

<div class="flex rounded-full border border-stone-300 bg-stone-100 p-0.5 gap-0.5">
	{#each options as option}
		<button
			type="button"
			onclick={() => (selected = option.value)}
			class="flex-1 rounded-full px-4 py-1.5 text-xs font-mono font-semibold transition-colors
				{selected === option.value
				? 'bg-stone-800 text-white'
				: 'text-stone-500 hover:text-stone-700'}"
		>
			{option.label}
		</button>
	{/each}
</div>
