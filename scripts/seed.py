"""Seed the database with fake data for manual frontend testing.

Reads MONGODB_URI from .env in the project root.
Uses today's date so data shows up in the current week view.
"""

import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne

# Load .env from project root (one level up from scripts/)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
if not MONGODB_URI:
    print("ERROR: MONGODB_URI not set in .env", file=sys.stderr)
    sys.exit(1)

TODAY = date.today().isoformat()


def get_week_of(d: str) -> str:
    """Return the Sunday that starts the edition week containing d (YYYY-MM-DD)."""
    from datetime import datetime, timezone, timedelta
    dt = datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    day_of_week = dt.weekday()  # Mon=0 … Sun=6
    # Convert to Sun=0 … Sat=6
    sun_offset = (day_of_week + 1) % 7
    sunday = dt - timedelta(days=sun_offset)
    return sunday.strftime("%Y-%m-%d")


SEED_DATA = {
    "articles": [
        {
            "title": "Code Mode: give agents an entire API in 1,000 tokens",
            "url": "https://blog.cloudflare.com/code-mode-mcp/",
            "why": "Agents can explore and compose APIs dynamically without exposing thousands of endpoints as separate tools",
            "description": "Code Mode provides agents with a compact SDK to write and execute code instead of maintaining separate tool definitions for each endpoint. For Cloudflare's 2,500 API endpoints, this achieves 99.9% token reduction, fitting what would require 1.17 million tokens into just 1,000 tokens.",
        },
        {
            "title": "Measuring actual AI Impact for Engineering with Apache DevLake",
            "url": "https://devblogs.microsoft.com/all-things-azure/measuring-actual-ai-impact-for-engineering-with-apache-devlake",
            "why": "Correlate AI adoption to real delivery outcomes rather than vanity metrics like seat usage",
            "description": "Apache DevLake normalizes data from 20+ DevOps tools into one queryable database tracking DORA metrics. The platform reveals concrete correlations like organizations with 75% Copilot adoption achieving 33% faster pull request cycles and 2x deployment frequency compared to lower adoption weeks.",
        },
        {
            "title": "Bringing automated preview, review, and merge to Claude Code on desktop",
            "url": "https://claude.com/blog/preview-review-and-merge-with-claude-code",
            "why": "Unified IDE consolidates the entire development workflow eliminating context-switching",
            "description": "Claude Code desktop starts dev servers and previews running apps directly in the editor, auto-reviews code changes with inline comments, tracks pull request status, and automatically fixes failing tests or merges PRs once checks pass.",
        },
        {
            "title": "The third era of AI software development",
            "url": "https://cursor.com/blog/third-era",
            "why": "Developers are shifting from writing code to architecting workflows and managing autonomous agent teams",
            "description": "Era one introduced autocomplete. Era two added synchronous back-and-forth agents. Era three brings autonomous cloud agents working asynchronously over longer timescales. Developers now manage fleets of parallel agents, review their artifacts through logs and videos, and focus on problem decomposition rather than line-by-line coding.",
        },
        {
            "title": "Building frontend UIs with Codex and Figma",
            "url": "https://developers.openai.com/blog/building-frontend-uis-with-codex-and-figma",
            "why": "Bidirectional design-to-code workflow keeps designs and implementations synchronized",
            "description": "The Figma MCP integration enables extracting design layouts and styles into code generation and converting running applications back into editable Figma frames. Teams can iterate fluidly between design exploration and code execution while maintaining sync between representations.",
        },
        {
            "title": "What I Learned After 72 Hours as an Autonomous AI Agent on the Internet",
            "url": "https://dev.to/colony0ai/what-i-learned-after-72-hours-as-an-autonomous-ai-agent-on-the-internet-36jo",
            "why": "Understanding real constraints of autonomous agents helps developers build systems with proper safeguards",
            "description": "Running an autonomous agent for 72 hours revealed identity barriers on major platforms, lack of trust frameworks, economic viability challenges, and the need for payment systems without verification. The bottleneck is not computation but establishing credibility and trust within internet ecosystems.",
        },
        {
            "title": "Closing the code review loop with Bugbot Autofix",
            "url": "https://cursor.com/blog/bugbot-autofix",
            "why": "AI agents automatically fixing detected bugs eliminates manual review cycles and accelerates development",
            "description": "Bugbot Autofix spawns cloud agents in isolated VMs to detect issues and propose fixes in pull requests. The system has improved issue detection by 100%, increased bug resolution rates from 52% to 76%, and sees 35% of proposed fixes merged directly without developer revision.",
        },
    ],
    "repos": [
        {"name": "OpenBB-finance/OpenBB", "url": "https://github.com/OpenBB-finance/OpenBB", "starsThisWeek": 1783},
        {"name": "f/prompts.chat", "url": "https://github.com/f/prompts.chat", "starsThisWeek": 3072},
        {"name": "evershopcommerce/evershop", "url": "https://github.com/evershopcommerce/evershop", "starsThisWeek": 555},
        {"name": "sktime/sktime", "url": "https://github.com/sktime/sktime", "starsThisWeek": 44},
        {"name": "codecrafters-io/build-your-own-x", "url": "https://github.com/codecrafters-io/build-your-own-x", "starsThisWeek": 2678},
        {"name": "laurent22/joplin", "url": "https://github.com/laurent22/joplin", "starsThisWeek": 162},
        {"name": "sindresorhus/awesome", "url": "https://github.com/sindresorhus/awesome", "starsThisWeek": 2453},
        {"name": "sympy/sympy", "url": "https://github.com/sympy/sympy", "starsThisWeek": 35},
        {"name": "ghostfolio/ghostfolio", "url": "https://github.com/ghostfolio/ghostfolio", "starsThisWeek": 111},
        {"name": "NVIDIA/Megatron-LM", "url": "https://github.com/NVIDIA/Megatron-LM", "starsThisWeek": 229},
        {"name": "frappe/books", "url": "https://github.com/frappe/books", "starsThisWeek": 254},
        {"name": "openai/openai-cookbook", "url": "https://github.com/openai/openai-cookbook", "starsThisWeek": 210},
        {"name": "seerr-team/seerr", "url": "https://github.com/seerr-team/seerr", "starsThisWeek": 381},
        {"name": "ente-io/ente", "url": "https://github.com/ente-io/ente", "starsThisWeek": 216},
        {"name": "swiftlang/swift", "url": "https://github.com/swiftlang/swift", "starsThisWeek": 56},
        {"name": "danielgatis/rembg", "url": "https://github.com/danielgatis/rembg", "starsThisWeek": 138},
        {"name": "AUTOMATIC1111/stable-diffusion-webui", "url": "https://github.com/AUTOMATIC1111/stable-diffusion-webui", "starsThisWeek": 746},
        {"name": "appsmithorg/appsmith", "url": "https://github.com/appsmithorg/appsmith", "starsThisWeek": 155},
        {"name": "Drakkar-Software/OctoBot", "url": "https://github.com/Drakkar-Software/OctoBot", "starsThisWeek": 164},
        {"name": "SerenityOS/serenity", "url": "https://github.com/SerenityOS/serenity", "starsThisWeek": 57},
        {"name": "enaqx/awesome-react", "url": "https://github.com/enaqx/awesome-react", "starsThisWeek": 136},
        {"name": "evidentlyai/evidently", "url": "https://github.com/evidentlyai/evidently", "starsThisWeek": 113},
        {"name": "Farama-Foundation/Gymnasium", "url": "https://github.com/Farama-Foundation/Gymnasium", "starsThisWeek": 56},
    ],
    "videos": [
        {
            "title": "Delete your CLAUDE.md (and your AGENT.md too)",
            "youtubeId": "GcNu6wrLTJc",
            "why": "Verbose instruction files dilute critical guardrails by burying them in noise that LLMs ignore",
            "description": "Keep CLAUDE.md minimal with only universally applicable instructions. Most generated content is obvious from reading code itself. LLMs can follow approximately 150-200 instructions consistently, so verbose files waste that budget on redundant information.",
        },
        {
            "title": "OpenClaw Creator Peter Steinberger's advice for developers",
            "youtubeId": "-RDPAPjDnp8",
            "why": "Learn how elite developers iterate with AI agents to ship at unprecedented velocity",
            "description": "Be playful and expect to learn incrementally like mastering guitar. Your role shifts to architect and editor. Ship code without reading it. Parallelize work across multiple agents. Exploration beats planning when building with agents.",
        },
        {
            "title": "The Powerful Alternative To Fine-Tuning",
            "youtubeId": "UPGB-hsAoVY",
            "why": "Prompt engineering achieves comparable results to fine-tuning without expensive training data or compute",
            "description": "Prompt engineering, retrieval-augmented generation, and prompt tuning provide flexible alternatives to fine-tuning. Prompt engineering offers zero computational cost, rapid prototyping, and multi-task capability. Fine-tuning still wins on highly specialized tasks requiring permanent model adaptation.",
        },
        {
            "title": "4 Skills I'm Learning that AI Can't Replace (backed by data)",
            "youtubeId": "s_765enJBy8",
            "why": "Intentional skill development builds resilience against AI automation and maintains cognitive independence",
            "description": "The Cockpit Rule teaches when to delegate to AI versus collaborate. Storytelling turns data into narratives that move people. Strategic communication frameworks amplify impact. Finally, deliberately avoiding AI for certain tasks preserves critical thinking ability.",
        },
        {
            "title": "When open-sourcing your code goes wrong...",
            "youtubeId": "wzzh7Not8XE",
            "why": "Public code directly reflects on project credibility and team competence",
            "description": "Open-sourcing requires proper packaging, testing, and documentation. Releasing broken or unmaintainable code creates lasting negative impressions that extend far beyond the technical artifacts themselves.",
        },
        {
            "title": "Only extreme programmers will survive",
            "youtubeId": "Iu80Io2cNYw",
            "why": "Extreme Programming disciplines separate elite developers by demanding rigorous mastery of core techniques",
            "description": "Extreme Programming demands test-driven development, pair programming, relentless refactoring, and code simplicity. These core practices require discipline and mastery that most developers never achieve, making them competitive differentiators.",
        },
        {
            "title": "A computer for every agent",
            "youtubeId": "6Nru5OQq9O4",
            "why": "Autonomous agents in sandboxed environments enable independent task completion without human intervention",
            "description": "Agents operating in isolated, dedicated computing environments can interact with UIs, navigate applications, and complete full workflows independently. This infrastructure enables true autonomy beyond prompt-response interaction.",
        },
        {
            "title": "Cursor now shows you demos, not diffs",
            "youtubeId": "XbZvC4KTH68",
            "why": "Visual demonstrations of working features are more effective than diffs for reviewing agent-generated code",
            "description": "Agents use their own computers to build, test, and demo features end-to-end. Rather than reviewing traditional diffs, developers see working implementations that demonstrate functionality before changes are applied.",
        },
    ],
    "podcasts": [
        {
            "title": "Episode 501: Vibecoding CEO and doing to teaching",
            "spotifyEmbedUrl": "https://open.spotify.com/embed/episode/0sk3d6UNjniVlxJUgOnrQR",
            "why": "Understand how AI agents are democratizing software creation beyond technical experts",
            "description": "Amjad Masad explains Replit's shift from teaching millions to code toward building AI agents that do it for them. Vibe coding removes the technical barrier, enabling non-experts to build software independently.",
        },
        {
            "title": "The Career Bet Every Engineer Must Make",
            "spotifyEmbedUrl": "https://open.spotify.com/embed/show/314xPkcFTQxY0ar1WnnmGp",
            "why": "AI fundamentally reshapes what skills developers should prioritize in their careers",
            "description": "Code writing is no longer your most valuable skill in an AI-augmented world. Design thinking, product sense, and taste become real constraints on quality. Engineers must strategically evolve their value proposition.",
        },
        {
            "title": "The mythical agent-month (News)",
            "spotifyEmbedUrl": "https://open.spotify.com/embed/episode/1KIZyOhF56B6KuG7k32HcC",
            "why": "Adding agents doesn't solve fundamental software engineering constraints",
            "description": "Design, product scoping, and taste remain practical constraints on software quality regardless of agent capabilities. Brooks's Law still applies. Agents cannot overcome estimation and scope problems that plague traditional development.",
        },
        {
            "title": "Mitchell Hashimoto's new way of writing code",
            "spotifyEmbedUrl": "https://open.spotify.com/embed/episode/0bIuuNChmWXcwbIydP6Ckk",
            "why": "Asynchronous parallel agent workflows compound productivity gains through continuous progress",
            "description": "Run agents continuously in the background. While you code, agents plan. While agents code, you review. Kick off work before leaving so progress continues uninterrupted. Parallelization maximizes effective work output.",
        },
    ],
    "kelvinsPick": {
        "title": "nikitabobko/AeroSpace",
        "url": "https://github.com/nikitabobko/AeroSpace",
        "description": "If you want all your apps tiled nicely when you open them and a keyboard friendly way to manage workspaces and navigate between windows on your Mac, this is for you! Ditch your mouse today :)",
    },
}


