import type { ObjectId } from 'mongodb';

export interface EntryDocument {
  _id: ObjectId;
  kind: 'article' | 'repo' | 'video' | 'podcast';
  title: string;
  url: string;
  date: string;
  weekOf: string;
  status: 'pending' | 'kept' | 'rejected';
  youtubeId?: string;
  spotifyEmbedUrl?: string;
  repoName?: string;
  starsThisWeek?: number;
  createdAt: Date;
  updatedAt: Date;
}

/** Serialized entry sent to the client (no ObjectId) */
export interface Entry {
  _id: string;
  kind: 'article' | 'repo' | 'video' | 'podcast';
  title: string;
  url: string;
  date: string;
  weekOf: string;
  status: 'pending' | 'kept' | 'rejected';
  why: string;
  description: string;
  youtubeId?: string;
  spotifyEmbedUrl?: string;
  repoName?: string;
  starsThisWeek?: number;
}

export interface WeeklyMetaDocument {
  _id: ObjectId;
  weekOf: string;
  kelvinsPick: {
    title: string;
    url: string;
    description: string;
  } | null;
}

export interface WeeklyMeta {
  weekOf: string;
  kelvinsPick: {
    title: string;
    url: string;
    description: string;
  } | null;
}

export interface IngestPayload {
  date: string;
  articles: { title: string; url: string }[];
  repos: { name: string; url: string; starsThisWeek: number }[];
  videos: { title: string; youtubeId: string }[];
  podcasts: { title: string; spotifyEmbedUrl: string }[];
}

/** Edition shape for export */
export interface Edition {
  date: string;
  articles: { title: string; url: string; why: string; description: string }[];
  repos: { name: string; url: string; starsThisWeek: number }[];
  videos: { title: string; youtubeId: string; why: string; description: string }[];
  podcasts: { title: string; spotifyEmbedUrl: string; why: string; description: string }[];
  kelvinsPick: { title: string; url: string; description: string };
}
