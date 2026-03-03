<script lang="ts">
	import type { Entry } from '$lib/types';

	let { entries }: { entries: Entry[] } = $props();

	const sections: { kind: Entry['kind']; label: string }[] = [
		{ kind: 'article', label: 'Articles' },
		{ kind: 'repo', label: 'Repos' },
		{ kind: 'video', label: 'Videos' },
		{ kind: 'podcast', label: 'Podcasts' }
	];

	function getDomain(url: string) {
		try {
			return new URL(url).hostname.replace('www.', '');
		} catch {
			return url;
		}
	}

	function getMeta(entry: Entry): string {
		if (entry.kind === 'repo') return entry.repoName || getDomain(entry.url);
		if (entry.kind === 'video') return entry.youtubeId ? `youtube/${entry.youtubeId}` : getDomain(entry.url);
		if (entry.kind === 'podcast') return entry.spotifyEmbedUrl ? 'spotify' : getDomain(entry.url);
		return getDomain(entry.url);
	}

	function statusIcon(status: Entry['status']): string {
		if (status === 'kept') return '✓';
		if (status === 'rejected') return '✗';
		return '○';
	}

	function statusColor(status: Entry['status']): string {
		if (status === 'kept') return 'text-green-600';
		if (status === 'rejected') return 'text-red-500';
		return 'text-stone-400';
	}
</script>

<div class="flex flex-col gap-6">
	{#each sections as section}
		{@const sectionEntries = entries.filter((e) => e.kind === section.kind)}
		{#if sectionEntries.length > 0}
			<div>
				<h2 class="section-heading">{section.label}</h2>
				<div class="flex flex-col gap-1.5">
					{#each sectionEntries as entry}
						<a
							href={entry.url}
							target="_blank"
							rel="noopener noreferrer"
							class="flex items-start gap-2.5 rounded-lg bg-white border border-stone-200 px-3 py-2.5 hover:border-stone-400 transition-colors group"
						>
							<span class="mt-0.5 text-xs font-mono font-bold {statusColor(entry.status)} shrink-0">
								{statusIcon(entry.status)}
							</span>
							<div class="flex-1 min-w-0">
								<p class="yizy-title text-sm line-clamp-1 group-hover:text-stone-900">{entry.title}</p>
								<p class="yizy-description text-xs mt-0.5">{getMeta(entry)}</p>
							</div>
						</a>
					{/each}
				</div>
			</div>
		{/if}
	{/each}

	{#if entries.length === 0}
		<div class="rounded-xl border border-dashed border-stone-300 p-10 text-center text-stone-400">
			<p class="text-sm font-mono">No entries</p>
		</div>
	{/if}
</div>
