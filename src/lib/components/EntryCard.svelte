<script lang="ts">
	import type { Entry } from '$lib/types';

	let { entry }: { entry: Entry } = $props();

	function domain(url: string): string {
		try {
			return new URL(url).hostname.replace('www.', '');
		} catch {
			return url;
		}
	}
</script>

<div class="flex flex-col gap-3 p-5">
	<!-- Kind badge -->
	<div class="flex items-center gap-2">
		<span class="section-heading px-2 py-0.5 rounded bg-stone-200 text-stone-500">
			{entry.kind}
		</span>
		{#if entry.kind === 'repo' && entry.starsThisWeek !== undefined}
			<span class="text-xs text-stone-400 font-mono">+{entry.starsThisWeek} ★ this week</span>
		{/if}
	</div>

	<!-- Title -->
	<h2 class="yizy-title text-lg leading-snug">
		<a href={entry.url} target="_blank" rel="noopener noreferrer" class="underline">{entry.title}</a>
	</h2>

	<!-- Kind-specific media -->
	{#if entry.kind === 'video' && entry.youtubeId}
		<div class="w-full aspect-video rounded overflow-hidden bg-stone-800">
			<iframe
				src="https://www.youtube.com/embed/{entry.youtubeId}"
				title={entry.title}
				class="w-full h-full"
				frameborder="0"
				allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
				allowfullscreen
			></iframe>
		</div>
	{:else if entry.kind === 'podcast' && entry.spotifyEmbedUrl}
		<div class="w-full rounded overflow-hidden">
			<iframe
				src={entry.spotifyEmbedUrl}
				title={entry.title}
				class="w-full"
				height="152"
				frameborder="0"
				allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
				loading="lazy"
			></iframe>
		</div>
	{:else if entry.kind === 'repo'}
		<div class="flex items-center gap-2 text-stone-400">
			<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
				<path d="M12 2C6.48 2 2 6.48 2 12c0 4.42 2.87 8.17 6.84 9.49.5.09.66-.22.66-.48v-1.7c-2.78.6-3.37-1.34-3.37-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.89 1.52 2.34 1.08 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.56-1.11-4.56-4.94 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.64 0 0 .84-.27 2.75 1.02A9.56 9.56 0 0 1 12 6.8c.85.004 1.71.115 2.51.337 1.91-1.29 2.75-1.02 2.75-1.02.55 1.37.2 2.39.1 2.64.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.69-4.57 4.93.36.31.68.92.68 1.85v2.74c0 .27.16.58.67.48A10.01 10.01 0 0 0 22 12c0-5.52-4.48-10-10-10z" />
			</svg>
			<span class="text-xs font-mono">{entry.repoName ?? domain(entry.url)}</span>
		</div>
	{:else}
		<div class="text-xs text-stone-400 font-mono">{domain(entry.url)}</div>
	{/if}

	<!-- Description -->
	{#if entry.description}
		<p class="yizy-description line-clamp-3">{entry.description}</p>
	{/if}

	<!-- Why -->
	{#if entry.why}
		<div class="border-l-2 border-stone-400 pl-3">
			<p class="text-xs text-stone-500 font-mono italic line-clamp-2">{entry.why}</p>
		</div>
	{/if}
</div>