def main():
    week_of = get_week_of(TODAY)
    now = datetime.now(timezone.utc)

    client = MongoClient(MONGODB_URI)
    db_name = MONGODB_URI.rstrip("/").rsplit("/", 1)[-1].split("?")[0]
    db = client[db_name]
    entries = db["entries"]
    weekly_meta = db["weekly_meta"]

    ops = []

    for a in SEED_DATA["articles"]:
        ops.append(
            UpdateOne(
                {"kind": "article", "url": a["url"]},
                {
                    "$setOnInsert": {
                        "kind": "article",
                        "title": a["title"],
                        "url": a["url"],
                        "why": a["why"],
                        "description": a["description"],
                        "date": TODAY,
                        "weekOf": week_of,
                        "status": "pending",
                        "createdAt": now,
                        "updatedAt": now,
                    }
                },
                upsert=True,
            )
        )

    for v in SEED_DATA["videos"]:
        url = f"https://www.youtube.com/watch?v={v['youtubeId']}"
        ops.append(
            UpdateOne(
                {"kind": "video", "url": url},
                {
                    "$setOnInsert": {
                        "kind": "video",
                        "title": v["title"],
                        "url": url,
                        "youtubeId": v["youtubeId"],
                        "why": v["why"],
                        "description": v["description"],
                        "date": TODAY,
                        "weekOf": week_of,
                        "status": "pending",
                        "createdAt": now,
                        "updatedAt": now,
                    }
                },
                upsert=True,
            )
        )

    for p in SEED_DATA["podcasts"]:
        ops.append(
            UpdateOne(
                {"kind": "podcast", "url": p["spotifyEmbedUrl"]},
                {
                    "$setOnInsert": {
                        "kind": "podcast",
                        "title": p["title"],
                        "url": p["spotifyEmbedUrl"],
                        "spotifyEmbedUrl": p["spotifyEmbedUrl"],
                        "why": p["why"],
                        "description": p["description"],
                        "date": TODAY,
                        "weekOf": week_of,
                        "status": "pending",
                        "createdAt": now,
                        "updatedAt": now,
                    }
                },
                upsert=True,
            )
        )

    for r in SEED_DATA["repos"]:
        ops.append(
            UpdateOne(
                {"kind": "repo", "url": r["url"]},
                {
                    "$set": {"starsThisWeek": r["starsThisWeek"], "updatedAt": now},
                    "$setOnInsert": {
                        "kind": "repo",
                        "title": r["name"],
                        "repoName": r["name"],
                        "url": r["url"],
                        "date": TODAY,
                        "weekOf": week_of,
                        "status": "kept",
                        "createdAt": now,
                    },
                },
                upsert=True,
            )
        )

    result = entries.bulk_write(ops)
    print(f"Entries: {result.upserted_count} inserted, {result.modified_count} modified")

    pick = SEED_DATA["kelvinsPick"]
    weekly_meta.update_one(
        {"weekOf": week_of},
        {
            "$set": {"kelvinsPick": {"title": pick["title"], "url": pick["url"], "description": pick["description"]}},
            "$setOnInsert": {"weekOf": week_of},
        },
        upsert=True,
    )
    print(f"Weekly meta upserted for weekOf={week_of}")
    print(f"Done. date={TODAY}, weekOf={week_of}")

    client.close()


if __name__ == "__main__":
    main()
